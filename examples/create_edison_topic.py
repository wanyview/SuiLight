#!/usr/bin/env python3
"""
SuiLight 示例脚本
创建限定主题讨论，生成知识胶囊，推送到 CapsuleHub
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.discussions import (
    topic_storage, agent_config_storage, discussion_storage,
    DiscussionTopic, TopicType, TopicStatus,
    AgentConfiguration, AgentConfig, AgentRole, OrchestrationConfig,
    AGENT_TEMPLATES
)


def create_edison_bulb_topic():
    """创建爱迪生发明电灯泡的限定主题"""
    
    topic_data = {
        "title": "复现：爱迪生发明电灯泡",
        "description": """
        在1879年的美国新泽西州门洛帕克实验室，
        还原托马斯·爱迪生发明实用电灯泡的历史过程。
        
        探讨的核心问题：
        1. 在当时的科技水平下，如何解决灯丝材料的选择？
        2. 真空技术如何影响灯泡寿命？
        3. 直流电力系统如何配套？
        4. 商业化推广面临哪些挑战？
        """,
        "topic_type": "restricted",
        "tags": ["history", "invention", "electricity", "edison"],
        "restricted_config": {
            "historical_context": {
                "era": "第二次工业革命",
                "year": 1879,
                "location": "美国新泽西州门洛帕克实验室",
                "description": """
                第二次工业革命时期，电气化时代刚刚开启。
                煤气灯仍是主流照明方式，电力照明具有巨大的市场潜力。
                爱迪生正在寻找一种实用、廉价的电灯方案。
                """
            },
            "technical_context": {
                "pre_conditions": [
                    "已知电流可以产生光热效应",
                    "已知金属在高温下会发光",
                    "已知真空环境可以减缓氧化",
                    "已知需要绝缘材料",
                    "已知需要稳定的电力来源"
                ],
                "constraints": [
                    "只能使用19世纪末的已知材料和工艺",
                    "灯丝必须在空气中持续发光至少数小时",
                    "成本需要低于煤气灯",
                    "无法使用后来的钨丝工艺"
                ],
                "available_resources": [
                    "铂金、铱等贵金属",
                    "碳化竹丝",
                    "玻璃吹制技术",
                    "真空泵技术",
                    "直流发电机",
                    "铜线传输",
                    "各类金属丝（铂、铱、钯、碳化纸等）"
                ],
                "tech_level": "1879年技术水平"
            },
            "goal": {
                "description": "探讨并还原爱迪生发明实用电灯泡的技术路径和关键突破",
                "success_criteria": [
                    "明确灯丝材料的选择逻辑",
                    "解释真空技术的作用",
                    "说明如何解决灯座和开关问题",
                    "描述商业化推广策略"
                ],
                "expected_outcomes": [
                    "电灯泡工作原理的知识胶囊",
                    "灯丝材料选择的决策过程",
                    "真空技术的关键作用",
                    "商业化路径分析"
                ]
            },
            "setting_narrative": """
            1879年，门洛帕克实验室。
            
            爱迪生已经尝试了数千种材料来制作灯丝。
            他明白，要让电灯取代煤气灯，必须满足：
            - 持续发光数百小时
            - 成本低廉
            - 安全可靠
            
            团队正在分析之前失败的原因，讨论下一步的实验方向。
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
            "agent_id": "edison",
            "role": "moderator",
            "name": "托马斯·爱迪生",
            "personality": "坚韧不拔、实用主义、不断实验",
            "expertise": ["发明创造", "电气工程", "商业化"],
            "perspective": "solution-oriented",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 1.0},
            "system_prompt_addon": "你作为爱迪生，领导门洛帕克实验室。你已经尝试了数千种材料，需要团队讨论下一步方案。"
        },
        {
            "agent_id": "chemist",
            "role": "expert",
            "name": "化学家",
            "personality": "严谨、科学、注重元素特性",
            "expertise": ["材料化学", "元素周期表", "金属性质"],
            "perspective": "science-based",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你负责分析各种材料的化学性质，为灯丝材料选择提供科学依据。"
        },
        {
            "agent_id": "physicist",
            "role": "expert",
            "name": "物理学家",
            "personality": "理论派、善于分析物理原理",
            "expertise": ["热力学", "电磁学", "真空技术"],
            "perspective": "theory-based",
            "participation": {"start_round": 1, "end_round": None, "speak_probability": 0.8},
            "system_prompt_addon": "你负责解释电光转换的物理原理，分析真空环境对灯泡寿命的影响。"
        },
        {
            "agent_id": "electrician",
            "role": "expert",
            "name": "电气工程师",
            "personality": "实用派、注重系统整合",
            "expertise": ["直流电路", "电力系统", "电机工程"],
            "perspective": "system-integrator",
            "participation": {"start_round": 2, "end_round": None, "speak_probability": 0.7},
            "system_prompt_addon": "你负责设计电力传输系统，确保灯泡能获得稳定的电流供应。"
        },
        {
            "agent_id": "critic",
            "role": "critic",
            "name": "评论家",
            "personality": "质疑、保守、代表反对声音",
            "expertise": ["市场分析", "成本控制", "竞争对手"],
            "perspective": "skeptical",
            "participation": {"start_round": 3, "end_round": None, "speak_probability": 0.6},
            "system_prompt_addon": "你代表质疑者，挑战方案的可行性和商业价值。"
        }
    ]
    
    config_data = {
        "topic_id": topic_id,
        "agents": agent_configs,
        "orchestration": {
            "moderator_agent_id": "edison",
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


def print_topic_summary(topic: DiscussionTopic):
    """打印主题摘要"""
    print("\n" + "="*60)
    print("📋 主题摘要")
    print("="*60)
    print(f"标题: {topic.title}")
    print(f"描述: {topic.description[:100]}...")
    print(f"类型: {'限定主题' if topic.topic_type == 'restricted' else '开放主题'}")
    print(f"状态: {topic.status}")
    
    if topic.restricted_config:
        ctx = topic.restricted_config
        print(f"\n📅 历史背景:")
        print(f"   时代: {ctx.historical_context.era}")
        print(f"   年份: {ctx.historical_context.year}")
        print(f"   地点: {ctx.historical_context.location}")
        
        print(f"\n🔧 技术背景:")
        print(f"   水平: {ctx.technical_context.tech_level}")
        print(f"   前置条件: {len(ctx.technical_context.pre_conditions)} 项")
        print(f"   限制条件: {len(ctx.technical_context.constraints)} 项")
        print(f"   可用资源: {len(ctx.technical_context.available_resources)} 项")
        
        print(f"\n🎯 目标:")
        print(f"   描述: {ctx.goal.description[:50]}...")
        print(f"   成功标准: {len(ctx.goal.success_criteria)} 项")
        print(f"   预期产出: {len(ctx.goal.expected_outcomes)} 项")
    
    print("="*60 + "\n")


def main():
    """主流程"""
    print("\n" + "🚀" * 20)
    print("SuiLight 限定主题示例")
    print("爱迪生发明电灯泡 - 知识胶囊生成")
    print("🚀" * 20 + "\n")
    
    # 1. 创建限定主题
    print("📝 步骤 1: 创建限定主题...")
    topic = create_edison_bulb_topic()
    
    # 2. 打印主题摘要
    print_topic_summary(topic)
    
    # 3. 配置参与 Agent
    print("🤖 步骤 2: 配置参与 Agent...")
    config = configure_agents_for_topic(topic.id)
    
    # 4. 启动讨论
    print("🎬 步骤 3: 启动讨论...")
    try:
        from src.discussions import router as discussions_router
        print("讨论系统已就绪，可通过 API 启动")
    except Exception as e:
        print(f"注意: {e}")
    
    print("\n" + "="*60)
    print("✅ 设置完成！")
    print("="*60)
    print(f"主题 ID: {topic.id}")
    print(f"Agent 配置 ID: {config.id}")
    print("\n下一步:")
    print("  1. 启动讨论: POST /api/discussions/topics/{topic_id}/start")
    print("  2. 添加消息: POST /api/discussions/{discussion_id}/messages")
    print("  3. 完成讨论: POST /api/discussions/{discussion_id}/complete")
    print("  4. 生成胶囊: 在讨论完成后自动生成")
    print("\n或运行 SuiLight 服务，通过 Web UI 管理")
    print("="*60 + "\n")
    
    return topic.id


if __name__ == "__main__":
    topic_id = main()
    print(f"\n📌 记住这个主题 ID: {topic_id}")
