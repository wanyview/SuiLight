#!/usr/bin/env python3
"""
SuiLight 开放主题示例
2026年前瞻：AI能否自主发现新的科学定律？
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.discussions import (
    topic_storage, agent_config_storage,
    DiscussionTopic, TopicType
)


def create_2026_futures_topic():
    """创建2026年前瞻开放主题"""
    
    topic_data = {
        "title": "2026年前瞻：AI能否自主发现新的科学定律？",
        "description": """
        在2026年的今天，基于当前的技术发展水平，
        探讨人工智能是否具备发现新科学定律的潜力。
        
        核心问题：
        1. AI能否从海量数据中发现人类未曾注意的模式？
        2. AI能否提出可证伪的假说？
        3. AI能否设计实验来验证假说？
        4. AI的创造力与人类的本质区别是什么？
        """,
        "topic_type": "open",
        "tags": ["AI", "science", "future", "discovery", "2026"],
        "open_config": {
            "keywords": ["AI", "科学发现", "机器学习", "假设生成", "自动化科学"],
            "domains": ["AI研究", "科学哲学", "认知科学", "计算机科学"],
            "exploration_depth": "deep",
            "initial_perspectives": [
                "AI乐观主义者：AI已经在围棋、蛋白质结构预测等领域超越人类",
                "AI怀疑论者：AI缺乏真正的理解和直觉",
                "科学哲学家：科学发现需要理解，而不仅仅是模式匹配",
                "工程师视角：AI作为工具可以加速科学发现过程"
            ]
        }
    }
    
    topic = topic_storage.create_topic(topic_data)
    print(f"主题已创建: {topic.id}")
    print(f"标题: {topic.title}")
    print(f"类型: 开放主题 (2026年前瞻)")
    
    return topic


def configure_agents_for_topic(topic_id: str):
    """为主题配置参与 Agent"""
    
    agent_configs = [
        {
            "agent_id": "ai_researcher",
            "role": "moderator",
            "name": "AI研究员",
            "personality": "技术导向、乐观务实",
            "expertise": ["机器学习", "深度学习", "科学AI"],
            "perspective": "AI-accelerated-discovery",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 1.0},
            "system_prompt_addon": "你作为AI研究员，亲眼见证了AlphaFold、AlphaGo等AI突破。你相信AI正在改变科学发现的方式。"
        },
        {
            "agent_id": "philosopher",
            "role": "critic",
            "name": "科学哲学家",
            "personality": "质疑、深刻、注重本质",
            "expertise": ["科学哲学", "认识论", "创造力的本质"],
            "perspective": "skeptical",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你代表怀疑论者，质疑AI是否真正理解宇宙的本质，还是只是在统计相关性。"
        },
        {
            "agent_id": "physicist",
            "role": "expert",
            "name": "理论物理学家",
            "personality": "严谨、追求简洁、注重数学美",
            "expertise": ["理论物理", "量子力学", "宇宙学"],
            "perspective": "theory-seeker",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你关心AI能否发现像相对论、量子力学那样简洁优美的理论。"
        },
        {
            "agent_id": "biologist",
            "role": "expert",
            "name": "计算生物学家",
            "personality": "数据驱动、跨学科",
            "expertise": ["生物信息学", "蛋白质结构", "系统生物学"],
            "perspective": "data-driven",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.7},
            "system_prompt_addon": "你见证了AlphaFold的突破，相信AI在生物发现中有巨大潜力。"
        },
        {
            "agent_id": "cognitive_scientist",
            "role": "expert",
            "name": "认知科学家",
            "personality": "好奇、跨学科、注重心智",
            "expertise": ["认知科学", "创造力研究", "人工智能"],
            "perspective": "human-AI-comparison",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.7},
            "system_prompt_addon": "你研究人类和AI的创造力差异，探讨思考的本质。"
        },
        {
            "agent_id": "engineer",
            "role": "expert",
            "name": "AI工程师",
            "personality": "实用、解决问题导向",
            "expertise": ["机器学习工程", "AI系统设计", "自动化实验"],
            "perspective": "tool-builder",
            "participation": {"start_round": 3, "end_round": None, "speak_probability": 0.6},
            "system_prompt_addon": "你从工程角度看待AI，关心如何构建自动化科学发现的系统。"
        }
    ]
    
    config_data = {
        "topic_id": topic_id,
        "agents": agent_configs,
        "orchestration": {
            "moderator_agent_id": "ai_researcher",
            "discussion_flow": "sequential",
            "round_limit": 5,
            "consensus_threshold": 0.6,
            "max_agents_per_round": 3
        }
    }
    
    config = agent_config_storage.create_config(topic_id, config_data)
    print(f"Agent 配置已创建: {config.id}")
    print(f"参与 Agent: {len(config.agents)} 个")
    
    return config


def main():
    print("\n" + "X" * 20)
    print("2026年前瞻：AI能否自主发现科学定律？")
    print("X" * 20 + "\n")
    
    print("步骤 1: 创建开放主题...")
    topic = create_2026_futures_topic()
    
    print("\n步骤 2: 配置参与 Agent...")
    config = configure_agents_for_topic(topic.id)
    
    print("\n" + "="*60)
    print("设置完成！")
    print("="*60)
    print(f"主题 ID: {topic.id}")
    print(f"Agent 配置 ID: {config.id}")
    print("\n下一步:")
    print("  1. 运行讨论: python3 examples/run_2026_futures_discussion.py")
    print("  2. 生成知识胶囊")
    print("  3. 推送到 CapsuleHub")
    print("="*60 + "\n")
    
    return topic.id


if __name__ == "__main__":
    topic_id = main()
    print(f"\n记住这个主题 ID: {topic_id}")
