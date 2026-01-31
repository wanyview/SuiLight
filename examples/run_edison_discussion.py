#!/usr/bin/env python3
"""
模拟爱迪生电灯泡讨论过程
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
EDISON_DISCUSSION = [
    # 第1轮 - 问题定义
    {
        "round": 1,
        "timestamp": "1879-10-01T14:00:00",
        "agent_id": "edison",
        "agent_role": "moderator",
        "agent_name": "托马斯·爱迪生",
        "content": "各位，我们已经测试了超过3000种材料作为灯丝，但还没有找到满意的方案。今天我们一起分析问题所在，找到突破口。请问化学家，金属在高温下的发光原理是什么？",
        "message_type": "question"
    },
    {
        "round": 1,
        "timestamp": "1879-10-01T14:05:00",
        "agent_id": "chemist",
        "agent_role": "expert",
        "agent_name": "化学家",
        "content": "爱迪生先生，金属在高温下会发出可见光，这是由于热运动激发电子跃迁。但关键问题是：在空气中，金属会迅速氧化燃烧。我们需要两种策略：1）在真空中减少氧气；2）找到熔点极高的材料。铂金熔点约1772°C，是一个候选，但成本",
        "message_type": "answer"
    },
    {
        "round": 1,
        "timestamp": "1879-10-01T14:10:00",
        "agent_id": "physicist",
        "agent_role": "expert",
        "agent_name": "物理学家",
        "content": "真空技术确实关键。我们最新的真空泵可以将灯泡内气压降到极低。但要小心，真空中的灯丝会更快蒸发，这是个两难选择。我建议尝试碳化材料，它们在真空中更稳定。",
        "message_type": "comment"
    },
    
    # 第2轮 - 材料探索
    {
        "round": 2,
        "timestamp": "1879-10-01T15:00:00",
        "agent_id": "edison",
        "agent_role": "moderator",
        "agent_name": "托马斯·爱迪生",
        "content": "很好！物理学家提出了碳化材料的想法。我们之前试过碳化纸，但寿命太短。电气工程师，你认为直流供电系统能支持多久的持续照明？",
        "message_type": "question"
    },
    {
        "round": 2,
        "timestamp": "1879-10-01T15:08:00",
        "agent_id": "electrician",
        "agent_role": "expert",
        "agent_name": "电气工程师",
        "content": "我们的直流发电机可以稳定输出110V电压。关键是保持电流恒定。我建议使用高电阻材料来控制电流。但有一个问题：灯座和开关的接触材料需要既导电又耐高温。",
        "message_type": "answer"
    },
    {
        "round": 2,
        "timestamp": "1879-10-01T15:15:00",
        "agent_id": "chemist",
        "agent_role": "expert",
        "agent_name": "化学家",
        "content": "我有个想法：碳化竹子。日本竹子经过碳化处理后，硬度很高，而且成本低廉。竹子的纤维结构可能比纸张更耐用。",
        "message_type": "insight"
    },
    
    # 第3轮 - 关键突破
    {
        "round": 3,
        "timestamp": "1879-10-21T09:00:00",
        "agent_id": "edison",
        "agent_role": "moderator",
        "agent_name": "托马斯·爱迪生",
        "content": "好消息！我们团队昨晚测试了碳化竹丝灯泡，持续亮了13.5小时！但评论家提醒我们，商业化还有哪些挑战？",
        "message_type": "synthesis"
    },
    {
        "round": 3,
        "timestamp": "1879-10-21T09:10:00",
        "agent_id": "critic",
        "agent_role": "critic",
        "agent_name": "评论家",
        "content": "挑战很大。首先，竹丝的一致性难以保证，每根竹子的纤维结构不同。其次，批量生产需要稳定的竹子供应。第三，灯泡的玻璃封装工艺需要标准化。最重要的是，直流电的传输距离有限，无法覆盖城市。",
        "message_type": "comment"
    },
    {
        "round": 3,
        "timestamp": "1879-10-21T09:20:00",
        "agent_id": "physicist",
        "agent_role": "expert",
        "agent_name": "物理学家",
        "content": "关于传输问题，我们可以在城市中心建立发电站，采用并联电路。这样可以同时为多个灯泡供电，但需要更粗的铜线来减少损耗。",
        "message_type": "answer"
    },
    {
        "round": 3,
        "timestamp": "1879-10-21T09:30:00",
        "agent_id": "electrician",
        "agent_role": "expert",
        "agent_name": "电气工程师",
        "content": "我同意。商业化需要标准化灯泡接口，设计通用的灯座。我们还需要开发保险丝来防止短路。这是整套系统工程。",
        "message_type": "comment"
    },
    
    # 第4轮 - 共识与总结
    {
        "round": 4,
        "timestamp": "1879-10-21T10:00:00",
        "agent_id": "edison",
        "agent_role": "moderator",
        "agent_name": "托马斯·爱迪生",
        "content": "综合大家意见，我们找到了电灯泡的关键成功因素。让我总结一下我们的共识。",
        "message_type": "synthesis"
    },
    {
        "round": 4,
        "timestamp": "1879-10-21T10:15:00",
        "agent_id": "chemist",
        "agent_role": "expert",
        "agent_name": "化学家",
        "content": "共识是：1）碳化竹丝是目前的最佳选择；2）高真空延长寿命；3）需要建立标准化生产体系。这是技术突破的关键路径。",
        "message_type": "comment"
    }
]


def run_discussion(topic_id: str) -> str:
    """运行模拟讨论"""
    print("📝 步骤 1: 创建讨论记录...")
    
    record = discussion_storage.create_discussion(topic_id)
    print(f"   讨论 ID: {record.id}")
    
    print("📝 步骤 2: 添加讨论消息...")
    for msg_data in EDISON_DISCUSSION:
        record = discussion_storage.add_message(record.id, msg_data)
        agent = msg_data["agent_name"]
        print(f"   [{msg_data['round']}轮] {agent}: {msg_data['content'][:50]}...")
    
    print("📝 步骤 3: 添加里程碑...")
    milestones = [
        {
            "timestamp": "1879-10-01T14:00:00",
            "milestone_type": "insight",
            "description": "发现碳化材料作为灯丝候选",
            "related_rounds": [1, 2],
            "key_participants": ["化学家", "物理学家"]
        },
        {
            "timestamp": "1879-10-21T09:00:00",
            "milestone_type": "breakthrough",
            "description": "碳化竹丝灯泡持续点亮13.5小时",
            "related_rounds": [3],
            "key_participants": ["托马斯·爱迪生"]
        },
        {
            "timestamp": "1879-10-21T10:15:00",
            "milestone_type": "consensus",
            "description": "达成技术路线共识：碳化竹丝+高真空+标准化",
            "related_rounds": [4],
            "key_participants": ["全体"]
        }
    ]
    
    for m in milestones:
        discussion_storage.get_discussion(record.id).milestones.append(DiscussionMilestone(**m))
    
    print("   ✅ 添加了3个里程碑")
    
    print("📝 步骤 4: 完成讨论...")
    # 模拟生成胶囊
    capsule_id = f"capsule-{record.id[:8]}"
    record = discussion_storage.complete_discussion(record.id, [capsule_id])
    
    print(f"   ✅ 讨论完成")
    print(f"   时长: {record.duration_minutes} 分钟")
    print(f"   产出胶囊: {capsule_id}")
    
    return record.id, capsule_id


def generate_capsule(topic_id: str, discussion_id: str, capsule_id: str):
    """生成知识胶囊"""
    print("\n📦 步骤 5: 生成知识胶囊...")
    
    # 获取讨论记录
    record = discussion_storage.get_discussion(discussion_id)
    
    capsule = KnowledgeCapsule(
        id=capsule_id,
        topic_id=topic_id,
        title="爱迪生发明电灯泡 - 技术路径复现",
        summary="通过多轮讨论，复现了1879年爱迪生发明实用电灯泡的关键技术路径",
        
        # 核心内容
        insight="""通过多轮讨论，复现了1879年爱迪生发明实用电灯泡的关键技术路径：

