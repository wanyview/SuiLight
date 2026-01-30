"""
SuiLight Knowledge Salon - 知识分享 API
FastAPI 路由
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Optional
import urllib.parse

from src.share import share_manager

router = APIRouter(prefix="/api/share", tags=["知识分享"])


@router.post("/links")
async def create_share_link(
    capsule_id: str,
    title: str,
    content: str = "",
    format: str = "link"
) -> Dict:
    """创建分享链接"""
    if not capsule_id or not title:
        raise HTTPException(status_code=400, detail="缺少必要参数")
    
    share = share_manager.create_share_link(
        capsule_id=capsule_id,
        title=title,
        content=content,
        format=format
    )
    
    share_url = f"https://suilight.vercel.app/share/{share.short_id}"
    
    return {
        "success": True,
        "data": {
            "share_id": share.id,
            "short_id": share.short_id,
            "share_url": share_url,
            "view_count": share.view_count
        }
    }


@router.get("/links/{share_id}")
async def get_share_link(share_id: str) -> Dict:
    """获取分享链接详情"""
    share = share_manager.get_share_link(share_id)
    if not share:
        raise HTTPException(status_code=404, detail="分享链接不存在")
    
    return {
        "success": True,
        "data": {
            "share_id": share.id,
            "short_id": share.short_id,
            "title": share.title,
            "content": share.content,
            "format": share.format,
            "view_count": share.view_count,
            "share_count": share.share_count,
            "created_at": share.created_at.isoformat()
        }
    }


@router.get("/links/{share_id}/url")
async def get_share_url(share_id: str) -> Dict:
    """获取分享链接 URL"""
    share = share_manager.get_share_link(share_id)
    if not share:
        raise HTTPException(status_code=404, detail="分享链接不存在")
    
    share_url = f"https://suilight.vercel.app/share/{share.short_id}"
    
    return {
        "success": True,
        "data": {
            "url": share_url,
            "short_id": share.short_id
        }
    }


@router.post("/links/{share_id}/track")
async def track_share(share_id: str) -> Dict:
    """追踪分享"""
    if not share_manager.increment_share_count(share_id):
        raise HTTPException(status_code=404, detail="分享链接不存在")
    
    return {
        "success": True,
        "message": "已记录"
    }


@router.get("/links/{share_id}/embed")
async def get_embed_code(
    share_id: str,
    width: str = "400px",
    height: str = "600px"
) -> Dict:
    """获取嵌入代码"""
    code = share_manager.generate_embed_code(share_id, width, height)
    if not code:
        raise HTTPException(status_code=404, detail="分享链接不存在")
    
    return {
        "success": True,
        "data": {
            "embed_code": code,
            "width": width,
            "height": height
        }
    }


@router.get("/links/{share_id}/markdown")
async def get_markdown(share_id: str) -> Dict:
    """获取 Markdown 格式"""
    share = share_manager.get_share_link(share_id)
    if not share:
        raise HTTPException(status_code=404, detail="分享链接不存在")
    
    markdown = share_manager.generate_markdown(share_id)
    
    return {
        "success": True,
        "data": {
            "markdown": markdown,
            "title": share.title
        }
    }


@router.get("/capsule/{capsule_id}/shares")
async def get_capsule_shares(capsule_id: str) -> Dict:
    """获取胶囊的所有分享链接"""
    shares = share_manager.get_shares_by_capsule(capsule_id)
    
    base_url = "https://suilight.vercel.app/share"
    
    return {
        "success": True,
        "data": {
            "count": len(shares),
            "shares": [
                {
                    "short_id": s.short_id,
                    "url": f"{base_url}/{s.short_id}",
                    "format": s.format,
                    "view_count": s.view_count,
                    "created_at": s.created_at.isoformat()
                }
                for s in shares
            ]
        }
    }


@router.get("/stats")
async def get_stats() -> Dict:
    """获取分享统计"""
    stats = share_manager.get_stats()
    
    return {
        "success": True,
        "data": stats
    }


@router.get("/export/text")
async def export_text(
    title: str = Query(...),
    insight: str = "",
    evidence: list = Query(default=[]),
    action_items: list = Query(default=[])
) -> Dict:
    """导出为纯文本"""
    capsule = {
        "title": title,
        "insight": insight,
        "evidence": evidence,
        "action_items": action_items,
        "quality_score": 0,
        "grade": "C",
        "id": "export"
    }
    
    text = share_manager.export_to_text(capsule)
    
    return {
        "success": True,
        "data": {
            "text": text
        }
    }


@router.get("/export/html")
async def export_html(
    title: str = Query(...),
    insight: str = "",
    evidence: list = Query(default=[]),
    action_items: list = Query(default=[]),
    dimensions: dict = Query(default={"truth": 0, "goodness": 0, "beauty": 0, "intelligence": 0})
) -> Dict:
    """导出为 HTML"""
    capsule = {
        "title": title,
        "insight": insight,
        "evidence": evidence,
        "action_items": action_items,
        "dimensions": dimensions,
        "quality_score": 0,
        "grade": "C",
        "id": "export"
    }
    
    html = share_manager.export_to_html(capsule)
    
    return {
        "success": True,
        "data": {
            "html": html,
            "filename": f"{title[:20]}.html" if len(title) > 20 else f"{title}.html"
        }
    }
