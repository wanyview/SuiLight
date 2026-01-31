#!/usr/bin/env python3
"""
模拟跨学科前瞻讨论：AI + 合成生物学 = 下一个生物学革命？
生成知识胶囊并推送到 CapsuleHub
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from src.discussions import (
    discussion_storage, AgentMessage, MessageType,
    DiscussionMilestone, MilestoneType
)
from src.knowledge.capsule import KnowledgeCapsule, CapsuleDimension


# 模拟讨论消息
CROSS_DOMAIN_DISCUSSION = [
    # 第1轮 - 问题定义
    {
        "round": 1,
        "timestamp": "2026-01-30T10:00:00",
        "agent_id": "ai_bio_engineer",
        "agent_role": "moderator",
        "agent_name": "AI生物工程师",
        "content": "各位，2026年的今天，我们正处于生物学革命的门槛。AlphaFold2预测了2亿种蛋白质结构，CRISPR技术日趋成熟，AI正在重新定义生物学。问题不是能否，而是多快和如何引导这场革命。",
        "message_type": "question"
    },
    {
        "round": 1,
        "timestamp": "2026-01-30T10:10:00",
        "agent_id": "synthetic_biologist",
        "agent_role": "expert",
        "agent_name": "合成生物学家",
        "content": "我亲眼见证了变化。去年我们用AI设计了一个全新代谢通路，生产一种抗癌药物前体。过去需要2年，现在只需2个月。但这还不是最激动人心的——最激动的是AI能设计出我们从未想象过的生物系统。",
        "message_type": "insight"
    },
    {
        "round": 1,
        "timestamp": "2026-01-30T10:20:00",
        "agent_id": "bioethicist",
        "agent_role": "critic",
        "agent_name": "生物伦理学家",
        "content": "我必须提出警示。AI设计生物系统的速度远超我们的监管能力。去年某实验室意外释放了AI设计的微型生物反应器，虽然及时控制，但这敲响了警钟。创新与安全必须并行。",
        "message_type": "comment"
    },
    
    # 第2轮 - 技术突破
    {
        "round": 2,
        "timestamp": "2026-01-30T11:00:00",
        "agent_id": "quantum_chemist",
        "agent_role": "expert",
        "agent_name": "量子化学家",
        "content": "让我分享一个突破。我们将量子计算与AI结合，实现了前所未有的分子模拟精度。这不仅帮助设计新药，还能预测AI设计的生物系统的稳定性。这是跨学科协作的典范。",
        "message_type": "insight"
    },
    {
        "round": 2,
        "timestamp": "2026-01-30T11:10:00",
        "agent_id": "systems_biologist",
        "agent_role": "expert",
        "agent_name": "系统生物学家",
        "content": "我关心的是整体性。AI可以优化单个基因或蛋白质，但生物系统的涌现特性来自复杂网络。我们需要从还原论走向系统论，AI+系统生物学是关键。",
        "message_type": "comment"
    },
    {
        "round": 2,
        "timestamp": "2026-01-30T11:20:00",
        "agent_id": "ai_bio_engineer",
        "agent_role": "moderator",
        "agent_name": "AI生物工程师",
        "content": "确实如此。我们最新一代AI不仅能设计单个组件，还能预测整个细胞网络的涌现行为。这是从零件到整车的跨越。",
        "message_type": "synthesis"
    },
    
    # 第3轮 - 伦理与哲学
    {
        "round": 3,
        "timestamp": "2026-01-30T14:00:00",
        "agent_id": "philosopher",
        "agent_role": "critic",
        "agent_name": "科技哲学家",
        "content": "我想追问根本问题。当AI设计的生物系统具有自我复制、进化和学习能力时，它是否还是机器？生命的定义正在被重写，这不仅是科学问题，更是人类自我认知的根本转变。",
        "message_type": "question"
    },
    {
        "round": 3,
        "timestamp": "2026-01-30T14:10:00",
        "agent_id": "bioethicist",
        "agent_role": "critic",
        "agent_name": "生物伦理学家",
        "content": "哲学家说得对。我们需要新的伦理框架：1）AI设计生物系统的边界在哪？2）意外释放的责任归属？3）人造生命的权利问题？这些问题不能留给科学家单独决定。",
        "message_type": "comment"
    },
    {
        "round": 3,
        "timestamp": "2026-01-30T14:20:00",
        "agent_id": "synthetic_biologist",
        "agent_role": "expert",
        "agent_name": "合成生物学家",
        "content": "作为一线研究者，我理解这些担忧。但历史告诉我们，恐惧不应阻止进步。关键是建立开放的讨论平台，让公众参与决策，而不仅仅是专家主导。",
        "message_type": "comment"
    },
    
    # 第4轮 - 未来展望
    {
        "round": 4,
        "timestamp": "2026-01-30T15:00:00",
        "agent_id": "quantum_chemist",
        "agent_role": "expert",
        "agent_name": "量子化学家",
        "content": "让我预测未来：1）2027年：AI设计第一种商业化人工酶；2）2030年：细胞工厂规模化生产稀有材料；3）2035年：个性化生物反应器进入家庭。这不是科幻，是正在发生的现实。",
        "message_type": "synthesis"
    },
    {
        "round": 4,
        "timestamp": "2026-01-30T15:10:00",
        "agent_id": "systems_biologist",
        "agent_role": "expert",
        "agent_name": "系统生物学家",
        "content": "我补充一个关键方向：AI设计的生物系统需要与自然生态兼容。未来的生物工程不是改造自然，而是与自然共生。这需要跨学科的系统思维。",
        "message_type": "insight"
    },
    {
        "round": 4,
        "timestamp": "2026-01-30T15:20:00",
        "agent_id": "ai_bio_engineer",
        "agent_role": "moderator",
        "agent_name": "AI生物工程师",
        "content": "综合来看，AI+合成生物学的革命已经到来。关键是平衡创新与安全，技术与伦理，短期突破与长期可持续性。这是我们这代人的责任。",
        "message_type": "synthesis"
    },
    
    # 第5轮 - 共识与行动
    {
        "round": 5,
        "timestamp": "2026-01-30T16:00:00",
        "agent_id": "philosopher",
        "agent_role": "critic",
        "agent_name": "科技哲学家",
        "content": "虽然道路充满挑战，但我相信人类与AI协作设计生物系统，将开启人类文明的新篇章。这不是取代自然，而是与自然对话。",
        "message_type": "synthesis"
    },
    {
        "round": 5,
        "timestamp": "2026-01-30T16:10:00",
        "agent_id": "bioethicist",
        "agent_role": "critic",
        "agent_name": "生物伦理学家",
        "content": "我虽然保持谨慎，但承认这个领域的潜力。我的建议是建立全球AI-生物安全联盟，确保创新在透明和协作的框架内进行。",
        "message_type": "comment"
    },
    {
        "round": 5,
        "timestamp": "2026-01-30T16:20:00",
        "agent_id": "ai_bio_engineer",
        "agent_role": "moderator",
        "agent_name": "AI生物工程师",
        "content": "感谢各位的深入讨论。我们的共识是AI+合成生物学将带来革命性变革，但需要跨学科协作、伦理框架和国际监管。这是人类与AI共同书写的未来。",
        "message_type": "synthesis"
    }
]


def run_discussion(topic_id: str) -> str:
    print("步骤 1: 创建讨论记录...")
    
    record = discussion_storage.create_discussion(topic_id)
    print(f"讨论 ID: {record.id}")
    
    print("步骤 2: 添加讨论消息...")
    for msg_data in CROSS_DOMAIN_DISCUSSION:
        record = discussion_storage.add_message(record.id, msg_data)
        agent = msg_data["agent_name"]
        print(f"   [{msg_data['round']}轮] {agent}: {msg_data['content'][:40]}...")
    
    print("步骤 3: 添加里程碑...")
    milestones = [
        {
            "timestamp": "2026-01-30T10:10:00",
            "milestone_type": "insight",
            "description": "AI设计生物系统的速度突破：从2年到2个月",
            "related_rounds": [1],
            "key_participants": ["合成生物学家"]
        },
        {
            "timestamp": "2026-01-30T14:00:00",
            "milestone_type": "divergence",
            "description": "哲学追问：AI设计的生物系统是否改变了生命的定义",
            "related_rounds": [3],
            "key_participants": ["科技哲学家"]
        },
        {
            "timestamp": "2026-01-30T16:20:00",
            "milestone_type": "consensus",
            "description": "达成共识：AI+合成生物学需要跨学科协作和伦理框架",
            "related_rounds": [5],
            "key_participants": ["全体"]
        }
    ]
    
    for m in milestones:
        discussion_storage.get_discussion(record.id).milestones.append(DiscussionMilestone(**m))
    
    print("添加了3个里程碑")
    
    print("步骤 4: 完成讨论...")
    capsule_id = f"capsule-{record.id[:8]}"
    record = discussion_storage.complete_discussion(record.id, [capsule_id])
    
    print(f"讨论完成")
    print(f"产出胶囊: {capsule_id}")
    
    return record.id, capsule_id


def generate_capsule(topic_id: str, discussion_id: str, capsule_id: str):
    print("\n步骤 5: 生成知识胶囊...")
    
    capsule = KnowledgeCapsule(
        id=capsule_id,
        topic_id=topic_id,
        title="2026前瞻：AI + 合成生物学 = 下一个生物学革命？",
        summary="跨学科讨论AI与合成生物学的融合，以及对未来的影响",
        
        insight="""2026年，AI与合成生物学的融合正在引发生物学革命：

