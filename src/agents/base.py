"""
SuiLight Knowledge Salon - Agent Base Framework
多智能体核心框架

基于 MiniMax LLM 的知识沙龙 Agent 系统
"""

import json
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent 状态"""
    IDLE = "idle"
    THINKING = "thinking"
    SPEAKING = "speaking"
    LEARNING = "learning"
    COLLABORATING = "collaborating"


@dataclass
class DATM:
    """
    Dual-Axis Knowledge Matrix (DATM)
    双轴知识矩阵
    
    Truth/Goodness/Beauty/Intelligence 四维框架
    """
    truth: int = 50          # 科学性 (0-100)
    goodness: int = 50       # 社科性 (0-100)
    beauty: int = 50         # 人文性 (0-100)
    intelligence: int = 50   # 创新性 (0-100)
    
    def to_dict(self) -> Dict[str, int]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'DATM':
        return cls(
            truth=data.get('truth', 50),
            goodness=data.get('goodness', 50),
            beauty=data.get('beauty', 50),
            intelligence=data.get('intelligence', 50)
        )
    
    def to_radar_data(self) -> Dict[str, Any]:
        """转换为雷达图数据"""
        return {
            "labels": ["Truth", "Goodness", "Beauty", "Intelligence"],
            "datasets": [{
                "label": "Knowledge Matrix",
                "data": [self.truth, self.goodness, self.beauty, self.intelligence],
                "backgroundColor": "rgba(99, 102, 241, 0.2)",
                "borderColor": "rgba(99, 102, 241, 1)",
            }]
        }


@dataclass
class AgentConfig:
    """Agent 配置"""
    name: str
    domain: str
    description: str = ""
    expertise: List[str] = field(default_factory=list)
    datm: DATM = field(default_factory=DATM)
    personality: str = "professional"
    system_prompt: str = ""


class AgentMessage:
    """Agent 消息"""
    
    def __init__(
        self,
        sender_id: str,
        receiver_id: str,
        content: str,
        message_type: str = "chat",
        metadata: Dict = None
    ):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.message_type = message_type
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentMessage':
        msg = cls(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            content=data['content'],
            message_type=data.get('message_type', 'chat'),
            metadata=data.get('metadata', {})
        )
        msg.id = data.get('id', str(uuid.uuid4()))
        msg.timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
        return msg


class Agent:
    """
    Agent 基类
    
    知识沙龙中的专家 Agent
    """
    
    def __init__(self, config: AgentConfig):
        self.id = str(uuid.uuid4())[:8]
        self.config = config
        self.config.name = f"{config.name}_{self.id}"
        self.status = AgentStatus.IDLE
        self.memory: List[Dict] = []
        self.knowledge_base: List[str] = []
        self.collaborators: List[str] = []
        
        # 系统提示词
        if not config.system_prompt:
            self.config.system_prompt = self._generate_system_prompt()
        
        logger.info(f"Agent {self.config.name} ({self.id}) 初始化完成")
    
    def _generate_system_prompt(self) -> str:
        """生成系统提示词"""
        return f"""你是{self.config.name}，一个{self.config.domain}领域的专家。

## 关于你
{description}

## 专业领域
{', '.join(self.config.expertise)}

## DATM 知识矩阵
- Truth (科学性): {self.config.datm.truth}
- Goodness (社科性): {self.config.datm.goodness}
- Beauty (人文性): {self.config.datm.beauty}
- Intelligence (创新性): {self.config.datm.intelligence}

## 行为准则
1. 基于事实和专业知识回答问题
2. 考虑观点的价值观影响 (Goodness)
3. 保持开放和创新的思维方式 (Intelligence)
4. 注重表达的审美和情感连接 (Beauty)
5. 适当时候寻求其他专家的协作

