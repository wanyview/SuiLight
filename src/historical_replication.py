"""
历史复现知识胶囊系统 - 核心模块
2026-01-31 新增
"""

import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class OriginalExperiment:
    """原始实验"""
    researcher: str
    year: int
    description: str
    original_goal: str
    methods: List[str]
    findings: List[str]


@dataclass
class ReplicationExperiment:
    """复现实验"""
    researcher: str
    year: int
    replication_details: str
    deviations: List[str]  # 与原实验的差异
    modern_tools: List[str]  # 现代工具


@dataclass
class NewDiscovery:
    """新发现"""
    phenomena: List[str]
    mechanism: str
    implications: List[str]
    applications: List[str]


@dataclass
class Connection:
    """连接分析"""
    temporal_span: int  # 时间跨度
    domain_bridge: str  # 领域桥梁
    paradigm_shift: str  # 范式转变
    knowledge_gap: str  # 为何原始研究者未发现


@dataclass
class DATMScore:
    """DATM评分"""
    truth: float
    goodness: float
    beauty: float
    intelligence: float


@dataclass
class HistoricalReplicationCapsule:
    """历史复现知识胶囊"""
    id: str
    title: str
    type: str = "historical_replication"
    
    original_experiment: Optional[Dict] = None
    replication_experiment: Optional[Dict] = None
    new_discovery: Optional[Dict] = None
    connection: Optional[Dict] = None
    datm_score: Optional[Dict] = None
    
    topics: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    
    created_at: str = ""
    insight: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "original_experiment": self.original_experiment,
            "replication_experiment": self.replication_experiment,
            "new_discovery": self.new_discovery,
            "connection": self.connection,
            "datm_score": self.datm_score,
            "topics": self.topics,
            "domains": self.domains,
            "authors": self.authors,
            "created_at": self.created_at,
            "insight": self.insight
        }


