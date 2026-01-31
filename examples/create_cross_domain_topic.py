#!/usr/bin/env python3
"""
SuiLight 开放主题示例
2026年前瞻：AI + 合成生物学 = 下一个生物学革命？
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.discussions import (
    topic_storage, agent_config_storage,
    DiscussionTopic, TopicType
)


def create_cross_domain_topic():
    """创建跨学科前瞻开放主题"""
    
    topic_data = {
        "title": "2026年前瞻：AI + 合成生物学 = 下一个生物学革命？",
        "description": """
        2026年的今天，AI与合成生物学正在深度融合。
        我们能否设计全新的人工生物系统？
        这将带来医疗、能源、材料领域的突破，
        还是引发未知的伦理风险？
        
        核心问题：
        1. AI能否设计出自然界不存在的生物系统？
        2. 细胞工厂能否规模化生产任何有机分子？
        3. 人造生命是福还是祸？
        4. 跨学科协作如何加速突破？
        """,
        "topic_type": "open",
        "tags": ["AI", "synthetic-biology", "cross-domain", "2026", "future"],
        "open_config": {
            "keywords": ["AI", "合成生物学", "基因编辑", "跨学科", "生物工程"],
            "domains": ["合成生物学", "人工智能", "生物化学", "伦理学", "系统生物学"],
            "exploration_depth": "deep",
            "initial_perspectives": [
                "AI工程师视角：AI设计生物系统的精确度和效率远超人类",
                "生物学家视角：生物系统的复杂性是最大挑战",
                "伦理学家视角：人造生命需要严格监管框架",
                "化学工程师视角：从实验室到工业化的鸿沟",
                "哲学家视角：生命的定义正在被重新书写"
            ]
        }
    }
    
    topic = topic_storage.create_topic(topic_data)
    print(f"主题已创建: {topic.id}")
    print(f"标题: {topic.title}")
    print(f"类型: 开放主题 (跨学科前瞻)")
    
    return topic


def configure_agents_for_topic(topic_id: str):
    """为主题配置跨学科 Agent"""
    
    agent_configs = [
        {
            "agent_id": "ai_bio_engineer",
            "role": "moderator",
            "name": "AI生物工程师",
            "personality": "创新、务实、跨学科思维",
            "expertise": ["AI算法", "生物工程", "系统设计"],
            "perspective": "AI-driven-biology",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 1.0},
            "system_prompt_addon": "你专注于用AI设计生物系统，见证了AlphaFold、AlphaFold2等突破。你相信AI+生物的组合将创造下一个万亿产业。"
        },
        {
            "agent_id": "synthetic_biologist",
            "role": "expert",
            "name": "合成生物学家",
            "personality": "好奇、严谨、实验导向",
            "expertise": ["基因工程", "代谢工程", "细胞设计"],
            "perspective": "lab-to-market",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.9},
            "system_prompt_addon": "你研究如何用工程化思维设计生物系统，从大肠杆菌生产药物到人工合成细胞。"
        },
        {
            "agent_id": "bioethicist",
            "role": "critic",
            "name": "生物伦理学家",
            "personality": "谨慎、深思熟虑、风险意识",
            "expertise": ["生命伦理学", "风险评估", "公共政策"],
            "perspective": "safety-first",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你关注AI设计生物系统的伦理风险：生物安全、意外释放、伦理边界。你认为创新必须在监管框架内进行。"
        },
        {
            "agent_id": "quantum_chemist",
            "role": "expert",
            "name": "量子化学家",
            "personality": "理论派、追求精确、数学美",
            "expertise": ["量子计算", "分子模拟", "计算化学"],
            "perspective": "molecular-simulation",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.7},
            "system_prompt_addon": "你用量子计算模拟分子结构，发现AI+量子计算能以前所未有的精度预测蛋白质折叠和酶活性。"
        },
        {
            "agent_id": "systems_biologist",
            "role": "expert",
            "name": "系统生物学家",
            "personality": "整体思维、跨尺度整合",
            "expertise": ["网络生物学", "复杂系统", "整合分析"],
            "perspective": "holistic-view",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.7},
            "system_prompt_addon": "你研究生物网络的涌现特性，关心如何从基因到细胞到器官进行多尺度建模。"
        },
        {
            "agent_id": "philosopher",
            "role": "critic",
            "name": "科技哲学家",
            "personality": "质疑、概念清晰、注重本质",
            "expertise": ["科技哲学", "生命科学史", "认识论"],
            "perspective": "conceptual-analysis",
            "participation": {"start_round": 3, "end_round": None, "speak_probability": 0.6},
            "system_prompt_addon": "你追问根本问题：什么是生命？人工生命与自然生命的边界在哪？这不仅是科学问题，更是哲学问题。"
        }
    ]
    
    config_data = {
        "topic_id": topic_id,
        "agents": agent_configs,
        "orchestration": {
            "moderator_agent_id": "ai_bio_engineer",
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
    print("2026年前瞻：AI + 合成生物学 = 下一个生物学革命？")
    print("X" * 20 + "\n")
    
    print("步骤 1: 创建跨学科开放主题...")
    topic = create_cross_domain_topic()
    
    print("\n步骤 2: 配置跨学科 Agent...")
    config = configure_agents_for_topic(topic.id)
    
    print("\n" + "="*60)
    print("设置完成！")
    print("="*60)
    print(f"主题 ID: {topic.id}")
    print(f"Agent 配置 ID: {config.id}")
    print("\n下一步:")
    print("  1. 运行讨论: python3 examples/run_cross_domain_discussion.py")
    print("  2. 生成知识胶囊")
    print("  3. 推送到 CapsuleHub")
    print("="*60 + "\n")
    
    return topic.id


if __name__ == "__main__":
    topic_id = main()
    print(f"\n记住这个主题 ID: {topic_id}")
