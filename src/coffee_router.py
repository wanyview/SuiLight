"""
SuiLight Knowledge Salon - 知识咖啡 API
FastAPI 路由
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
import random

from src.coffee import (
    coffee_manager,
    TopicStatus
)

router = APIRouter(prefix="/api/coffee", tags=["知识咖啡"])


# ============ 话题墙 API ============

@router.get("/topics")
async def list_topics(
    status: str = None,
    category: str = None,
    limit: int = 20
) -> Dict:
    """列出话题"""
    topics = coffee_manager.list_topics(
        status=status,
        category=category,
        limit=limit
    )
    
    return {
        "success": True,
        "data": {
            "count": len(topics),
            "topics": [t.to_dict() for t in topics]
        }
    }


@router.post("/topics")
async def create_topic(
    title: str,
    description: str = "",
    category: str = "general",
    author_anon_id: str = ""
) -> Dict:
    """创建话题"""
    if not title or len(title) < 5:
        raise HTTPException(status_code=400, detail="话题标题至少5个字符")
    
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


@router.get("/topics/{topic_id}")
async def get_topic(topic_id: str) -> Dict:
    """获取话题详情"""
    topic = coffee_manager.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="话题不存在")
    
    # 获取关联观点
    opinions = coffee_manager.get_opinions_by_topic(topic_id)
    
    return {
        "success": True,
        "data": {
            "topic": topic.to_dict(),
            "opinions": [o.to_dict() for o in opinions]
        }
    }


@router.post("/topics/{topic_id}/vote")
async def vote_topic(topic_id: str) -> Dict:
    """对话题投票"""
    if not coffee_manager.vote_topic(topic_id):
        raise HTTPException(status_code=404, detail="话题不存在")
    
    topic = coffee_manager.get_topic(topic_id)
    
    return {
        "success": True,
        "data": {
            "vote_count": topic.vote_count
        }
    }


@router.post("/topics/{topic_id}/close")
async def close_topic(topic_id: str) -> Dict:
    """关闭话题"""
    if not coffee_manager.close_topic(topic_id):
        raise HTTPException(status_code=404, detail="话题不存在")
    
    return {
        "success": True,
        "message": "话题已关闭"
    }


# ============ 灵感卡片 API ============

@router.get("/inspiration")
async def get_inspiration(category: str = None) -> Dict:
    """获取随机灵感卡片"""
    card = coffee_manager.get_random_inspiration(category)
    if not card:
        raise HTTPException(status_code=404, detail="没有灵感卡片")
    
    return {
        "success": True,
        "data": card.to_dict()
    }


@router.post("/inspiration")
async def create_inspiration(
    content: str,
    category: str = "general",
    author_anon_id: str = ""
) -> Dict:
    """创建灵感卡片"""
    if not content or len(content) < 5:
        raise HTTPException(status_code=400, detail="灵感内容至少5个字符")
    
    card = coffee_manager.create_inspiration(
        content=content,
        category=category,
        author_anon_id=author_anon_id
    )
    
    return {
        "success": True,
        "data": card.to_dict()
    }


@router.post("/inspiration/{card_id}/like")
async def like_inspiration(card_id: str) -> Dict:
    """点赞灵感卡片"""
    if not coffee_manager.like_inspiration(card_id):
        raise HTTPException(status_code=404, detail="灵感卡片不存在")
    
    return {
        "success": True,
        "message": "已点赞"
    }


@router.post("/inspiration/{card_id}/use")
async def use_inspiration(card_id: str) -> Dict:
    """标记灵感卡片已被使用 (用于沙龙)"""
    if not coffee_manager.mark_inspiration_used(card_id):
        raise HTTPException(status_code=404, detail="灵感卡片不存在")
    
    return {
        "success": True,
        "message": "已标记为使用"
    }


@router.get("/inspirations/popular")
async def get_popular_inspirations(limit: int = 10) -> Dict:
    """获取热门灵感卡片"""
    cards = coffee_manager.get_popular_inspirations(limit=limit)
    
    return {
        "success": True,
        "data": {
            "count": len(cards),
            "inspirations": [c.to_dict() for c in cards]
        }
    }


# ============ 匿名讨论 API ============

@router.get("/discussions")
async def get_discussions(
    topic_id: str = None,
    limit: int = 20
) -> Dict:
    """获取讨论列表"""
    if topic_id:
        opinions = coffee_manager.get_opinions_by_topic(topic_id)
    else:
        opinions = list(coffee_manager.opinions.values())
    
    # 按时间排序
    opinions.sort(key=lambda x: x.created_at, reverse=True)
    
    return {
        "success": True,
        "data": {
            "count": len(opinions),
            "discussions": [o.to_dict() for o in opinions[:limit]]
        }
    }


@router.post("/discussions")
async def create_discussion(
    topic_id: str,
    content: str,
    stance: str = "neutral",
    anon_id: str = ""
) -> Dict:
    """创建匿名观点"""
    if not content or len(content) < 10:
        raise HTTPException(status_code=400, detail="观点内容至少10个字符")
    
    if stance not in ["positive", "negative", "neutral"]:
        raise HTTPException(status_code=400, detail="立场只能是 positive/negative/neutral")
    
    opinion = coffee_manager.create_opinion(
        topic_id=topic_id,
        content=content,
        stance=stance,
        anon_id=anon_id
    )
    
    if not opinion:
        raise HTTPException(status_code=404, detail="话题不存在")
    
    return {
        "success": True,
        "data": opinion.to_dict()
    }


@router.post("/opinions/{opinion_id}/vote")
async def vote_opinion(opinion_id: str, agree: bool = True) -> Dict:
    """对观点投票"""
    if not coffee_manager.vote_opinion(opinion_id, agree):
        raise HTTPException(status_code=404, detail="观点不存在")
    
    return {
        "success": True,
        "message": "已投票"
    }


# ============ 统计 API ============

@router.get("/stats")
async def get_stats() -> Dict:
    """获取统计信息"""
    stats = coffee_manager.get_stats()
    
    return {
        "success": True,
        "data": stats
    }


# ============ 快捷操作 ============

@router.get("/random-topic")
async def get_random_topic() -> Dict:
    """获取随机活跃话题"""
    topics = coffee_manager.list_topics(status="active", limit=50)
    if not topics:
        return {
            "success": True,
            "data": None,
            "message": "暂无活跃话题"
        }
    
    topic = random.choice(topics)
    
    return {
        "success": True,
        "data": topic.to_dict()
    }


@router.get("/hot-topics")
async def get_hot_topics(limit: int = 5) -> Dict:
    """获取热门话题 (按投票数)"""
    topics = coffee_manager.list_topics(limit=limit)
    
    return {
        "success": True,
        "data": {
            "count": len(topics),
            "topics": [t.to_dict() for t in topics]
        }
    }
