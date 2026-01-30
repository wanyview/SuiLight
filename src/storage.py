"""
SuiLight Knowledge Salon - 对话历史持久化
基于 SQLite 的轻量级存储
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "suilight.db")


class StorageManager:
    """
    存储管理器
    
    支持:
    - 对话历史存储
    - 讨论记录存储
    - 知识沉淀存储
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DB_PATH
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 对话历史表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                agent_name TEXT,
                user_message TEXT NOT NULL,
                bot_response TEXT,
                timestamp TEXT,
                metadata TEXT
            )
        """)
        
        # 讨论记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discussion_history (
                id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                title TEXT,
                phase TEXT,
                participants TEXT,
                contributions TEXT,
                insights TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # 知识沉淀表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge沉淀 (
                id TEXT PRIMARY KEY,
                topic_id TEXT,
                agent_id TEXT,
                content TEXT,
                insight_type TEXT,
                confidence REAL,
                created_at TEXT
            )
        """)
        
        # Agent 信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                domain TEXT,
                description TEXT,
                expertise TEXT,
                datm TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        logger.info(f"数据库初始化: {self.db_path}")
    
    # ============ 对话历史 ============
    
    def save_chat(
        self,
        agent_id: str,
        agent_name: str,
        user_message: str,
        bot_response: str,
        metadata: Dict = None
    ) -> str:
        """保存对话"""
        import uuid
        chat_id = str(uuid.uuid4())[:8]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO chat_history 
            (id, agent_id, agent_name, user_message, bot_response, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            chat_id,
            agent_id,
            agent_name,
            user_message,
            bot_response,
            datetime.now().isoformat(),
            json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()
        
        return chat_id
    
    def get_chat_history(
        self,
        agent_id: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """获取对话历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if agent_id:
            cursor.execute("""
                SELECT * FROM chat_history 
                WHERE agent_id = ?
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (agent_id, limit, offset))
        else:
            cursor.execute("""
                SELECT * FROM chat_history 
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ["id", "agent_id", "agent_name", "user_message", "bot_response", 
                   "timestamp", "metadata"]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_chat_by_agent(self, agent_id: str) -> List[Dict]:
        """获取与指定 Agent 的所有对话"""
        return self.get_chat_history(agent_id=agent_id, limit=1000)
    
    def search_chat(self, query: str, limit: int = 20) -> List[Dict]:
        """搜索对话"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM chat_history 
            WHERE user_message LIKE ? OR bot_response LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ["id", "agent_id", "agent_name", "user_message", "bot_response", 
                   "timestamp", "metadata"]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def clear_chat_history(self, agent_id: str = None) -> int:
        """清空对话历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if agent_id:
            cursor.execute("DELETE FROM chat_history WHERE agent_id = ?", (agent_id,))
        else:
            cursor.execute("DELETE FROM chat_history")
        
        count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return count
    
    # ============ 讨论记录 ============
    
    def save_discussion(
        self,
        topic_id: str,
        title: str,
        phase: str,
        participants: List[Dict],
        contributions: List[Dict] = None,
        insights: List[Dict] = None
    ) -> str:
        """保存讨论"""
        import uuid
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否存在
        cursor.execute("SELECT id FROM discussion_history WHERE topic_id = ?", (topic_id,))
        existing = cursor.fetchone()
        
        now = datetime.now().isoformat()
        
        if existing:
            # 更新
            cursor.execute("""
                UPDATE discussion_history
                SET phase = ?, participants = ?, contributions = ?, insights = ?, updated_at = ?
                WHERE topic_id = ?
            """, (
                json.dumps(participants),
                json.dumps(contributions or []),
                json.dumps(insights or []),
                now,
                topic_id
            ))
        else:
            # 插入
            cursor.execute("""
                INSERT INTO discussion_history
                (id, topic_id, title, phase, participants, contributions, insights, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4())[:8],
                topic_id,
                title,
                phase,
                json.dumps(participants),
                json.dumps(contributions or []),
                json.dumps(insights or []),
                now,
                now
            ))
        
        conn.commit()
        conn.close()
        
        return topic_id
    
    def get_discussion_history(self, topic_id: str = None, limit: int = 50) -> List[Dict]:
        """获取讨论历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if topic_id:
            cursor.execute("SELECT * FROM discussion_history WHERE topic_id = ?", (topic_id,))
        else:
            cursor.execute("SELECT * FROM discussion_history ORDER BY updated_at DESC LIMIT ?", (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ["id", "topic_id", "title", "phase", "participants", 
                   "contributions", "insights", "created_at", "updated_at"]
        
        result = []
        for row in rows:
            item = dict(zip(columns, row))
            # 解析 JSON
            item["participants"] = json.loads(item["participants"] or "[]")
            item["contributions"] = json.loads(item["contributions"] or "[]")
            item["insights"] = json.loads(item["insights"] or "[]")
            result.append(item)
        
        return result
    
    # ============ 知识沉淀 ============
    
    def save_insight(
        self,
        topic_id: str,
        agent_id: str,
        content: str,
        insight_type: str = "general",
        confidence: float = 0.5
    ) -> str:
        """保存洞见"""
        import uuid
        insight_id = str(uuid.uuid4())[:8]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO knowledge沉淀
            (id, topic_id, agent_id, content, insight_type, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            insight_id,
            topic_id,
            agent_id,
            content,
            insight_type,
            confidence,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return insight_id
    
    def get_insights(self, topic_id: str = None, limit: int = 100) -> List[Dict]:
        """获取洞见"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if topic_id:
            cursor.execute("""
                SELECT * FROM knowledge沉淀 
                WHERE topic_id = ?
                ORDER BY confidence DESC, created_at DESC
                LIMIT ?
            """, (topic_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM knowledge沉淀 
                ORDER BY confidence DESC, created_at DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ["id", "topic_id", "agent_id", "content", "insight_type", 
                   "confidence", "created_at"]
        
        return [dict(zip(columns, row)) for row in rows]
    
    # ============ Agent 持久化 ============
    
    def save_agent(self, agent: Dict):
        """保存 Agent 信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO agents
            (id, name, domain, description, expertise, datm, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            agent.get("id"),
            agent.get("name"),
            agent.get("domain"),
            agent.get("description"),
            json.dumps(agent.get("expertise", [])),
            json.dumps(agent.get("datm", {})),
            now,
            now
        ))
        
        conn.commit()
        conn.close()
    
    def get_saved_agents(self) -> List[Dict]:
        """获取保存的 Agent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM agents ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        columns = ["id", "name", "domain", "description", "expertise", "datm", "created_at", "updated_at"]
        
        result = []
        for row in rows:
            item = dict(zip(columns, row))
            item["expertise"] = json.loads(item["expertise"] or "[]")
            item["datm"] = json.loads(item["datm"] or "{}")
            result.append(item)
        
        return result
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        chat_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM discussion_history")
        discussion_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM knowledge沉淀")
        insight_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM agents")
        agent_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "chat_count": chat_count,
            "discussion_count": discussion_count,
            "insight_count": insight_count,
            "agent_count": agent_count
        }


# 全局实例
storage = StorageManager()
