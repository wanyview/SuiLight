# SuiLight-Knowledge-Salon
# 基于 SuiLight 的知识沙龙多智能体系统

基于 MiniMax LLM 的知识沙龙多智能体协作平台。

## 架构

```
SuiLight-Knowledge-Salon/
├── src/
│   ├── agents/           # Agent 核心模块
│   │   ├── base.py       # Agent 基类
│   │   ├── registry.py   # Agent 注册表
│   │   └── protocols.py  # 通信协议
│   │
│   ├── knowledge/        # 知识引擎
│   │   ├── parser.py     # 文档解析
│   │   ├── graph.py      # 知识图谱
│   │   └── generator.py  # Agent 生成器
│   │
│   ├── emergence/        # 涌现系统
│   │   ├── coordinator.py # 多 Agent 协调
│   │   └── fusion.py     # 知识融合
│   │
│   ├── memory/           # 记忆系统
│   │   ├── logs.py       # 交互日志
│   │   └──沉淀/         # 知识沉淀
│   │
│   └── api/              # API 层
│       ├── routes.py
│       └── models.py
│
├── integrations/
│   └── minimax/          # MiniMax 集成
│       ├── client.py
│       └── prompts.py
│
├── ui/                   # 前端界面
│   └── (React/Vue)
│
├── scripts/              # 部署脚本 (来自 SuiLight)
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── tests/                # 测试
    └── ...
```

## 快速开始

```bash
# 克隆项目
git clone https://github.com/wanyview/SuiLight-Knowledge-Salon.git
cd SuiLight-Knowledge-Salon

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env, 添加 MiniMax API Key

# 运行
python -m uvicorn src.main:app --reload
```

## 文档

详见 [ANALYSIS.md](ANALYSIS.md) 了解完整发展规划。

## 许可证

MIT License
