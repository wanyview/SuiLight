"""
SuiLight 讨论记录系统
记录完整的讨论过程和涌现成果
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
from enum import Enum


class MessageType(str, Enum):
    """消息类型"""
    QUESTION = "question"
    ANSWER = "answer"
    COMMENT = "comment"
    SYNTHESIS = "synthesis"
    INSIGHT = "insight"


class MilestoneType(str, Enum):
    """里程碑类型"""
    INSIGHT = "insight"      # 关键洞见
    CONSENSUS = "consensus"  # 达成共识
    DIVERGENCE = "divergence" # 观点分歧
    BREAKTHROUGH = "breakthrough" # 突破


class AgentMessage(BaseModel):
    """Agent 消息"""
    round: int = Field(..., description="讨论轮次")
    timestamp: str = Field(..., description="时间戳")
    agent_id: str = Field(..., description="Agent ID")
    agent_role: str = Field(..., description="Agent 角色")
    agent_name: str = Field(..., description="Agent 名称")
    content: str = Field(..., description="消息内容")
    message_type: MessageType = MessageType.COMMENT
    reaction_agents: List[str] = Field(default_factory=list, description="反应的 Agent")


class DiscussionMilestone(BaseModel):
    """讨论里程碑"""
    timestamp: str = Field(..., description="时间戳")
    milestone_type: MilestoneType
    description: str = Field(..., description="描述")
    related_rounds: List[int] = Field(default_factory=list, description="相关轮次")
    key_participants: List[str] = Field(default_factory=list, description="关键参与者")


class DiscussionOutcome(BaseModel):
    """讨论成果"""
    capsule_ids: List[str] = Field(default_factory=list, description="产出的胶囊 ID")
    insights: List[str] = Field(default_factory=list, description="关键洞见")
    action_items: List[str] = Field(default_factory=list, description="后续行动")
    consensus_points: List[str] = Field(default_factory=list, description="共识点")


class DiscussionRecord(BaseModel):
    """讨论记录"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    topic_id: str = Field(..., description="主题 ID")
    
    # 时间线
    timeline: List[AgentMessage] = Field(default_factory=list, description="消息时间线")
    
    # 里程碑
    milestones: List[DiscussionMilestone] = Field(default_factory=list, description="里程碑")
    
    # 成果
    outcomes: DiscussionOutcome = Field(default_factory=DiscussionOutcome)
    
    # 元数据
    status: str = Field(default="in_progress", description="状态")
    total_rounds: int = 0
    total_agents: int = 0
    duration_minutes: int = 0
    
    # DATM 评分
    quality_score: Dict[str, float] = Field(default_factory=dict)
    
    # 时间戳
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    
    def add_message(self, message: AgentMessage):
        """添加消息"""
        self.timeline.append(message)
        self.total_rounds = max(self.total_rounds, message.round)
    
    def add_milestone(self, milestone: DiscussionMilestone):
        """添加里程碑"""
        self.milestones.append(milestone)
    
    def finalize(self, capsules: List[str]):
        """完成讨论"""
        self.status = "completed"
        self.ended_at = datetime.utcnow()
        self.outcomes.capsule_ids = capsules
        self.duration_minutes = int((self.ended_at - self.started_at).total_seconds() / 60)


class DiscussionStorage:
    """讨论记录存储"""
    
    def __init__(self, storage_dir: str = "./data"):
        from pathlib import Path
        import sqlite3
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.storage_dir / "discussions.db"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 讨论记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discussions (
                id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                data TEXT NOT NULL,
                started_at TEXT,
                ended_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_discussion(self, topic_id: str) -> DiscussionRecord:
        """创建讨论记录"""
        import sqlite3
        
        record = DiscussionRecord(topic_id=topic_id)
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO discussions (id, topic_id, data, started_at)
            VALUES (?, ?, ?, ?)
        """, (
            record.id,
            topic_id,
            record.model_dump_json(),
            record.started_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return record
    
    def get_discussion(self, discussion_id: str) -> Optional[DiscussionRecord]:
        """获取讨论记录"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM discussions WHERE id = ?", (discussion_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return DiscussionRecord.model_validate_json(row[0])
        return None
    
    def get_discussions_by_topic(self, topic_id: str) -> List[DiscussionRecord]:
        """获取主题的所有讨论"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM discussions WHERE topic_id = ?", (topic_id,))
        
        discussions = []
        for row in cursor.fetchall():
            try:
                discussions.append(DiscussionRecord.model_validate_json(row[0]))
            except Exception:
                continue
        
        conn.close()
        return discussions
    
    def add_message(self, discussion_id: str, message: Dict):
        """添加消息"""
        import sqlite3
        
        record = self.get_discussion(discussion_id)
        if not record:
            return None
        
        record.add_message(AgentMessage(**message))
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE discussions SET data = ? WHERE id = ?",
            (record.model_dump_json(), discussion_id)
        )
        
        conn.commit()
        conn.close()
        
        return record
    
    def complete_discussion(self, discussion_id: str, capsule_ids: List[str]):
        """完成讨论"""
        import sqlite3
        
        record = self.get_discussion(discussion_id)
        if not record:
            return None
        
        record.finalize(capsule_ids)
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE discussions SET data = ?, ended_at = ? WHERE id = ?",
            (record.model_dump_json(), record.ended_at.isoformat(), discussion_id)
        )
        
        conn.commit()
        conn.close()
        
        return record
    
    def get_discussion_history(self, topic_id: str) -> Dict:
        """获取讨论历史摘要"""
        discussions = self.get_discussions_by_topic(topic_id)
        
        total_messages = sum(len(d.timeline) for d in discussions)
        total_milestones = sum(len(d.milestones) for d in discussions)
        all_capsules = []
        for d in discussions:
            all_capsules.extend(d.outcomes.capsule_ids)
        
        return {
            "topic_id": topic_id,
            "discussion_count": len(discussions),
            "total_messages": total_messages,
            "total_milestones": total_milestones,
            "total_capsules": len(all_capsules),
            "latest_discussion": discussions[0].id if discussions else None
        }


# 单例实例
discussion_storage = DiscussionStorage()
