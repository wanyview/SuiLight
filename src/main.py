"""
SuiLight Knowledge Salon - API Server
知识沙龙多智能体系统 API 服务

功能:
- Agent 管理 (创建、对话、学习)
- 预设伟大思想家 (100位专家)
- 协作讨论框架
- 知识沉淀
"""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化
registry = AgentRegistry()
generator = AgentGenerator()
discussion_manager = DiscussionManager(registry)

# FastAPI 应用
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 SuiLight Knowledge Salon 启动")
    logger.info("📚 100位伟大思想家知识沙龙")
    logger.info(f"🧠 当前注册 Agent: {len(registry.list_all())} 位")
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

# ============ API 端点 ============

@app.get("/")
async def root():
    return {
        "name": "SuiLight Knowledge Salon",
        "version": "1.0.0",
        "status": "running",
        "message": "知识沙龙多智能体系统已启动",
        "features": [
            "100位伟大思想家 Agent",
            "多学科协作讨论",
            "知识涌现与沉淀",
            "多 LLM 支持"
        ]
    }

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
        # 搜索
        from src.agents.presets import GREAT_MINDS
        results = {}
        for name, info in GREAT_MINDS.items():
            if search.lower() in name.lower():
                results[name] = info
        return {
            "success": True,
            "data": {"count": len(results), "results": results}
        }
    
    if domain:
        from src.agents.presets import GREAT_MINDS
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
    """批量创建预设 Agent"""
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


# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
