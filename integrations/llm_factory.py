"""
SuiLight Knowledge Salon - LLM 工厂
支持多种 LLM 后端 (免费/本地/云端)
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM 提供商"""
    MOCK = "mock"           # 免费 Mock 模式
    OLLAMA = "ollama"       # 本地 Ollama
    GROQ = "groq"          # Groq 免费 tier
    OPENAI = "openai"       # OpenAI (GPT-4)
    MINIMAX = "minimax"     # MiniMax
    ANTHROPIC = "anthropic" # Claude


@dataclass
class LLMConfig:
    """LLM 配置"""
    provider: str = "mock"  # 默认使用免费 Mock
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Ollama 本地
    ollama_host: str = "http://localhost:11434"


class LLMClient:
    """
    LLM 客户端工厂
    
    支持多种后端，自动切换
    """
    
    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        self.provider = self.config.provider
        
        # 初始化各后端
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        if self.provider == LLMProvider.MOCK.value:
            logger.info("🔧 使用 Mock 模式 (免费)")
            self.client = MockLLM()
            
        elif self.provider == LLMProvider.OLLAMA.value:
            logger.info(f"🔧 使用 Ollama (本地: {self.config.ollama_host})")
            self.client = OllamaLLM(self.config)
            
        elif self.provider == LLMProvider.GROQ.value:
            logger.info("🔧 使用 Groq (免费 tier)")
            self.client = GroqLLM(self.config)
            
        elif self.provider == LLMProvider.OPENAI.value:
            logger.info("🔧 使用 OpenAI GPT")
            self.client = OpenAILLM(self.config)
            
        elif self.provider == LLMProvider.MINIMAX.value:
            logger.info("🔧 使用 MiniMax")
            self.client = MiniMaxLLM(self.config)
            
        else:
            logger.warning(f"未知 provider: {self.provider}, 使用 Mock")
            self.client = MockLLM()
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """聊天接口"""
        return self.client.chat(
            messages=messages,
            system_prompt=system_prompt,
            temperature=temperature or self.config.temperature,
            max_tokens=max_tokens or self.config.max_tokens
        )
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        """嵌入向量"""
        return self.client.embedding(texts)


# ============ 各后端实现 ============

class BaseLLM:
    """LLM 基类"""
    
    def chat(self, messages, system_prompt=None, temperature=0.7, max_tokens=2000) -> str:
        raise NotImplementedError
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        return [[0.0] * 384 for _ in texts]  # 返回零向量


class MockLLM(BaseLLM):
    """免费 Mock 模式 (无需 API Key)"""
    
    def chat(self, messages, system_prompt=None, temperature=0.7, max_tokens=2000) -> str:
        # 提取用户消息
        user_msg = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_msg = msg.get("content", "")
                break
        
        if not user_msg:
            return "你好！我是知识沙龙的 AI 助手。"
        
        # 智能回复
        return f"【知识沙龙】{user_msg}\n\n这是一个模拟回复。\n\n配置真实的 LLM 后端后可获得更智能的回答：\n- Ollama (本地免费)\n- Groq (免费 tier)\n- OpenAI (付费)"
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        import numpy as np
        return [np.random.rand(384).tolist() for _ in texts]


class OllamaLLM(BaseLLM):
    """Ollama 本地模型 (免费)"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.base_url = config.ollama_host
        self.model = config.model or "llama3"
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            logger.warning("requests 库未安装")
            self.requests = None
    
    def chat(self, messages, system_prompt=None, temperature=0.7, max_tokens=2000) -> str:
        if not self.requests:
            return MockLLM().chat(messages)
        
        try:
            # 构建消息
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend([{"role": m["role"], "content": m["content"]} for m in messages])
            
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "messages": all_messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                logger.error(f"Ollama 错误: {response.status_code}")
                return MockLLM().chat(messages)
                
        except Exception as e:
            logger.error(f"Ollama 调用失败: {e}")
            return MockLLM().chat(messages)
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        """Ollama embedding"""
        import numpy as np
        return [np.random.rand(384).tolist() for _ in texts]


class GroqLLM(BaseLLM):
    """Groq 免费 tier (免费高速)"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = config.api_key or os.getenv("GROQ_API_KEY", "")
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            logger.warning("groq 库未安装: pip install groq")
            self.client = None
    
    def chat(self, messages, system_prompt=None, temperature=0.7, max_tokens=2000) -> str:
        if not self.client:
            return MockLLM().chat(messages)
        
        try:
            # 构建消息
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend([{"role": m["role"], "content": m["content"]} for m in messages])
            
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Groq 免费模型
                messages=all_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq 调用失败: {e}")
            return MockLLM().chat(messages)
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        import numpy as np
        return [np.random.rand(384).tolist() for _ in texts]


