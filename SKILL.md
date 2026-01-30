---
name: suilight-knowledge-salon
description: "SuiLight 知识沙龙 - 多智能体知识协作平台。支持创建 100+ 位思想家 Agent，围绕科学发现/发明进行协作讨论，知识涌现与沉淀。可用于教育、科研、决策支持等场景。"
metadata: {
  "moltbot": {
    "emoji": "🧠",
    "repo": "wanyview/SuiLight",
    "docs": "https://github.com/wanyview/SuiLight",
    "author": "Kai Digital Agent"
  }
}
---

# SuiLight 知识沙龙 🧠

SuiLight 知识沙龙是一个**多智能体知识协作平台**，可以创建 100+ 位历史级别的思想家 Agent，围绕科学发现、发明创造、社会议题进行深度协作讨论。

## 核心特性

### 🤖 100+ 伟大思想家 Agent

预置 100 位历史级别的科学家、思想家、发明家：

| 分类 | 代表人物 | 领域 |
|------|----------|------|
| **自然科学** | 牛顿、爱因斯坦、达尔文 | 物理、生物、数学 |
| **社会科学** | 亚当·斯密、凯恩斯、弗洛伊德 | 经济、心理、社会 |
| **人文科学** | 苏格拉底、孔子、达芬奇 | 哲学、艺术、文学 |
| **交叉科学** | 爱迪生、特斯拉、鲁班 | 发明、工程、医学 |

每个 Agent 都有独特的 **DATM 知识矩阵** (Truth/Goodness/Beauty/Intelligence)。

### 💬 协作讨论系统

多 Agent 围绕议题进行深度讨论：

```
讨论流程:
1. 引言 (Introduction)    → 主讲人开场
2. 分析 (Perspectives)    → 多角度分析
3. 辩论 (Debate)          → 观点碰撞
4. 综合 (Synthesis)       → 整合观点
5. 结论 (Conclusion)      → 总结洞见
```

### 📚 知识涌现与沉淀

- 自动提取讨论中的共识与分歧
- 识别创新性想法
- 生成知识洞见
- 持久化存储对话历史

### ⚡ 异步任务队列

支持后台运行长时间任务：
- 批量创建 Agent
- 运行完整讨论流程
- 批量提取洞见

---

## 快速开始

### 1. 安装

```bash
git clone https://github.com/wanyview/SuiLight.git
cd SuiLight

pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 启动 API 服务 (默认 Mock 模式，无需 API Key)
python -m uvicorn src.main:app --reload

# 访问 Web UI
# http://localhost:8000
```

### 3. 使用示例

```python
import requests

# 1. 批量创建 100 位思想家
resp = requests.post("http://localhost:8000/api/tasks/create_agents_background", json={
    "limit": 100
})

# 2. 创建讨论
resp = requests.post("http://localhost:8000/api/discussions", json={
    "title": "如何用 AI 解决气候变化问题？",
    "description": "结合科学、技术、经济多角度讨论",
    "category": "交叉科学"
})

# 3. 开始讨论
topic_id = resp.json()["data"]["id"]
requests.post(f"http://localhost:8000/api/discussions/{topic_id}/assign")
requests.post(f"http://localhost:8000/api/discussions/{topic_id}/start")

# 4. 提取洞见
insights = requests.post(f"http://localhost:8000/api/discussions/{topic_id}/extract_insights")
```

---

## API 参考

### Agent 管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/agents` | GET | 列出所有 Agent |
| `/api/agents` | POST | 创建 Agent |
| `/api/presets/create_all` | POST | 批量创建 100 位思想家 |

### 对话

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat` | POST | 与 Agent 对话 |
| `/api/collaborate` | POST | 多 Agent 协作 |

### 讨论系统

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/discussions` | POST | 创建讨论 |
| `/api/discussions/{id}/start` | POST | 开始讨论 |
| `/api/discussions/{id}/contribute` | POST | 添加观点 |
| `/api/discussions/{id}/extract_insights` | POST | 提取洞见 |