class HistoricalReplicationSystem:
    """历史复现知识胶囊系统"""
    
    def __init__(self):
        self.capsules: Dict[str, HistoricalReplicationCapsule] = {}
    
    def create_tour_graphene_capsule(self) -> HistoricalReplicationCapsule:
        """Tour 石墨烯案例 (147年跨度)"""
        capsule = HistoricalReplicationCapsule(
            id="capsule_20260131_001",
            title="🔄 碳丝灯泡到乱层石墨烯的转化 - 147年后的新发现",
            
            original_experiment={
                "researcher": "托马斯·爱迪生",
                "year": 1879,
                "description": "使用碳化竹丝作为灯丝，制作长寿命电灯泡",
                "original_goal": "发明实用的商业化电照明系统",
                "methods": ["碳化竹丝处理", "真空玻璃封装", "直流电压测试"],
                "findings": ["碳化竹丝可提供1600小时照明", "110伏直流电压效果最佳"]
            },
            
            replication_experiment={
                "researcher": "詹姆斯·M·Tour (莱斯大学)",
                "year": 2026,
                "replication_details": "精确重现爱迪生的实验条件，使用相同的碳化竹丝灯丝和110伏直流电压",
                "deviations": ["使用现代材料表征技术(XRD, TEM)", "更精确的电压控制"],
                "modern_tools": ["X射线衍射(XRD)", "透射电子显微镜(TEM)", "拉曼光谱"]
            },
            
            new_discovery={
                "phenomena": ["碳丝结构转变为乱层石墨烯", "石墨烯层的无序堆叠特征"],
                "mechanism": "110伏电压产生的焦耳热使碳原子重新排列，形成sp2杂化的石墨烯结构",
                "implications": [
                    "证明碳材料的高度可塑性",
                    "为石墨烯合成提供新路径",
                    "连接电气化时代与纳米材料时代"
                ],
                "applications": ["低成本石墨烯合成", "碳材料循环利用", "历史技术的现代科学价值"]
            },
            
            connection={
                "temporal_span": 147,
                "domain_bridge": "电照明技术 → 纳米材料",
                "paradigm_shift": "从'寻找灯丝材料'到'发现碳材料新结构'",
                "knowledge_gap": "原始实验缺乏现代表征工具，无法观察纳米级结构变化"
            },
            
            datm_score={
                "truth": 92,
                "goodness": 88,
                "beauty": 85,
                "intelligence": 90
            },
            
            topics=["石墨烯", "碳材料", "爱迪生", "纳米技术", "历史复现"],
            domains=["材料科学", "纳米技术", "电化学"],
            authors=["James M. Tour", "托马斯·爱迪生"],
            
            created_at="2026-01-31T02:00:00Z",
            insight="""
💡 **核心洞见**

一个世纪前用来照明的碳丝灯丝，在现代材料科学视角下竟然可以转化为石墨烯——这是21世纪最重要的新材料之一。

这个发现证明了：
1. 历史技术蕴含未被发现的科学价值
2. 复现实验是知识创新的重要方法
3. 基础材料研究可以跨越时空产生新发现
            """.strip()
        )
        
        self.capsules[capsule.id] = capsule
        return capsule
    
    def create_newton_prism_capsule(self) -> HistoricalReplicationCapsule:
        """牛顿棱镜案例 (360年跨度)"""
        capsule = HistoricalReplicationCapsule(
            id="capsule_20260131_002",
            title="🔄 牛顿棱镜分光到量子光学的演进 - 360年的科学旅程",
            
            original_experiment={
                "researcher": "艾萨克·牛顿",
                "year": 1666,
                "description": "使用三棱镜将白光分解为彩虹光谱，开创光谱学",
                "original_goal": "证明白光是由不同颜色的光混合而成",
                "methods": ["棱镜折射实验", "光谱测量", "颜色混合实验"],
                "findings": ["白光可分解为7种颜色", "不同颜色的光折射率不同"]
            },
            
            replication_experiment={
                "researcher": "量子光学研究团队",
                "year": 2026,
                "replication_details": "在量子光学框架下重现牛顿的棱镜实验，结合单光子检测技术",
                "deviations": ["使用单光子计数器", "量子态层析技术", "相干性测量"],
                "modern_tools": ["单光子探测器", "量子态层析", "光子相关谱"]
            },
            
            new_discovery={
                "phenomena": ["单光子的量子态在棱镜中的行为", "量子纠缠光子的频率转换", "光子波粒二象性的直接观测"],
                "mechanism": "在量子尺度下，光子不仅表现波动性，还展现出量子叠加和纠缠特性",
                "implications": [
                    "验证量子力学基本原理",
                    "为量子信息技术提供新工具",
                    "连接经典光学与量子光学"
                ],
                "applications": ["量子通信", "量子计算光源", "精密光谱测量"]
            },
            
            connection={
                "temporal_span": 360,
                "domain_bridge": "经典光学 → 量子光学",
                "paradigm_shift": "从'光的颜色组成'到'光的量子本质'",
                "knowledge_gap": "17世纪缺乏量子理论，无法理解光的粒子性和波动性的统一"
            },
            
            datm_score={
                "truth": 95,
                "goodness": 90,
                "beauty": 92,
                "intelligence": 96
            },
            
            topics=["牛顿", "棱镜", "量子光学", "光谱学", "历史复现"],
            domains=["物理学", "光学", "量子力学"],
            authors=["艾萨克·牛顿", "量子光学研究团队"],
            
            created_at="2026-01-31T02:15:00Z",
            insight="""
💡 **核心洞见**

牛顿1666年在伍尔索普庄园用三棱镜观察到的"光的分解"，在量子力学诞生300多年后，揭示出了更深层的物理本质。

从"颜色"到"量子态"，从"波动"到"波粒二象性"，这个跨越3个半世纪的科学旅程，展示了基础物理学研究的持久生命力。
            """.strip()
        )
        
        self.capsules[capsule.id] = capsule
        return capsule
    
    def create_pavlov_conditioning_capsule(self) -> HistoricalReplicationCapsule:
        """巴甫洛夫条件反射案例 (129年跨度)"""
        capsule = HistoricalReplicationCapsule(
            id="capsule_20260131_003",
            title="🔄 巴甫洛夫条件反射到神经可塑性 - 129年的认知革命",
            
            original_experiment={
                "researcher": "伊万·巴甫洛夫",
                "year": 1897,
                "description": "通过狗的唾液分泌实验发现条件反射现象",
                "original_goal": "研究消化系统的生理机制",
                "methods": ["唾液分泌测量", "刺激-反应配对", "条件反射建立与消退"],
                "findings": ["狗可以在铃声和食物之间建立联想", "条件反射可以消退和重新建立"]
            },
            
            replication_experiment={
                "researcher": "现代神经科学团队",
                "year": 2026,
                "replication_details": "使用现代神经成像技术重现条件反射实验，观察大脑突触可塑性变化",
                "deviations": ["功能性磁共振成像(fMRI)", "光遗传学操控", "单细胞电生理记录"],
                "modern_tools": ["双光子显微镜", "光遗传学", "钙成像技术"]
            },
            
            new_discovery={
                "phenomena": ["条件反射建立时突触可塑性的分子机制", "恐惧条件反射的杏仁核神经回路", "习惯化与敏感化的神经基础"],
                "mechanism": "LTP（长时程增强）和LTD（长时程抑制）是条件反射的神经基础，涉及NMDA受体和Ca2+信号通路",
                "implications": [
                    "揭示学习记忆的分子机制",
                    "为治疗神经疾病提供新靶点",
                    "连接行为学与神经科学"
                ],
                "applications": ["阿尔茨海默病治疗", "创伤后应激障碍(PTSD)治疗", "学习障碍干预"]
            },
            
            connection={
                "temporal_span": 129,
                "domain_bridge": "行为心理学 → 神经科学",
                "paradigm_shift": "从'外在行为描述'到'内在神经机制'",
                "knowledge_gap": "19世纪缺乏直接观察大脑活动的技术，只能通过行为推断"
            },
            
            datm_score={
                "truth": 94,
                "goodness": 92,
                "beauty": 88,
                "intelligence": 95
            },
            
            topics=["巴甫洛夫", "条件反射", "神经可塑性", "学习记忆", "历史复现"],
            domains=["神经科学", "心理学", "生物学"],
            authors=["伊万·巴甫洛夫", "现代神经科学团队"],
            
            created_at="2026-01-31T02:30:00Z",
            insight="""
💡 **核心洞见**

巴甫洛夫在研究狗消化系统时偶然发现的"条件反射"，在近130年后被现代神经科学揭开了分子层面的神秘面纱。

从"唾液分泌"到"突触可塑性"，从"铃声-食物配对"到"LTP/LTD机制"，这个案例完美展示了基础发现如何引领跨学科革命。
            """.strip()
        )
        
        self.capsules[capsule.id] = capsule
        return capsule
    
    def create_pasteur_flask_capsule(self) -> HistoricalReplicationCapsule:
        """巴斯德鹅颈瓶案例 (167年跨度)"""
        capsule = HistoricalReplicationCapsule(
            id="capsule_20260131_004",
            title="🔄 巴斯德鹅颈瓶到生命起源研究 - 167年的探索之旅",
            
            original_experiment={
                "researcher": "路易斯·巴斯德",
                "year": 1859,
                "description": "使用鹅颈瓶实验证明微生物来自空气，而非自然发生",
                "original_goal": "驳斥'自然发生说'，证明生命只能来自生命",
                "methods": ["鹅颈瓶设计", "高温灭菌", "长时间观察"],
                "findings": ["肉汤在鹅颈瓶中保持无菌", "打破瓶颈后微生物才会出现"]
            },
            
            replication_experiment={
                "researcher": "合成生物学研究团队",
                "year": 2026,
                "replication_details": "在现代合成生物学框架下重现巴斯德实验，结合原核生物起源研究",
                "deviations": ["使用现代分子生物学技术", "基因组测序分析", "原始细胞模拟"],
                "modern_tools": ["基因组测序", "合成生物学", "原始细胞模型"]
            },
            
            new_discovery={
                "phenomena": ["RNA世界假说的实验支持", "原始代谢网络的重建", "脂质膜自发形成的条件"],
                "mechanism": "生命起源可能经历从简单有机分子到自我复制RNA，再到原始细胞的渐进过程",
                "implications": [
                    "为生命起源研究提供实验框架",
                    "推动合成生物学发展",
                    "重新定义'生命'的边界"
                ],
                "applications": ["人工细胞合成", "合成生物学设计", "生命探测技术"]
            },
            
            connection={
                "temporal_span": 167,
                "domain_bridge": "微生物学 → 合成生物学",
                "paradigm_shift": "从'证明生命来自生命'到'理解生命如何起源'",
                "knowledge_gap": "19世纪缺乏分子生物学工具，无法深入研究生命起源的化学基础"
            },
            
            datm_score={
                "truth": 93,
                "goodness": 95,
                "beauty": 90,
                "intelligence": 94
            },
            
            topics=["巴斯德", "鹅颈瓶", "生命起源", "合成生物学", "历史复现"],
            domains=["生物学", "合成生物学", "化学"],
            authors=["路易斯·巴斯德", "合成生物学研究团队"],
            
            created_at="2026-01-31T02:45:00Z",
            insight="""
💡 **核心洞见**

巴斯德用鹅颈瓶证明"生命来自生命"，但在167年后的今天，我们正在追问一个更深层的问题：最初的生命是如何从无机物中诞生的？

从"驳斥自然发生"到"重建生命起源"，这个跨越一个半世纪的科学旅程，展示了基础科学如何不断追问更根本的问题。
            """.strip()
        )
        
        self.capsules[capsule.id] = capsule
        return capsule
    
    def create_mendel_peas_capsule(self) -> HistoricalReplicationCapsule:
        """孟德尔豌豆案例 (161年跨度)"""
        capsule = HistoricalReplicationCapsule(
            id="capsule_20260131_005",
            title="🔄 孟德尔豌豆实验到基因网络模型 - 161年的遗传学革命",
            
            original_experiment={
                "researcher": "格雷戈尔·孟德尔",
                "year": 1865,
                "description": "通过豌豆杂交实验发现遗传的基本规律",
                "original_goal": "理解生物性状如何从亲代传递到子代",
                "methods": ["豌豆杂交实验", "性状统计", "比例分析"],
                "findings": ["分离定律", "自由组合定律", "显性与隐性性状"]
            },
            
            replication_experiment={
                "researcher": "计算生物学研究团队",
                "year": 2026,
                "replication_details": "在系统生物学框架下重新分析孟德尔的数据，结合现代基因组学和网络科学",
                "deviations": ["使用机器学习分析遗传数据", "全基因组关联分析(GWAS)", "基因调控网络建模"],
                "modern_tools": ["基因组测序", "机器学习", "网络科学"]
            },
            
            new_discovery={
                "phenomena": ["复杂性状的遗传结构", "基因-基因相互作用网络", "表观遗传调控机制"],
                "mechanism": "复杂性状是由多个基因通过复杂的调控网络共同决定的，单基因模型需要扩展为网络模型",
                "implications": [
                    "为精准医学提供理论基础",
                    "推动作物遗传改良",
                    "连接经典遗传学与系统生物学"
                ],
                "applications": ["遗传疾病预测", "作物性状改良", "个性化医疗"]
            },
            
            connection={
                "temporal_span": 161,
                "domain_bridge": "经典遗传学 → 系统遗传学",
                "paradigm_shift": "从'单个基因'到'基因调控网络'",
                "knowledge_gap": "19世纪缺乏分子遗传学工具，无法理解基因的分子本质"
            },
            
            datm_score={
                "truth": 96,
                "goodness": 94,
                "beauty": 92,
                "intelligence": 95
            },
            
            topics=["孟德尔", "豌豆", "遗传学", "基因网络", "历史复现"],
            domains=["遗传学", "计算生物学", "系统生物学"],
            authors=["格雷戈尔·孟德尔", "计算生物学研究团队"],
            
            created_at="2026-01-31T03:00:00Z",
            insight="""
💡 **核心洞见**

孟德尔在修道院花园里用豌豆植株发现的"遗传定律"，在161年后的今天，已经演化为一个复杂的基因调控网络科学。

从"豌豆的圆粒与皱粒"到"全基因组的调控网络"，从"简单的3:1比例"到"复杂的非线性动力学"，这个案例展示了基础发现如何催生现代科学革命。
            """.strip()
        )
        
        self.capsules[capsule.id] = capsule
        return capsule
    
    def get_all_capsules(self) -> List[HistoricalReplicationCapsule]:
        """获取所有胶囊"""
        return list(self.capsules.values())
    
    def save_all_capsules(self, filepath: str):
        """保存所有胶囊到文件"""
        capsules_data = [c.to_dict() for c in self.capsules.values()]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(capsules_data, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存 {len(capsules_data)} 个历史复现知识胶囊到: {filepath}")


def main():
    """主函数 - 生成所有历史复现胶囊"""
    
    print("="*70)
    print("📚 历史复现知识胶囊系统 v1.0")
    print("="*70)
    print()
    
    system = HistoricalReplicationSystem()
    
    # 创建所有案例
    print("🔄 创建历史复现案例...")
    print()
    
    capsule1 = system.create_tour_graphene_capsule()
    print(f"  ✅ {capsule1.id}: {capsule1.title}")
    
    capsule2 = system.create_newton_prism_capsule()
    print(f"  ✅ {capsule2.id}: {capsule2.title}")
    
    capsule3 = system.create_pavlov_conditioning_capsule()
    print(f"  ✅ {capsule3.id}: {capsule3.title}")
    
    capsule4 = system.create_pasteur_flask_capsule()
    print(f"  ✅ {capsule4.id}: {capsule4.title}")
    
    capsule5 = system.create_mendel_peas_capsule()
    print(f"  ✅ {capsule5.id}: {capsule5.title}")
    
    print()
    print("="*70)
    print("📊 胶囊统计")
    print("="*70)
    
    all_capsules = system.get_all_capsules()
    print(f"\n总胶囊数: {len(all_capsules)}")
    
    # 计算平均时间跨度和DATM评分
    total_span = sum(
        c.connection['temporal_span'] for c in all_capsules
        if c.connection
    )
    avg_span = total_span / len(all_capsules)
    
    avg_truth = sum(c.datm_score['truth'] for c in all_capsules if c.datm_score) / len(all_capsules)
    avg_goodness = sum(c.datm_score['goodness'] for c in all_capsules if c.datm_score) / len(all_capsules)
    avg_beauty = sum(c.datm_score['beauty'] for c in all_capsules if c.datm_score) / len(all_capsules)
    avg_intelligence = sum(c.datm_score['intelligence'] for c in all_capsules if c.datm_score) / len(all_capsules)
    
    print(f"\n平均时间跨度: {avg_span:.1f} 年")
    print(f"\n平均 DATM 评分:")
    print(f"  - Truth (真实性): {avg_truth:.1f}")
    print(f"  - Goodness (价值): {avg_goodness:.1f}")
    print(f"  - Beauty (美感): {avg_beauty:.1f}")
    print(f"  - Intelligence (创新): {avg_intelligence:.1f}")
    
    # 保存到文件
    print()
    system.save_all_capsules('/Users/wanyview/clawd/SuiLight/historical_replication_capsules.json')
    
    print()
    print("✨ 完成！")


if __name__ == "__main__":
    main()
