# SuiLight Knowledge Salon
# 知识沙龙多智能体系统

基于多种 LLM 的知识沙龙多智能体协作平台。

## ✨ 特性

- 🤖 **100 位伟大思想家** - 预设历史级别的科学家、思想家、发明家
- 🧠 **DATM 知识矩阵** - Truth/Goodness/Beauty/Intelligence 四维框架
- 💬 **协作讨论** - 多 Agent 围绕科学发现/发明深度讨论
- 📚 **知识涌现** - 从讨论中提取洞见和创新想法
- 🌐 **多 LLM 支持** - 免费 + 付费，本地 + 云端

## 🚀 快速开始

### 方式 1: Mock 模式 (立即可用, 免费)

```bash
git clone https://github.com/wanyview/SuiLight.git
cd SuiLight

pip install -r requirements.txt

python -m uvicorn src.main:app --reload

# 访问 http://localhost:8000
```

### 方式 2: Ollama 本地 (免费)

```bash
# 1. 安装 Ollama: https://ollama.ai
# 2. ollama pull llama3
# 3. 设置环境变量
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3

python -m uvicorn src.main:app --reload
```

### 方式 3: Groq (免费高速)

```bash
# 1. 注册获取 API Key: https://console.groq.cloud
export GROQ_API_KEY="your-key"
export LLM_PROVIDER=groq

python -m uvicorn src.main:app --reload
```

## 🤖 100 位伟大思想家

### 自然科学 (物理学/化学/生物学/数学/天文学)
| Agent | 领域 | 贡献 |
|-------|------|------|
| 艾萨克·牛顿 | 物理 | 万有引力、经典力学 |
| 阿尔伯特·爱因斯坦 | 物理 | 相对论 |
| 玛丽·居里 | 物理/化学 | 放射性 |
| 查尔斯·达尔文 | 生物 | 进化论 |
| 欧拉/高斯/冯·诺依曼 | 数学 | 各领域 |

### 社会科学 (经济学/心理学/社会学)
| Agent | 领域 | 贡献 |
|-------|------|------|
| 亚当·斯密 | 经济 | 国富论 |
| 凯恩斯 | 经济 | 宏观经济学 |
| 弗洛伊德/荣格 | 心理 | 精神分析 |
| 韦伯/涂尔干 | 社会 | 社会学 |

### 人文科学 (哲学/艺术/文学)
| Agent | 领域 | 贡献 |
|-------|------|------|
| 苏格拉底/柏拉图/亚里士多德 | 哲学 | 西方哲学 |
| 孔子 | 哲学 | 儒家思想 |
| 达芬奇/莎士比亚 | 艺术 | 文艺复兴 |

### 交叉科学 (发明/工程/医学)
| Agent | 领域 | 贡献 |
|-------|------|------|
| 爱迪生 | 发明 | 电灯、2000+专利 |
| 特斯拉 | 工程 | 交流电 |
| 莱特兄弟 | 工程 | 飞机 |
| 希波克拉底 | 医学 | 医学之父 |

## 💬 讨论系统

### 创建讨论
```bash
curl -X POST "http://localhost:8000/api/discussions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "如何结合爱迪生的发明方法论与现代 AI 技术？",
    "description": "分析爱迪生的系统性试错方法，探讨如何应用于 AI 系统的发明创新",
    "category": "交叉科学",
    "target_level": "invention"
  }'
```

### 分配参与者
```bash
curl -X POST "http://localhost:8000/api/discussions/{topic_id}/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_ids": ["agent1_id", "agent2_id"]
  }'
```

### 开始讨论
```bash
curl -X POST "http://localhost:8000/api/discussions/{topic_id}/start"
```

### 添加贡献
```bash
curl -X POST "http://localhost:8000/api/discussions/{topic_id}/contribute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_id",
    "content": "我认为这个问题的关键在于...",
    "role": "commentator",
    "round_num": 1
  }'
```

### 提取洞见
```bash
curl -X POST "http://localhost:8000/api/discussions/{topic_id}/extract_insights"
```

## 📊 DATM 知识矩阵

每个 Agent 都有 Truth/Goodness/Beauty/Intelligence 四维评估:

```
Truth (真)      - 科学性、客观性、证据支撑
Goodness (善)   - 社科性、价值观、伦理考量  
Beauty (美)     - 人文性、美学、表达方式
Intelligence (灵) - 创新性、洞察力、前沿性
```

## 🏗️ 架构

```
SuiLight/
├── src/
│   ├── agents/
│   │   ├── base.py       # Agent 核心 + DATM
│   │   ├── presets.py    # 🆕 100位伟大思想家预设
│   │   └── registry.py   # Agent 注册表
│   │
│   ├── knowledge/
│   │   ├── generator.py  # 冷启动 Agent 生成
│   │   └── discussion.py # 🆕 协作讨论框架
│   │
│   └── api/
│       └── main.py       # FastAPI 服务
│
├── integrations/
│   ├── llm_factory.py    # 多 LLM 工厂
│   └── minimax/
│
├── .env.example
└── requirements.txt
```

## 📡 API 文档

### Agent 管理
- `GET /api/agents` - 列出所有 Agent
- `POST /api/agents` - 创建 Agent
- `POST /api/presets/create_all` - 批量创建 100 位思想家

### 讨论系统
- `POST /api/discussions` - 创建讨论
- `GET /api/discussions/suggestions` - 获取讨论建议
- `POST /api/discussions/{id}/start` - 开始讨论
- `POST /api/discussions/{id}/contribute` - 添加贡献
- `POST /api/discussions/{id}/extract_insights` - 提取洞见

### 对话
- `POST /api/chat` - 与 Agent 对话
- `POST /api/collaborate` - 多 Agent 协作

## 📖 预设讨论话题

1. **如何结合爱迪生的发明方法论与现代 AI 技术？**
2. **牛顿的万有引力定律如何启发暗物质研究？**
3. **如何用达芬奇的跨学科思维解决气候危机？**
4. **达尔文进化论对社会制度设计的启示**
5. **孔子思想与西方心理学的人格理论比较**

## 📦 LLM 支持

| 提供商 | 费用 | 速度 | 质量 | 设置 |
|--------|------|------|------|------|
| Mock | 免费 | 即时 | ⭐⭐ | 无需 |
| Groq | 免费 | 极快 | ⭐⭐⭐⭐⭐ | 简单 |
| Ollama | 免费 | 取决于硬件 | ⭐⭐⭐⭐ | 中等 |
| OpenAI | 付费 | 快 | ⭐⭐⭐⭐⭐ | 简单 |
| MiniMax | 付费 | 快 | ⭐⭐⭐⭐ | 简单 |

## 🛠️ 开发

```bash
pip install -r requirements.txt

# 运行
python -m uvicorn src.main:app --reload

# 测试
pytest
```

## 📄 许可证

MIT License

---

**让知识流动起来，让思想碰撞出火花** 🌟
