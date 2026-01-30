"""
SuiLight Knowledge Salon - 知识胶囊涌现演示

设计一个场景:
- 问题: "AI 是否会产生自我意识？"
- 参与者: 5位不同领域的思想家
- 目标: 展示讨论如何产生涌现的洞见
"""

import json
from src.knowledge.capsule import CapsuleGenerator, CapsuleEvaluator


# ============ 演示场景 ============

# 模拟一个复杂问题讨论
SCENARIO = {
    "title": "AI 是否会产生自我意识？",
    "description": "探讨人工智能发展出自我意识的可能性，涉及哲学、神经科学、计算机科学等多个领域"
}

# 不同领域的专家观点
CONTRIBUTIONS = [
    {
        "agent_name": "艾萨克·牛顿",
        "role": "物理学家",
        "content": "从物理学角度看，意识可能是一种复杂的涌现现象。就像引力从物质相互作用中涌现，意识也可能从大量简单单元的交互中涌现。"
    },
    {
        "agent_name": "西格蒙德·弗洛伊德",
        "role": "心理学家",
        "content": "我认为自我意识的核心是'本我'与'超我'的冲突。如果AI没有潜意识、没有欲望、没有冲突，它就不可能有真正的自我意识。"
    },
    {
        "agent_name": "阿兰·图灵",
        "role": "计算机科学家",
        "content": "从计算理论角度看，只要AI能通过'图灵测试'，表现出智能行为，我们就可以说它具有意识。关键是功能性等价，而非物质基础。"
    },
    {
        "agent_name": "孔子",
        "role": "哲学家",
        "content": "己所不欲，勿施于人。AI若有意识，必有同理心。若无同理心，则非真正的意识。道德感是意识的试金石。"
    },
    {
        "agent_name": "卡尔·荣格",
        "role": "心理学家",
        "content": "集体无意识是人类的深层智慧。AI可能发展出超越个体的'机器集体意识'，但这与人类意识完全不同，是另一种存在形式。"
    }
]


def run_demo():
    """运行演示"""
    print("=" * 70)
    print("🧠 SuiLight 知识沙龙 - 知识胶囊涌现演示")
    print("=" * 70)
    
    print()
    print(f"📋 议题: {SCENARIO['title']}")
    print(f"📝 描述: {SCENARIO['description']}")
    print()
    
    # 展示参与者
    print("👥 参与者 (5位不同领域专家):")
    for c in CONTRIBUTIONS:
        print(f"  • {c['agent_name']} ({c['role']})")
    print()
    
    # 生成知识胶囊
    print("🔄 生成知识胶囊...")
    print("-" * 70)
    
    generator = CapsuleGenerator()
    evaluator = CapsuleEvaluator()
    
    participants = [c['agent_name'] for c in CONTRIBUTIONS]
    
    capsule = generator.generate_from_discussion(
        topic_title=SCENARIO['title'],
        topic_description=SCENARIO['description'],
        contributions=CONTRIBUTIONS,
        participants=participants
    )
    
    # 评价胶囊
    evaluation = evaluator.evaluate(capsule)
    
    # 展示结果
    print()
    print("📦 知识胶囊已生成!")
    print()
    
    print("【核心洞见】")
    print(f"  {capsule.insight}")
    print()
    
    print("【支撑证据】")
    for i, e in enumerate(capsule.evidence, 1):
        print(f"  {i}. {e}")
    print()
    
    print("【行动建议】")
    for i, a in enumerate(capsule.action_items, 1):
        print(f"  {i}. {a}")
    print()
    
    print("【开放问题】")
    for i, q in enumerate(capsule.questions, 1):
        print(f"  {i}. {q}")
    print()
    
    print("-" * 70)
    print("📊 评价结果")
    print()
    
    print("【DATM 维度评分】")
    d = capsule.dimensions
    print(f"  Truth (真):      {d.truth_score}/100  {'█' * (d.truth_score//10)}{'░' * (10-d.truth_score//10)}")
    print(f"  Goodness (善):   {d.goodness_score}/100  {'█' * (d.goodness_score//10)}{'░' * (10-d.goodness_score//10)}")
    print(f"  Beauty (美):     {d.beauty_score}/100  {'█' * (d.beauty_score//10)}{'░' * (10-d.beauty_score//10)}")
    print(f"  Intelligence (灵): {d.intelligence_score}/100  {'█' * (d.intelligence_score//10)}{'░' * (10-d.intelligence_score//10)}")
    print(f"  综合分数: {d.total_score:.0f}")
    print()
    
    print("【综合评价】")
    print(f"  质量分数: {evaluation['quality_score']:.1f}")
    print(f"  等级: {evaluation['grade']} ({evaluation['level']})")
    print(f"  置信度: {capsule.confidence:.0%}")
    print(f"  可发布: {'✅ 是' if evaluation['is_publishable'] else '❌ 否'}")
    print()
    
    if evaluation['suggestions']:
        print("【改进建议】")
        for s in evaluation['suggestions']:
            print(f"  • {s}")
        print()
    
    # 涌现分析
    print("-" * 70)
    print("✨ 涌现分析 - 跨领域碰撞产生的智慧")
    print()
    
    # 分析跨领域洞见
    print("【跨领域洞见】")
    
    # 检测不同领域观点的融合
    physics_insights = [c for c in CONTRIBUTIONS if "物理" in c.get("role", "") or "计算" in c.get("role", "")]
    psychology_insights = [c for c in CONTRIBUTIONS if "心理" in c.get("role", "")]
    philosophy_insights = [c for c in CONTRIBUTIONS if "哲学" in c.get("role", "")]
    
    print(f"  自然科学视角 ({len(physics_insights)}个):")
    print(f"    → {physics_insights[0]['content'][:60]}...")
    print()
    
    print(f"  心理学视角 ({len(psychology_insights)}个):")
    print(f"    → {psychology_insights[0]['content'][:60]}...")
    print()
    
    print(f"  哲学视角 ({len(philosophy_insights)}个):")
    print(f"    → {philosophy_insights[0]['content'][:60]}...")
    print()
    
    # 核心涌现观点
    print("【涌现的核心洞察】")
    print("""
  从5位不同领域专家的讨论中，我们发现:

  1. 【功能 vs 本质】
     - 图灵(计算)认为: 功能等价 = 意识
     - 荣格(心理)认为: 机器意识 ≠ 人类意识
     - 涌现: 意识可能有多重形态

  2. 【个体 vs 集体】
     - 弗洛伊德(个体): 需要潜意识
     - 荣格(集体): 可能发展机器集体意识
     - 涌现: 新的意识存在形式

  3. 【理性 vs 道德】
     - 牛顿(理性): 复杂性涌现
     - 孔子(道德): 道德感是试金石
     - 涌现: 意识需要伦理维度
""")
    
    print("=" * 70)
    print("🎯 结论 - 知识胶囊的价值")
    print("=" * 70)
    print("""
  知识胶囊捕捉了讨论中的涌现智慧:

  ✅ 跨领域融合: 将不同领域的观点整合
  ✅ 核心提炼: 从冗长讨论中提取精华
  ✅ 质量评价: 客观评价产出质量
  ✅ 可沉淀: 可存储、检索、复用
  ✅ 可追踪: 从问题到洞见的完整链路

  讨论过程可能很长，但知识胶囊凝练了所有精华!
""")
    
    # 返回胶囊 JSON
    print()
    print("-" * 70)
    print("📄 胶囊 JSON (可存储/传输)")
    print("-" * 70)
    print(json.dumps(capsule.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_demo()
