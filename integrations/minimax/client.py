"""
SuiLight Knowledge Salon - MiniMax Integration
MiniMax LLM 集成
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

# 尝试导入 OpenAI 兼容的 MiniMax API
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("Warning: openai library not installed. Install with: pip install openai")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MiniMaxConfig:
    """MiniMax 配置"""
    api_key: str = ""
    base_url: str = "https://api.minimax.io"
    model: str = "MiniMax-M2.1"
    temperature: float = 0.7
    max_tokens: int = 2000


class MiniMaxClient:
    """
    MiniMax API 客户端
    
    封装 MiniMax LLM 调用
    """
    
    def __init__(self, config: MiniMaxConfig = None):
        if config is None:
            config = MiniMaxConfig(
                api_key=os.getenv("MINIMAX_API_KEY", ""),
                model=os.getenv("MINIMAX_MODEL", "MiniMax-M2.1")
            )
        
        self.config = config
        
        if not self.config.api_key:
            logger.warning("MiniMax API Key 未配置，使用 Mock 模式")
            self.client = None
        elif HAS_OPENAI:
            self.client = OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
        else:
            logger.error("需要安装 openai 库: pip install openai")
            self.client = None
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        聊天接口
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大 token 数
            
        Returns:
            生成的回复
        """
        # 构建消息
        all_messages = []
        
        if system_prompt:
            all_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        all_messages.extend(messages)
        
        # 使用默认值
        temperature = temperature or self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        if self.client is None:
            # Mock 模式
            return self._mock_chat(all_messages)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=all_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"MiniMax API 调用失败: {e}")
            return self._mock_chat(all_messages)
    
    def _mock_chat(self, messages: List[Dict]) -> str:
        """Mock 聊天 (无 API Key 时使用)"""
        # 提取最后用户消息
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        if not user_message:
            return "你好！"
        
        return f"【MiniMax Mock】收到你的消息: {user_message}\n\n(请配置 MiniMax API Key 启用真实对话)"
    
    def embedding(self, texts: List[str]) -> List[List[float]]:
        """
        获取文本嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        if self.client is None:
            # Mock 模式
            import numpy as np
            return [np.random.rand(384).tolist() for _ in texts]
        
        try:
            # MiniMax 可能不支持 embedding，使用替代方案
            logger.warning("Embedding API 未实现，返回随机向量")
            import numpy as np
            return [np.random.rand(384).tolist() for _ in texts]
        except Exception as e:
            logger.error(f"Embedding 调用失败: {e}")
            import numpy as np
            return [np.random.rand(384).tolist() for _ in texts]


class AgentLLMInterface:
    """
    Agent LLM 接口
    
    将 Agent 连接到 MiniMax LLM
    """
    
    def __init__(self, minimax_client: MiniMaxClient = None):
        self.client = minimax_client or MiniMaxClient()
    
    def think(self, agent, message: str, context: List[Dict] = None) -> str:
        """
        Agent 思考 (调用 LLM)
        
        Args:
            agent: Agent 实例
            message: 用户消息
            context: 对话上下文
            
        Returns:
            思考结果
        """
        # 构建消息
        messages = []
        
        if context:
            # 添加历史上下文
            for c in context[-5:]:  # 只用最近 5 条
                messages.append({
                    "role": c.get("role", "assistant"),
                    "content": c.get("content", "")
                })
        
        # 添加当前消息
        messages.append({
            "role": "user",
            "content": message
        })
        
        # 调用 LLM
        response = self.client.chat(
            messages=messages,
            system_prompt=agent.config.system_prompt,
            temperature=0.7
        )
        
        return response
    
    def batch_think(
        self,
        agents: List[Agent],
        message: str,
        context: Dict[Agent, List[Dict]] = None
    ) -> Dict[Agent, str]:
        """
        多 Agent 并发思考
        
        Args:
            agents: Agent 列表
            message: 消息
            context: 各 Agent 的上下文
            
        Returns:
            Agent -> 响应 的映射
        """
        responses = {}
        
        for agent in agents:
            agent_context = context.get(agent, []) if context else None
            responses[agent] = self.think(agent, message, agent_context)
        
        return responses


def create_minimax_client(api_key: str = None) -> MiniMaxClient:
    """创建 MiniMax 客户端"""
    config = MiniMaxConfig(api_key=api_key or os.getenv("MINIMAX_API_KEY", ""))
    return MiniMaxClient(config)


# 使用示例
if __name__ == "__main__":
    # 创建客户端
    client = create_minimax_client()
    
    # 测试聊天
    messages = [
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
    
    response = client.chat(messages)
    print(f"回复: {response}")
