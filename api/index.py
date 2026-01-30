"""
SuiLight Knowledge Salon - Vercel Serverless API

这个版本适配 Vercel Serverless Functions
"""

import os
import json
from typing import Dict, List, Optional

# 简化的内存存储 (Serverless 环境)
agents_db = {}
discussions_db = {}
tasks_db = {}
capsules_db = {}

# 响应模板
def json_response(data, status=200):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(data, ensure_ascii=False)
    }


def cors_response():
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({"message": "OK"})
    }


# ============ Agent API ============

def list_agents():
    return json_response({
        "success": True,
        "data": {
            "total": len(agents_db),
            "agents": list(agents_db.values())
        }
    })


def create_agent(body):
    agent_id = body.get("id", f"agent_{len(agents_db) + 1}")
    agent = {
        "id": agent_id,
        "name": body.get("name", "未命名"),
        "domain": body.get("domain", "general"),
        "description": body.get("description", ""),
        "expertise": body.get("expertise", []),
        "datm": body.get("datm", {
            "truth": 50,
            "goodness": 50,
            "beauty": 50,
            "intelligence": 50
        }),
        "status": "idle"
    }
    agents_db[agent_id] = agent
    return json_response({
        "success": True,
        "data": agent
    })


def chat(body):
    agent_id = body.get("agent_id")
    message = body.get("message", "")
    
    if agent_id not in agents_db:
        return json_response({"error": "Agent 不存在"}, 404)
    
    agent = agents_db[agent_id]
    name = agent.get("name", "Agent")
    
    # 简单回复 (实际应调用 LLM)
    response = f"【{name}】收到: {message}\n\n(这是 Vercel Serverless 版本)"
    
    return json_response({
        "success": True,
        "data": {
            "agent_id": agent_id,
            "agent_name": name,
            "response": response,
            "datm": agent.get("datm", {})
        }
    })


# ============ Discussion API ============

def list_discussions():
    return json_response({
        "success": True,
        "data": list(discussions_db.values())
    })


def create_discussion(body):
    topic_id = f"topic_{len(discussions_db) + 1}"
    topic = {
        "id": topic_id,
        "title": body.get("title", "未命名"),
        "description": body.get("description", ""),
        "category": body.get("category", "交叉科学"),
        "status": "active"
    }
    discussions_db[topic_id] = topic
    return json_response({
        "success": True,
        "data": topic
    })


def get_discussion(topic_id):
    if topic_id not in discussions_db:
        return json_response({"error": "讨论不存在"}, 404)
    return json_response({
        "success": True,
        "data": discussions_db[topic_id]
    })


def start_discussion(topic_id):
    if topic_id not in discussions_db:
        return json_response({"error": "讨论不存在"}, 404)
    
    discussions_db[topic_id]["status"] = "running"
    return json_response({
        "success": True,
        "data": {
            "message": "讨论已开始",
            "topic": discussions_db[topic_id]
        }
    })


# ============ Capsule API ============

def generate_capsule(body):
    """从讨论生成知识胶囊"""
    topic_id = body.get("topic_id")
    title = body.get("title", "知识胶囊")
    insights = body.get("insights", [])
    
    # 生成胶囊
    capsule = {
        "id": f"capsule_{len(capsules_db) + 1}",
        "title": f"关于「{title}」的知识胶囊",
        "insight": insights[0] if insights else "暂无洞见",
        "evidence": [],
        "action_items": [],
        "dimensions": {
            "truth": 60,
            "goodness": 55,
            "beauty": 50,
            "intelligence": 70
        },
        "quality_score": 58.75,
        "grade": "C",
        "created_at": "2026-01-30"
    }
    
    capsules_db[capsule["id"]] = capsule
    
    return json_response({
        "success": True,
        "data": capsule
    })


def list_capsules():
    return json_response({
        "success": True,
        "data": {
            "total": len(capsules_db),
            "capsules": list(capsules_db.values())
        }
    })


# ============ 预设 Agent ============

def get_presets():
    """100位思想家预设 (简版)"""
    presets = [
        {"name": "艾萨克·牛顿", "domain": "physics", "datm": {"truth": 100, "goodness": 70, "beauty": 65, "intelligence": 95}},
        {"name": "阿尔伯特·爱因斯坦", "domain": "physics", "datm": {"truth": 95, "goodness": 65, "beauty": 70, "intelligence": 100}},
        {"name": "查尔斯·达尔文", "domain": "biology", "datm": {"truth": 95, "goodness": 75, "beauty": 70, "intelligence": 90}},
        {"name": "亚当·斯密", "domain": "economics", "datm": {"truth": 85, "goodness": 75, "beauty": 65, "intelligence": 90}},
        {"name": "西格蒙德·弗洛伊德", "domain": "psychology", "datm": {"truth": 70, "goodness": 60, "beauty": 80, "intelligence": 90}},
        {"name": "孔子", "domain": "philosophy", "datm": {"truth": 80, "goodness": 95, "beauty": 85, "intelligence": 85}},
        {"name": "苏格拉底", "domain": "philosophy", "datm": {"truth": 90, "goodness": 90, "beauty": 85, "intelligence": 95}},
        {"name": "托马斯·爱迪生", "domain": "engineering", "datm": {"truth": 80, "goodness": 65, "beauty": 55, "intelligence": 95}},
    ]
    return json_response({
        "success": True,
        "data": {
            "total": len(presets),
            "presets": presets
        }
    })


