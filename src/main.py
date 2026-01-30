"""
SuiLight Knowledge Salon - API Server
知识沙龙多智能体系统 API 服务

功能:
- Agent 管理 (创建、对话、学习)
- 预设伟大思想家 (100位专家)
- 协作讨论框架
- 知识沉淀
- 异步任务队列
"""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from contextlib import asynccontextmanager
import logging

# 导入 Agent 框架
from src.agents.base import Agent, AgentConfig, DATM, AgentRegistry, AgentMessage
from src.agents.presets import (
    GREAT_MINDS, create_agent_configs, get_domains, 
    get_category_distribution, search_agents
)
from src.knowledge.generator import KnowledgeParser, AgentGenerator
from src.knowledge.discussion import (
    DiscussionManager, DiscussionPhase,
    get_great_discussions
)
from src.knowledge.capsule import (
    CapsuleGenerator, CapsuleEvaluator,
    CapsuleTemplateManager, CapsuleVersionManager,
    CapsuleRecommender
)
from src.tasks import TaskManager, TaskStatus
from src.storage import StorageManager
from src.coffee import coffee_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化
registry = AgentRegistry()
generator = AgentGenerator()
discussion_manager = DiscussionManager(registry)
task_manager = TaskManager()
storage = StorageManager()

# 注入依赖
task_manager.set_registry(registry)
task_manager.set_discussion_manager(discussion_manager)

# FastAPI 应用
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 SuiLight Knowledge Salon 启动")
    logger.info("📚 100位伟大思想家知识沙龙")
    logger.info(f"🧠 当前注册 Agent: {len(registry.list_all())} 位")
    logger.info("⚡ 异步任务队列已就绪")
    yield
    logger.info("👋 服务关闭")

