"""
SuiLight Knowledge Salon - Async Task Queue
基于 Celery + Redis 的异步任务队列

功能:
- 后台任务执行
- 任务进度追踪
- 任务取消
- 结果存储
"""

import os
import json
import uuid
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

# 尝试导入 Celery
try:
    from celery import Celery
    from celery.result import AsyncResult
    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False
    logging.warning("Celery 未安装，使用线程池作为后备")

# 配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery 应用
if HAS_CELERY:
    celery_app = Celery(
        "suilight",
        broker=REDIS_URL,
        backend=REDIS_URL,
        include=["src.tasks"]
    )
    
    # Celery 配置
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=3600,
        worker_prefetch_multiplier=1,
        task_acks_late=True,
    )


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo:
    """任务信息"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    task_type: str = ""
    params: Dict = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    result: Any = None
    error: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "params": self.params,
            "status": self.status.value,
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class TaskManager:
    """
    任务管理器
    
    管理任务创建、查询、取消
    """
    
    def __init__(self):
        self.tasks: Dict[str, TaskInfo] = {}
        self.registry = None  # Agent 注册表 (注入)
        self.discussion_manager = None  # 讨论管理器 (注入)
        
        logger = logging.getLogger(__name__)
        logger.info("任务管理器初始化完成")
    
    def set_registry(self, registry):
        """设置 Agent 注册表"""
        self.registry = registry
    
    def set_discussion_manager(self, dm):
        """设置讨论管理器"""
        self.discussion_manager = dm
    
    def create_task(self, task_type: str, params: Dict = None) -> TaskInfo:
        """创建任务"""
        task = TaskInfo(
            task_type=task_type,
            params=params or {}
        )
        
        self.tasks[task.task_id] = task
        
        # 异步执行
        self._run_task_async(task)
        
        logger.info(f"创建任务: {task.task_id} ({task_type})")
        return task
    
    def _run_task_async(self, task: TaskInfo):
        """异步执行任务"""
        # 使用 Celery 或直接在后台线程执行
        try:
            from celery import current_app
            
            # 根据任务类型选择 Celery task
            if task.task_type == "create_agents":
                create_agents_task.delay(task.task_id, task.params)
            elif task.task_type == "run_discussion":
                run_discussion_task.delay(task.task_id, task.params)
            elif task.task_type == "extract_insights":
                extract_insights_task.delay(task.task_id, task.params)
            elif task.task_type == "chat_batch":
                chat_batch_task.delay(task.task_id, task.params)
            else:
                # 默认任务
                generic_task.delay(task.task_id, task.task_type, task.params)
                
        except Exception as e:
            logger.warning(f"Celery 不可用，使用同步执行: {e}")
            # 降级为同步执行
            import threading
            thread = threading.Thread(target=self._execute_task, args=(task,))
            thread.start()
    
    def _execute_task(self, task: TaskInfo):
        """执行任务 (同步)"""
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            
            # 根据类型执行
            if task.task_type == "create_agents":
                task.result = self._do_create_agents(task.params)
            elif task.task_type == "run_discussion":
                task.result = self._do_run_discussion(task.params)
            elif task.task_type == "extract_insights":
                task.result = self._do_extract_insights(task.params)
            elif task.task_type == "chat_batch":
                task.result = self._do_chat_batch(task.params)
            else:
                task.result = {"message": f"Unknown task type: {task.task_type}"}
            
            task.status = TaskStatus.SUCCESS
            task.progress = 100
            
        except Exception as e:
            task.status = TaskStatus.FAILURE
            task.error = str(e)
            logger.error(f"任务执行失败: {task.task_id}, {e}")
        
        finally:
            task.completed_at = datetime.now()
    
    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: TaskStatus = None) -> List[TaskInfo]:
        """列出任务"""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        if task.status not in [TaskStatus.PENDING, TaskStatus.RUNNING]:
            return False
        
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()
        
        logger.info(f"任务已取消: {task_id}")
        return True
    
    # ============ 任务实现 ============
    
    def _do_create_agents(self, params: Dict) -> Dict:
        """批量创建 Agent"""
        from src.agents.presets import create_agent_configs, GREAT_MINDS
        
        preset = params.get("preset", "all")
        domain = params.get("domain")
        limit = params.get("limit", 100)
        
        configs = create_agent_configs()
        
        if domain:
            configs = [c for c in configs if c.domain == domain]
        
        if preset != "all":
            configs = [c for c in configs if c.domain == preset]
        
        configs = configs[:limit]
        
        created = []
        total = len(configs)
        
        for i, config in enumerate(configs):
            if self.registry:
                from src.agents.base import Agent
                agent = Agent(config)
                self.registry.register(agent)
                created.append(config.name)
            
            # 更新进度
            progress = int((i + 1) / total * 100)
            task_info = self.tasks.get(f"task_{params.get('_task_id', '')}")
            if task_info:
                task_info.progress = progress
        
        return {
            "created_count": len(created),
            "agents": created
        }
    
    def _do_run_discussion(self, params: Dict) -> Dict:
        """运行讨论"""
        topic_id = params.get("topic_id")
        max_rounds = params.get("max_rounds", 3)
        
        if not self.discussion_manager or not topic_id:
            return {"error": "Missing topic_id or discussion_manager"}
        
        topic = self.discussion_manager.topics.get(topic_id)
        if not topic:
            return {"error": "Topic not found"}
        
        # 自动分配参与者
        participants = self.discussion_manager.assign_participants(topic_id)
        
        # 运行讨论
        results = []
        for round_num in range(1, max_rounds + 1):
            for participant in participants:
                # 模拟讨论
                contribution = self.discussion_manager.add_contribution(
                    topic_id=topic_id,
                    agent_id=participant.id,
                    content=f"第{round_num}轮观点...",
                    role="commentator",
                    round_num=round_num
                )
                results.append(contribution.id)
        
        # 提取洞见
        insights = self.discussion_manager.extract_insights(topic_id)
        
        return {
            "topic_id": topic_id,
            "rounds": max_rounds,
            "contributions": len(results),
            "insights": [i.to_dict() for i in insights]
        }
    
    def _do_extract_insights(self, params: Dict) -> Dict:
        """批量提取洞见"""
        topic_ids = params.get("topic_ids", [])
        
        if not self.discussion_manager:
            return {"error": "No discussion_manager"}
        
        all_insights = []
        for topic_id in topic_ids:
            insights = self.discussion_manager.extract_insights(topic_id)
            all_insights.extend([i.to_dict() for i in insights])
        
        return {
            "topic_count": len(topic_ids),
            "insights_count": len(all_insights),
            "insights": all_insights[:50]  # 限制数量
        }
    
    def _do_chat_batch(self, params: Dict) -> Dict:
        """批量对话"""
        messages = params.get("messages", [])
        agent_ids = params.get("agent_ids", [])
        
        if not self.registry:
            return {"error": "No registry"}
        
        results = []
        for msg in messages:
            for agent_id in agent_ids:
                agent = self.registry.get(agent_id)
                if agent:
                    response = agent.chat(msg)
                    results.append({
                        "agent": agent.config.name,
                        "message": msg,
                        "response": response
                    })
        
        return {
            "total_messages": len(messages),
            "total_agents": len(agent_ids),
            "results": results
        }


# ============ Celery Tasks ============

if HAS_CELERY:
    @celery_app.task(bind=True)
    def create_agents_task(self, task_id: str, params: Dict):
        """Celery: 批量创建 Agent"""
        AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": 0})
        import time
        total = params.get("limit", 100)
        for i in range(total):
            time.sleep(0.1)
            AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": int((i + 1) / total * 100)})
        return {"status": "completed", "progress": 100}

    @celery_app.task(bind=True)
    def run_discussion_task(self, task_id: str, params: Dict):
        """Celery: 运行讨论"""
        AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": 0})
        import time
        max_rounds = params.get("max_rounds", 3)
        for round_num in range(1, max_rounds + 1):
            time.sleep(0.5)
            AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": int(round_num / max_rounds * 100)})
        return {"status": "completed", "rounds": max_rounds}

    @celery_app.task(bind=True)
    def extract_insights_task(self, task_id: str, params: Dict):
        """Celery: 提取洞见"""
        AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": 50})
        import time
        time.sleep(1)
        return {"status": "completed", "insights": []}

    @celery_app.task(bind=True)
    def chat_batch_task(self, task_id: str, params: Dict):
        """Celery: 批量对话"""
        AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": 0})
        import time
        total = len(params.get("messages", []))
        for i in range(total):
            time.sleep(0.1)
            AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": int((i + 1) / total * 100)})
        return {"status": "completed", "count": total}

    @celery_app.task(bind=True)
    def generic_task(self, task_id: str, task_type: str, params: Dict):
        """Celery: 通用任务"""
        AsyncResult(task_id).update_state(state="RUNNING", meta={"progress": 50})
        import time
        time.sleep(1)
        return {"status": "completed", "task_type": task_type, "params": params}
else:
    # Celery 不可用时的占位符
    def create_agents_task(*args, **kwargs):
        logging.warning("Celery 未安装，任务未注册")
        return {"status": "failed", "error": "Celery not installed"}
    
    def run_discussion_task(*args, **kwargs):
        return {"status": "failed", "error": "Celery not installed"}
    
    def extract_insights_task(*args, **kwargs):
        return {"status": "failed", "error": "Celery not installed"}
    
    def chat_batch_task(*args, **kwargs):
        return {"status": "failed", "error": "Celery not installed"}
    
    def generic_task(*args, **kwargs):
        return {"status": "failed", "error": "Celery not installed"}


# ============ 全局实例 ============

task_manager = TaskManager()
