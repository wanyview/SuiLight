"""
SuiLight 主题管理系统
支持限定主题和开放主题讨论
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
from enum import Enum


class TopicType(str, Enum):
    """主题类型"""
    RESTRICTED = "restricted"  # 限定主题
    OPEN = "open"              # 开放主题


class TopicStatus(str, Enum):
    """主题状态"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class HistoricalContext(BaseModel):
    """历史背景"""
    era: str = Field(..., description="时代")
    year: int = Field(..., description="年份")
    location: str = Field(..., description="地点")
    description: str = Field(..., description="背景描述")


class TechnicalContext(BaseModel):
    """技术背景"""
    pre_conditions: List[str] = Field(default_factory=list, description="前置条件")
    constraints: List[str] = Field(default_factory=list, description="限制条件")
    available_resources: List[str] = Field(default_factory=list, description="可用资源")
    tech_level: str = Field(default="contemporary", description="技术水平")


class DiscussionGoal(BaseModel):
    """讨论目标"""
    description: str = Field(..., description="目标描述")
    success_criteria: List[str] = Field(default_factory=list, description="成功标准")
    expected_outcomes: List[str] = Field(default_factory=list, description="预期产出")


class RestrictedConfig(BaseModel):
    """限定主题配置"""
    historical_context: HistoricalContext
    technical_context: TechnicalContext
    goal: DiscussionGoal
    setting_narrative: str = Field("", description="背景叙事")


class OpenConfig(BaseModel):
    """开放主题配置"""
    keywords: List[str] = Field(default_factory=list, description="关键词")
    domains: List[str] = Field(default_factory=list, description="相关领域")
    exploration_depth: str = Field(default="medium", description="探索深度")
    initial_perspectives: List[str] = Field(default_factory=list, description="初始视角")


class DiscussionTopic(BaseModel):
    """讨论主题"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(..., description="主题标题")
    description: str = Field("", description="详细描述")
    topic_type: TopicType
    
    # 限定主题配置
    restricted_config: Optional[RestrictedConfig] = None
    
    # 开放主题配置
    open_config: Optional[OpenConfig] = None
    
    # 元数据
    status: TopicStatus = TopicStatus.DRAFT
    tags: List[str] = Field(default_factory=list, description="标签")
    
    # 创建者
    created_by: str = Field(default="system", description="创建者")
    
    # 时间戳
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 统计
    participant_count: int = 0
    message_count: int = 0
    capsule_count: int = 0


class TopicStorage:
    """主题存储"""
    
    def __init__(self, storage_dir: str = "./data"):
        from pathlib import Path
        import sqlite3
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.storage_dir / "topics.db"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 主题表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_topic(self, topic_data: Dict) -> DiscussionTopic:
        """创建主题"""
        import sqlite3
        
        topic = DiscussionTopic(**topic_data)
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO topics (id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (
            topic.id,
            topic.model_dump_json(),
            topic.created_at.isoformat(),
            topic.updated_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return topic
    
    def get_topic(self, topic_id: str) -> Optional[DiscussionTopic]:
        """获取主题"""
        import sqlite3
        from .capsule import KnowledgeCapsule
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM topics WHERE id = ?", (topic_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return DiscussionTopic.model_validate_json(row[0])
        return None
    
    def list_topics(
        self, 
        topic_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[DiscussionTopic]:
        """列出主题"""
        import sqlite3
        from .capsule import KnowledgeCapsule
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        query = "SELECT data FROM topics"
        params = []
        
        if topic_type:
            query += " WHERE data LIKE ?"
            params.append(f'%"topic_type": "{topic_type}"%')
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        
        topics = []
        for row in cursor.fetchall():
            try:
                topics.append(DiscussionTopic.model_validate_json(row[0]))
            except Exception:
                continue
        
        conn.close()
        return topics
    
    def update_status(self, topic_id: str, status: str):
        """更新主题状态"""
        import sqlite3
        
        topic = self.get_topic(topic_id)
        if not topic:
            return None
        
        topic.status = TopicStatus(status)
        topic.updated_at = datetime.utcnow()
        
        if status == "active":
            topic.started_at = datetime.utcnow()
        elif status == "completed":
            topic.completed_at = datetime.utcnow()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE topics SET data = ?, updated_at = ? WHERE id = ?",
            (topic.model_dump_json(), topic.updated_at.isoformat(), topic_id)
        )
        
        conn.commit()
        conn.close()
        
        return topic
    
    def increment_stats(self, topic_id: str, field: str = "message_count"):
        """更新统计"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute(f"UPDATE topics SET {field} = {field} + 1 WHERE id = ?", (topic_id,))
        
        conn.commit()
        conn.close()


# 单例实例
topic_storage = TopicStorage()
