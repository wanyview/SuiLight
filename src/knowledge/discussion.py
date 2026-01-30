"""
SuiLight Knowledge Salon - 协作讨论框架
多 Agent 围绕话题进行深度讨论

功能:
1. 议题管理 - 创建、分配、追踪讨论议题
2. 协作流程 - 多 Agent 轮流发言、辩论、总结
3. 知识沉淀 - 从讨论中提取洞见、生成新知识
4. 涌现机制 - 通过多视角碰撞产生创新想法
"""

import json
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from collections import defaultdict
import logging

from .base import Agent, AgentRegistry, AgentMessage
from .presets import GREAT_MINDS, create_agent_configs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscussionPhase(Enum):
    """讨论阶段"""
    SETUP = "setup"           # 准备阶段
    INTRODUCTION = "intro"    # 引言
    PERSPECTIVES = "perspectives"  # 多角度分析
    DEBATE = "debate"         # 辩论
    SYNTHESIS = "synthesis"   # 综合
    CONCLUSION = "conclusion" # 结论
    CLOSED = "closed"         # 已结束


class ParticipantRole(Enum):
    """参与者角色"""
    LECTOR = "lector"         # 主讲人
    COMMENTATOR = "commentator"  # 评论员
    CRITIC = "critic"         # 批评者
    SYNTHESIZER = "synthesizer"  # 综合者
    QUESTIONER = "questioner" # 提问者