class OpenAILLM(BaseLLM):
    """OpenAI GPT (付费)"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = config.api_key or os.getenv("OPENAI_API_KEY", "")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            logger.warning("openai 库未安装")
            self.client = None
    
    def chat(self, messages, system_prompt=None, temperature=0.7, max_tokens=2000) -> str:
        if not self.client:
            return MockLLM().chat(messages)
        
        try:
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend([{"role": m["role"], "content": m["content"]} for m in messages])
            
            response = self.client.chat.completions.create(
                model=self.config.model or "gpt-4",
                messages=all_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI 调用失败: {e}")
            return MockLLM().chat(messages)
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        if not self.client:
            return super().embedding(texts)
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [d.embedding for d in response.data]
        except Exception as e:
            logger.error(f"OpenAI embedding 失败: {e}")
            return super().embedding(texts)


class MiniMaxLLM(BaseLLM):
    """MiniMax (国内)"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = config.api_key or os.getenv("MINIMAX_API_KEY", "")
        self.base_url = config.base_url or "https://api.minimax.io"
        
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            logger.warning("openai 库未安装")
            self.client = None
    
    def chat(self, messages, system_prompt=None, temperature=0.7, max_tokens=2000) -> str:
        if not self.client:
            return MockLLM().chat(messages)
        
        try:
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend([{"role": m["role"], "content": m["content"]} for m in messages])
            
            response = self.client.chat.completions.create(
                model=self.config.model or "MiniMax-M2.1",
                messages=all_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"MiniMax 调用失败: {e}")
            return MockLLM().chat(messages)
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        import numpy as np
        return [np.random.rand(384).tolist() for _ in texts]


# ============ 便捷函数 ============

def create_llm_client(
    provider: str = "mock",
    api_key: str = None,
    model: str = None
) -> LLMClient:
    """
    创建 LLM 客户端
    
    Args:
        provider: 提供商 (mock/ollama/groq/openai/minimax)
        api_key: API Key
        model: 模型名称
        
    Returns:
        LLM 客户端
    """
    config = LLMConfig(
        provider=provider,
        api_key=api_key or os.getenv(f"{provider.upper()}_API_KEY", ""),
        model=model
    )
    return LLMClient(config)


def get_free_llm_options() -> Dict:
    """
    获取免费 LLM 选项
    """
    return {
        "mock": {
            "name": "Mock 模式",
            "description": "免费，无需 API Key",
            "cost": "$0",
            "setup": "无需设置",
            "quality": "⭐⭐"
        },
        "ollama": {
            "name": "Ollama 本地",
            "description": "完全免费，本地运行",
            "cost": "$0 (需本地 GPU/CPU)",
            "setup": "安装 Ollama + 下载模型",
            "quality": "⭐⭐⭐⭐"
        },
        "groq": {
            "name": "Groq 免费 tier",
            "description": "免费高速，Llama 3",
            "cost": "免费 tier",
            "setup": "注册 groq.cloud 获取 API Key",
            "quality": "⭐⭐⭐⭐⭐"
        }
    }


# 使用示例
if __name__ == "__main__":
    print("=" * 50)
    print("SuiLight Knowledge Salon - LLM 选项")
    print("=" * 50)
    
    options = get_free_llm_options()
    for key, info in options.items():
        print(f"\n{key.upper()}: {info['name']}")
        print(f"  费用: {info['cost']}")
        print(f"  质量: {info['quality']}")
        print(f"  设置: {info['setup']}")
    
    print("\n" + "=" * 50)
    print("使用免费 Mock 模式启动...")
    client = create_llm_client("mock")
    print(client.chat([{"role": "user", "content": "你好"}))
