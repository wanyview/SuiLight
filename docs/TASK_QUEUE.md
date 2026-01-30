# SuiLight Knowledge Salon - 异步任务队列

支持后台任务、进度追踪、任务取消。

## 架构

```
Task Queue System
├── Celery Worker        - 任务执行引擎
├── Redis Backend        - 消息队列 + 结果存储
├── Task API             - 任务管理 REST 接口
└── Task Monitor         - 任务状态监控
```

## 快速开始

### 1. 启动 Redis (必须)

```bash
# Docker 启动
docker run -d -p 6379:6379 redis:alpine

# 或本地安装
brew install redis
redis-server
```

### 2. 启动 Celery Worker

```bash
cd SuiLight
celery -A src.tasks worker --loglevel=info
```

### 3. 启动 API 服务

```bash
python -m uvicorn src.main:app --reload
```

## 使用示例

```python
import requests

# 1. 提交后台任务
resp = requests.post("http://localhost:8000/api/tasks", json={
    "task_type": "create_agents",
    "params": {
        "preset": "all",
        "domain": "physics"
    }
})
task_id = resp.json()["data"]["task_id"]

# 2. 查询任务状态
resp = requests.get(f"http://localhost:8000/api/tasks/{task_id}")
print(resp.json()["data"])
# {
#   "status": "running",
#   "progress": 45,
#   "result": null
# }

# 3. 等待任务完成
while True:
    resp = requests.get(f"http://localhost:8000/api/tasks/{task_id}")
    data = resp.json()["data"]
    if data["status"] == "completed":
        print("结果:", data["result"])
        break
    elif data["status"] == "failed":
        print("失败:", data["error"])
        break
```

## 内置任务类型

| 任务类型 | 说明 | 参数 |
|----------|------|------|
| `create_agents` | 批量创建 Agent | preset, domain, limit |
| `run_discussion` | 运行完整讨论 | topic_id, max_rounds |
| `extract_insights` | 批量提取洞见 | topic_ids |
| `chat_batch` | 批量对话 | messages, agent_ids |

## 配置

```bash
# .env 添加
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_URL=redis://localhost:6379/0
```