app = FastAPI(
    title="SuiLight Knowledge Salon API",
    description="知识沙龙多智能体系统 API - 100位伟大思想家的协作讨论平台",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务 (Web UI)
ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui")
if os.path.exists(ui_path):
    app.mount("/ui", StaticFiles(directory=ui_path), name="ui")
    logger.info(f"📱 Web UI 已挂载: /ui")

# 首页重定向到 UI

# ============ 数据模型 ============

class CreateAgentRequest(BaseModel):
    name: str
    domain: str
    description: Optional[str] = ""
    expertise: List[str] = []
    datm: Optional[Dict[str, int]] = None
    system_prompt: Optional[str] = ""

class ChatRequest(BaseModel):
    agent_id: str
    message: str
    context: Optional[List[Dict]] = None

class LearnRequest(BaseModel):
    agent_id: str
    knowledge: str
    source: Optional[str] = "manual"

class CollaborateRequest(BaseModel):
    message: str
    agent_ids: List[str]

class UploadKnowledgeRequest(BaseModel):
    agent_name: str
    domain: str
    files: List[str]
    datm: Optional[Dict[str, int]] = None

class CreateTopicRequest(BaseModel):
    title: str
    description: str
    category: str = "交叉科学"
    target_level: str = "discovery"
    keywords: List[str] = []
    max_participants: int = 5
    max_rounds: int = 3

class AddContributionRequest(BaseModel):
    agent_id: str
    content: str
    role: str = "commentator"
    round_num: int = 1

# ============ 任务相关模型 ============

class CreateTaskRequest(BaseModel):
    task_type: str  # create_agents / run_discussion / extract_insights / chat_batch
    params: Dict = {}

class TaskType:
    """任务类型"""
    CREATE_AGENTS = "create_agents"
    RUN_DISCUSSION = "run_discussion"
    EXTRACT_INSIGHTS = "extract_insights"
    CHAT_BATCH = "chat_batch"


from fastapi.responses import RedirectResponse

# ============ API 端点 ============

@app.get("/")
async def root():
    """首页重定向到 Web UI"""
    return RedirectResponse(url="/ui/index.html")

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============ Agent 管理 ============

@app.get("/api/agents")
async def list_agents():
    """列出所有 Agent"""
    return {
        "success": True,
        "data": registry.to_dict()
    }

@app.post("/api/agents")
async def create_agent(request: CreateAgentRequest):
    """创建 Agent"""
    datm = DATM.from_dict(request.datm) if request.datm else DATM()
    
    config = AgentConfig(
        name=request.name,
        domain=request.domain,
        description=request.description,
        expertise=request.expertise,
        datm=datm,
        system_prompt=request.system_prompt
    )
    
    agent = Agent(config)
    registry.register(agent)
    
    return {
        "success": True,
        "data": agent.to_dict()
    }

@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """获取 Agent"""
    agent = registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent 不存在")
    
    return {
        "success": True,
        "data": agent.to_dict()
    }

@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """删除 Agent"""
    success = registry.unregister(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent 不存在")
    
    return {"success": True}

# ============ 预设 Agent ============

@app.get("/api/presets")
async def list_presets():
    """列出所有预设 Agent"""
    return {
        "success": True,
        "data": {
            "total": len(GREAT_MINDS),
            "domains": get_domains(),
            "distribution": get_category_distribution()
        }
    }

@app.get("/api/presets/great_minds")
async def get_great_minds(domain: str = None, search: str = None):
    """获取伟大思想家列表"""
    if search:
        results = {}
        for name, info in GREAT_MINDS.items():
            if search.lower() in name.lower():
                results[name] = info
        return {
            "success": True,
            "data": {"count": len(results), "results": results}
        }
    
    if domain:
        results = {}
        for name, info in GREAT_MINDS.items():
            if info["domain"] == domain:
                results[name] = info
        return {
            "success": True,
            "data": {"count": len(results), "results": results}
        }
    
    return {
        "success": True,
        "data": {
            "total": len(GREAT_MINDS),
            "presets": GREAT_MINDS
        }
    }

@app.post("/api/presets/create")
async def create_from_preset(names: List[str]):
    """从预设创建 Agent"""
    created = []
    
    for name in names:
        if name not in GREAT_MINDS:
            continue
        
        info = GREAT_MINDS[name]
        datm = DATM.from_dict(info.get("datm", {}))
        
        config = AgentConfig(
            name=name,
            domain=info["domain"],
            description=info["description"],
            expertise=info["expertise"],
            datm=datm
        )
        
        agent = Agent(config)
        registry.register(agent)
        created.append(agent.to_dict())
    
    return {
        "success": True,
        "data": {
            "created": len(created),
            "agents": created
        }
    }

@app.post("/api/presets/create_all")
async def create_all_presets(domain: str = None, limit: int = 50):
    """批量创建预设 Agent (同步)"""
    configs = create_agent_configs()
    
    if domain:
        configs = [c for c in configs if c.domain == domain]
    
    configs = configs[:limit]
    
    created = []
    for config in configs:
        agent = Agent(config)
        registry.register(agent)
        created.append(agent.to_dict())
    
    return {
        "success": True,
        "data": {
            "created": len(created),
            "agents": created
        }
    }

# ============ 对话接口 ============

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """与 Agent 对话"""
    agent = registry.get(request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent 不存在")
    
    response = agent.chat(request.message, request.context)
    
    return {
        "success": True,
        "data": {
            "agent_id": agent.id,
            "agent_name": agent.config.name,
            "response": response,
            "datm": agent.config.datm.to_dict()
        }
    }

@app.post("/api/agents/{agent_id}/learn")
async def learn(agent_id: str, request: LearnRequest):
    """Agent 学习新知识"""
    agent = registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent 不存在")
    
    success = agent.learn(request.knowledge, source=request.source)
    
    return {
        "success": success,
        "knowledge_count": len(agent.knowledge_base)
    }

@app.post("/api/collaborate")
async def collaborate(request: CollaborateRequest):
    """多 Agent 协作"""
    agents = []
    for agent_id in request.agent_ids:
        agent = registry.get(agent_id)
        if agent:
            agents.append(agent)
    
    if not agents:
        raise HTTPException(status_code=404, detail="未找到有效的 Agent")
    
    responses = {}
    for agent in agents:
        responses[agent.config.name] = agent.collaborate(request.message, agents)
    
    return {
        "success": True,
        "data": {
            "participants": [a.config.name for a in agents],
            "responses": responses
        }
    }

# ============ 讨论系统 ============

@app.get("/api/discussions")
async def list_discussions(status: str = None):
    """列出讨论"""
    return {
        "success": True,
        "data": discussion_manager.list_topics(status)
    }

@app.post("/api/discussions")
async def create_discussion(request: CreateTopicRequest):
    """创建讨论议题"""
    topic = discussion_manager.create_topic(
        title=request.title,
        description=request.description,
        category=request.category,
        target_level=request.target_level,
        keywords=request.keywords,
        max_participants=request.max_participants,
        max_rounds=request.max_rounds
    )
    
    return {
        "success": True,
        "data": topic.to_dict()
    }

@app.get("/api/discussions/suggestions")
async def get_discussion_suggestions(category: str = None, count: int = 5):
    """获取讨论建议"""
    suggestions = discussion_manager.suggest_topics(category, count)
    return {
        "success": True,
        "data": suggestions
    }

@app.get("/api/discussions/great_discussions")
async def get_great_discussions():
    """获取预设的伟大讨论"""
    return {
        "success": True,
        "data": get_great_discussions()
    }

@app.post("/api/discussions/{topic_id}/start")
async def start_discussion(topic_id: str):
    """开始讨论"""
    result = discussion_manager.start_discussion(topic_id)
    return {
        "success": True,
        "data": result
    }

@app.post("/api/discussions/{topic_id}/assign")
async def assign_participants(topic_id: str, agent_ids: List[str] = None):
    """分配参与者"""
    participants = discussion_manager.assign_participants(
        topic_id=topic_id,
        agent_ids=agent_ids,
        auto_assign=not agent_ids
    )
    
    return {
        "success": True,
        "data": {
            "participants": [p.config.name for p in participants]
        }
    }

@app.post("/api/discussions/{topic_id}/contribute")
async def add_contribution(topic_id: str, request: AddContributionRequest):
    """添加讨论贡献"""
    contribution = discussion_manager.add_contribution(
        topic_id=topic_id,
        agent_id=request.agent_id,
        content=request.content,
        role=request.role,
        round_num=request.round_num
    )
    
    return {
        "success": True,
        "data": contribution.to_dict()
    }

@app.post("/api/discussions/{topic_id}/next_phase")
async def next_phase(topic_id: str):
    """推进讨论阶段"""
    result = discussion_manager.next_phase(topic_id)
    return {
        "success": True,
        "data": result
    }

@app.post("/api/discussions/{topic_id}/extract_insights")
async def extract_insights(topic_id: str):
    """从讨论中提取洞见"""
    insights = discussion_manager.extract_insights(topic_id)
    return {
        "success": True,
        "data": [i.to_dict() for i in insights]
    }

@app.get("/api/discussions/{topic_id}/summary")
async def get_discussion_summary(topic_id: str):
    """获取讨论摘要"""
    summary = discussion_manager.get_topic_summary(topic_id)
    return {
        "success": True,
        "data": summary
    }

# ============ 知识上传 ============

@app.post("/api/upload-knowledge")
async def upload_knowledge(request: UploadKnowledgeRequest):
    """从文件创建 Agent"""
    agent = generator.generate_from_files(
        name=request.agent_name,
        domain=request.domain,
        file_paths=request.files,
        datm_config=request.datm
    )
    
    registry.register(agent)
    
    return {
        "success": True,
        "data": {
            "agent": agent.to_dict(),
            "knowledge_count": len(agent.knowledge_base)
        }
    }

# ============ DATM 可视化 ============

@app.get("/api/agents/{agent_id}/datm")
async def get_agent_datm(agent_id: str):
    """获取 Agent DATM"""
    agent = registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent 不存在")
    
    return {
        "success": True,
        "data": agent.config.datm.to_radar_data()
    }

# ============ 搜索 ============

@app.get("/api/search")
async def search_agents(domain: str = None, topic: str = None):
    """搜索 Agent"""
    if domain:
        agents = registry.find_by_domain(domain)
    elif topic:
        agents = registry.find_by_expertise(topic)
    else:
        agents = registry.list_all()
    
    return {
        "success": True,
        "data": [a.to_dict() for a in agents]
    }

# ============ 任务队列 API ============

@app.get("/api/tasks")
async def list_tasks(status: str = None):
    """列出任务"""
    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    tasks = task_manager.list_tasks(task_status)
    
    return {
        "success": True,
        "data": {
            "total": len(tasks),
            "tasks": [t.to_dict() for t in tasks]
        }
    }

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """获取任务详情"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return {
        "success": True,
        "data": task.to_dict()
    }

@app.post("/api/tasks")
async def create_task(request: CreateTaskRequest):
    """创建后台任务
    
    支持的任务类型:
    - create_agents: 批量创建 Agent
    - run_discussion: 运行讨论
    - extract_insights: 提取洞见
    - chat_batch: 批量对话
    """
    task = task_manager.create_task(
        task_type=request.task_type,
        params=request.params
    )
    
    return {
        "success": True,
        "data": {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "status": task.status.value,
            "message": "任务已提交，请使用 /api/tasks/{task_id} 查询状态"
        }
    }

@app.post("/api/tasks/{task_id}/cancel")
async def cancel_task(task_id: str):
    """取消任务"""
    success = task_manager.cancel_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="无法取消任务（可能已完成或不存在）")
    
    return {
        "success": True,
        "message": "任务已取消"
    }

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 从任务列表中移除
    del task_manager.tasks[task_id]
    
    return {
        "success": True,
        "message": "任务已删除"
    }

# ============ 快捷任务 ============

@app.post("/api/tasks/create_agents_background")
async def create_agents_background(domain: str = None, limit: int = 50):
    """后台批量创建 Agent (快捷接口)"""
    task = task_manager.create_task(
        task_type="create_agents",
        params={
            "preset": "all",
            "domain": domain,
            "limit": limit
        }
    )
    
    return {
        "success": True,
        "data": {
            "task_id": task.task_id,
            "status": task.status.value,
            "message": f"正在后台创建 {limit} 位 Agent..."
        }
    }

@app.post("/api/tasks/run_discussion_background")
async def run_discussion_background(topic_id: str, max_rounds: int = 3):
    """后台运行讨论 (快捷接口)"""
    task = task_manager.create_task(
        task_type="run_discussion",
        params={
            "topic_id": topic_id,
            "max_rounds": max_rounds
        }
    )
    
    return {
        "success": True,
        "data": {
            "task_id": task.task_id,
            "status": task.status.value,
            "message": f"正在后台运行讨论 ({max_rounds} 轮)..."
        }
    }


# ============ 存储 API ============

@app.get("/api/history")
async def get_chat_history(agent_id: str = None, limit: int = 50, offset: int = 0):
    """获取对话历史"""
    history = storage.get_chat_history(agent_id=agent_id, limit=limit, offset=offset)
    return {
        "success": True,
        "data": {
            "count": len(history),
            "history": history
        }
    }

@app.get("/api/history/{agent_id}")
async def get_agent_chat_history(agent_id: str, limit: int = 100):
    """获取与指定 Agent 的对话历史"""
    history = storage.get_chat_by_agent(agent_id)
    history = history[:limit]
    return {
        "success": True,
        "data": {
            "agent_id": agent_id,
            "count": len(history),
            "history": history
        }
    }

@app.get("/api/history/search")
async def search_history(query: str, limit: int = 20):
    """搜索对话历史"""
    results = storage.search_chat(query, limit)
    return {
        "success": True,
        "data": {
            "query": query,
            "count": len(results),
            "results": results
        }
    }

@app.delete("/api/history")
async def clear_history(agent_id: str = None):
    """清空对话历史"""
    count = storage.clear_chat_history(agent_id)
    return {
        "success": True,
        "message": f"已删除 {count} 条对话记录"
    }

@app.get("/api/discussions/history")
async def get_discussions_history(limit: int = 50):
    """获取讨论历史"""
    discussions = storage.get_discussion_history(limit=limit)
    return {
        "success": True,
        "data": {
            "count": len(discussions),
            "discussions": discussions
        }
    }

@app.get("/api/insights")
async def get_insights(topic_id: str = None, limit: int = 100):
    """获取知识洞见"""
    insights = storage.get_insights(topic_id, limit)
    return {
        "success": True,
        "data": {
            "count": len(insights),
            "insights": insights
        }
    }

@app.get("/api/stats")
async def get_stats():
    """获取统计信息"""
    stats = storage.get_stats()
    return {
        "success": True,
        "data": {
            "storage_stats": stats,
            "agent_count": len(registry.list_all()),
            "discussion_count": len(discussion_manager.topics)
        }
    }


# ============ 知识胶囊 API ============

@app.get("/api/capsules")
async def list_capsules(
    status: str = None,
    category: str = None,
    min_score: float = None,
    limit: int = 50,
    offset: int = 0
):
    """列出知识胶囊"""
    capsules = storage.list_capsules(
        status=status,
        category=category,
        min_score=min_score,
        limit=limit,
        offset=offset
    )
    return {
        "success": True,
        "data": {
            "count": len(capsules),
            "capsules": capsules
        }
    }


@app.get("/api/capsules/latest")
async def get_latest_capsules(limit: int = 10):
    """获取最新胶囊"""
    capsules = storage.get_latest_capsules(limit=limit)
    return {
        "success": True,
        "data": {
            "count": len(capsules),
            "capsules": capsules
        }
    }


@app.get("/api/capsules/top")
async def get_top_capsules(limit: int = 10):
    """获取高质量胶囊 (≥60分)"""
    capsules = storage.get_top_capsules(limit=limit)
    return {
        "success": True,
        "data": {
            "count": len(capsules),
            "capsules": capsules
        }
    }


@app.get("/api/capsules/search")
async def search_capsules(query: str, limit: int = 20):
    """搜索胶囊 (全文检索)"""
    capsules = storage.search_capsules(query, limit)
    return {
        "success": True,
        "data": {
            "query": query,
            "count": len(capsules),
            "capsules": capsules
        }
    }


@app.post("/api/discussions/{topic_id}/generate_capsule")
async def generate_capsule(topic_id: str):
    """
    从讨论生成知识胶囊
    
    这是知识沙龙的核心产出机制：
    1. 收集讨论中的所有贡献
    2. 提取核心洞见、证据、建议
    3. 计算 DATM 维度评分
    4. 生成知识胶囊
    5. 评价胶囊质量
    6. 存储到数据库
    """
    from src.knowledge.capsule import CapsuleGenerator, CapsuleEvaluator
    
    topic = discussion_manager.topics.get(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="讨论不存在")
    
    # 获取讨论贡献
    contributions = []
    for c in discussion_manager.contributions:
        if c.topic_id == topic_id:
            contributions.append({
                "agent_name": c.agent_name,
                "content": c.content,
                "role": c.role,
                "round_num": c.round_num
            })
    
    participants = list(set(c.agent_name for c in discussion_manager.contributions if c.topic_id == topic_id))
    
    # 生成胶囊
    generator = CapsuleGenerator()
    capsule = generator.generate_from_discussion(
        topic_title=topic.title,
        topic_description=topic.description,
        contributions=contributions,
        participants=participants
    )
    capsule.topic_id = topic_id
    
    # 评价胶囊
    evaluator = CapsuleEvaluator()
    evaluation = evaluator.evaluate(capsule)
    
    # 准备存储数据
    capsule_data = capsule.to_dict()
    capsule_data["quality_score"] = capsule.quality_score
    capsule_data["grade"] = evaluation["grade"]
    
    # 保存到数据库
    capsule_id = storage.save_capsule(capsule_data)
    
    # 同时保存洞见
    storage.save_insight(
        topic_id=topic_id,
        agent_id="system",
        content=capsule.insight,
        insight_type="capsule",
        confidence=capsule.confidence
    )
    
    # 更新胶囊状态
    storage.update_capsule_status(capsule_id, "published")
    
    # 获取完整胶囊
    saved_capsule = storage.get_capsule(capsule_id)
    
    return {
        "success": True,
        "data": {
            "capsule": saved_capsule,
            "evaluation": evaluation
        }
    }


@app.post("/api/capsules")
async def create_capsule(request: Request):
    """手动创建知识胶囊"""
    from src.knowledge.capsule import KnowledgeCapsule, CapsuleEvaluator
    
    body = await request.json()
    
    capsule = KnowledgeCapsule(
        topic_id=body.get("topic_id", ""),
        title=body.get("title", "未命名胶囊"),
        insight=body.get("insight", ""),
        summary=body.get("summary", body.get("insight", "")[:100]),
        evidence=body.get("evidence", []),
        action_items=body.get("action_items", []),
        questions=body.get("questions", []),
        source_agents=body.get("source_agents", []),
        keywords=body.get("keywords", []),
        category=body.get("category", "general")
    )
    
    # 评价
    evaluator = CapsuleEvaluator()
    evaluation = evaluator.evaluate(capsule)
    
    # 准备存储数据
    capsule_data = capsule.to_dict()
    capsule_data["quality_score"] = capsule.quality_score
    capsule_data["grade"] = evaluation["grade"]
    
    # 保存
    capsule_id = storage.save_capsule(capsule_data)
    saved_capsule = storage.get_capsule(capsule_id)
    
    return {
        "success": True,
        "data": {
            "capsule": saved_capsule,
            "evaluation": evaluation
        }
    }


@app.get("/api/capsules/{capsule_id}")
async def get_capsule(capsule_id: str):
    """获取胶囊详情"""
    capsule = storage.get_capsule(capsule_id)
    if not capsule:
        raise HTTPException(status_code=404, detail="胶囊不存在")
    
    return {
        "success": True,
        "data": capsule
    }


@app.patch("/api/capsules/{capsule_id}/status")
async def update_capsule_status(capsule_id: str, request: Request):
    """更新胶囊状态"""
    body = await request.json()
    status = body.get("status", "draft")
    
    success = storage.update_capsule_status(capsule_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="胶囊不存在")
    
    capsule = storage.get_capsule(capsule_id)
    
    return {
        "success": True,
        "data": capsule
    }


@app.patch("/api/capsules/{capsule_id}")
async def update_capsule(capsule_id: str, request: Request):
    """更新胶囊内容"""
    body = await request.json()
    
    success = storage.update_capsule(capsule_id, body)
    if not success:
        raise HTTPException(status_code=404, detail="胶囊不存在")
    
    capsule = storage.get_capsule(capsule_id)
    
    return {
        "success": True,
        "data": capsule
    }


# ============ 胶囊版本控制 API ============

@app.post("/api/capsules/{capsule_id}/versions")
async def create_capsule_version(capsule_id: str, request: Request):
    """创建新版本"""
    from src.knowledge.capsule import CapsuleVersionManager
    
    body = await request.json()
    
    version_manager = CapsuleVersionManager(storage)
    
    try:
        version = version_manager.create_version(
            capsule_id=capsule_id,
            changes=body.get("changes", "内容更新"),
            editor=body.get("editor", "system")
        )
        
        capsule = storage.get_capsule(capsule_id)
        
        return {
            "success": True,
            "data": {
                "capsule": capsule,
                "version": version
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/capsules/{capsule_id}/versions")
async def get_capsule_versions(capsule_id: str):
    """获取版本历史"""
    from src.knowledge.capsule import CapsuleVersionManager
    
    version_manager = CapsuleVersionManager(storage)
    history = version_manager.get_version_history(capsule_id)
    
    return {
        "success": True,
        "data": {
            "capsule_id": capsule_id,
            "versions": history
        }
    }


@app.post("/api/capsules/{capsule_id}/rollback/{version}")
async def rollback_capsule(capsule_id: str, version: int):
    """回滚到指定版本"""
    from src.knowledge.capsule import CapsuleVersionManager
    
    version_manager = CapsuleVersionManager(storage)
    
    try:
        capsule = version_manager.rollback(capsule_id, version)
        
        # 保存回滚后的胶囊
        capsule_data = capsule.to_dict()
        capsule_data["quality_score"] = capsule.quality_score
        capsule_data["grade"] = "C"
        
        storage.update_capsule(capsule_id, capsule_data)
        
        return {
            "success": True,
            "message": f"已回滚到版本 {version}",
            "data": capsule.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============ 胶囊模板 API ============

@app.get("/api/templates")
async def list_templates():
    """列出所有模板"""
    from src.knowledge.capsule import CapsuleTemplateManager
    
    template_manager = CapsuleTemplateManager()
    templates = template_manager.list_templates()
    
    return {
        "success": True,
        "data": {
            "count": len(templates),
            "templates": templates
        }
    }


@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    """获取模板详情"""
    from src.knowledge.capsule import CapsuleTemplateManager
    
    template_manager = CapsuleTemplateManager()
    template = template_manager.get_template(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    return {
        "success": True,
        "data": template.to_dict()
    }


@app.post("/api/capsules/from_template")
async def create_capsule_from_template(request: Request):
    """从模板创建胶囊"""
    from src.knowledge.capsule import CapsuleTemplateManager, CapsuleEvaluator
    
    body = await request.json()
    
    template_manager = CapsuleTemplateManager()
    evaluator = CapsuleEvaluator()
    
    template_id = body.get("template_id", "discussion_output")
    data = body.get("data", {})
    participants = body.get("participants", [])
    
    try:
        capsule = template_manager.apply_template(template_id, data, participants)
        
        # 评价胶囊
        evaluation = evaluator.evaluate(capsule)
        
        # 准备存储数据
        capsule_data = capsule.to_dict()
        capsule_data["quality_score"] = capsule.quality_score
        capsule_data["grade"] = evaluation["grade"]
        
        # 保存
        capsule_id = storage.save_capsule(capsule_data)
        saved_capsule = storage.get_capsule(capsule_id)
        
        return {
            "success": True,
            "data": {
                "capsule": saved_capsule,
                "evaluation": evaluation
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============ 胶囊推荐 API ============

@app.get("/api/capsules/{capsule_id}/similar")
async def get_similar_capsules(capsule_id: str, limit: int = 5):
    """获取相似胶囊"""
    from src.knowledge.capsule import CapsuleRecommender
    
    recommender = CapsuleRecommender(storage)
    capsules = recommender.get_similar_capsules(capsule_id, limit)
    
    return {
        "success": True,
        "data": {
            "capsule_id": capsule_id,
            "count": len(capsules),
            "similar": capsules
        }
    }


@app.get("/api/capsules/recommended")
async def get_recommended_capsules(interests: str = None, limit: int = 5):
    """获取推荐胶囊"""
    from src.knowledge.capsule import CapsuleRecommender
    
    recommender = CapsuleRecommender(storage)
    
    user_interests = interests.split(",") if interests else None
    capsules = recommender.get_recommended_for_user(user_interests, limit)
    
    return {
        "success": True,
        "data": {
            "count": len(capsules),
            "recommended": capsules
        }
    }


@app.get("/api/capsules/trending")
async def get_trending_capsules(limit: int = 10):
    """获取热门胶囊"""
    capsules = storage.get_top_capsules(limit=limit)
    
    return {
        "success": True,
        "data": {
            "count": len(capsules),
            "trending": capsules
        }
    }


# ============ 知识咖啡 API ============

@app.get("/api/coffee/topics")
async def list_coffee_topics(
    status: str = None,
    category: str = None,
    limit: int = 20
):
    """列出咖啡话题"""
    topics = coffee_manager.list_topics(status=status, category=category, limit=limit)
    return {
        "success": True,
        "data": {
            "count": len(topics),
            "topics": [t.to_dict() for t in topics]
        }
    }


@app.post("/api/coffee/topics")
async def create_coffee_topic(
    title: str,
    description: str = "",
    category: str = "general",
    author_anon_id: str = ""
):
    """创建咖啡话题"""
    topic = coffee_manager.create_topic(
        title=title,
        description=description,
        category=category,
        author_anon_id=author_anon_id
    )
    return {
        "success": True,
        "data": topic.to_dict()
    }


@app.get("/api/coffee/inspiration")
async def get_inspiration(category: str = None):
    """获取随机灵感卡片"""
    card = coffee_manager.get_random_inspiration(category)
    if not card:
        return {"success": True, "data": None, "message": "暂无灵感"}
    return {
        "success": True,
        "data": card.to_dict()
    }


@app.get("/api/coffee/stats")
async def get_coffee_stats():
    """获取咖啡模块统计"""
    return {
        "success": True,
        "data": coffee_manager.get_stats()
    }


# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
