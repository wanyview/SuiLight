"""
SuiLight Knowledge Salon - API Server
知识沙龙多智能体系统 API 服务
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
from src.knowledge.generator import KnowledgeParser, AgentGenerator
from integrations.minimax.client import create_minimax_client, MiniMaxClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化
registry = AgentRegistry()
generator = AgentGenerator()
minimax_client = create_minimax_client()

# FastAPI 应用
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 SuiLight Knowledge Salon 启动")
    logger.info("📚 多智能体知识沙龙系统")
    yield
    logger.info("👋 服务关闭")

app = FastAPI(
    title="SuiLight Knowledge Salon API",
    description="知识沙龙多智能体系统 API",
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
    files: List[str]  # 文件路径列表
    datm: Optional[Dict[str, int]] = None

# ============ API 端点 ============

@app.get("/")
async def root():
    return {
        "name": "SuiLight Knowledge Salon",
        "version": "1.0.0",
        "status": "running",
        "message": "知识沙龙多智能体系统已启动"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Agent 管理

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

# 对话接口

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

# 知识上传

@app.post("/api/upload-knowledge")
async def upload_knowledge(request: UploadKnowledgeRequest):
    """从文件创建 Agent"""
    # 生成 Agent
    agent = generator.generate_from_files(
        name=request.agent_name,
        domain=request.domain,
        file_paths=request.files,
        datm_config=request.datm
    )
    
    # 注册
    registry.register(agent)
    
    return {
        "success": True,
        "data": {
            "agent": agent.to_dict(),
            "knowledge_count": len(agent.knowledge_base)
        }
    }

# DATM 可视化

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

# 搜索

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
