"""
SuiLight Knowledge Salon - 扩展模板 API
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional

from src.knowledge.extended_templates import (
    extended_template_manager,
    SCIENTIFIC_DOMAINS,
    CapsuleTemplateType
)

router = APIRouter(prefix="/api/templates", tags=["扩展模板"])


@router.get("/domains")
async def list_domains() -> Dict:
    """列出所有科学领域"""
    domains = extended_template_manager.list_domains()
    return {
        "success": True,
        "data": {
            "count": len(domains),
            "domains": domains
        }
    }


@router.get("/extended")
async def list_extended_templates(
    domain: str = None,
    depth: str = None,
    type: str = None
) -> Dict:
    """列出扩展模板 (支持筛选)"""
    templates = extended_template_manager.list_templates(domain=domain, depth=depth)
    
    if type:
        templates = [t for t in templates if t["type"] == type]
    
    return {
        "success": True,
        "data": {
            "count": len(templates),
            "templates": templates
        }
    }


@router.get("/extended/{template_id}")
async def get_extended_template(template_id: str) -> Dict:
    """获取扩展模板详情"""
    template = extended_template_manager.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    return {
        "success": True,
        "data": template.to_dict()
    }


@router.post("/extended/generate")
async def generate_from_extended_template(
    template_id: str,
    data: Dict,
    participants: List[str] = None
) -> Dict:
    """从扩展模板生成胶囊"""
    try:
        capsule_data = extended_template_manager.apply_template(
            template_id=template_id,
            data=data,
            participants=participants
        )
        
        # 保存到存储
        from src.main import storage
        capsule_id = storage.save_capsule(capsule_data)
        saved_capsule = storage.get_capsule(capsule_id)
        
        return {
            "success": True,
            "data": {
                "capsule": saved_capsule,
                "template_id": template_id
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/science-categories")
async def get_science_categories() -> Dict:
    """获取完整科学分类"""
    categories = {
        "自然科学": {
            "icon": "🔬",
            "domains": [k for k, v in SCIENTIFIC_DOMAINS.items() 
                       if v["name"] in ["物理学", "化学", "生物学", "数学", "天文学", "地球科学"]]
        },
        "社会科学": {
            "icon": "⚖️",
            "domains": [k for k, v in SCIENTIFIC_DOMAINS.items() 
                       if v["name"] in ["经济学", "心理学", "社会学", "政治学", "法学", "教育学"]]
        },
        "人文科学": {
            "icon": "🎨",
            "domains": [k for k, v in SCIENTIFIC_DOMAINS.items() 
                       if v["name"] in ["哲学", "历史学", "文学", "艺术", "宗教学", "语言学"]]
        },
        "技术工程": {
            "icon": "⚙️",
            "domains": [k for k, v in SCIENTIFIC_DOMAINS.items() 
                       if v["name"] in ["计算机科学", "工程学", "医学", "人工智能"]]
        },
        "交叉科学": {
            "icon": "🔗",
            "domains": [k for k, v in SCIENTIFIC_DOMAINS.items() 
                       if v["name"] in ["认知科学", "复杂系统", "环境科学", "科技与社会"]]
        }
    }
    
    return {
        "success": True,
        "data": categories
    }


@router.post("/generate-cross-disciplinary")
async def generate_crossdisciplinary_capsule(
    title: str,
    domains: List[str],  # 涉及的领域
    depth: str = "intermediate",
    core_question: str,
    insights: Dict  # 各领域的洞见
) -> Dict:
    """
    生成跨学科胶囊
    
    专门处理交叉学科问题
    """
    from src.main import storage
    from src.knowledge.capsule import CapsuleDimension
    
    # 收集所有洞见
    all_insights = []
    all_evidence = []
    all_agents = []
    keywords = []
    
    for domain in domains:
        if domain in insights:
            insight_data = insights[domain]
            all_insights.append(insight_data.get("insight", ""))
            if insight_data.get("evidence"):
                all_evidence.extend(insight_data["evidence"])
            if insight_data.get("agents"):
                all_agents.extend(insight_data["agents"])
            keywords.append(domain)
    
    # 构建胶囊
    capsule_data = {
        "title": f"跨学科: {title}",
        "insight": "跨学科视角整合: " + " | ".join(all_insights[:2]),
        "summary": f"整合{len(domains)}个领域的视角回答核心问题",
        "evidence": all_evidence[:5],
        "action_items": ["开展跨学科研讨", "建立领域桥梁", "整合多视角"],
        "questions": ["各领域如何互补", "是否存在根本矛盾"],
        "source_agents": list(set(all_agents))[:10],
        "keywords": keywords + ["跨学科", "交叉科学"],
        "category": "interdisciplinary",
        "dimensions": {
            "truth_score": 70,
            "goodness_score": 75,
            "beauty_score": 65,
            "intelligence_score": 85,
            "total_score": 73.75
        },
        "quality_score": 51.6,
        "grade": "B"
    }
    
    # 保存
    capsule_id = storage.save_capsule(capsule_data)
    saved_capsule = storage.get_capsule(capsule_id)
    
    return {
        "success": True,
        "data": {
            "capsule": saved_capsule,
            "domains": domains,
            "cross_type": True
        }
    }
