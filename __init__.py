"""
SuiLight Knowledge Salon
========================

多智能体知识协作平台

快速开始:
    from suilight import create_app, create_agent

    app = create_app()
    # 或单独使用 Agent
    agent = create_agent("牛顿", domain="physics")

安装:
    pip install -e .
    
启动:
    python -m suilight
    # 或
    suilight
"""

__version__ = "1.0.0"
__author__ = "Kai Digital Agent"

# 便捷导入
from .src.main import app
from .src.agents.base import Agent, AgentConfig, DATM, AgentRegistry
from .src.knowledge.generator import AgentGenerator
from .src.knowledge.discussion import DiscussionManager
from .src.tasks import TaskManager
from .src.storage import StorageManager
from .src.agents.presets import GREAT_MINDS, create_agent_configs

__all__ = [
    # FastAPI App
    "app",
    
    # Agent 相关
    "Agent",
    "AgentConfig", 
    "DATM",
    "AgentRegistry",
    
    # 知识引擎
    "AgentGenerator",
    "DiscussionManager",
    
    # 任务与存储
    "TaskManager",
    "StorageManager",
    
    # 预设
    "GREAT_MINDS",
    "create_agent_configs",
]


def create_app(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    创建并启动 SuiLight 应用
    
    Args:
        host: 绑定地址
        port: 端口
        reload: 热重载模式
        
    Returns:
        FastAPI 应用实例
    """
    import uvicorn
    from .src.main import app as suilight_app
    
    # 启动服务
    uvicorn.run(
        suilight_app,
        host=host,
        port=port,
        reload=reload
    )
    
    return suilight_app


def create_agent(
    name: str,
    domain: str,
    description: str = "",
    expertise: list = None,
    datm: dict = None
) -> Agent:
    """
    创建自定义 Agent
    
    Args:
        name: Agent 名称
        domain: 领域
        description: 描述
        expertise: 专长列表
        datm: DATM 配置
        
    Returns:
        Agent 实例
    """
    datm_obj = DATM.from_dict(datm) if datm else DATM()
    
    config = AgentConfig(
        name=name,
        domain=domain,
        description=description,
        expertise=expertise or [],
        datm=datm_obj
    )
    
    return Agent(config)


def create_discussion(
    title: str,
    description: str,
    category: str = "交叉科学"
) -> DiscussionManager:
    """
    创建讨论管理器
    
    Args:
        title: 讨论标题
        description: 描述
        category: 领域分类
        
    Returns:
        DiscussionManager 实例
    """
    from .src.knowledge.discussion import DiscussionManager
    from .src.agents.base import AgentRegistry
    
    registry = AgentRegistry()
    dm = DiscussionManager(registry)
    
    topic = dm.create_topic(
        title=title,
        description=description,
        category=category
    )
    
    return dm, topic


def load_preset_agents(limit: int = 100, domain: str = None) -> list:
    """
    加载预设 Agent
    
    Args:
        limit: 最大数量
        domain: 领域过滤
        
    Returns:
        Agent 列表
    """
    from .src.agents.base import Agent, AgentRegistry
    from .src.agents.presets import create_agent_configs
    
    configs = create_agent_configs()
    
    if domain:
        configs = [c for c in configs if c.domain == domain]
    
    configs = configs[:limit]
    
    registry = AgentRegistry()
    agents = []
    
    for config in configs:
        agent = Agent(config)
        registry.register(agent)
        agents.append(agent)
    
    return agents
