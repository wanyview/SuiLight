"""
SuiLight Knowledge Salon - 知识胶囊系统
知识沙龙的最终产出物

核心概念:
- 知识胶囊 = 讨论的精华产出
- 评价标准 = 胶囊质量
- 平衡机制 = 过程 vs 成果
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CapsuleStatus(Enum):
    """胶囊状态"""
    DRAFT = "draft"           # 草稿
    REVIEW = "review"         # 评审中
    APPROVED = "approved"      # 通过
    REJECTED = "rejected"      # 拒绝


@dataclass
class CapsuleDimension:
    """胶囊维度评分"""
    truth_score: int = 0       # 科学性 (0-100)
    goodness_score: int = 0    # 社科性 (0-100)
    beauty_score: int = 0      # 人文性 (0-100)
    intelligence_score: int = 0  # 创新性 (0-100)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def total_score(self) -> float:
        return (self.truth_score + self.goodness_score + 
                self.beauty_score + self.intelligence_score) / 4


@dataclass
class KnowledgeCapsule:
    """
    知识胶囊
    
    知识沙龙的最终产出物，包含:
    - 核心洞见 (insight)
    - 支撑证据 (evidence)
    - 行动建议 (action_items)
    - 多维评价 (DATM)
    """
    
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic_id: str = ""                    # 来源讨论 ID
    title: str = ""                       # 胶囊标题
    summary: str = ""                     # 简短摘要 (100字内)
    
    # 核心内容
    insight: str = ""                     # 核心洞见
    evidence: List[str] = field(default_factory=list)  # 支撑证据
    action_items: List[str] = field(default_factory=list)  # 行动建议
    questions: List[str] = field(default_factory=list)     # 开放问题
    
    # 维度评分
    dimensions: CapsuleDimension = field(default_factory=CapsuleDimension)
    
    # 元数据
    source_agents: List[str] = field(default_factory=list)  # 参与的 Agent
    keywords: List[str] = field(default_factory=list)       # 关键词
    category: str = ""                                      # 分类
    
    # 状态
    status: CapsuleStatus = CapsuleStatus.DRAFT
    confidence: float = 0.0        # 置信度 (0-1)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "title": self.title,
            "summary": self.summary,
            "insight": self.insight,
            "evidence": self.evidence,
            "action_items": self.action_items,
            "questions": self.questions,
            "dimensions": self.dimensions.to_dict(),
            "total_score": self.dimensions.total_score,
            "source_agents": self.source_agents,
            "keywords": self.keywords,
            "category": self.category,
            "status": self.status.value,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @property
    def quality_score(self) -> float:
        """综合质量分数 = 维度分数 × 置信度"""
        return self.dimensions.total_score * self.confidence


class CapsuleGenerator:
    """
    知识胶囊生成器
    
    从讨论内容中提取和生成知识胶囊
    """
    
    def __init__(self):
        logger.info("胶囊生成器初始化完成")
    
    def generate_from_discussion(
        self,
        topic_title: str,
        topic_description: str,
        contributions: List[Dict],
        participants: List[str]
    ) -> KnowledgeCapsule:
        """
        从讨论生成胶囊
        
        Args:
            topic_title: 讨论标题
            topic_description: 讨论描述
            contributions: 贡献列表 (每条包含 agent_name, content)
            participants: 参与者列表
            
        Returns:
            KnowledgeCapsule 实例
        """
        capsule = KnowledgeCapsule(
            topic_id=topic_title[:8],
            title=f"关于「{topic_title}」的知识胶囊",
            summary=self._generate_summary(topic_description, contributions)
        )
        
        # 提取核心洞见
        capsule.insight = self._extract_insight(contributions)
        
        # 提取支撑证据
        capsule.evidence = self._extract_evidence(contributions)
        
        # 提取行动建议
        capsule.action_items = self._extract_actions(contributions)
        
        # 提取开放问题
        capsule.questions = self._extract_questions(contributions)
        
        # 计算维度评分
        capsule.dimensions = self._calculate_dimensions(contributions)
        
        # 设置元数据
        capsule.source_agents = list(set(participants))
        capsule.keywords = self._extract_keywords(contributions)
        capsule.category = self._infer_category(topic_title, topic_description)
        
        # 计算置信度
        capsule.confidence = self._calculate_confidence(
            len(contributions), 
            len(participants),
            capsule.dimensions.total_score
        )
        
        logger.info(f"生成知识胶囊: {capsule.id}, 质量分数: {capsule.quality_score:.1f}")
        
        return capsule
    
    def _generate_summary(self, description: str, contributions: List[Dict]) -> str:
        """生成摘要"""
        # 简单提取前 3 条贡献的核心内容
        key_points = []
        for c in contributions[:3]:
            content = c.get("content", "")[:100]
            if content:
                key_points.append(content)
        
        summary = " ".join(key_points)
        return summary[:100] + "..." if len(summary) > 100 else summary
    
    def _extract_insight(self, contributions: List[Dict]) -> str:
        """提取核心洞见"""
        insights = []
        
        for c in contributions:
            content = c.get("content", "")
            # 寻找包含洞见关键词的句子
            if any(kw in content for kw in ["关键", "核心", "重要", "发现", "结论"]):
                insights.append(content[:200])
        
        if insights:
            # 返回最长的一个
            return max(insights, key=len)[:500]
        
        # 如果没有明确洞见，提取第一条
        if contributions:
            return contributions[0].get("content", "")[:500]
        
        return "暂无明确洞见"
    
    def _extract_evidence(self, contributions: List[Dict]) -> List[str]:
        """提取支撑证据"""
        evidence = []
        
        for c in contributions:
            content = c.get("content", "")
            # 寻找包含证据/数据关键词的句子
            if any(kw in content for kw in ["因为", "由于", "根据", "数据", "研究", "显示"]):
                evidence.append(content[:150])
        
        return evidence[:5]  # 最多 5 条
    
    def _extract_actions(self, contributions: List[Dict]) -> List[str]:
        """提取行动建议"""
        actions = []
        
        for c in contributions:
            content = c.get("content", "")
            # 寻找包含行动关键词的句子
            if any(kw in content for kw in ["应该", "需要", "建议", "可以", "尝试"]):
                actions.append(content[:150])
        
        return actions[:5]  # 最多 5 条
    
    def _extract_questions(self, contributions: List[Dict]) -> List[str]:
        """提取开放问题"""
        questions = []
        
        for c in contributions:
            content = c.get("content", "")
            # 寻找问号或疑问词
            if "?" in content or any(kw in content for kw in ["是否", "能否", "为什么", "如何"]):
                questions.append(content[:150])
        
        return questions[:5]  # 最多 5 条
    
    def _calculate_dimensions(self, contributions: List[Dict]) -> CapsuleDimension:
        """计算维度评分"""
        dimension = CapsuleDimension()
        
        # 简单统计各类关键词出现频率
        truth_count = 0    # 科学性关键词
        goodness_count = 0  # 社科性关键词
        beauty_count = 0    # 人文性关键词
        intelligence_count = 0  # 创新性关键词
        
        truth_kws = ["科学", "数据", "研究", "实验", "证明", "客观"]
        goodness_kws = ["伦理", "价值", "社会", "公平", "责任", "应该"]
        beauty_kws = ["美", "艺术", "文化", "情感", "表达", "体验"]
        intelligence_kws = ["创新", "突破", "新", "变革", "未来", "可能"]
        
        total = len(contributions) or 1
        
        for c in contributions:
            content = c.get("content", "")
            truth_count += sum(1 for kw in truth_kws if kw in content)
            goodness_count += sum(1 for kw in goodness_kws if kw in content)
            beauty_count += sum(1 for kw in beauty_kws if kw in content)
            intelligence_count += sum(1 for kw in intelligence_kws if kw in content)
        
        # 归一化到 0-100
        dimension.truth_score = min(100, int(truth_count / total * 100))
        dimension.goodness_score = min(100, int(goodness_count / total * 100))
        dimension.beauty_score = min(100, int(beauty_count / total * 100))
        dimension.intelligence_score = min(100, int(intelligence_count / total * 100))
        
        return dimension
    
    def _extract_keywords(self, contributions: List[Dict]) -> List[str]:
        """提取关键词"""
        keywords = []
        
        for c in contributions:
            content = c.get("content", "")
            # 简单提取高频词 (这里简化处理)
            words = content.split()[:5]
            for word in words:
                if len(word) > 2 and word not in keywords:
                    keywords.append(word)
        
        return keywords[:10]
    
    def _infer_category(self, title: str, description: str) -> str:
        """推断分类"""
        text = (title + " " + description).lower()
        
        categories = {
            "自然科学": ["物理", "化学", "生物", "数学", "科学", "自然"],
            "社会科学": ["经济", "社会", "心理", "政治", "管理"],
            "人文科学": ["哲学", "艺术", "文化", "历史", "文学"],
            "交叉科学": ["技术", "工程", "医学", "AI", "人工智能"]
        }
        
        for category, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return category
        
        return "交叉科学"
    
    def _calculate_confidence(
        self, 
        contribution_count: int, 
        participant_count: int,
        dimension_score: float
    ) -> float:
        """计算置信度"""
        # 基于参与度和维度评分计算
        participation_factor = min(1.0, (contribution_count / 10) * 0.5 + 
                                   (participant_count / 5) * 0.3)
        score_factor = dimension_score / 100
        
        confidence = participation_factor * 0.6 + score_factor * 0.4
        return round(min(1.0, confidence), 2)


class CapsuleEvaluator:
    """
    胶囊评价器
    
    评价知识胶囊的质量
    """
    
    # 评价标准
    QUALITY_THRESHOLDS = {
        "excellent": 80,   # 优秀 >= 80
        "good": 60,        # 良好 >= 60
        "fair": 40,        # 一般 >= 40
        "poor": 0          # 较差 < 40
    }
    
    def evaluate(self, capsule: KnowledgeCapsule) -> Dict:
        """
        评价胶囊
        
        Returns:
            评价结果
        """
        quality = capsule.quality_score
        dimensions = capsule.dimensions
        
        # 确定等级
        if quality >= self.QUALITY_THRESHOLDS["excellent"]:
            grade = "A"
            level = "优秀"
        elif quality >= self.QUALITY_THRESHOLDS["good"]:
            grade = "B"
            level = "良好"
        elif quality >= self.QUALITY_THRESHOLDS["fair"]:
            grade = "C"
            level = "一般"
        else:
            grade = "D"
            level = "待改进"
        
        # 改进建议
        suggestions = []
        if dimensions.truth_score < 60:
            suggestions.append("建议增加科学性支撑，增加数据和证据")
        if dimensions.goodness_score < 60:
            suggestions.append("建议增加价值判断和伦理考量")
        if dimensions.beauty_score < 60:
            suggestions.append("建议提升表达的感染力和美学价值")
        if dimensions.intelligence_score < 60:
            suggestions.append("建议增加创新性思考和前瞻性观点")
        if capsule.confidence < 0.6:
            suggestions.append("建议邀请更多专家参与讨论")
        
        return {
            "capsule_id": capsule.id,
            "quality_score": round(quality, 1),
            "grade": grade,
            "level": level,
            "dimensions": {
                "truth": dimensions.truth_score,
                "goodness": dimensions.goodness_score,
                "beauty": dimensions.beauty_score,
                "intelligence": dimensions.intelligence_score,
                "average": dimensions.total_score
            },
            "confidence": capsule.confidence,
            "suggestions": suggestions,
            "is_publishable": quality >= self.QUALITY_THRESHOLDS["good"]
        }


# 示例：生成一个知识胶囊
def demo():
    """演示"""
    generator = CapsuleGenerator()
    evaluator = CapsuleEvaluator()
    
    # 模拟讨论内容
    contributions = [
        {
            "agent_name": "爱迪生",
            "content": "我认为解决这个问题的关键是系统性试错。我们需要尝试多种方案，然后根据结果筛选。"
        },
        {
            "agent_name": "爱因斯坦", 
            "content": "但我认为更重要的是理论指导。没有正确的理论框架，尝试再多也是徒劳的。"
        },
        {
            "agent_name": "特斯拉",
            "content": "我同意爱迪生的观点，实践出真知。同时也要注意效率，不能盲目试错。"
        }
    ]
    
    participants = ["爱迪生", "爱因斯坦", "特斯拉"]
    
    # 生成胶囊
    capsule = generator.generate_from_discussion(
        topic_title="如何有效解决复杂问题？",
        topic_description="探讨解决复杂问题的方法论",
        contributions=contributions,
        participants=participants
    )
    
    print("=" * 60)
    print("📦 知识胶囊示例")
    print("=" * 60)
    print(f"标题: {capsule.title}")
    print(f"摘要: {capsule.summary}")
    print(f"\n核心洞见:")
    print(f"  {capsule.insight}")
    print(f"\n支撑证据 ({len(capsule.evidence)}条):")
    for e in capsule.evidence:
        print(f"  - {e}")
    print(f"\n行动建议 ({len(capsule.action_items)}条):")
    for a in capsule.action_items:
        print(f"  - {a}")
    print(f"\n维度评分:")
    print(f"  Truth (真): {capsule.dimensions.truth_score}")
    print(f"  Goodness (善): {capsule.dimensions.goodness_score}")
    print(f"  Beauty (美): {capsule.dimensions.beauty_score}")
    print(f"  Intelligence (灵): {capsule.dimensions.intelligence_score}")
    print(f"  综合分数: {capsule.dimensions.total_score:.1f}")
    print(f"置信度: {capsule.confidence:.0%}")
    print(f"质量分数: {capsule.quality_score:.1f}")
    
    # 评价
    print("\n" + "=" * 60)
    print("📊 评价结果")
    print("=" * 60)
    evaluation = evaluator.evaluate(capsule)
    print(f"等级: {evaluation['grade']} ({evaluation['level']})")
    print(f"质量分数: {evaluation['quality_score']:.1f}")
    print(f"可发布: {'✅ 是' if evaluation['is_publishable'] else '❌ 否'}")
    if evaluation['suggestions']:
        print("改进建议:")
        for s in evaluation['suggestions']:
            print(f"  - {s}")


if __name__ == "__main__":
    demo()