def create_all_agents():
    """创建所有预设 Agent"""
    created = []
    for p in [
        {"name": "艾萨克·牛顿", "domain": "physics", "datm": {"truth": 100, "goodness": 70, "beauty": 65, "intelligence": 95}},
        {"name": "阿尔伯特·爱因斯坦", "domain": "physics", "datm": {"truth": 95, "goodness": 65, "beauty": 70, "intelligence": 100}},
        {"name": "查尔斯·达尔文", "domain": "biology", "datm": {"truth": 95, "goodness": 75, "beauty": 70, "intelligence": 90}},
        {"name": "亚当·斯密", "domain": "economics", "datm": {"truth": 85, "goodness": 75, "beauty": 65, "intelligence": 90}},
        {"name": "西格蒙德·弗洛伊德", "domain": "psychology", "datm": {"truth": 70, "goodness": 60, "beauty": 80, "intelligence": 90}},
        {"name": "孔子", "domain": "philosophy", "datm": {"truth": 80, "goodness": 95, "beauty": 85, "intelligence": 85}},
        {"name": "苏格拉底", "domain": "philosophy", "datm": {"truth": 90, "goodness": 90, "beauty": 85, "intelligence": 95}},
        {"name": "托马斯·爱迪生", "domain": "engineering", "datm": {"truth": 80, "goodness": 65, "beauty": 55, "intelligence": 95}},
    ]:
        agent_id = f"agent_{len(agents_db) + 1}"
        agent = {
            "id": agent_id,
            "name": p["name"],
            "domain": p["domain"],
            "description": f"{p['name']} - {p['domain']} 领域专家",
            "expertise": [],
            "datm": p["datm"],
            "status": "idle"
        }
        agents_db[agent_id] = agent
        created.append(agent)
    
    return json_response({
        "success": True,
        "data": {
            "created": len(created),
            "agents": created
        }
    })


# ============ 路由处理 ============

ROUTES = {
    # Agent
    ("GET", "/api/agents"): list_agents,
    ("POST", "/api/agents"): lambda: create_agent({}),
    ("POST", "/api/chat"): lambda: chat({}),
    
    # Discussion
    ("GET", "/api/discussions"): list_discussions,
    ("POST", "/api/discussions"): lambda: create_discussion({}),
    ("GET", "/api/discussions/{id}"): lambda: get_discussion(""),
    ("POST", "/api/discussions/{id}/start"): lambda: start_discussion(""),
    ("POST", "/api/discussions/{id}/generate_capsule"): lambda: generate_capsule({}),
    
    # Capsule
    ("GET", "/api/capsules"): list_capsules,
    ("POST", "/api/capsules"): lambda: generate_capsule({}),
    
    # Presets
    ("GET", "/api/presets"): get_presets,
    ("POST", "/api/presets/create_all"): create_all_agents,
    
    # Root
    ("GET", "/"): lambda: json_response({
        "name": "SuiLight Knowledge Salon",
        "version": "1.0.0",
        "status": "running on Vercel",
        "message": "知识沙龙多智能体系统",
        "endpoints": [
            "GET /api/agents",
            "POST /api/agents",
            "POST /api/chat",
            "GET /api/discussions",
            "POST /api/discussions",
            "GET /api/capsules",
            "POST /api/capsules",
            "GET /api/presets"
        ]
    }),
}


def handler(event, context):
    """Vercel Serverless Handler"""
    method = event.get("httpMethod", "GET")
    path = event.get("path", "/")
    
    # CORS 预检
    if method == "OPTIONS":
        return cors_response()
    
    # 查找路由
    key = (method, path)
    handler_func = ROUTES.get(key)
    
    if handler_func:
        try:
            if method in ["POST", "PUT", "PATCH"]:
                body = json.loads(event.get("body", "{}"))
                return handler_func(body)
            else:
                return handler_func()
        except Exception as e:
            return json_response({"error": str(e)}, 500)
    
    # 路径参数处理
    if "/api/discussions/" in path and method == "GET":
        topic_id = path.split("/")[-1]
        return get_discussion(topic_id)
    
    if "/api/discussions/" in path and method == "POST":
        # POST /api/discussions/{id}/start
        if "/start" in path:
            topic_id = path.split("/")[-2]
            return start_discussion(topic_id)
        # POST /api/discussions/{id}/generate_capsule
        if "/generate" in path:
            topic_id = path.split("/")[-2]
            return generate_capsule({"topic_id": topic_id})
    
    return json_response({"error": "Not Found", "path": path}, 404)
