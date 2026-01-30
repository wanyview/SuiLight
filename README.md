# SuiLight Knowledge Salon
# 知识沙龙多智能体系统

基于多种 LLM 的知识沙龙多智能体协作平台。

## ✨ 特性

- 🤖 **100 位伟大思想家** - 预设历史级别的科学家、思想家、发明家
- 🧠 **DATM 知识矩阵** - Truth/Goodness/Beauty/Intelligence 四维框架
- 💬 **协作讨论** - 多 Agent 围绕科学发现/发明深度讨论
- 📚 **知识涌现** - 从讨论中提取洞见和创新想法
- ⚡ **异步任务队列** - 支持后台任务、多任务并行
- 🌐 **多 LLM 支持** - 免费 + 付费，本地 + 云端

## 🚀 快速开始 (5分钟)

### 1. 克隆并安装

```bash
git clone https://github.com/wanyview/SuiLight.git
cd SuiLight

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 方式 A: 使用 Makefile (推荐)
make run

# 方式 B: 直接运行
python -m uvicorn src.main:app --reload

# 方式 C: 使用 CLI
suilight --port 8000
```

### 3. 访问

```
Web UI: http://localhost:8000
API Docs: http://localhost:8000/docs
```

---

## 📖 完整文档

### 高级用法

```bash
# 启动 Celery Worker (后台任务需要)
make worker

# 运行测试
make test

# 代码检查
make check
```

### Docker 部署

```bash
# 构建
make docker

# 运行
docker run -p 8000:8000 suilight
```

---

## 🏗️ 架构

```
SuiLight/
├── src/
│   ├── agents/           # Agent 核心
│   │   ├── base.py       # Agent + DATM
│   │   ├── presets.py    # 100位思想家
│   │   └── registry.py   # 注册表
│   ├── knowledge/        # 知识引擎
│   │   ├── generator.py  # 冷启动生成
│   │   └── discussion.py # 讨论框架
│   ├── tasks.py          # 异步任务
│   ├── storage.py        # 持久化
│   └── main.py           # FastAPI API
├── ui/                   # Web UI
├── tests/                # 测试
├── Makefile              # 构建脚本
├── SKILL.md              # Skill 文档
└── pyproject.toml        # 包配置
```

---

## 📚 功能说明

### Agent 管理

| 功能 | 说明 |
|------|------|
| 预设 Agent | 100 位历史思想家 |
| 自定义 Agent | 创建自己的 Agent |
| DATM 评估 | 四维知识矩阵 |
| 对话历史 | 自动持久化 |

### 讨论系统

| 功能 | 说明 |
|------|------|
| 创建讨论 | 定义议题和目标 |
| 分配 Agent | 自动或手动分配 |
| 多轮讨论 | 引言→分析→辩论→综合 |
| 提取洞见 | 从讨论中提取智慧 |

### 任务队列

| 功能 | 说明 |
|------|------|
| 后台执行 | 长时间任务不阻塞 |
| 进度追踪 | 实时查看进度 |
| 任务取消 | 支持取消运行中任务 |

---

## 💰 LLM 选项

| 选项 | 费用 | 速度 | 质量 | 推荐场景 |
|------|------|------|------|----------|
| **Mock** | 免费 | 即时 | ⭐⭐ | 开发测试 |
| **Groq** | 免费 | 极快 | ⭐⭐⭐⭐⭐ | **生产推荐** |
| **Ollama** | 免费 | 取决于硬件 | ⭐⭐⭐⭐ | 本地部署 |
| **OpenAI** | 付费 | 快 | ⭐⭐⭐⭐⭐ | 高质量需求 |

### 配置 LLM

```bash
# Groq (推荐)
export GROQ_API_KEY="your-key"
export LLM_PROVIDER=groq

# Ollama
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3

# OpenAI
export OPENAI_API_KEY="your-key"
export LLM_PROVIDER=openai
export LLM_MODEL="gpt-4"
```

---

## 🛠️ 开发

```bash
# 克隆
git clone https://github.com/wanyview/SuiLight.git
cd SuiLight

# 开发环境
make install-dev

# 运行测试
make test

# 代码格式化
make format

# 检查
make check
```

---

## 📦 作为 Python 包使用

```python
from suilight import create_agent, create_app

# 创建 Agent
agent = create_agent(
    name="你的专家",
    domain="custom",
    datm={"truth": 85, "goodness": 70, "beauty": 60, "intelligence": 80}
)

# 对话
response = agent.chat("你好，请介绍一下你的专长")

# 启动服务
create_app(port=8000)
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎 Issue 和 Pull Request！

---

**让知识流动起来，让思想碰撞出火花** 🌟
