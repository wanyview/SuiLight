# SuiLight Knowledge Salon
# 知识沙龙多智能体系统

基于多种 LLM 的知识沙龙多智能体协作平台。

## ✨ 特性

- 🤖 **多智能体协作** - 多个专家 Agent 实时对话
- 🧠 **DATM 知识矩阵** - Truth/Goodness/Beauty/Intelligence 四维框架
- 📚 **冷启动专家** - 从文档自动生成 Agent
- 🔄 **知识涌现** - 多 Agent 交流产生新知识
- 🌐 **多 LLM 支持** - 免费 + 付费，本地 + 云端

## 🚀 快速开始

### 方式 1: Mock 模式 (立即可用, 免费)

```bash
git clone https://github.com/wanyview/SuiLight.git
cd SuiLight

# 安装依赖
pip install -r requirements.txt

# 运行 (默认使用 Mock 模式)
python -m uvicorn src.main:app --reload

# 访问
# http://localhost:8000
```

### 方式 2: Ollama 本地 (免费, 推荐)

```bash
# 1. 安装 Ollama
# https://ollama.ai

# 2. 下载模型
ollama pull llama3

# 3. 配置环境变量
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3

# 4. 运行
python -m uvicorn src.main:app --reload
```

### 方式 3: Groq (免费高速)

```bash
# 1. 注册获取 API Key
# https://console.groq.cloud

# 2. 配置
export GROQ_API_KEY="your-api-key"
export LLM_PROVIDER=groq

# 3. 运行
python -m uvicorn src.main:app --reload
```

## 📦 支持的 LLM

| 提供商 | 费用 | 质量 | 设置难度 |
|--------|------|------|----------|
| Mock | 免费 | ⭐⭐ | 无需设置 |
| Ollama (本地) | 免费 (硬件) | ⭐⭐⭐⭐ | 中等 |
| Groq | 免费 tier | ⭐⭐⭐⭐⭐ | 简单 |
| OpenAI (GPT-4) | 付费 | ⭐⭐⭐⭐⭐ | 简单 |
| MiniMax | 付费 | ⭐⭐⭐⭐ | 简单 |

## 🏗️ 架构

```
SuiLight-Knowledge-Salon/
├── src/
│   ├── agents/           # Agent 核心
│   │   └── base.py       # Agent 基类 + DATM
│   │
│   ├── knowledge/        # 知识引擎
│   │   └── generator.py  # 冷启动 Agent 生成
│   │
│   └── api/              # FastAPI 服务
│       └── main.py
│
├── integrations/
│   ├── llm_factory.py   # 🆕 多 LLM 工厂
│   └── minimax/         # MiniMax 集成
│
├── .env.example          # 环境变量模板
└── requirements.txt      # 依赖列表
```

## 📡 API 示例

```python
import requests

# 创建 Agent
resp = requests.post("http://localhost:8000/api/agents", json={
    "name": "咖啡专家",
    "domain": "coffee",
    "expertise": ["咖啡冲煮", "咖啡豆", "咖啡文化"],
    "datm": {"truth": 85, "goodness": 60, "beauty": 50, "intelligence": 75}
})
agent = resp.json()["data"]

# 对话
resp = requests.post("http://localhost:8000/api/chat", json={
    "agent_id": agent["id"],
    "message": "什么是手冲咖啡？"
})
print(resp.json()["data"]["response"])
```

## 📖 文档

- [完整发展规划](ANALYSIS.md)
- [GitHub 优化方案](docs/DEVELOPMENT_ROADMAP.md)

## 🛠️ 开发

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install black isort mypy

# 代码检查
black src/ tests/
isort src/ tests/
mypy src/

# 运行测试
pytest
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**让知识流动起来** 🌊
