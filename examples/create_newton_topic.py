#!/usr/bin/env python3
"""
SuiLight 示例脚本
创建限定主题：复现牛顿发现万有引力
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.discussions import (
    topic_storage, agent_config_storage,
    DiscussionTopic, TopicType
)


def create_newton_gravity_topic():
    """创建复现牛顿发现万有引力的限定主题"""
    
    topic_data = {
        "title": "复现：牛顿发现万有引力定律",
        "description": """
        在1665-1666年的英国剑桥和伍尔索普庄园，
        还原艾萨克·牛顿发现万有引力定律的历史过程。
        
        探讨的核心问题：
        1. 苹果落地与天体运动之间有何联系？
        2. 地球对月亮的引力如何计算？
        3. 开普勒定律与引力定律的关系是什么？
        4. 平方反比定律如何推导得出？
        """,
        "topic_type": "restricted",
        "tags": ["history", "physics", "newton", "gravity", "astronomy"],
        "restricted_config": {
            "historical_context": {
                "era": "科学革命时期",
                "year": 1666,
                "location": "英国伍尔索普庄园",
                "description": """
                17世纪的欧洲，科学革命正在兴起。
                哥白尼提出了日心说，开普勒发现了行星运动定律，
                伽利略改进了望远镜并发现了木星的卫星。
                
                牛顿回到家乡躲避瘟疫，在这段时间里，
                他开始思考天体运动的本质原因。
                """
            },
            "technical_context": {
                "pre_conditions": [
                    "已知开普勒行星运动三定律",
                    "已知地球表面的重力加速度",
                    "已知地球半径和月球距离",
                    "已知圆周运动向心力公式",
                    "已知地球对月球的引力应与重力同源"
                ],
                "constraints": [
                    "只能使用17世纪的数学工具（微积分初步）",
                    "天文数据精度有限",
                    "没有精确的万有引力常数G",
                    "需要解释苹果落地和月亮绕地的统一性"
                ],
                "available_resources": [
                    "开普勒行星运动定律",
                    "伽利略的力学研究",
                    "笛卡尔的机械哲学",
                    "天文观测数据（地球半径、月球距离）",
                    "木星的卫星周期（伽利略卫星）",
                    "胡克等人的弹簧研究"
                ],
                "tech_level": "1666年技术水平"
            },
            "goal": {
                "description": "探讨并还原牛顿发现万有引力定律的思维过程和关键推导",
                "success_criteria": [
                    "建立苹果落地与月亮绕地的联系",
                    "推导平方反比定律",
                    "统一天地物理学",
                    "解释潮汐现象"
                ],
                "expected_outcomes": [
                    "万有引力定律的发现过程",
                    "月地检验的数学推导",
                    "开普勒定律与引力定律的关系",
                    "对后来物理学的影响"
                ]
            },
            "setting_narrative": """
            1666年，英格兰林肯郡伍尔索普庄园。
            
            牛顿从剑桥大学回到家乡躲避鼠疫。
            一个阳光明媚的下午，他坐在苹果树下，
            看着成熟的苹果落到地上。
            
            一个问题闪过他的脑海：
            "为什么苹果总是垂直落地？"
            "为什么它不向旁边或向上移动？"
            
            答案必然与地球有关。
            但如果地球对苹果有引力，
            为什么不能对月亮也有同样的引力？
            
            月亮为什么不落向地球？
            除非...它正在"落"向地球，
            只是同时也在向前运动，
            就像一个永远落不到地球上的炮弹！
            """
        }
    }
    
    topic = topic_storage.create_topic(topic_data)
    print(f"✅ 主题已创建: {topic.id}")
    print(f"   标题: {topic.title}")
    print(f"   时代: {topic.restricted_config.historical_context.year}年")
    
    return topic


def configure_agents_for_topic(topic_id: str):
    """为主题配置参与 Agent"""
    
    agent_configs = [
        {
            "agent_id": "newton",
            "role": "moderator",
            "name": "艾萨克·牛顿",
            "personality": "深邃、独立、善于抽象思考",
            "expertise": ["数学", "物理学", "天文学", "光学"],
            "perspective": "unifier",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 1.0},
            "system_prompt_addon": "你作为牛顿，正在伍尔索普庄园。你观察到苹果落地，开始思考天地统一的物理规律。你需要整合已知的天文数据和力学知识，推导出引力定律。"
        },
        {
            "agent_id": "mathematician",
            "role": "expert",
            "name": "数学家",
            "personality": "严谨、精确、注重逻辑",
            "expertise": ["几何学", "微积分", "数学分析"],
            "perspective": "mathematical",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你负责提供数学工具支持，分析如何用数学语言描述引力作用。"
        },
        {
            "agent_id": "astronomer",
            "role": "expert",
            "name": "天文学家",
            "personality": "观测导向、注重数据",
            "expertise": ["行星运动", "天文观测", "月地系统"],
            "perspective": "observation-based",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你提供天文观测数据，帮助验证引力假设的准确性。"
        },
        {
            "agent_id": "mechanist",
            "role": "expert",
            "name": "力学家",
            "personality": "务实、注重实验验证",
            "expertise": ["力学", "运动定律", "向心力"],
            "perspective": "dynamics",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.7},
            "system_prompt_addon": "你从力学角度分析圆周运动和向心力，帮助理解月亮为何不落向地球。"
        },
        {
            "agent_id": "philosopher",
            "role": "critic",
            "name": "自然哲学家",
            "personality": "质疑、注重哲学思辨",
            "expertise": ["机械哲学", "自然观", "科学方法论"],
            "perspective": "critical",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.6},
            "system_prompt_addon": "你代表当时的自然哲学家，质疑超距作用的合理性，探讨引力的本质。"
        }
    ]
    
    config_data = {
        "topic_id": topic_id,
        "agents": agent_configs,
        "orchestration": {
            "moderator_agent_id": "newton",
            "discussion_flow": "sequential",
            "round_limit": 5,
            "consensus_threshold": 0.7,
            "max_agents_per_round": 3
        }
    }
    
    config = agent_config_storage.create_config(topic_id, config_data)
    print(f"✅ Agent 配置已创建: {config.id}")
    print(f"   参与 Agent: {len(config.agents)} 个")
    
    return config


def main():
    """主流程"""
    print("\n" + "🍎" * 20)
    print("牛顿发现万有引力 - 限定主题")
    print("🍎" * 20 + "\n")
    
    # 1. 创建限定主题
    print("📝 步骤 1: 创建限定主题...")
    topic = create_newton_gravity_topic()
    
    # 2. 配置参与 Agent
    print("\n🤖 步骤 2: 配置参与 Agent...")
    config = configure_agents_for_topic(topic.id)
    
    print("\n" + "="*60)
    print("✅ 设置完成！")
    print("="*60)
    print(f"主题 ID: {topic.id}")
    print(f"Agent 配置 ID: {config.id}")
    print("\n下一步:")
    print("  1. 运行讨论: python3 examples/run_newton_discussion.py")
    print("  2. 生成知识胶囊")
    print("  3. 推送到 CapsuleHub")
    print("="*60 + "\n")
    
    return topic.id


if __name__ == "__main__":
    topic_id = main()
    print(f"\n📌 记住这个主题 ID: {topic_id}")
