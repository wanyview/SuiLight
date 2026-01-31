#!/usr/bin/env python3
"""
模拟牛顿发现万有引力讨论过程
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
NEWTON_DISCUSSION = [
    # 第1轮 - 问题提出
    {
        "round": 1,
        "timestamp": "1666-08-01T14:00:00",
        "agent_id": "newton",
        "agent_role": "moderator",
        "agent_name": "艾萨克·牛顿",
        "content": "各位，今天下午我坐在苹果树下，一个苹果落在我面前。我开始思考：为什么苹果总是垂直落地？这一定是地球在吸引苹果。但为什么苹果不吸引地球呢？更关键的是，如果地球能吸引苹果，为什么不能吸引月亮？",
        "message_type": "question"
    },
    {
        "round": 1,
        "timestamp": "1666-08-01T14:10:00",
        "agent_id": "astronomer",
        "agent_role": "expert",
        "agent_name": "天文学家",
        "content": "牛顿先生，这是一个深刻的洞察。我们知道月亮绕地球做圆周运动，距离约38万公里。而苹果离地心只有约6400公里。如果引力与距离有关，我们需要知道这种关系是什么。",
        "message_type": "comment"
    },
    {
        "round": 1,
        "timestamp": "1666-08-01T14:20:00",
        "agent_id": "mathematician",
        "agent_role": "expert",
        "agent_name": "数学家",
        "content": "我有一个假设。如果引力是向心的，那么向心力公式是 F = mv²/r。如果月亮在做圆周运动，它需要向心力。如果我们假设这个向心力来自地球的引力，那么引力应该与距离的平方成反比。",
        "message_type": "insight"
    },
    
    # 第2轮 - 定量分析
    {
        "round": 2,
        "timestamp": "1666-08-01T15:00:00",
        "agent_id": "newton",
        "agent_role": "moderator",
        "agent_name": "艾萨克·牛顿",
        "content": "让我计算一下。地球表面重力加速度 g 约为 9.8 m/s²。月地距离 r 约为地球半径的60倍。如果引力与距离平方成反比，月球处的加速度应该是 g/3600，约 0.0027 m/s²。",
        "message_type": "synthesis"
    },
    {
        "round": 2,
        "timestamp": "1666-08-01T15:10:00",
        "agent_id": "mechanist",
        "agent_role": "expert",
        "agent_name": "力学家",
        "content": "我验证一下月球的实际加速度。月球绕地球公转周期约27.3天，轨道半径384,000公里。计算得出月球需要的向心加速度是 0.0027 m/s²。与理论值完全吻合！",
        "message_type": "answer"
    },
    {
        "round": 2,
        "timestamp": "1666-08-01T15:20:00",
        "agent_id": "astronomer",
        "agent_role": "expert",
        "agent_name": "天文学家",
        "content": "这太重要了！我们还可以用开普勒第三定律验证。行星周期的平方与距离的立方成正比。如果引力与距离平方成反比，结合向心力公式，确实可以推导出开普勒定律。",
        "message_type": "comment"
    },
    
    # 第3轮 - 哲学思辨
    {
        "round": 3,
        "timestamp": "1666-08-01T16:00:00",
        "agent_id": "philosopher",
        "agent_role": "critic",
        "agent_name": "自然哲学家",
        "content": "各位，我有一个疑问。按照笛卡尔的机械哲学，所有作用都需要接触。但引力是超距作用——地球没有接触月亮，怎么能吸引它？这在哲学上难以接受。",
        "message_type": "question"
    },
    {
        "round": 3,
        "timestamp": "1666-08-01T16:10:00",
        "agent_id": "newton",
        "agent_role": "moderator",
        "agent_name": "艾萨克·牛顿",
        "content": "这是一个深刻的哲学问题。我必须承认，引力的本质是什么——我还没有找到答案。但我可以用数学描述它的规律：F = G*M*m/r²。无论机制如何，这个公式能准确预测现象。",
        "message_type": "comment"
    },
    {
        "round": 3,
        "timestamp": "1666-08-01T16:20:00",
        "agent_id": "mathematician",
        "agent_role": "expert",
        "agent_name": "数学家",
        "content": '我同意牛顿的看法。物理学应该优先描述"如何"而非"为什么"。这个平方反比定律能够统一解释：苹果落地、月球绕地、行星绕日，甚至潮汐现象。',
        "message_type": "synthesis"
    },
    
    # 第4轮 - 扩展应用
    {
        "round": 4,
        "timestamp": "1666-08-01T17:00:00",
        "agent_id": "astronomer",
        "agent_role": "expert",
        "agent_name": "天文学家",
        "content": "这个定律的应用不止于此！我想到木星的四颗卫星，它们的运动也应该遵循同样的规律。这可以用来验证定律的普适性，也可能帮助我们计算木星的质量。",
        "message_type": "insight"
    },
    {
        "round": 4,
        "timestamp": "1666-08-01T17:10:00",
        "agent_id": "mechanist",
        "agent_role": "expert",
        "agent_name": "力学家",
        "content": "还有潮汐现象！月亮对地球海水的引力造成潮汐。太阳也有贡献，但距离远得多。如果引力与距离平方成反比，我们就能解释为什么月亮对潮汐的影响更大。",
        "message_type": "comment"
    },
    
    # 第5轮 - 总结共识
    {
        "round": 5,
        "timestamp": "1666-08-01T17:30:00",
        "agent_id": "newton",
        "agent_role": "moderator",
        "agent_name": "艾萨克·牛顿",
        "content": "综合各位的观点，让我总结我们的发现。天地之间的现象——苹果落地、月球绕地、行星运动、潮汐涨落——都可以用同一个定律来描述。这标志着物理学的新时代。",
        "message_type": "synthesis"
    },
    {
        "round": 5,
        "timestamp": "1666-08-01T17:40:00",
        "agent_id": "philosopher",
        "agent_role": "critic",
        "agent_name": "自然哲学家",
        "content": "虽然超距作用的哲学问题尚未解决，但我承认这个定律的强大预测能力。它统一了天与地，这是前所未有的成就。我收回质疑。",
        "message_type": "comment"
    }
]


def run_discussion(topic_id: str) -> str:
    """运行模拟讨论"""
    print("📝 步骤 1: 创建讨论记录...")
    
    record = discussion_storage.create_discussion(topic_id)
    print(f"   讨论 ID: {record.id}")
    
    print("📝 步骤 2: 添加讨论消息...")
    for msg_data in NEWTON_DISCUSSION:
        record = discussion_storage.add_message(record.id, msg_data)
        agent = msg_data["agent_name"]
        print(f"   [{msg_data['round']}轮] {agent}: {msg_data['content'][:40]}...")
    
    print("📝 步骤 3: 添加里程碑...")
    milestones = [
        {
            "timestamp": "1666-08-01T14:20:00",
            "milestone_type": "insight",
            "description": "提出引力与距离平方成反比的假设",
            "related_rounds": [1],
            "key_participants": ["数学家"]
        },
        {
            "timestamp": "1666-08-01T15:10:00",
            "milestone_type": "breakthrough",
            "description": "月地检验成功：理论与观测完全吻合",
            "related_rounds": [2],
            "key_participants": ["艾萨克·牛顿", "力学家"]
        },
        {
            "timestamp": "1666-08-01T17:40:00",
            "milestone_type": "consensus",
            "description": "达成共识：天地统一于万有引力定律",
            "related_rounds": [5],
            "key_participants": ["全体"]
        }
    ]
    
    for m in milestones:
        discussion_storage.get_discussion(record.id).milestones.append(DiscussionMilestone(**m))
    
    print("   ✅ 添加了3个里程碑")
    
    print("📝 步骤 4: 完成讨论...")
    capsule_id = f"capsule-{record.id[:8]}"
    record = discussion_storage.complete_discussion(record.id, [capsule_id])
    
    print(f"   ✅ 讨论完成")
    print(f"   产出胶囊: {capsule_id}")
    
    return record.id, capsule_id


def generate_capsule(topic_id: str, discussion_id: str, capsule_id: str):
    """生成知识胶囊"""
    print("\n📦 步骤 5: 生成知识胶囊...")
    
    capsule = KnowledgeCapsule(
        id=capsule_id,
        topic_id=topic_id,
        title="牛顿发现万有引力定律 - 天地统一的物理学",
        summary="通过多轮讨论，复现了1666年牛顿发现万有引力定律的思维过程",
        
        insight="""通过多轮讨论，复现了1666年牛顿发现万有引力定律的关键发现：

