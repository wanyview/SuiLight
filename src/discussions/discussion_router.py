"""
SuiLight 讨论系统 API
主题管理、Agent配置、讨论记录
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .topic_manager import topic_storage, DiscussionTopic, TopicType, TopicStatus
from .agent_config import agent_config_storage, AgentConfiguration, AGENT_TEMPLATES
from .discussion_record import discussion_storage, DiscussionRecord


router = APIRouter(prefix="/api/discussions", tags=["discussions"])


# ========== 主题管理 ==========

class CreateTopicRequest(BaseModel):
    """创建主题请求"""
    title: str
    description: str = ""
    topic_type: str  # "restricted" or "open"
    tags: List[str] = []
    
    # 限定主题配置
    restricted_config: Optional[dict] = None
    
    # 开放主题配置
    open_config: Optional[dict] = None


@router.post("/topics/")
async def create_topic(data: CreateTopicRequest):
    """创建讨论主题"""
    topic_data = {
        "title": data.title,
        "description": data.description,
        "topic_type": data.topic_type,
        "tags": data.tags
    }
    
    if data.topic_type == "restricted" and data.restricted_config:
        from .topic_manager import RestrictedConfig, HistoricalContext, TechnicalContext, DiscussionGoal
        topic_data["restricted_config"] = {
            "historical_context": data.restricted_config.get("historical_context", {}),
            "technical_context": data.restricted_config.get("technical_context", {}),
            "goal": data.restricted_config.get("goal", {})
        }
    
    if data.topic_type == "open" and data.open_config:
        from .topic_manager import OpenConfig
        topic_data["open_config"] = data.open_config
    
    topic = topic_storage.create_topic(topic_data)
    
    return {
        "status": "success",
        "topic": topic
    }


@router.get("/topics/")
async def list_topics(
    topic_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20
):
    """列出主题"""
    topics = topic_storage.list_topics(
        topic_type=topic_type,
        status=status,
        limit=limit
    )
    
    return {
        "topics": topics,
        "count": len(topics)
    }


@router.get("/topics/{topic_id}")
async def get_topic(topic_id: str):
    """获取主题详情"""
    topic = topic_storage.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return topic


@router.put("/topics/{topic_id}/status")
async def update_topic_status(topic_id: str, status: str):
    """更新主题状态"""
    topic = topic_storage.update_status(topic_id, status)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return {
        "status": "success",
        "topic": topic
    }


# ========== Agent 配置 ==========

class CreateAgentConfigRequest(BaseModel):
    """创建 Agent 配置请求"""
    topic_id: str
    agents: List[dict]
    orchestration: dict


@router.post("/agent-configs/")
async def create_agent_config(data: CreateAgentConfigRequest):
    """创建 Agent 配置"""
    config_data = {
        "topic_id": data.topic_id,
        "agents": data.agents,
        "orchestration": data.orchestration or {
            "moderator_agent_id": "",
            "discussion_flow": "sequential",
            "round_limit": 10,
            "consensus_threshold": 0.7
        }
    }
    
    config = agent_config_storage.create_config(data.topic_id, config_data)
    
    return {
        "status": "success",
        "config": config
    }


@router.get("/topics/{topic_id}/agent-config")
async def get_topic_agent_config(topic_id: str):
    """获取主题的 Agent 配置"""
    config = agent_config_storage.get_config_by_topic(topic_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent config not found")
    
    return config


@router.get("/agent-templates/")
async def list_agent_templates():
    """列出 Agent 模板"""
    return {
        "templates": AGENT_TEMPLATES
    }


# ========== 讨论记录 ==========

@router.post("/topics/{topic_id}/start")
async def start_discussion(topic_id: str):
    """开始讨论"""
    topic = topic_storage.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # 检查 Agent 配置
    agent_config = agent_config_storage.get_config_by_topic(topic_id)
    if not agent_config:
        raise HTTPException(status_code=400, detail="Agent config required before starting discussion")
    
    # 更新主题状态
    topic_storage.update_status(topic_id, "active")
    
    # 创建讨论记录
    record = discussion_storage.create_discussion(topic_id)
    
    return {
        "status": "success",
        "discussion": record,
        "message": "Discussion started"
    }


@router.post("/discussions/{discussion_id}/messages")
async def add_message(discussion_id: str, message: dict):
    """添加消息"""
    record = discussion_storage.add_message(discussion_id, message)
    if not record:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    return {
        "status": "success",
        "message_count": len(record.timeline)
    }


@router.post("/discussions/{discussion_id}/complete")
async def complete_discussion(discussion_id: str, capsule_ids: List[str]):
    """完成讨论"""
    record = discussion_storage.complete_discussion(discussion_id, capsule_ids)
    if not record:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    # 更新主题状态
    topic_storage.update_status(record.topic_id, "completed")
    
    return {
        "status": "success",
        "outcomes": record.outcomes,
        "duration_minutes": record.duration_minutes
    }


@router.get("/discussions/{discussion_id}")
async def get_discussion(discussion_id: str):
    """获取讨论记录"""
    record = discussion_storage.get_discussion(discussion_id)
    if not record:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    return record


@router.get("/topics/{topic_id}/history")
async def get_topic_history(topic_id: str):
    """获取主题讨论历史"""
    history = discussion_storage.get_discussion_history(topic_id)
    return history
