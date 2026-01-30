"""
SuiLight Knowledge Salon - 知识分享模块
分享链接、嵌入代码、导出功能
"""

import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ShareLink:
    """分享链接"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    short_id: str = field(default_factory=lambda: hashlib.md5(uuid.uuid4().bytes).hexdigest()[:6])
    capsule_id: str = ""
    title: str = ""
    content: str = ""
    format: str = "link"  # link/embed/markdown
    view_count: int = 0
    share_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "short_id": self.short_id,
            "capsule_id": self.capsule_id,
            "title": self.title,
            "format": self.format,
            "view_count": self.view_count,
            "share_count": self.share_count,
            "created_at": self.created_at.isoformat()
        }


class ShareManager:
    """
    分享管理器
    
    功能:
    - 生成分享链接
    - 生成嵌入代码
    - 导出功能
    - 访问统计
    """
    
    def __init__(self):
        # 内存存储
        self.share_links: Dict[str, ShareLink] = {}
        self.url_prefix = "https://suilight.vercel.app/share"  # 部署后的前缀
        
        logger.info("分享管理器初始化完成")
    
    def create_share_link(
        self,
        capsule_id: str,
        title: str,
        content: str = "",
        format: str = "link"
    ) -> ShareLink:
        """创建分享链接"""
        share = ShareLink(
            capsule_id=capsule_id,
            title=title,
            content=content,
            format=format
        )
        
        self.share_links[share.id] = share
        
        logger.info(f"分享链接已创建: {share.short_id}")
        
        return share
    
    def get_share_link(self, share_id: str) -> Optional[ShareLink]:
        """获取分享链接"""
        # 支持短 ID
        for share in self.share_links.values():
            if share.short_id == share_id or share.id == share_id:
                share.view_count += 1
                return share
        return None
    
    def get_shares_by_capsule(self, capsule_id: str) -> List[ShareLink]:
        """获取胶囊的所有分享链接"""
        return [s for s in self.share_links.values() if s.capsule_id == capsule_id]
    
    def increment_share_count(self, share_id: str) -> bool:
        """增加分享次数"""
        share = self.get_share_link(share_id)
        if share:
            share.share_count += 1
            return True
        return False
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_shares": len(self.share_links),
            "total_views": sum(s.view_count for s in self.share_links.values()),
            "total_shares_count": sum(s.share_count for s in self.share_links.values())
        }
    
    def generate_embed_code(self, share_id: str, width: str = "400px", height: str = "600px") -> str:
        """生成嵌入代码"""
        share = self.get_share_link(share_id)
        if not share:
            return ""
        
        embed_url = f"{self.url_prefix}/{share.short_id}?embed=true"
        
        return f'<iframe src="{embed_url}" width="{width}" height="{height}" frameborder="0" allowfullscreen></iframe>'
    
    def generate_markdown(self, share_id: str) -> str:
        """生成 Markdown 格式"""
        share = self.get_share_link(share_id)
        if not share:
            return ""
        
        link = f"{self.url_prefix}/{share.short_id}"
        
        return f"""## {share.title}

{share.content or '点击查看知识胶囊'}

---
🔗 [查看完整胶囊]({link})

*来自 SuiLight 知识沙龙*"""
    
    def export_to_text(self, capsule: Dict) -> str:
        """导出为纯文本"""
        lines = [
            "=" * 50,
            capsule.get("title", "知识胶囊"),
            "=" * 50,
            "",
            "核心洞见:",
            capsule.get("insight", ""),
            "",
            "支撑证据:",
        ]
        
        for i, e in enumerate(capsule.get("evidence", []), 1):
            lines.append(f"  {i}. {e}")
        
        lines.extend([
            "",
            "行动建议:",
        ])
        
        for i, a in enumerate(capsule.get("action_items", []), 1):
            lines.extend([
                f"  {i}. {a}",
            ])
        
        lines.extend([
            "",
            "=" * 50,
            f"质量评分: {capsule.get('quality_score', 0)}",
            f"等级: {capsule.get('grade', 'C')}",
            "=" * 50,
            "",
            f"🔗 {self.url_prefix}/capsule/{capsule.get('id')}",
        ])
        
        return "\n".join(lines)
    
    def export_to_html(self, capsule: Dict) -> str:
        """导出为 HTML"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{capsule.get('title', '知识胶囊')}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }}
        h1 {{ color: #4f46e5; }}
        .section {{ margin: 1.5rem 0; }}
        .label {{ font-weight: bold; color: #6b7280; }}
        .score {{ display: inline-block; background: #e0e7ff; padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin-right: 0.5rem; }}
    </style>
</head>
<body>
    <h1>📦 {capsule.get('title', '知识胶囊')}</h1>
    
    <div class="section">
        <p class="label">核心洞见</p>
        <p>{capsule.get('insight', '')}</p>
    </div>
    
    <div class="section">
        <p class="label">支撑证据</p>
        <ul>
            {''.join(f'<li>{e}</li>' for e in capsule.get('evidence', []))}
        </ul>
    </div>
    
    <div class="section">
        <p class="label">行动建议</p>
        <ol>
            {''.join(f'<li>{a}</li>' for a in capsule.get('action_items', []))}
        </ol>
    </div>
    
    <div class="section">
        <p class="label">质量评分</p>
        <span class="score">Truth: {capsule.get('dimensions', {}).get('truth', 0)}</span>
        <span class="score">Goodness: {capsule.get('dimensions', {}).get('goodness', 0)}</span>
        <span class="score">Beauty: {capsule.get('dimensions', {}).get('beauty', 0)}</span>
        <span class="score">Intelligence: {capsule.get('dimensions', {}).get('intelligence', 0)}</span>
    </div>
    
    <hr>
    <p style="color: #9ca3af; font-size: 0.875rem;">
        来自 <a href="https://suilight.vercel.app">SuiLight 知识沙龙</a>
    </p>
</body>
</html>"""


# 全局实例
share_manager = ShareManager()
