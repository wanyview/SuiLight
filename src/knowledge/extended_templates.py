"""
SuiLight Knowledge Salon - 扩展模板系统
覆盖全面科学领域 + 多层次深度 + 跨学科交叉
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CapsuleTemplateType(Enum):
    """胶囊模板类型 - 扩展版"""
    
    # 按学科分类
    NATURAL_SCIENCE = "natural_science"      # 自然科学
    SOCIAL_SCIENCE = "social_science"        # 社会科学
    HUMANITIES = "humanities"                # 人文科学
    TECHNOLOGY = "technology"                # 技术工程
    INTERDISCIPLINARY = "interdisciplinary"   # 交叉科学
    
    # 按深度分类
    INTRODUCTION = "introduction"            # 入门级
    INTERMEDIATE = "intermediate"          # 进阶级
    ADVANCED = "advanced"                  # 深入级
    
    # 按类型分类
    PROBLEM_SOLVING = "problem_solving"     # 问题解决型
    OPINION_SUMMARY = "opinion_summary"     # 观点总结型
    DECISION_ADVICE = "decision_advice"     # 决策建议型
    KNOWLEDGE沉淀 = "knowledge_summarization"  # 知识沉淀型
    DISCUSSION_OUTPUT = "discussion_output"  # 讨论产出型
    RESEARCH_REVIEW = "research_review"     # 研究综述型
    EXPERT_OPINION = "expert_opinion"      # 专家观点型
    CASE_STUDY = "case_study"              # 案例分析型


# ============ 扩展模板定义 ============

# 科学领域分类
SCIENTIFIC_DOMAINS = {
    # 自然科学
    "physics": {"name": "物理学", "icon": "🔬", "subfields": ["力学", "电磁学", "量子物理", "相对论"]},
    "chemistry": {"name": "化学", "icon": "🧪", "subfields": ["有机化学", "无机化学", "物理化学", "分析化学"]},
    "biology": {"name": "生物学", "icon": "🧬", "subfields": ["遗传学", "细胞生物学", "生态学", "进化论"]},
    "mathematics": {"name": "数学", "icon": "📐", "subfields": ["代数", "几何", "分析", "概率论"]},
    "astronomy": {"name": "天文学", "icon": "🌌", "subfields": ["宇宙学", "星系", "恒星", "行星"]},
    "earth_science": {"name": "地球科学", "icon": "🌍", "subfields": ["地质学", "气象学", "海洋学"]},
    
    # 社会科学
    "economics": {"name": "经济学", "icon": "💰", "subfields": ["微观经济", "宏观经济", "行为经济"]},
    "psychology": {"name": "心理学", "icon": "🧠", "subfields": ["认知心理", "社会心理", "发展心理"]},
    "sociology": {"name": "社会学", "icon": "👥", "subfields": ["社会结构", "文化", "变迁"]},
    "political_science": {"name": "政治学", "icon": "🏛️", "subfields": ["政治理论", "国际关系", "公共政策"]},
    "law": {"name": "法学", "icon": "⚖️", "subfields": ["宪法", "民法", "刑法", "国际法"]},
    "education": {"name": "教育学", "icon": "📚", "subfields": ["教育心理", "课程设计", "教育技术"]},
    
    # 人文科学
    "philosophy": {"name": "哲学", "icon": "🤔", "subfields": ["形而上学", "认识论", "伦理学", "美学"]},
    "history": {"name": "历史学", "icon": "📜", "subfields": ["世界史", "中国史", "思想史"]},
    "literature": {"name": "文学", "icon": "📖", "subfields": ["古典文学", "现代文学", "比较文学"]},
    "art": {"name": "艺术", "icon": "🎨", "subfields": ["绘画", "音乐", "雕塑", "建筑"]},
    "religion": {"name": "宗教学", "icon": "⛪", "subfields": ["佛教", "基督教", "伊斯兰教"]},
    "linguistics": {"name": "语言学", "icon": "🗣️", "subfields": ["语法", "语义", "语用"]},
    
    # 技术工程
    "computer_science": {"name": "计算机科学", "icon": "💻", "subfields": ["算法", "数据结构", "人工智能"]},
    "engineering": {"name": "工程学", "icon": "⚙️", "subfields": ["机械", "电子", "土木"]},
    "medicine": {"name": "医学", "icon": "🏥", "subfields": ["临床医学", "基础医学", "公共卫生"]},
    "ai": {"name": "人工智能", "icon": "🤖", "subfields": ["机器学习", "自然语言处理", "计算机视觉"]},
    
    # 交叉科学
    "cognitive_science": {"name": "认知科学", "icon": "🧠", "subfields": ["神经科学", "心理学", "AI"]},
    "complex_systems": {"name": "复杂系统", "icon": "🔗", "subfields": ["系统论", "网络科学", "复杂性"]},
    "environmental_science": {"name": "环境科学", "icon": "🌿", "subfields": ["生态学", "气候变化", "可持续发展"]},
    "science_technology_society": {"name": "科技与社会", "icon": "🔬", "subfields": ["科技史", "科技伦理", "创新研究"]},
}


@dataclass
class CapsuleTemplate:
    """扩展胶囊模板"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    type: CapsuleTemplateType = CapsuleTemplateType.DISCUSSION_OUTPUT
    domain: str = "general"  # 科学领域
    depth: str = "intermediate"  # 深度: intro/intermediate/advanced
    description: str = ""
    
    # 字段定义
    fields: List[Dict] = field(default_factory=list)
    
    # 示例
    example: Dict = field(default_factory=dict)
    
    # 元数据
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "domain": self.domain,
            "depth": self.depth,
            "description": self.description,
            "fields": self.fields,
            "example": self.example,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat()
        }


