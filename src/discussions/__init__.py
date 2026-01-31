"""
SuiLight 讨论系统模块
主题管理、Agent配置、讨论记录
"""

from .topic_manager import (
    topic_storage,
    DiscussionTopic,
    TopicType,
    TopicStatus,
    RestrictedConfig,
    OpenConfig
)

from .agent_config import (
    agent_config_storage,
    AgentConfiguration,
    AgentConfig,
    OrchestrationConfig,
    AGENT_TEMPLATES
)

from .discussion_record import (
    discussion_storage,
    DiscussionRecord,
    AgentMessage,
    DiscussionMilestone,
    MessageType,
    MilestoneType
)

from .discussion_router import router

__all__ = [
    # Topic Manager
    "topic_storage",
    "DiscussionTopic",
    "TopicType",
    "TopicStatus",
    "RestrictedConfig",
    "OpenConfig",
    
    # Agent Config
    "agent_config_storage",
    "AgentConfiguration",
    "AgentConfig",
    "OrchestrationConfig",
    "AGENT_TEMPLATES",
    
    # Discussion Record
    "discussion_storage",
    "DiscussionRecord",
    "AgentMessage",
    "DiscussionMilestone",
    "MessageType",
    "MilestoneType",
    
    # Router
    "router"
]
