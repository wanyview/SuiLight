"""
SuiLight Knowledge Salon - 三设机制 API
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional

from src.knowledge.three_set import (
    three_set_manager,
    ThinkerProfile,
    ThoughtDesign,
    ExperimentDesign
)

router = APIRouter(prefix="/api/three-set", tags=["三设机制"])


# ============ 思想家 API ============

@router.get("/thinkers")
async def list_thinkers(
    field: str = None,
    era: str = None
) -> Dict:
    """列出思想家"""
    thinkers = three_set_manager.list_thinkers(field=field, era=era)
    return {
        "success": True,
        "data": {
            "count": len(thinkers),
            "thinkers": thinkers
        }
    }


@router.get("/thinkers/{name}")
async def get_thinker(name: str) -> Dict:
    """获取思想家详情"""
    profile = three_set_manager.get_thinker(name)
    if not profile:
        raise HTTPException(status_code=404, detail="思想家不存在")
    
    return {
        "success": True,
        "data": profile.to_dict()
    }


@router.post("/thinkers")
async def add_thinker(profile: Dict) -> Dict:
    """添加思想家"""
    thinker = ThinkerProfile(**profile)
    three_set_manager.add_thinker(thinker)
    
    return {
        "success": True,
        "data": thinker.to_dict()
    }


@router.post("/thinkers/{name}/respond")
async def generate_thinker_response(
    name: str,
    topic: str,
    style: str = "dialogue"
) -> Dict:
    """生成思想家风格的回复"""
    response = three_set_manager.generate_thinker_response(name, topic, style)
    
    return {
        "success": True,
        "data": {
            "thinker": name,
            "topic": topic,
            "style": style,
            "response": response
        }
    }


@router.get("/thinkers/{name}/related")
async def get_related_thinkers(name: str) -> Dict:
    """获取相关思想家"""
    profile = three_set_manager.get_thinker(name)
    if not profile:
        raise HTTPException(status_code=404, detail="思想家不存在")
    
    related = []
    
    # 获取关联思想家
    for related_name in profile.related_thinkers + profile.mentors + profile.followers + profile.opponents:
        related_profile = three_set_manager.get_thinker(related_name)
        if related_profile:
            related.append({
                "name": related_name,
                "relationship": "related",
                "profile": related_profile.to_dict()
            })
    
    return {
        "success": True,
        "data": {
            "thinker": name,
            "related": related
        }
    }


# ============ 思想设计 API ============

@router.get("/thoughts")
async def list_thoughts(limit: int = 50) -> Dict:
    """列出思想"""
    thoughts = list(three_set_manager.thoughts.values())[:limit]
    return {
        "success": True,
        "data": {
            "count": len(thoughts),
            "thoughts": [t.to_dict() for t in thoughts]
        }
    }


@router.get("/thoughts/{thought_id}")
async def get_thought(thought_id: str) -> Dict:
    """获取思想详情"""
    thought = three_set_manager.get_thought(thought_id)
    if not thought:
        raise HTTPException(status_code=404, detail="思想不存在")
    
    return {
        "success": True,
        "data": thought.to_dict()
    }


@router.post("/thoughts")
async def add_thought(thought: Dict) -> Dict:
    """添加思想"""
    thought_obj = ThoughtDesign(**thought)
    three_set_manager.add_thought(thought_obj)
    
    return {
        "success": True,
        "data": thought_obj.to_dict()
    }


# ============ 实验验证 API ============

@router.get("/experiments")
async def list_experiments(thought_id: str = None) -> Dict:
    """列出实验"""
    experiments = list(three_set_manager.experiments.values())
    
    if thought_id:
        experiments = [e for e in experiments if e.thought_id == thought_id]
    
    return {
        "success": True,
        "data": {
            "count": len(experiments),
            "experiments": [e.to_dict() for e in experiments]
        }
    }


@router.get("/experiments/{exp_id}")
async def get_experiment(exp_id: str) -> Dict:
    """获取实验详情"""
    exp = three_set_manager.get_experiment(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    return {
        "success": True,
        "data": exp.to_dict()
    }


@router.post("/experiments")
async def add_experiment(exp: Dict) -> Dict:
    """添加实验"""
    exp_obj = ExperimentDesign(**exp)
    three_set_manager.add_experiment(exp_obj)
    
    return {
        "success": True,
        "data": exp_obj.to_dict()
    }


@router.get("/thoughts/{thought_id}/verify")
async def verify_thought(thought_id: str) -> Dict:
    """验证思想"""
    result = three_set_manager.verify_thought(thought_id)
    
    return {
        "success": True,
        "data": result
    }


# ============ 统计 API ============

@router.get("/stats")
async def get_stats() -> Dict:
    """获取三设统计"""
    stats = three_set_manager.get_stats()
    
    return {
        "success": True,
        "data": stats
    }


# ============ 演示 API ============

@router.get("/demo/discussion")
async def demo_discussion(topic: str = "AI是否会产生意识") -> Dict:
    """
    演示：多思想家讨论
    
    模拟几位思想家对同一问题的观点
    """
    # 选择相关思想家
    thinkers = ["图灵", "康德", "尼采", "霍金"]
    
    responses = []
    for name in thinkers:
        response = three_set_manager.generate_thinker_response(name, topic)
        responses.append({
            "thinker": name,
            "response": response
        })
    
    return {
        "success": True,
        "data": {
            "topic": topic,
            "responses": responses
        }
    }


@router.get("/demo/verification")
async def demo_verification(thought_title: str = "自然选择") -> Dict:
    """
    演示：思想验证
    
    展示思想 + 思想家 + 实验的关联
    """
    # 简化的演示
    return {
        "success": True,
        "data": {
            "thought": thought_title,
            "primary_thinker": "达尔文",
            "supporters": ["华莱士", "道金斯"],
            "experiments": [
                {"title": "加拉帕戈斯雀鸟研究", "type": "case_study", "result": "支持自然选择"},
                {"title": "抗生素抗性实验", "type": "data", "result": "支持自然选择"},
                {"title": "农场狐狸驯化", "type": "experiment", "result": "支持人工选择，类比自然选择"}
            ],
            "verification_result": "strong"
        }
    }