class ExtendedTemplateManager:
    """
    扩展模板管理器
    
    特性:
    - 覆盖全面科学领域 (40+ 子领域)
    - 多层次深度 (入门/进阶/深入)
    - 跨学科交叉模板
    - 领域特定的字段定义
    """
    
    def __init__(self):
        self.templates: Dict[str, CapsuleTemplate] = {}
        self._init_comprehensive_presets()
        logger.info("扩展模板管理器初始化完成")
    
    def _init_comprehensive_presets(self):
        """初始化全面预设模板"""
        
        # ==================== 自然科学模板 ====================
        
        # 物理学模板
        for domain, info in SCIENTIFIC_DOMAINS.items():
            if domain in ["physics", "mathematics", "chemistry", "biology"]:
                # 入门级
                self.templates[f"{domain}_intro"] = CapsuleTemplate(
                    name=f"{info['name']}入门",
                    type=CapsuleTemplateType.INTRODUCTION,
                    domain=domain,
                    depth="introduction",
                    description=f"帮助理解{info['name']}的基本概念和核心原理",
                    fields=[
                        {"name": "concept", "label": "核心概念", "type": "text", "required": True},
                        {"name": "basic_principle", "label": "基本原理", "type": "text", "required": True},
                        {"name": "simple_example", "label": "简单示例", "type": "text", "required": True},
                        {"name": "key_formula", "label": "关键公式", "type": "text", "required": False},
                        {"name": "application", "label": "实际应用", "type": "text", "required": False}
                    ],
                    example={
                        "concept": "牛顿第一定律",
                        "basic_principle": "物体保持静止或匀速直线运动状态，直到外力迫使它改变运动状态为止",
                        "simple_example": "冰面上滑行的冰球，在摩擦力作用下最终停止",
                        "key_formula": "F=ma",
                        "application": "汽车刹车设计、航天器轨道计算"
                    }
                )
                
                # 深入级
                self.templates[f"{domain}_advanced"] = CapsuleTemplate(
                    name=f"{info['name']}深入",
                    type=CapsuleTemplateType.ADVANCED,
                    domain=domain,
                    depth="advanced",
                    description=f"{info['name']}的高级专题研究",
                    fields=[
                        {"name": "research_question", "label": "研究问题", "type": "text", "required": True},
                        {"name": "theoretical_framework", "label": "理论框架", "type": "text", "required": True},
                        {"name": "methodology", "label": "研究方法", "type": "text", "required": True},
                        {"name": "key_findings", "label": "关键发现", "type": "list", "required": True},
                        {"name": "limitations", "label": "局限性", "type": "text", "required": False},
                        {"name": "future_directions", "label": "未来方向", "type": "text", "required": False}
                    ],
                    example={
                        "research_question": "量子纠缠的宏观显现条件",
                        "theoretical_framework": "量子力学多世界解释",
                        "methodology": "低温超导实验+理论模拟",
                        "key_findings": [
                            "量子纠缠在宏观尺度的维持条件",
                            "退相干时间的延长方法"
                        ],
                        "limitations": "实验条件苛刻",
                        "future_directions": "室温超导相关的量子态维持"
                    }
                )
        
        # ==================== 社会科学模板 ====================
        
        for domain, info in SCIENTIFIC_DOMAINS.items():
            if domain in ["economics", "psychology", "sociology"]:
                self.templates[f"{domain}_analysis"] = CapsuleTemplate(
                    name=f"{info['name']}分析",
                    type=CapsuleTemplateType.CASE_STUDY,
                    domain=domain,
                    depth="intermediate",
                    description=f"运用{info['name']}视角分析社会现象",
                    fields=[
                        {"name": "phenomenon", "label": "社会现象", "type": "text", "required": True},
                        {"name": "theoretical_lens", "label": "理论视角", "type": "text", "required": True},
                        {"name": "analysis", "label": "分析过程", "type": "text", "required": True},
                        {"name": "implications", "label": "社会影响", "type": "text", "required": True},
                        {"name": "policy_suggestion", "label": "政策建议", "type": "text", "required": False}
                    ],
                    example={
                        "phenomenon": "数字鸿沟",
                        "theoretical_lens": "社会分层理论+技术采纳模型",
                        "analysis": "社会经济地位影响数字技术获取和使用",
                        "implications": "教育不平等加剧、劳动力市场分化",
                        "policy_suggestion": "数字基础设施普惠政策"
                    }
                )
        
        # ==================== 交叉科学模板 ====================
        
        # 认知科学模板
        self.templates["cognitive_science_synthesis"] = CapsuleTemplate(
            name="认知科学综合",
            type=CapsuleTemplateType.INTERDISCIPLINARY,
            domain="cognitive_science",
            depth="advanced",
            description="整合神经科学、心理学和AI的跨学科研究",
            fields=[
                {"name": "cognitive_question", "label": "认知问题", "type": "text", "required": True},
                {"name": "neuroscience_insight", "label": "神经科学视角", "type": "text", "required": True},
                {"name": "psychology_insight", "label": "心理学视角", "type": "text", "required": True},
                {"name": "ai_insight", "label": "AI视角", "type": "text", "required": True},
                {"name": "unified_model", "label": "整合模型", "type": "text", "required": True},
                {"name": "research_gaps", "label": "研究空白", "type": "text", "required": False}
            ],
            example={
                "cognitive_question": "意识是如何从神经活动中产生的？",
                "neuroscience_insight": "神经元集群的同步活动模式",
                "psychology_insight": "主观体验的现象学描述",
                "ai_insight": "整合信息理论(IIT)的计算模型",
                "unified_model": "全局工作空间理论的神经实现",
                "research_gaps": "缺乏意识测量的客观指标"
            }
        )
        
        # 复杂系统模板
        self.templates["complex_systems_analysis"] = CapsuleTemplate(
            name="复杂系统分析",
            type=CapsuleTemplateType.INTERDISCIPLINARY,
            domain="complex_systems",
            depth="advanced",
            description="分析跨学科的复杂系统现象",
            fields=[
                {"name": "system_description", "label": "系统描述", "type": "text", "required": True},
                {"name": "components", "label": "组成部分", "type": "list", "required": True},
                {"name": "interactions", "label": "相互作用", "type": "text", "required": True},
                {"name": "emergent_properties", "label": "涌现性质", "type": "list", "required": True},
                {"name": "nonlinear_dynamics", "label": "非线性动力学", "type": "text", "required": True},
                {"name": "prediction", "label": "预测与控制", "type": "text", "required": True}
            ],
            example={
                "system_description": "城市交通系统",
                "components": ["道路网络", "车辆", "交通信号", "驾驶员行为"],
                "interactions": "交通流量影响出行决策，出行决策反过来影响交通流量",
                "emergent_properties": ["交通拥堵涌现", "出行模式自组织"],
                "nonlinear_dynamics": "交通流量存在相变临界点",
                "prediction": "基于实时数据的交通预测和信号优化"
            }
        )
        
        # 环境科学模板
        self.templates["environmental_assessment"] = CapsuleTemplate(
            name="环境评估",
            type=CapsuleTemplateType.INTERDISCIPLINARY,
            domain="environmental_science",
            depth="intermediate",
            description="评估环境问题的多学科视角",
            fields=[
                {"name": "environmental_issue", "label": "环境问题", "type": "text", "required": True},
                {"name": "scientific_analysis", "label": "科学分析", "type": "text", "required": True},
                {"name": "economic_impact", "label": "经济影响", "type": "text", "required": True},
                {"name": "social_implications", "label": "社会影响", "type": "text", "required": True},
                {"name": "policy_options", "label": "政策选项", "type": "list", "required": True},
                {"name": "recommendation", "label": "综合建议", "type": "text", "required": True}
            ],
            example={
                "environmental_issue": "城市空气污染",
                "scientific_analysis": "PM2.5来源解析和扩散模型",
                "economic_impact": "医疗成本增加、生产力损失",
                "social_implications": "健康不平等、公众焦虑",
                "policy_options": ["限行政策", "产业转型", "公共交通优化"],
                "recommendation": "多管齐下的综合治理策略"
            }
        )
        
        # ==================== 通用模板 ====================
        
        # 研究综述模板
        self.templates["research_review"] = CapsuleTemplate(
            name="研究综述",
            type=CapsuleTemplateType.RESEARCH_REVIEW,
            domain="general",
            depth="advanced",
            description="系统梳理某一领域的研究进展",
            fields=[
                {"name": "research_area", "label": "研究领域", "type": "text", "required": True},
                {"name": "historical_development", "label": "历史发展", "type": "text", "required": True},
                {"name": "key_theories", "label": "核心理论", "type": "list", "required": True},
                {"name": "major_findings", "label": "主要发现", "type": "list", "required": True},
                {"name": "controversies", "label": "争议问题", "type": "list", "required": False},
                {"name": "future_directions", "label": "未来方向", "type": "text", "required": True}
            ],
            example={
                "research_area": "人工智能可解释性研究",
                "historical_development": "从规则系统到深度学习",
                "key_theories": ["注意力机制", "梯度可视化", "概念瓶颈模型"],
                "major_findings": [
                    "神经网络存在黑箱问题",
                    "可解释性影响用户信任"
                ],
                "controversies": ["事后解释是否真正反映模型行为"],
                "future_directions": "内在可解释的神经网络架构"
            }
        )
        
        # 专家观点模板
        self.templates["expert_opinion"] = CapsuleTemplate(
            name="专家观点",
            type=CapsuleTemplateType.EXPERT_OPINION,
            domain="general",
            depth="intermediate",
            description="记录专家对特定问题的独到见解",
            fields=[
                {"name": "question", "label": "专家问题", "type": "text", "required": True},
                {"name": "expert_background", "label": "专家背景", "type": "text", "required": True},
                {"name": "key_insight", "label": "核心洞见", "type": "text", "required": True},
                {"name": "reasoning", "label": "推理过程", "type": "text", "required": True},
                {"name": "implications", "label": "启示意义", "type": "text", "required": True},
                {"name": "limitations", "label": "局限性", "type": "text", "required": False}
            ],
            example={
                "question": "AI是否会产生意识？",
                "expert_background": "神经科学家+AI研究者",
                "key_insight": "意识可能是信息整合的产物，AI可以通过增加整合度接近意识状态",
                "reasoning": "整合信息理论(IIT)提供了量化意识的方法",
                "implications": "AI伦理需要考虑准意识主体的权利",
                "limitations": "意识的主观性难以客观测量"
            }
        )
        
        logger.info(f"已初始化 {len(self.templates)} 个扩展模板")
    
    def list_templates(self, domain: str = None, depth: str = None) -> List[Dict]:
        """列出模板 (支持筛选)"""
        templates = list(self.templates.values())
        
        if domain:
            templates = [t for t in templates if t.domain == domain]
        
        if depth:
            templates = [t for t in templates if t.depth == depth]
        
        return [t.to_dict() for t in templates]
    
    def get_template(self, template_id: str) -> Optional[CapsuleTemplate]:
        """获取模板"""
        return self.templates.get(template_id)
    
    def list_domains(self) -> List[Dict]:
        """列出所有科学领域"""
        return [
            {"id": k, **v} for k, v in SCIENTIFIC_DOMAINS.items()
        ]
    
    def apply_template(
        self,
        template_id: str,
        data: Dict,
        participants: List[str] = None
    ) -> Dict:
        """应用模板生成胶囊数据"""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"模板不存在: {template_id}")
        
        template.usage_count += 1
        
        # 构建胶囊数据
        capsule_data = {
            "title": data.get("title", f"关于「{data.get('topic', data.get('concept', '未知主题'))}」的知识胶囊"),
            "insight": data.get("key_insight", data.get("insight", data.get("consensus", ""))),
            "summary": self._generate_summary(data),
            "evidence": self._extract_evidence(data, template),
            "action_items": self._extract_actions(data, template),
            "questions": data.get("questions", data.get("controversies", [])),
            "source_agents": participants or [],
            "keywords": self._extract_keywords(data, template),
            "category": template.domain,
            "template_type": template.type.value,
            "template_depth": template.depth
        }
        
        # 估算评分
        from .capsule import CapsuleDimension
        dimensions = CapsuleDimension(
            truth_score=self._calculate_truth_score(data, template),
            goodness_score=self._calculate_goodness_score(data, template),
            beauty_score=60 + len(capsule_data["evidence"]) * 5,
            intelligence_score=70 + len(capsule_data["action_items"]) * 5
        )
        
        capsule_data["dimensions"] = dimensions.to_dict()
        capsule_data["quality_score"] = dimensions.total_score * 0.7
        capsule_data["grade"] = "A" if dimensions.total_score >= 80 else "B" if dimensions.total_score >= 60 else "C"
        
        return capsule_data
    
    def _generate_summary(self, data: Dict) -> str:
        """生成摘要"""
        key_points = []
        for key in ["concept", "research_question", "phenomenon", "question"]:
            if key in data and data[key]:
                key_points.append(data[key][:50])
        return " ".join(key_points)[:100]
    
    def _extract_evidence(self, data: Dict, template: CapsuleTemplate) -> List[str]:
        """提取证据"""
        evidence = []
        for field_def in template.fields:
            if field_def["type"] == "list" and field_def["name"] in data:
                evidence.extend(data[field_def["name"]])
        return evidence[:5]
    
    def _extract_actions(self, data: Dict, template: CapsuleTemplate) -> List[str]:
        """提取行动建议"""
        actions = []
        for key in ["recommendation", "policy_options", "future_directions"]:
            if key in data:
                if isinstance(data[key], list):
                    actions.extend(data[key])
                else:
                    actions.append(data[key])
        return [a for a in actions if isinstance(a, str)][:5]
    
    def _extract_keywords(self, data: Dict, template: CapsuleTemplate) -> List[str]:
        """提取关键词"""
        keywords = []
        for key in ["concept", "research_area", "domain"]:
            if key in data:
                keywords.append(data[key])
        return keywords[:10]
    
    def _calculate_truth_score(self, data: Dict, template: CapsuleTemplate) -> int:
        """计算 Truth 评分"""
        score = 50
        # 基于字段完整性
        filled = sum(1 for f in template.fields if f.get("required") and f["name"] in data)
        score += filled * 5
        return min(100, score)
    
    def _calculate_goodness_score(self, data: Dict, template: CapsuleTemplate) -> int:
        """计算 Goodness 评分"""
        score = 50
        # 基于是否有影响分析
        for key in ["implications", "policy_suggestion", "social_implications"]:
            if key in data:
                score += 10
                break
        return min(100, score)


# 全局实例
extended_template_manager = ExtendedTemplateManager()
