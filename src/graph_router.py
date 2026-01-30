"""
SuiLight Knowledge Salon - 知识图谱 API
FastAPI 路由
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional

from src.graph import graph_manager

router = APIRouter(prefix="/api/graph", tags=["知识图谱"])


@router.get("/export")
async def export_graph(limit: int = 100) -> Dict:
    """导出图谱 JSON (D3.js 格式)"""
    # 从存储获取胶囊
    from src.main import storage
    capsules = storage.list_capsules(limit=limit)
    
    graph_json = graph_manager.export_graph_json(capsules)
    
    return {
        "success": True,
        "data": graph_json
    }


@router.get("/clusters")
async def get_clusters(limit: int = 100) -> Dict:
    """获取聚类分析"""
    from src.main import storage
    capsules = storage.list_capsules(limit=limit)
    
    clusters = graph_manager.get_cluster_analysis(capsules)
    
    return {
        "success": True,
        "data": clusters
    }


@router.get("/timeline")
async def get_timeline(limit: int = 100) -> Dict:
    """获取时间线"""
    from src.main import storage
    capsules = storage.list_capsules(limit=limit)
    
    timeline = graph_manager.get_timeline(capsules)
    
    return {
        "success": True,
        "data": timeline
    }


@router.get("/capsules/{capsule_id}/related")
async def get_related_capsules(capsule_id: str, limit: int = 5) -> Dict:
    """获取相关胶囊"""
    from src.main import storage
    capsules = storage.list_capsules(limit=100)
    
    related = graph_manager.get_related_capsules(capsule_id, capsules, limit)
    
    return {
        "success": True,
        "data": {
            "capsule_id": capsule_id,
            "count": len(related),
            "related": related
        }
    }


@router.get("/statistics")
async def get_statistics(limit: int = 100) -> Dict:
    """获取图谱统计"""
    from src.main import storage
    capsules = storage.list_capsules(limit=limit)
    
    stats = graph_manager.get_statistics(capsules)
    
    return {
        "success": True,
        "data": stats
    }


@router.get("/visualization")
async def get_visualization_data(limit: int = 50) -> Dict:
    """获取可视化数据 (前端直接使用)"""
    from src.main import storage
    capsules = storage.list_capsules(limit=limit)
    
    # 导出图谱
    graph = graph_manager.export_graph_json(capsules)
    
    # 获取聚类
    clusters = graph_manager.get_cluster_analysis(capsules)
    
    # 获取时间线
    timeline = graph_manager.get_timeline(capsules)
    
    # 获取统计
    stats = graph_manager.get_statistics(capsules)
    
    return {
        "success": True,
        "data": {
            "graph": graph,
            "clusters": clusters,
            "timeline": timeline,
            "statistics": stats
        }
    }