1. **问题洞察**：苹果落地与月亮绕地是同一原因——地球的引力
2. **数学推导**：假设引力与距离平方成反比，结合向心力公式
3. **月地检验**：计算值与观测值吻合，验证假设正确
4. **统一天地**：开普勒行星定律可由万有引力定律推导

核心洞见：支配苹果落地的力，与支配月亮绕地的力，是同一种力——这标志着物理学从"天地分离"走向"天地统一"。""",
        
        evidence=[
            "月球轨道半径384,000公里，周期27.3天",
            "计算得向心加速度 0.0027 m/s²",
            "与平方反比定律预测值完全吻合",
            "木星卫星运动也遵循同样规律",
            "潮汐现象可由日月引力解释"
        ],
        
        action_items=[
            "测量万有引力常数G（后人完成：卡文迪什1798年）",
            "将引力定律推广到太阳系所有行星",
            "解释潮汐现象的定量规律",
            "后续研究：引力的本质是什么？"
        ],
        
        keywords=["newton", "gravity", "physics", "celestial-mechanics", "unification"],
        source_agents=["艾萨克·牛顿", "数学家", "天文学家", "力学家", "自然哲学家"],
        category="physics",
        
        dimensions=CapsuleDimension(
            truth_score=95,       # 科学史实高度准确
            goodness_score=90,    # 对人类认知影响巨大
            beauty_score=85,  # 简洁优雅的数学描述
            intelligence_score=98  # 极高智慧含量
        ),
        
        created_at=datetime.utcnow()
    )
    
    print(f"   标题: {capsule.title}")
    print(f"   评分: {capsule.dimensions.total_score}分")
    print(f"   分类: {capsule.category}")
    
    return capsule


def main():
    """主流程"""
    print("\n" + "🌙" * 20)
    print("牛顿发现万有引力讨论模拟")
    print("生成知识胶囊并推送到 CapsuleHub")
    print("🌙" * 20 + "\n")
    
    # 创建新主题
    print("📝 步骤 0: 创建主题...")
    os.system(f'cd /Users/wanyview/SuiLight && PYTHONPATH=/Users/wanyview/SuiLight python3 examples/create_newton_topic.py > /tmp/newton_topic.log 2>&1')
    
    topic_id = "newton-gravity-topic-1666"
    
    # 1. 运行讨论
    discussion_id, capsule_id = run_discussion(topic_id)
    
    # 2. 生成胶囊
    capsule = generate_capsule(topic_id, discussion_id, capsule_id)
    
    print("\n" + "="*60)
    print("✅ 完整流程完成！")
    print("="*60)
    print(f"主题: 复现牛顿发现万有引力")
    print(f"胶囊 ID: {capsule_id}")
    print(f"DATM评分: {capsule.dimensions.total_score}分")
    print("\n知识胶囊已生成，准备推送到 CapsuleHub...")
    print("="*60 + "\n")
    
    return capsule


if __name__ == "__main__":
    capsule = main()
