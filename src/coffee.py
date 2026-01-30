"""
SuiLight Knowledge Salon - 知识咖啡模块
轻松交流、灵感碰撞、匿名讨论
"""

import json
import uuid
import random
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TopicStatus(Enum):
    """话题状态"""
    DRAFT = "draft"       # 草稿
    ACTIVE = "active"     # 活跃
    CLOSED = "closed"     # 已关闭


@dataclass
class CoffeeTopic:
    """咖啡话题"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""                    # 话题标题
    description: str = ""              # 话题描述
    category: str = "general"          # 分类
    author_anon_id: str = ""           # 作者匿名ID
    status: TopicStatus = TopicStatus.DRAFT
    vote_count: int = 0                # 投票数
    view_count: int = 0                # 查看数
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "author_anon_id": self.author_anon_id,
            "status": self.status.value,
            "vote_count": self.vote_count,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class InspirationCard:
    """灵感卡片"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: str = ""                   # 灵感内容
    category: str = "general"           # 分类
    author_anon_id: str = ""            # 作者匿名ID
    likes: int = 0                      # 点赞数
    used_in_salon: bool = False         # 是否已被沙龙使用
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "author_anon_id": self.author_anon_id,
            "likes": self.likes,
            "used_in_salon": self.used_in_salon,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class AnonymousOpinion:
    """匿名观点"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic_id: str = ""                  # 关联话题
    content: str = ""                   # 观点内容
    stance: str = "neutral"             # 立场: positive/negative/neutral
    anon_id: str = ""                   # 匿名ID
    agree_count: int = 0                # 同意数
    disagree_count: int = 0             # 不同意数
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "content": self.content,
            "stance": self.stance,
            "anon_id": self.anon_id,
            "agree_count": self.agree_count,
            "disagree_count": self.disagree_count,
            "created_at": self.created_at.isoformat()
        }


# 预设灵感卡片
PRESET_INSPIRATIONS = [
    # AI 治理相关
    "如果 AI 拥有自我意识，它应该拥有权利吗？",
    "如何平衡 AI 创新与安全监管？",
    "AI 生成的创意作品版权归谁？",
    "超级 AI 会不会超越人类控制？",
    "AI 能替代人类做道德决策吗？",
    
    # 学习相关
    "未来哪些技能最重要？",
    "如何培养批判性思维？",
    "项目式学习真的有效吗？",
    "跨学科学习有哪些挑战？",
    "如何平衡兴趣与应试？",
    
    # 社会相关
    "技术发展太快，教育如何跟上？",
    "如何定义'成功'？",
    "AI 时代还需要记忆吗？",
    "创造力可以被训练吗？",
    "未来的工作会是什么样子？",
    
    # 哲学相关
    "什么是有意义的人生？",
    "知识的边界在哪里？",
    "思考是如何产生的？",
    "真理可以被完全认知吗？",
    "自由意志存在吗？"
]


class CoffeeManager:
    """
    知识咖啡管理器
    
    功能:
    - 话题墙管理
    - 灵感卡片
    - 匿名讨论
    - 观点投票
    """
    
    def __init__(self):
        # 内存存储 (生产环境应使用数据库)
        self.topics: Dict[str, CoffeeTopic] = {}
        self.inspirations: Dict[str, InspirationCard] = {}
        self.opinions: Dict[str, AnonymousOpinion] = {}
        
        # 初始化预设灵感
        self._init_preset_inspirations()
        
        logger.info("知识咖啡管理器初始化完成")
    
    def _init_preset_inspirations(self):
        """初始化预设灵感卡片"""
        for content in PRESET_INSPIRATIONS:
            card = InspirationCard(
                content=content,
                category="preset"
            )
            self.inspirations[card.id] = card
    
    # ============ 话题管理 ============
    
    def create_topic(
        self,
        title: str,
        description: str = "",
        category: str = "general",
        author_anon_id: str = ""
    ) -> CoffeeTopic:
        """创建话题"""
        topic = CoffeeTopic(
            title=title,
            description=description,
            category=category,
            author_anon_id=author_anon_id or f"anon_{random.randint(1000,9999)}",
            status=TopicStatus.ACTIVE
        )
        
        self.topics[topic.id] = topic
        logger.info(f"话题已创建: {topic.id} - {topic.title}")
        
        return topic
    
    def get_topic(self, topic_id: str) -> Optional[CoffeeTopic]:
        """获取话题"""
        return self.topics.get(topic_id)
    
    def list_topics(
        self,
        status: str = None,
        category: str = None,
        limit: int = 20
    ) -> List[CoffeeTopic]:
        """列出话题"""
        results = []
        
        for topic in self.topics.values():
            if status and topic.status.value != status:
                continue
            if category and topic.category != category:
                continue
            results.append(topic)
        
        # 按投票数和创建时间排序
        results.sort(key=lambda x: (x.vote_count, x.created_at), reverse=True)
        
        return results[:limit]
    
    def vote_topic(self, topic_id: str) -> bool:
        """对话题投票"""
        topic = self.topics.get(topic_id)
        if not topic:
            return False
        
        topic.vote_count += 1
        topic.updated_at = datetime.now()
        return True
    
    def close_topic(self, topic_id: str) -> bool:
        """关闭话题"""
        topic = self.topics.get(topic_id)
        if not topic:
            return False
        
        topic.status = TopicStatus.CLOSED
        topic.updated_at = datetime.now()
        return True
    
    # ============ 灵感卡片 ============
    
    def get_random_inspiration(self, category: str = None) -> Optional[InspirationCard]:
        """获取随机灵感卡片"""
        candidates = list(self.inspirations.values())
        
        if category:
            candidates = [c for c in candidates if c.category == category]
        
        if not candidates:
            return None
        
        return random.choice(candidates)
    
    def create_inspiration(
        self,
        content: str,
        category: str = "general",
        author_anon_id: str = ""
    ) -> InspirationCard:
        """创建灵感卡片"""
        card = InspirationCard(
            content=content,
            category=category,
            author_anon_id=author_anon_id or f"anon_{random.randint(1000,9999)}"
        )
        
        self.inspirations[card.id] = card
        logger.info(f"灵感卡片已创建: {card.id}")
        
        return card
    
    def like_inspiration(self, card_id: str) -> bool:
        """点赞灵感卡片"""
        card = self.inspirations.get(card_id)
        if not card:
            return False
        
        card.likes += 1
        return True
    
    def mark_inspiration_used(self, card_id: str) -> bool:
        """标记灵感卡片已被使用"""
        card = self.inspirations.get(card_id)
        if not card:
            return False
        
        card.used_in_salon = True
        return True
    
    def get_popular_inspirations(self, limit: int = 10) -> List[InspirationCard]:
        """获取热门灵感卡片"""
        cards = list(self.inspirations.values())
        cards.sort(key=lambda x: x.likes, reverse=True)
        return cards[:limit]
    
    # ============ 匿名观点 ============
    
    def create_opinion(
        self,
        topic_id: str,
        content: str,
        stance: str = "neutral",
        anon_id: str = ""
    ) -> Optional[AnonymousOpinion]:
        """创建匿名观点"""
        if topic_id not in self.topics:
            return None
        
        opinion = AnonymousOpinion(
            topic_id=topic_id,
            content=content,
            stance=stance,
            anon_id=anon_id or f"anon_{random.randint(1000,9999)}"
        )
        
        self.opinions[opinion.id] = opinion
        
        # 增加话题查看数
        self.topics[topic_id].view_count += 1
        
        logger.info(f"匿名观点已创建: {opinion.id}")
        
        return opinion
    
    def get_opinions_by_topic(self, topic_id: str) -> List[AnonymousOpinion]:
        """获取话题的所有观点"""
        return [
            op for op in self.opinions.values()
            if op.topic_id == topic_id
        ]
    
    def vote_opinion(self, opinion_id: str, agree: bool) -> bool:
        """对观点投票"""
        opinion = self.opinions.get(opinion_id)
        if not opinion:
            return False
        
        if agree:
            opinion.agree_count += 1
        else:
            opinion.disagree_count += 1
        
        return True
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "topic_count": len(self.topics),
            "active_topic_count": len([t for t in self.topics.values() if t.status == TopicStatus.ACTIVE]),
            "inspiration_count": len(self.inspirations),
            "opinion_count": len(self.opinions)
        }


# 全局实例
coffee_manager = CoffeeManager()
