"""
SuiLight Agent 配置系统
配置讨论中的智能体
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
from enum import Enum


class AgentRole(str, Enum):
    """Agent 角色"""
    MODERATOR = "moderator"      # 主持人
    EXPERT = "expert"            # 专家
    HISTORIAN = "historian"      # 历史学家
    CRITIC = "critic"            # 评论家
    SYNTHESIZER = "synthesizer"  # 综合者


class AgentConfig(BaseModel):
    """单个 Agent 配置"""
    agent_id: str = Field(..., description="Agent ID")
    role: AgentRole = Field(..., description="角色")
    name: str = Field(..., description="名称")
    personality: Optional[str] = Field(None, description="性格特点")
    expertise: List[str] = Field(default_factory=list, description="专业领域")
    perspective: str = Field(default="neutral", description="观点立场")
    
    # 参与配置
    participation: Dict[str, Any] = Field(
        default_factory=lambda: {
            "start_round": 1,
            "end_round": None,
            "speak_probability": 1.0
        },
        description="参与配置"
    )
    
    # 系统提示词增强
    system_prompt_addon: str = Field(default="", description="系统提示词附加")


class OrchestrationConfig(BaseModel):
    """讨论编排配置"""
    moderator_agent_id: str = Field(..., description="主持人 Agent ID")
    discussion_flow: str = Field(default="sequential", description="讨论流程")
    round_limit: int = Field(default=10, description="最大轮数")
    consensus_threshold: float = Field(default=0.7, description="共识阈值")
    max_agents_per_round: int = Field(default=3, description="每轮最大发言 Agent 数")


class AgentConfiguration(BaseModel):
    """完整的 Agent 配置"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    topic_id: str = Field(..., description="关联主题 ID")
    
    # Agent 列表
    agents: List[AgentConfig] = Field(default_factory=list, description="Agent 配置列表")
    
    # 编排配置
    orchestration: OrchestrationConfig = Field(default_factory=OrchestrationConfig)
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentConfigStorage:
    """Agent 配置存储"""
    
    def __init__(self, storage_dir: str = "./data"):
        from pathlib import Path
        import sqlite3
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.storage_dir / "agent_configs.db"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_configs (
                id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_config(self, topic_id: str, config_data: Dict) -> AgentConfiguration:
        """创建 Agent 配置"""
        import sqlite3
        
        # 添加 topic_id
        config_data["topic_id"] = topic_id
        
        config = AgentConfiguration(**config_data)
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_configs (id, topic_id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            config.id,
            topic_id,
            config.model_dump_json(),
            config.created_at.isoformat(),
            config.updated_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return config
    
    def get_config(self, config_id: str) -> Optional[AgentConfiguration]:
        """获取配置"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM agent_configs WHERE id = ?", (config_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return AgentConfiguration.model_validate_json(row[0])
        return None
    
    def get_config_by_topic(self, topic_id: str) -> Optional[AgentConfiguration]:
        """获取主题的 Agent 配置"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM agent_configs WHERE topic_id = ?", (topic_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return AgentConfiguration.model_validate_json(row[0])
        return None
    
    def list_configs(self, limit: int = 20) -> List[AgentConfiguration]:
        """列出所有配置"""
        import sqlite3
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM agent_configs ORDER BY created_at DESC LIMIT ?", (limit,))
        
        configs = []
        for row in cursor.fetchall():
            try:
                configs.append(AgentConfiguration.model_validate_json(row[0]))
            except Exception:
                continue
        
        conn.close()
        return configs


# 预设 Agent 模板
AGENT_TEMPLATES = {
    "scientist": {
        "role": "expert",
        "name": "科学家",
        "personality": "理性、严谨、追求真理",
        "expertise": ["科学研究", "实验方法", "数据分析"],
        "perspective": "evidence-based"
    },
    "historian": {
        "role": "historian",
        "name": "历史学家",
        "personality": "博学、审慎、重视背景",
        "expertise": ["历史事件", "时代背景", "人物研究"],
        "perspective": "historical-context"
    },
    "philosopher": {
        "role": "critic",
        "name": "哲学家",
        "personality": "深刻、爱质疑、追求本质",
        "expertise": ["伦理学", "认识论", "逻辑学"],
        "perspective": "critical-thinking"
    },
    "inventor": {
        "role": "expert",
        "name": "发明家",
        "personality": "创新、实践导向、解决问题",
        "expertise": ["工程学", "技术创新", "实用方案"],
        "perspective": "solution-oriented"
    }
}


# 单例实例
agent_config_storage = AgentConfigStorage()