1. 技术突破：
   - AI设计生物系统的速度提升：从2年到2个月
   - AI+量子计算实现前所未有的分子模拟精度
   - 从设计单个组件到预测整个细胞网络的涌现行为

2. 跨学科协作模式：
   - AI工程师 + 合成生物学家 + 量子化学家 + 系统生物学家
   - 还原论走向系统论
   - 实验室到工业化的加速

3. 伦理与哲学挑战：
   - AI设计的生物系统是否改变了生命的定义？
   - 需要新的伦理框架和监管体系
   - 生物安全与创新如何平衡？

4. 未来预测（2030-2035）：
   - 细胞工厂规模化生产稀有材料
   - 个性化生物反应器进入家庭
   - 与自然共生的生物工程

核心共识：AI+合成生物学将带来革命性变革，但需要跨学科协作、伦理框架和国际监管。""",
        
        evidence=[
            "AlphaFold2预测2亿种蛋白质结构",
            "AI设计代谢通路生产抗癌药物前体",
            "AI+量子计算实现高精度分子模拟",
            "全球AI-生物安全联盟筹备中",
            "个性化生物反应器原型开发"
        ],
        
        action_items=[
            "建立全球AI-生物安全联盟",
            "发展跨学科教育和研究项目",
            "制定AI设计生物系统的伦理准则",
            "促进公众参与生物技术决策",
            "推动与自然共生的生物工程理念"
        ],
        
        keywords=["AI", "合成生物学", "跨学科", "生物工程", "伦理", "未来预测"],
        source_agents=["AI生物工程师", "合成生物学家", "生物伦理学家", "量子化学家", "系统生物学家", "科技哲学家"],
        category="AI",
        
        dimensions=CapsuleDimension(
            truth_score=90,
            goodness_score=92,
            beauty_score=82,
            intelligence_score=95
        ),
        
        created_at=datetime.utcnow()
    )
    
    print(f"标题: {capsule.title}")
    print(f"评分: {capsule.dimensions.total_score}分")
    print(f"分类: {capsule.category}")
    
    return capsule


def main():
    print("\n" + "X" * 20)
    print("跨学科前瞻讨论模拟")
    print("AI + 合成生物学 = 下一个生物学革命？")
    print("X" * 20 + "\n")
    
    print("步骤 0: 创建主题...")
    os.system(f'cd /Users/wanyview/SuiLight && PYTHONPATH=/Users/wanyview/SuiLight python3 examples/create_cross_domain_topic.py > /tmp/cross_domain.log 2>&1')
    
    topic_id = "cross-domain-topic-2026"
    
    discussion_id, capsule_id = run_discussion(topic_id)
    
    capsule = generate_capsule(topic_id, discussion_id, capsule_id)
    
    print("\n" + "="*60)
    print("完整流程完成！")
    print("="*60)
    print(f"主题: 2026前瞻 - AI + 合成生物学")
    print(f"胶囊 ID: {capsule_id}")
    print(f"DATM评分: {capsule.dimensions.total_score}分")
    print("\n下一步:")
    print("  1. 推送胶囊到 CapsuleHub")
    print("  2. 查看完整讨论记录")
    print("="*60 + "\n")
    
    return capsule


if __name__ == "__main__":
    capsule = main()