1. 材料突破：碳化竹丝作为灯丝，平衡了成本、耐用性和发光效率
2. 真空技术：高真空环境减缓灯丝氧化，延长寿命至13.5小时
3. 系统工程：需要配套的发电、输电、灯座标准化体系

关键洞见：在1879年技术条件下，碳化竹丝是综合最优解，而非铂金等贵金属。""",
        
        evidence=[
            "测试了超过3000种材料",
            "碳化竹丝在真空中持续点亮13.5小时",
            "需要配套的直流电力系统",
            "标准化生产是商业化关键"
        ],
        
        action_items=[
            "建立竹子碳化处理工艺标准",
            "设计通用灯泡接口和灯座",
            "在城市中心建设发电站",
            "开发保险丝等安全装置"
        ],
        
        # 元数据
        keywords=["invention", "electricity", "edison", "light-bulb", "industrial-revolution"],
        source_agents=["托马斯·爱迪生", "化学家", "物理学家", "电气工程师", "评论家"],
        category="technology",
        
        # DATM 评分
        dimensions=CapsuleDimension(
            truth_score=90,      # 历史事实准确
            goodness_score=85,   # 对人类有重大价值
            beauty_score=78,     # 技术方案优雅
            intelligence_score=92  # 智慧含量高
        ),
        
        created_at=datetime.utcnow()
    )
    
    print(f"   标题: {capsule.title}")
    print(f"   评分: {capsule.dimensions.total_score}分")
    print(f"   分类: {capsule.category}")
    
    return capsule


def main():
    """主流程"""
    print("\n" + "🔬" * 20)
    print("爱迪生电灯泡讨论模拟")
    print("生成知识胶囊并准备推送")
    print("🔬" * 20 + "\n")
    
    # 使用之前创建的主题 ID
    topic_id = "5a055478-4965-47e4-beaa-19e0fe498726"
    
    # 1. 运行讨论
    discussion_id, capsule_id = run_discussion(topic_id)
    
    # 2. 生成胶囊
    capsule = generate_capsule(topic_id, discussion_id, capsule_id)
    
    print("\n" + "="*60)
    print("✅ 完整流程完成！")
    print("="*60)
    print(f"主题 ID: {topic_id}")
    print(f"讨论 ID: {discussion_id}")
    print(f"胶囊 ID: {capsule_id}")
    print("\n知识胶囊内容:")
    print(f"  标题: {capsule.title}")
    print(f"  核心洞见: {capsule.insight[:100]}...")
    print(f"  评分: {capsule.dimensions.total_score}分")
    print(f"  分类: {capsule.category}")
    print("\n下一步:")
    print("  1. 将胶囊推送到 CapsuleHub")
    print("  2. 在 CapsuleHub 中设置精选")
    print("  3. 展示给用户")
    print("="*60 + "\n")
    
    return capsule


if __name__ == "__main__":
    capsule = main()