@dataclass
class DiscussionTopic:
    """讨论议题"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    category: str = ""  # 自然科学/社会科学/人文科学/交叉科学
    target_level: str = "discovery"  # discovery/invention/innovation
    keywords: List[str] = field(default_factory=list)
    
    # 讨论配置
    max_participants: int = 5
    max_rounds: int = 3  # 讨论轮数
    enable_debate: bool = True
    
    # 状态
    phase: DiscussionPhase = DiscussionPhase.SETUP
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # 参与者
    participants: List[Dict] = field(default_factory=list)
    lector_id: str = ""  # 主讲人
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "target_level": self.target_level,
            "keywords": self.keywords,
            "max_participants": self.max_participants,
            "max_rounds": self.max_rounds,
            "phase": self.phase.value,
            "created_at": self.created_at.isoformat(),
            "participants": self.participants,
            "lector_id": self.lector_id
        }


@dataclass
class DiscussionContribution:
    """讨论贡献"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic_id: str = ""
    agent_id: str = ""
    agent_name: str = ""
    role: str = ""  # ParticipantRole
    round_num: int = 1
    phase: str = ""
    content: str = ""
    datm_snapshot: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "role": self.role,
            "round_num": self.round_num,
            "phase": self.phase,
            "content": self.content,
            "datm_snapshot": self.datm_snapshot,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class DiscussionInsight:
    """讨论洞见 (从讨论中涌现)"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic_id: str = ""
    content: str = ""
    source_contributions: List[str] = field(default_factory=list)  # 贡献 ID 列表
    insight_type: str = "pattern"  # pattern/synthesis/innovation/question
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "content": self.content,
            "source_contributions": self.source_contributions,
            "insight_type": self.insight_type,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat()
        }


class DiscussionManager:
    """
    讨论管理器
    
    负责:
    - 创建和管理讨论
    - 分配参与者
    - 推进讨论阶段
    - 提取洞见
    """
    
    def __init__(self, registry: AgentRegistry = None):
        self.registry = registry or AgentRegistry()
        self.topics: Dict[str, DiscussionTopic] = {}
        self.contributions: List[DiscussionContribution] = []
        self.insights: List[DiscussionInsight] = []
        self.presets = GREAT_MINDS
        
        logger.info("讨论管理器初始化完成")
    
    # ============ 议题管理 ============
    
    def create_topic(
        self,
        title: str,
        description: str,
        category: str = "interdisciplinary",
        target_level: str = "discovery",
        keywords: List[str] = None,
        max_participants: int = 5,
        max_rounds: int = 3
    ) -> DiscussionTopic:
        """创建讨论议题"""
        topic = DiscussionTopic(
            title=title,
            description=description,
            category=category,
            target_level=target_level,
            keywords=keywords or [],
            max_participants=max_participants,
            max_rounds=max_rounds
        )
        
        self.topics[topic.id] = topic
        
        logger.info(f"创建讨论议题: {title} ({topic.id})")
        return topic
    
    def suggest_topics(self, category: str = None, count: int = 5) -> List[Dict]:
        """
        建议讨论议题
        
        基于预设的伟大思想家，生成有深度的讨论话题
        """
        suggested = []
        
        # 按类别筛选
        if category:
            domain_map = {
                "自然科学": ["physics", "chemistry", "biology", "mathematics", "astronomy"],
                "社会科学": ["economics", "psychology", "sociology", "political_science"],
                "人文科学": ["philosophy", "art", "literature"],
                "交叉科学": ["interdisciplinary", "engineering", "medicine", "computer_science"]
            }
            domains = domain_map.get(category, [])
        else:
            domains = None
        
        # 生成话题模板
        topic_templates = [
            {
                "template": "如果{name}活到今天，他会如何解决{problem}问题？",
                "level": "innovation",
                "category": "interdisciplinary"
            },
            {
                "template": "{name}的发现/发明方法论对现代{field}有什么启示？",
                "level": "discovery",
                "category": None
            },
            {
                "template": "如何结合{name}的{expertise}与现代技术解决{problem}？",
                "level": "invention",
                "category": "interdisciplinary"
            },
            {
                "template": "{name}的核心思想在{field}领域如何进一步发展？",
                "level": "innovation",
                "category": None
            },
            {
                "template": "比较{name}与另一位伟人在{field}的观点异同",
                "level": "discovery",
                "category": None
            }
        ]
        
        # 选择思想家
        candidates = []
        for name, info in self.presets.items():
            if domains:
                if info["domain"] not in domains:
                    continue
            candidates.append((name, info))
        
        if not candidates:
            candidates = list(self.presets.items())[:20]
        
        import random
        selected = random.sample(candidates, min(len(candidates), count))
        
        for name, info in selected:
            template = random.choice(topic_templates)
            
            topic = {
                "title": template["template"].format(
                    name=name,
                    field=info["domain"],
                    problem=self._generate_problem(info["domain"]),
                    expertise=info["expertise"][0] if info["expertise"] else "思想"
                ),
                "description": f"围绕{name}的贡献和思想进行深度讨论",
                "category": template["category"] or info["domain"],
                "target_level": template["level"],
                "keywords": info["expertise"][:3],
                "suggested_agents": [name]
            }
            suggested.append(topic)
        
        return suggested
    
    def _generate_problem(self, domain: str) -> str:
        """生成领域相关问题"""
        problems = {
            "physics": "能源危机",
            "chemistry": "材料科学瓶颈",
            "biology": "疾病治疗",
            "mathematics": "复杂系统建模",
            "astronomy": "宇宙探索",
            "economics": "可持续发展",
            "psychology": "心理健康",
            "philosophy": "人工智能伦理",
            "computer_science": "通用人工智能",
            "engineering": "太空殖民",
            "medicine": "衰老逆转",
            "interdisciplinary": "全球性问题"
        }
        return problems.get(domain, "当代重大挑战")
    
    # ============ 参与者管理 ============
    
    def assign_participants(
        self,
        topic_id: str,
        agent_ids: List[str] = None,
        auto_assign: bool = True,
        roles: Dict[str, str] = None
    ) -> List[Agent]:
        """
        分配参与者
        
        Args:
            topic_id: 议题 ID
            agent_ids: 指定的 Agent ID 列表
            auto_assign: 是否自动从预设中补充
            roles: 角色分配 {agent_id: role}
            
        Returns:
            参与者的 Agent 列表
        """
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"议题不存在: {topic_id}")
        
        participants = []
        
        # 使用指定的 Agent
        if agent_ids:
            for aid in agent_ids:
                agent = self.registry.get(aid)
                if agent:
                    participants.append(agent)
        
        # 自动补充
        if auto_assign and len(participants) < topic.max_participants:
            needed = topic.max_participants - len(participants)
            
            # 从预设中寻找合适的 Agent
            for name, info in self.presets.items():
                if len(participants) >= topic.max_participants:
                    break
                
                # 检查是否已在参与者中
                if any(a.config.name == name for a in participants):
                    continue
                
                # 检查领域匹配
                if topic.category != "interdisciplinary" and info["domain"] != topic.category:
                    continue
                
                # 创建 Agent
                agent = self._create_agent_from_preset(name, info)
                self.registry.register(agent)
                participants.append(agent)
        
        # 更新议题
        topic.participants = [
            {"id": p.id, "name": p.config.name, "role": roles.get(p.id, "commentator")}
            for p in participants
        ]
        topic.lector_id = participants[0].id if participants else ""
        
        logger.info(f"为议题 {topic_id} 分配了 {len(participants)} 位参与者")
        return participants
    
    def _create_agent_from_preset(self, name: str, preset: Dict) -> Agent:
        """从预设创建 Agent"""
        from .base import Agent, AgentConfig, DATM
        
        datm = DATM.from_dict(preset.get("datm", {}))
        config = AgentConfig(
            name=name,
            domain=preset["domain"],
            description=preset["description"],
            expertise=preset["expertise"],
            datm=datm
        )
        return Agent(config)
    
    # ============ 讨论流程 ============
    
    def start_discussion(self, topic_id: str) -> Dict:
        """开始讨论"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"议题不存在: {topic_id}")
        
        if not topic.participants:
            raise ValueError("未分配参与者")
        
        # 进入引言阶段
        topic.phase = DiscussionPhase.INTRODUCTION
        topic.updated_at = datetime.now()
        
        # 获取主讲人
        lector = self.registry.get(topic.lector_id)
        
        return {
            "topic": topic.to_dict(),
            "phase": topic.phase.value,
            "lector": lector.config.name if lector else None,
            "message": f"讨论开始！主讲人: {lector.config.name if lector else '未知'}"
        }
    
    def next_phase(self, topic_id: str) -> Dict:
        """推进到下一阶段"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"议题不存在: {topic_id}")
        
        phases = list(DiscussionPhase)
        current_index = phases.index(topic.phase)
        
        if current_index + 1 < len(phases):
            topic.phase = phases[current_index + 1]
            topic.updated_at = datetime.now()
            
            return {
                "phase": topic.phase.value,
                "message": f"进入 {topic.phase.value} 阶段"
            }
        else:
            topic.phase = DiscussionPhase.CLOSED
            return {
                "phase": topic.phase.value,
                "message": "讨论结束"
            }
    
    def add_contribution(
        self,
        topic_id: str,
        agent_id: str,
        content: str,
        role: str = "commentator",
        round_num: int = 1
    ) -> DiscussionContribution:
        """添加讨论贡献"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"议题不存在: {topic_id}")
        
        agent = self.registry.get(agent_id)
        if not agent:
            raise ValueError(f"Agent 不存在: {agent_id}")
        
        contribution = DiscussionContribution(
            topic_id=topic_id,
            agent_id=agent_id,
            agent_name=agent.config.name,
            role=role,
            round_num=round_num,
            phase=topic.phase.value,
            content=content,
            datm_snapshot=agent.config.datm.to_dict()
        )
        
        self.contributions.append(contribution)
        
        logger.info(f"{agent.config.name} 在 {topic.phase.value} 阶段贡献内容")
        return contribution
    
    # ============ 知识沉淀 ============
    
    def extract_insights(self, topic_id: str) -> List[DiscussionInsight]:
        """从讨论中提取洞见"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"议题不存在: {topic_id}")
        
        # 获取该议题的所有贡献
        contributions = [c for c in self.contributions if c.topic_id == topic_id]
        
        if not contributions:
            return []
        
        insights = []
        
        # 1. 提取模式 (共识/分歧)
        patterns = self._extract_patterns(contributions)
        for pattern in patterns:
            insight = DiscussionInsight(
                topic_id=topic_id,
                content=pattern,
                source_contributions=[c.id for c in contributions],
                insight_type="pattern",
                confidence=0.7
            )
            insights.append(insight)
        
        # 2. 综合观点
        synthesis = self._synthesize_views(contributions)
        if synthesis:
            insight = DiscussionInsight(
                topic_id=topic_id,
                content=synthesis,
                source_contributions=[c.id for c in contributions],
                insight_type="synthesis",
                confidence=0.6
            )
            insights.append(insight)
        
        # 3. 涌现创新
        innovations = self._extract_innovations(contributions)
        for innovation in innovations:
            insight = DiscussionInsight(
                topic_id=topic_id,
                content=innovation,
                source_contributions=[c.id for c in contributions],
                insight_type="innovation",
                confidence=0.5
            )
            insights.append(insight)
        
        # 4. 开放问题
        questions = self._extract_questions(contributions)
        for question in questions:
            insight = DiscussionInsight(
                topic_id=topic_id,
                content=question,
                source_contributions=[c.id for c in contributions],
                insight_type="question",
                confidence=0.5
            )
            insights.append(insight)
        
        self.insights.extend(insights)
        
        logger.info(f"从讨论 {topic_id} 中提取 {len(insights)} 个洞见")
        return insights
    
    def _extract_patterns(self, contributions: List[DiscussionContribution]) -> List[str]:
        """提取共识/分歧模式"""
        patterns = []
        
        # 简单的模式提取
        agent_views = defaultdict(list)
        for c in contributions:
            agent_views[c.agent_name].append(c.content)
        
        # 检查是否有共识关键词
        consensus_keywords = ["同意", "共识", "一致", "的确", "确实"]
        dissent_keywords = ["但是", "然而", "相反", "不同", "质疑"]
        
        for name, views in agent_views.items():
            full_text = " ".join(views)
            
            has_consensus = any(kw in full_text for kw in consensus_keywords)
            has_dissent = any(kw in full_text for kw in dissent_keywords)
            
            if has_consensus:
                patterns.append(f"{name} 的观点与其他参与者形成共识")
            if has_dissent:
                patterns.append(f"{name} 提出了不同观点")
        
        return patterns
    
    def _synthesize_views(self, contributions: List[DiscussionContribution]) -> str:
        """综合观点"""
        if not contributions:
            return ""
        
        # 简单综合
        unique_views = set()
        for c in contributions:
            # 提取核心观点
            if len(c.content) > 20:
                view = c.content[:100]
                unique_views.add(view)
        
        if unique_views:
            synthesis = f"讨论涵盖 {len(unique_views)} 个不同观点，"
            synthesis += "体现了多学科交叉的综合视角。"
            return synthesis
        
        return ""
    
    def _extract_innovations(self, contributions: List[DiscussionContribution]) -> List[str]:
        """提取创新想法"""
        innovations = []
        
        innovation_keywords = ["创新", "突破", "新方法", "结合", "融合", "也许可以"]
        
        for c in contributions:
            if any(kw in c.content for kw in innovation_keywords):
                # 提取创新建议
                sentences = c.content.split("。")
                for sent in sentences:
                    if any(kw in sent for kw in innovation_keywords):
                        innovations.append(f"来自 {c.agent_name} 的创新建议: {sent.strip()}")
        
        return innovations[:3]  # 最多 3 个
    
    def _extract_questions(self, contributions: List[DiscussionContribution]) -> List[str]:
        """提取开放问题"""
        questions = []
        
        question_markers = ["?", "？", "是否", "能否", "怎么", "为什么"]
        
        for c in contributions:
            if any(m in c.content for m in question_markers):
                # 提取问题
                sentences = c.content.replace("?", "？").split("？")
                for sent in sentences:
                    sent = sent.strip()
                    if len(sent) > 10 and len(sent) < 200:
                        questions.append(f"{c.agent_name} 提出: {sent}？")
        
        return questions[:5]  # 最多 5 个
    
    # ============ 统计与报告 ============
    
    def get_topic_summary(self, topic_id: str) -> Dict:
        """获取议题摘要"""
        topic = self.topics.get(topic_id)
        if not topic:
            raise ValueError(f"议题不存在: {topic_id}")
        
        contributions = [c for c in self.contributions if c.topic_id == topic_id]
        insights = [i for i in self.insights if i.topic_id == topic_id]
        
        # 按阶段统计
        by_phase = defaultdict(list)
        for c in contributions:
            by_phase[c.phase].append(c)
        
        # 按 Agent 统计
        by_agent = defaultdict(int)
        for c in contributions:
            by_agent[c.agent_name] += 1
        
        return {
            "topic": topic.to_dict(),
            "statistics": {
                "total_contributions": len(contributions),
                "total_insights": len(insights),
                "phases": {p: len(v) for p, v in by_phase.items()},
                "agents": dict(by_agent)
            },
            "phases": list(DiscussionPhase),
            "current_phase": topic.phase.value
        }
    
    def list_topics(self, status: str = None) -> List[Dict]:
        """列出议题"""
        topics = []
        
        for tid, topic in self.topics.items():
            if status:
                if topic.phase.value != status:
                    continue
            
            topics.append(topic.to_dict())
        
        return topics


# ============ 预设讨论话题 ============

GREAT_DISCUSSIONS = [
    {
        "title": "如何结合爱迪生的发明方法论与现代 AI 技术？",
        "description": "分析爱迪生的系统性试错方法，探讨如何应用于 AI 系统的发明创新",
        "category": "交叉科学",
        "target_level": "invention",
        "keywords": ["发明方法论", "系统试错", "AI创新"],
        "suggested_agents": ["托马斯·爱迪生", "艾伦·图灵", "本杰明·富兰克林", "约翰·冯·诺依曼"]
    },
    {
        "title": "牛顿的万有引力定律如何启发暗物质研究？",
        "description": "从牛顿到爱因斯坦再到现代宇宙学，讨论引力的本质",
        "category": "自然科学",
        "target_level": "discovery",
        "keywords": ["引力", "暗物质", "宇宙学"],
        "suggested_agents": ["艾萨克·牛顿", "阿尔伯特·爱因斯坦", "埃德温·哈勃", "卡尔·萨根"]
    },
    {
        "title": "如何用达芬奇的跨学科思维解决气候危机？",
        "description": "借鉴文艺复兴时期的跨学科整合能力，探讨复杂系统问题的解决",
        "category": "交叉科学",
        "target_level": "innovation",
        "keywords": ["跨学科", "复杂系统", "气候危机"],
        "suggested_agents": ["列奥纳多·达·芬奇", "雷切尔·卡森", "赫伯特·西蒙", "伊利亚·普里戈金"]
    },
    {
        "title": "达尔文进化论对社会制度设计的启示",
        "description": "自然选择原理如何应用于社会制度和组织的演化设计",
        "category": "社会科学",
        "target_level": "innovation",
        "keywords": ["进化", "制度设计", "社会演化"],
        "suggested_agents": ["查尔斯·达尔文", "亚当·斯密", "卡尔·马克思", "约瑟夫·熊彼特"]
    },
    {
        "title": "孔子思想与西方心理学的人格理论比较",
        "description": "对比中西方对人性和人格的不同理解",
        "category": "人文科学",
        "target_level": "discovery",
        "keywords": ["人格", "儒学", "心理学"],
        "suggested_agents": ["孔子", "西格蒙德·弗洛伊德", "卡尔·荣格", "马斯洛"]
    }
]


def get_great_discussions() -> List[Dict]:
    """获取预设讨论话题"""
    return GREAT_DISCUSSIONS
