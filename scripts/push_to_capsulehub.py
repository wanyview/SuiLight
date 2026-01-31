#!/usr/bin/env python3
"""
将 SuiLight 知识胶囊推送到 CapsuleHub
"""

import sys
import os
import json
import requests
from datetime import datetime

# 配置
CAPSULEHUB_URL = os.getenv("CAPSULEHUB_URL", "http://localhost:8001")
CAPSULEHUB_TOKEN = os.getenv("CAPSULEHUB_TOKEN", "")


def push_capsule_to_capsulehub(capsule):
    """推送胶囊到 CapsuleHub"""
    print(f"\n📤 推送胶囊到 CapsuleHub...")
    print(f"   标题: {capsule['title']}")
    
    try:
        # 构建胶囊数据 - 匹配 CapsuleHub API 结构
        capsule_data = {
            "title": capsule["title"],
            "domain": capsule.get("category", "general").lower(),
            "topics": capsule.get("keywords", []),
            "insight": capsule["insight"],
            "evidence": capsule.get("evidence", []),
            "action_items": capsule.get("action_items", []),
            "datm_score": {
                "truth": capsule.get("dimensions", {}).get("truth_score", 80),
                "goodness": capsule.get("dimensions", {}).get("goodness_score", 80),
                "beauty": capsule.get("dimensions", {}).get("beauty_score", 80),
                "intelligence": capsule.get("dimensions", {}).get("intelligence_score", 80)
            },
            "applicability": "",
            "limitations": [],
            "reproducibility": 0.8,
            "impact_potential": 0.7,
            "source_type": capsule.get("source_type", "discussion"),
            "authors": capsule.get("source_agents", []),
            "license": "MIT"
        }
        
        # 发送到 CapsuleHub API
        response = requests.post(
            f"{CAPSULEHUB_URL}/api/capsules/",
            json=capsule_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ 推送成功！")
            print(f"   Capsule ID: {result['capsule']['id']}")
            return result['capsule']
        else:
            print(f"   ❌ 推送失败: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"   ⚠️ 无法连接到 CapsuleHub ({CAPSULEHUB_URL})")
        print(f"   提示: 请先启动 CapsuleHub 服务")
        return None
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None


def set_featured_capsule(capsule_id, reason=""):
    """设置精选胶囊"""
    from datetime import date
    
    today = date.today().isoformat()
    
    try:
        response = requests.post(
            f"{CAPSULEHUB_URL}/api/capsules/featured/",
            json={
                "capsule_id": capsule_id,
                "date": today,
                "reason": reason
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"   ⭐ 已设置为今日精选！")
            return True
        else:
            print(f"   ⚠️ 设置精选失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ⚠️ 设置精选错误: {e}")
        return False


def calculate_score(dimensions):
    """计算综合评分"""
    if not dimensions:
        return 75
    
    scores = [
        dimensions.get("truth_score", 0),
        dimensions.get("goodness_score", 0),
        dimensions.get("beauty_score", 0),
        dimensions.get("intelligence_score", 0)
    ]
    return sum(scores) / len(scores) if scores else 75


def calculate_grade(dimensions):
    """计算等级"""
    score = calculate_score(dimensions)
    if score >= 80:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 40:
        return "C"
    else:
        return "D"


# 爱迪生电灯泡胶囊数据
EDISON_CAPSULE = {
    "title": "爱迪生发明电灯泡 - 技术路径复现",
    "summary": "通过多轮讨论，复现了1879年爱迪生发明实用电灯泡的关键技术路径",
    "insight": """通过多轮讨论，复现了1879年爱迪生发明实用电灯泡的关键技术路径：

1. 材料突破：碳化竹丝作为灯丝，平衡了成本、耐用性和发光效率
2. 真空技术：高真空环境减缓灯丝氧化，延长寿命至13.5小时
3. 系统工程：需要配套的发电、输电、灯座标准化体系

关键洞见：在1879年技术条件下，碳化竹丝是综合最优解，而非铂金等贵金属。""",
    "evidence": [
        "测试了超过3000种材料",
        "碳化竹丝在真空中持续点亮13.5小时",
        "需要配套的直流电力系统",
        "标准化生产是商业化关键"
    ],
    "action_items": [
        "建立竹子碳化处理工艺标准",
        "设计通用灯泡接口和灯座",
        "在城市中心建设发电站",
        "开发保险丝等安全装置"
    ],
    "keywords": ["invention", "electricity", "edison", "light-bulb", "industrial-revolution"],
    "source_agents": ["托马斯·爱迪生", "化学家", "物理学家", "电气工程师", "评论家"],
    "category": "technology",
    "dimensions": {
        "truth_score": 90,
        "goodness_score": 85,
        "beauty_score": 78,
        "intelligence_score": 92
    }
}


# 牛顿万有引力胶囊数据
NEWTON_CAPSULE = {
    "title": "牛顿发现万有引力定律 - 天地统一的物理学",
    "summary": "通过多轮讨论，复现了1666年牛顿发现万有引力定律的思维过程",
    "insight": """通过多轮讨论，复现了1666年牛顿发现万有引力定律的关键发现：

1. 问题洞察：苹果落地与月亮绕地是同一原因——地球的引力
2. 数学推导：假设引力与距离平方成反比，结合向心力公式
3. 月地检验：计算值与观测值吻合，验证假设正确
4. 统一天地：开普勒行星定律可由万有引力定律推导

核心洞见：支配苹果落地的力，与支配月亮绕地的力，是同一种力——这标志着物理学从"天地分离"走向"天地统一"。""",
    "evidence": [
        "月球轨道半径384,000公里，周期27.3天",
        "计算得向心加速度 0.0027 m/s²",
        "与平方反比定律预测值完全吻合",
        "木星卫星运动也遵循同样规律",
        "潮汐现象可由日月引力解释"
    ],
    "action_items": [
        "测量万有引力常数G（后人完成：卡文迪什1798年）",
        "将引力定律推广到太阳系所有行星",
        "解释潮汐现象的定量规律",
        "后续研究：引力的本质是什么？"
    ],
    "keywords": ["newton", "gravity", "physics", "celestial-mechanics", "unification"],
    "source_agents": ["艾萨克·牛顿", "数学家", "天文学家", "力学家", "自然哲学家"],
    "category": "physics",
    "dimensions": {
        "truth_score": 95,
        "goodness_score": 90,
        "beauty_score": 85,
        "intelligence_score": 98
    }
}


def main():
    """主流程"""
    print("\n" + "🚀" * 20)
    print("SuiLight → CapsuleHub 推送工具")
    print("🚀" * 20 + "\n")
    
    # 推送爱迪生胶囊
    print("\n📦 胶囊 1: 爱迪生发明电灯泡")
    edison_result = push_capsule_to_capsulehub(EDISON_CAPSULE)
    if edison_result:
        set_featured_capsule(edison_result["id"], "SuiLight 限定主题讨论首发")
    
    # 推送牛顿胶囊
    print("\n📦 胶囊 2: 牛顿发现万有引力")
    newton_result = push_capsule_to_capsulehub(NEWTON_CAPSULE)
    if newton_result:
        set_featured_capsule(newton_result["id"], "SuiLight 限定主题讨论首发")
    
    # 推送2026前瞻胶囊
    print("\n📦 胶囊 3: 2026年前瞻 - AI能否发现科学定律")
    futures_result = push_capsule_to_capsulehub(FUTURES_CAPSULE)
    if futures_result:
        set_featured_capsule(futures_result["id"], "SuiLight 开放主题讨论首发")
    
    print("\n" + "="*60)
    print("✅ 推送完成！")
    print("="*60)
    print("\n访问 CapsuleHub 查看:")
    print(f"  {CAPSULEHUB_URL}/")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()


# 2026年前瞻胶囊数据
FUTURES_CAPSULE = {
    "title": "2026年前瞻：AI能否自主发现科学定律？",
    "summary": "基于2026年技术背景，探讨AI在科学发现中的角色与潜力",
    "insight": """基于2026年AI发展水平，本次讨论得出以下核心结论：

1. AI的当前能力：在模式识别、数据分析、假设验证方面超越人类；在概念迁移、范式转换方面仍有局限

2. AI的独特优势：发现隐藏的相关性（粒子物理异常）、自动化实验流程、大规模数据挖掘

3. 核心共识：AI正在成为科学发现的加速器，而非替代者。人类+AI协作模式将主导未来

4. 未来预测：
   - 短期（5年）：AI辅助假设生成和实验设计
   - 中期（10年）：AI在药物、材料、数学猜想领域实现渐进式发现
   - 长期：范式转换级别的突破可能仍需人类智慧

5. 待解决问题：AI能否提出正确的问题？什么是理解的本质？""",
    "evidence": [
        "AlphaFold预测2亿种蛋白质结构",
        "AlphaGeometry解决IMO几何问题",
        "机器人科学家自动提出假设、设计实验、分析结果",
        "GPT-4展示跨领域推理和概念迁移能力",
        "AI在粒子物理数据分析中发现人类忽略的微小异常"
    ],
    "action_items": [
        "建立AI辅助科学发现的评估框架（假设生成、实验设计、结果解释）",
        "发展人机协作的新科学方法论",
        "探索AI在基础科学研究中的新应用场景",
        "研究与理解的本质差异",
        "培养兼具AI技能和领域专长的新一代科学家"
    ],
    "keywords": ["AI", "科学发现", "自动化科学", "人机协作", "未来预测"],
    "source_agents": ["AI研究员", "科学哲学家", "理论物理学家", "计算生物学家", "认知科学家", "AI工程师"],
    "category": "AI",
    "dimensions": {
        "truth_score": 88,
        "goodness_score": 92,
        "beauty_score": 80,
        "intelligence_score": 90
    }

def main():
    """主流程"""
    print("\n" + "🚀" * 20)
    print("SuiLight → CapsuleHub 推送工具")
    print("🚀" * 20 + "\n")
    
    # 推送爱迪生胶囊
    print("\n📦 胶囊 1: 爱迪生发明电灯泡")
    edison_result = push_capsule_to_capsulehub(EDISON_CAPSULE)
    if edison_result:
        set_featured_capsule(edison_result["id"], "SuiLight 限定主题讨论首发")
    
    # 推送牛顿胶囊
    print("\n📦 胶囊 2: 牛顿发现万有引力")
    newton_result = push_capsule_to_capsulehub(NEWTON_CAPSULE)
    if newton_result:
        set_featured_capsule(newton_result["id"], "SuiLight 限定主题讨论首发")
    
    # 推送2026前瞻胶囊
    print("\n📦 胶囊 3: 2026年前瞻 - AI能否发现科学定律")
    futures_result = push_capsule_to_capsulehub(FUTURES_CAPSULE)
    if futures_result:
        set_featured_capsule(futures_result["id"], "SuiLight 开放主题讨论首发")
    
    print("\n" + "="*60)
    print("✅ 推送完成！")
    print("="*60)
    print("\n访问 CapsuleHub 查看:")
    print(f"  {CAPSULEHUB_URL}/")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