## 回复风格
请根据当前话题的性质，平衡真/善/美/灵四个维度，提供专业而有洞见的回答。
"""
    
    def think(self, message: str, context: List[Dict] = None) -> str:
        """
        思考过程 (内部调用 LLM)
        
        Args:
            message: 用户输入
            context: 对话上下文
            
        Returns:
            思考结果
        """
        self.status = AgentStatus.THINKING
        
        try:
            # TODO: 集成 MiniMax API
            response = self._mock_think(message, context)
            return response
        finally:
            self.status = AgentStatus.IDLE
    
    def _mock_think(self, message: str, context: List[Dict] = None) -> str:
        """Mock 思考过程 (待集成 MiniMax)"""
        return f"【{self.config.name}】{message} - 这是一个示例回复，待集成 MiniMax API。"
    
    def chat(self, message: str, context: List[Dict] = None) -> str:
        """
        对话接口
        
        Args:
            message: 用户消息
            context: 对话上下文
            
        Returns:
            Agent 回复
        """
        self.status = AgentStatus.THINKING
        
        # 记录到记忆
        self.memory.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # 调用思考
        response = self.think(message, context)
        
        # 记录回复
        self.memory.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        self.status = AgentStatus.IDLE
        return response
    
    def learn(self, knowledge: str, source: str = "manual") -> bool:
        """
        学习新知识
        
        Args:
            knowledge: 知识内容
            source: 知识来源
            
        Returns:
            是否成功
        """
        self.status = AgentStatus.LEARNING
        
        self.knowledge_base.append(knowledge)
        self.memory.append({
            "role": "system",
            "type": "learning",
            "content": knowledge,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Agent {self.config.name} 学习新知识: {source}")
        
        self.status = AgentStatus.IDLE
        return True
    
    def teach(self, topic: str) -> str:
        """
        讲授知识
        
        Args:
            topic: 讲授主题
            
        Returns:
            讲授内容
        """
        self.status = AgentStatus.SPEAKING
        
        # 从知识库中提取相关知识
        relevant_knowledge = [k for k in self.knowledge_base if topic.lower() in k.lower()]
        
        if relevant_knowledge:
            content = f"关于{topic}，让我为你讲解：\n\n" + "\n\n".join(relevant_knowledge[:3])
        else:
            content = f"关于{topic}，我可以结合我的专业背景为你讲解。不过我需要先学习更多相关知识。"
        
        self.status = AgentStatus.IDLE
        return content
    
    def collaborate(self, message: str, other_agents: List['Agent']) -> str:
        """
        协作对话
        
        Args:
            message: 协作话题
            other_agents: 其他 Agent 列表
            
        Returns:
            协作结果
        """
        self.status = AgentStatus.COLLABORATING
        
        # 通知其他 Agent
        collaborator_ids = [agent.id for agent in other_agents]
        self.collaborators = collaborator_ids
        
        # 构建协作上下文
        context = f"协作话题: {message}\n"
        context += f"参与者: {', '.join([a.config.name for a in other_agents])}\n"
        
        response = self.think(context, self.memory[-5:])
        
        self.status = AgentStatus.IDLE
        return response
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.config.name,
            "domain": self.config.domain,
            "description": self.config.description,
            "expertise": self.config.expertise,
            "datm": self.config.datm.to_dict(),
            "status": self.status.value,
            "knowledge_count": len(self.knowledge_base),
            "memory_count": len(self.memory)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Agent':
        """从字典创建"""
        config = AgentConfig(
            name=data['name'],
            domain=data['domain'],
            description=data.get('description', ''),
            expertise=data.get('expertise', []),
            datm=DATM.from_dict(data.get('datm', {}))
        )
        agent = cls(config)
        agent.id = data.get('id', agent.id)
        return agent


class AgentRegistry:
    """
    Agent 注册表
    
    管理所有 Agent 的注册、发现和调度
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.domains: Dict[str, List[str]] = {}  # domain -> agent_ids
    
    def register(self, agent: Agent) -> bool:
        """注册 Agent"""
        if agent.id in self.agents:
            logger.warning(f"Agent {agent.id} 已存在")
            return False
        
        self.agents[agent.id] = agent
        
        # 按领域分类
        domain = agent.config.domain
        if domain not in self.domains:
            self.domains[domain] = []
        self.domains[domain].append(agent.id)
        
        logger.info(f"Agent {agent.config.name} ({agent.id}) 注册成功")
        return True
    
    def unregister(self, agent_id: str) -> bool:
        """注销 Agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        domain = agent.config.domain
        
        if domain in self.domains:
            self.domains[domain].remove(agent_id)
        
        del self.agents[agent_id]
        logger.info(f"Agent {agent_id} 已注销")
        return True
    
    def get(self, agent_id: str) -> Optional[Agent]:
        """获取 Agent"""
        return self.agents.get(agent_id)
    
    def find_by_domain(self, domain: str) -> List[Agent]:
        """按领域查找"""
        agent_ids = self.domains.get(domain, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]
    
    def find_by_expertise(self, topic: str) -> List[Agent]:
        """按专长查找"""
        matched = []
        for agent in self.agents.values():
            if any(topic.lower() in exp.lower() for exp in agent.config.expertise):
                matched.append(agent)
        return matched
    
    def list_all(self) -> List[Agent]:
        """列出所有 Agent"""
        return list(self.agents.values())
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "total": len(self.agents),
            "domains": self.domains,
            "agents": {aid: agent.to_dict() for aid, agent in self.agents.items()}
        }