### 任务队列

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tasks` | GET | 列出任务 |
| `/api/tasks` | POST | 创建任务 |
| `/api/tasks/{id}` | GET | 查询状态 |

### 历史

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/history` | GET | 对话历史 |
| `/api/history/search` | GET | 搜索历史 |

---

## 配置选项

### LLM 后端

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `LLM_PROVIDER` | 提供商 (mock/ollama/groq/openai/minimax) | mock |
| `GROQ_API_KEY` | Groq API Key | - |
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `MINIMAX_API_KEY` | MiniMax API Key | - |
| `LLM_MODEL` | 模型名称 | llama3 |

### 推荐免费配置

**Groq (免费高速)**:
```bash
export GROQ_API_KEY="your-key"
export LLM_PROVIDER=groq
```

**Ollama (本地免费)**:
```bash
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3
```

---

## 应用场景

### 🎓 教育场景

- 历史人物对话: "如果孔子和爱因斯坦对话"
- 思想实验: "电车难题的多角度分析"
- 跨学科讨论: "AI 是否拥有意识"

### 🔬 科研场景

- 文献综述: "让不同领域的专家评价新论文"
- 假设验证: "多角度审视研究假设"
- 创新激发: "跨领域头脑风暴"

### 💼 商业决策

- 风险评估: "多专家视角的风险分析"
- 市场洞察: "不同视角的市场预测"
- 战略规划: "多维度战略讨论"

### 🏛️ 公共议题

- 政策讨论: "AI 监管的多方观点"
- 社会议题: "气候变化的多学科讨论"
- 伦理困境: "基因编辑的伦理边界"

---

## DATM 知识矩阵

每个 Agent 都有四维评估：

```
Truth (真)      - 科学性、客观性、证据支撑
Goodness (善)   - 社科性、价值观、伦理考量
Beauty (美)     - 人文性、美学、表达方式
Intelligence (灵) - 创新性、洞察力、前沿性
```

### 自定义 Agent DATM

```python
requests.post("http://localhost:8000/api/agents", json={
    "name": "你的专家",
    "domain": "custom",
    "datm": {
        "truth": 85,
        "goodness": 70,
        "beauty": 60,
        "intelligence": 80
    }
})
```

---

## 架构

```
SuiLight/
├── src/
│   ├── agents/           # Agent 核心
│   │   ├── base.py       # Agent 基类
│   │   ├── presets.py    # 100位思想家预设
│   │   └── registry.py   # Agent 注册表
│   │
│   ├── knowledge/        # 知识引擎
│   │   ├── generator.py  # 冷启动生成
│   │   └── discussion.py # 讨论框架
│   │
│   ├── tasks.py          # 异步任务队列
│   ├── storage.py        # 持久化存储
│   └── main.py           # FastAPI 服务
│
├── ui/                   # Web UI
│   └── index.html
│
└── requirements.txt
```

---

## 最佳实践

1. **明确讨论目标** - 好的议题是成功讨论的一半
2. **合理配置参与者** - 选择不同视角的 Agent
3. **多轮迭代** - 至少 3 轮讨论获得深度洞见
4. **提取并保存洞见** - 重要洞见要及时保存
5. **结合真实知识** - 让 Agent 学习领域文档

---

## 与其他系统集成

### 作为 FastAPI 服务调用

```python
from src.main import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 独立使用 Agent

```python
from src.agents.base import Agent, AgentConfig, DATM

config = AgentConfig(
    name="自定义专家",
    domain="custom",
    datm=DATM(truth=85, goodness=70, beauty=60, intelligence=80)
)

agent = Agent(config)
response = agent.chat("你好，请介绍一下你的专长")
```

### 自定义讨论流程

```python
from src.knowledge.discussion import DiscussionManager

dm = DiscussionManager(registry)
topic = dm.create_topic(
    title="自定义议题",
    description="描述",
    category="custom"
)

dm.assign_participants(topic.id)
dm.start_discussion(topic.id)
```

---

## License

MIT License

---

**让知识流动起来，让思想碰撞出火花** 🌟
