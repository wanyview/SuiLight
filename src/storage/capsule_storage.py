"""
SuiLight Knowledge Salon - SQLite 胶囊存储模块

功能:
- 知识胶囊的持久化存储
- 历史复现胶囊管理
- 知识胶囊查询和检索
- 自动创建数据库和表
"""

import sqlite3
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CapsuleStorage:
    """
    SQLite 胶囊存储管理器
    
    支持:
    - 历史复现胶囊
    - 知识胶囊
    - 胶囊 CRUD 操作
    - 多维度查询
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化存储管理器
        
        Args:
            db_path: 数据库路径，如果为 None 则使用默认路径
        """
        if db_path is None:
            # 默认数据库路径
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(base_dir, "data", "capsules.db")
        
        self.db_path = db_path
        self._ensure_db_exists()
        logger.info(f"胶囊存储初始化完成: {db_path}")
    
    def _ensure_db_exists(self):
        """确保数据库和表存在"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 知识胶囊表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_capsules (
                    id TEXT PRIMARY KEY,
                    topic_id TEXT,
                    title TEXT NOT NULL,
                    summary TEXT,
                    insight TEXT,
                    evidence TEXT,          -- JSON 数组
                    action_items TEXT,      -- JSON 数组
                    questions TEXT,         -- JSON 数组
                    dimensions TEXT,        -- JSON 对象
                    source_agents TEXT,     -- JSON 数组
                    keywords TEXT,          -- JSON 数组
                    category TEXT,
                    status TEXT DEFAULT 'draft',
                    confidence REAL DEFAULT 0.0,
                    quality_score REAL DEFAULT 0.0,
                    version INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # 历史复现胶囊表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historical_replication_capsules (
                    id TEXT PRIMARY KEY,
                    original_agent TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    era TEXT,
                    topic_id TEXT,
                    title TEXT NOT NULL,
                    summary TEXT,
                    insight TEXT,
                    evidence TEXT,          -- JSON 数组
                    action_items TEXT,      -- JSON 数组
                    questions TEXT,         -- JSON 数组
                    dimensions TEXT,        -- JSON 对象
                    source_agents TEXT,     -- JSON 数组
                    keywords TEXT,          -- JSON 数组
                    category TEXT,
                    status TEXT DEFAULT 'draft',
                    confidence REAL DEFAULT 0.0,
                    quality_score REAL DEFAULT 0.0,
                    replication_quality REAL DEFAULT 0.0,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # 胶囊模板表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS capsule_templates (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT,
                    description TEXT,
                    fields TEXT,            -- JSON 数组
                    example TEXT,           -- JSON 对象
                    usage_count INTEGER DEFAULT 0,
                    created_at TEXT
                )
            """)
            
            # 胶囊版本历史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS capsule_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    capsule_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    changes TEXT,
                    editor TEXT,
                    edited_at TEXT,
                    content_snapshot TEXT,  -- JSON 对象
                    FOREIGN KEY (capsule_id) REFERENCES knowledge_capsules(id)
                )
            """)
            
            conn.commit()
            logger.info("数据库表初始化完成")
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            conn.close()
    
    def _json_dumps(self, obj: Any) -> str:
        """安全地将对象转换为 JSON 字符串"""
        if obj is None:
            return None
        try:
            return json.dumps(obj, ensure_ascii=False)
        except (TypeError, ValueError):
            return json.dumps(str(obj), ensure_ascii=False)
    
    def _json_loads(self, json_str: str) -> Any:
        """安全地将 JSON 字符串转换为对象"""
        if json_str is None:
            return None
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return str(json_str)
    
    # ============= 知识胶囊 CRUD =============
    
    def save_knowledge_capsule(self, capsule: Dict) -> bool:
        """
        保存知识胶囊
        
        Args:
            capsule: 胶囊数据字典
            
        Returns:
            是否保存成功
        """
        now = datetime.now().isoformat()
        
        # 确保必要字段
        if "id" not in capsule:
            capsule["id"] = f"kc_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if "created_at" not in capsule:
            capsule["created_at"] = now
        capsule["updated_at"] = now
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO knowledge_capsules
                (id, topic_id, title, summary, insight, evidence, action_items,
                 questions, dimensions, source_agents, keywords, category,
                 status, confidence, quality_score, version, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                capsule.get("id"),
                capsule.get("topic_id"),
                capsule.get("title"),
                capsule.get("summary"),
                capsule.get("insight"),
                self._json_dumps(capsule.get("evidence")),
                self._json_dumps(capsule.get("action_items")),
                self._json_dumps(capsule.get("questions")),
                self._json_dumps(capsule.get("dimensions")),
                self._json_dumps(capsule.get("source_agents")),
                self._json_dumps(capsule.get("keywords")),
                capsule.get("category"),
                capsule.get("status", "draft"),
                capsule.get("confidence", 0.0),
                capsule.get("quality_score", 0.0),
                capsule.get("version", 1),
                capsule.get("created_at"),
                capsule.get("updated_at")
            ))
            
            logger.info(f"保存知识胶囊: {capsule.get('id')}")
            return True
    
    def get_knowledge_capsule(self, capsule_id: str) -> Optional[Dict]:
        """
        获取知识胶囊
        
        Args:
            capsule_id: 胶囊 ID
            
        Returns:
            胶囊数据字典，不存在则返回 None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM knowledge_capsules WHERE id = ?",
                (capsule_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return self._row_to_capsule_dict(row)
    
    def list_knowledge_capsules(
        self,
        category: str = None,
        status: str = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """
        列出知识胶囊
        
        Args:
            category: 分类过滤
            status: 状态过滤
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            胶囊列表
        """
        query = "SELECT * FROM knowledge_capsules WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_capsule_dict(row) for row in rows]
    
    def delete_knowledge_capsule(self, capsule_id: str) -> bool:
        """
        删除知识胶囊
        
        Args:
            capsule_id: 胶囊 ID
            
        Returns:
            是否删除成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM knowledge_capsules WHERE id = ?",
                (capsule_id,)
            )
            
            logger.info(f"删除知识胶囊: {capsule_id}")
            return cursor.rowcount > 0
    
    def _row_to_capsule_dict(self, row: sqlite3.Row) -> Dict:
        """将数据库行转换为胶囊字典"""
        return {
            "id": row["id"],
            "topic_id": row["topic_id"],
            "title": row["title"],
            "summary": row["summary"],
            "insight": row["insight"],
            "evidence": self._json_loads(row["evidence"]),
            "action_items": self._json_loads(row["action_items"]),
            "questions": self._json_loads(row["questions"]),
            "dimensions": self._json_loads(row["dimensions"]),
            "source_agents": self._json_loads(row["source_agents"]),
            "keywords": self._json_loads(row["keywords"]),
            "category": row["category"],
            "status": row["status"],
            "confidence": row["confidence"],
            "quality_score": row["quality_score"],
            "version": row["version"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    
    # ============= 历史复现胶囊 CRUD =============
    
    def save_historical_capsule(self, capsule: Dict) -> bool:
        """
        保存历史复现胶囊
        
        Args:
            capsule: 胶囊数据字典
            
        Returns:
            是否保存成功
        """
        now = datetime.now().isoformat()
        
        if "id" not in capsule:
            capsule["id"] = f"hc_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if "created_at" not in capsule:
            capsule["created_at"] = now
        capsule["updated_at"] = now
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO historical_replication_capsules
                (id, original_agent, agent_name, era, topic_id, title, summary,
                 insight, evidence, action_items, questions, dimensions,
                 source_agents, keywords, category, status, confidence,
                 quality_score, replication_quality, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                capsule.get("id"),
                capsule.get("original_agent"),
                capsule.get("agent_name"),
                capsule.get("era"),
                capsule.get("topic_id"),
                capsule.get("title"),
                capsule.get("summary"),
                capsule.get("insight"),
                self._json_dumps(capsule.get("evidence")),
                self._json_dumps(capsule.get("action_items")),
                self._json_dumps(capsule.get("questions")),
                self._json_dumps(capsule.get("dimensions")),
                self._json_dumps(capsule.get("source_agents")),
                self._json_dumps(capsule.get("keywords")),
                capsule.get("category"),
                capsule.get("status", "draft"),
                capsule.get("confidence", 0.0),
                capsule.get("quality_score", 0.0),
                capsule.get("replication_quality", 0.0),
                capsule.get("created_at"),
                capsule.get("updated_at")
            ))
            
            logger.info(f"保存历史复现胶囊: {capsule.get('id')}")
            return True
    
    def get_historical_capsule(self, capsule_id: str) -> Optional[Dict]:
        """
        获取历史复现胶囊
        
        Args:
            capsule_id: 胶囊 ID
            
        Returns:
            胶囊数据字典
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM historical_replication_capsules WHERE id = ?",
                (capsule_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return self._row_to_historical_capsule_dict(row)
    
    def list_historical_capsules(
        self,
        agent_name: str = None,
        era: str = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """
        列出历史复现胶囊
        
        Args:
            agent_name: 专家名称过滤
            era: 时代过滤
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            胶囊列表
        """
        query = "SELECT * FROM historical_replication_capsules WHERE 1=1"
        params = []
        
        if agent_name:
            query += " AND agent_name = ?"
            params.append(agent_name)
        if era:
            query += " AND era = ?"
            params.append(era)
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_historical_capsule_dict(row) for row in rows]
    
    def _row_to_historical_capsule_dict(self, row: sqlite3.Row) -> Dict:
        """将数据库行转换为历史胶囊字典"""
        return {
            "id": row["id"],
            "original_agent": row["original_agent"],
            "agent_name": row["agent_name"],
            "era": row["era"],
            "topic_id": row["topic_id"],
            "title": row["title"],
            "summary": row["summary"],
            "insight": row["insight"],
            "evidence": self._json_loads(row["evidence"]),
            "action_items": self._json_loads(row["action_items"]),
            "questions": self._json_loads(row["questions"]),
            "dimensions": self._json_loads(row["dimensions"]),
            "source_agents": self._json_loads(row["source_agents"]),
            "keywords": self._json_loads(row["keywords"]),
            "category": row["category"],
            "status": row["status"],
            "confidence": row["confidence"],
            "quality_score": row["quality_score"],
            "replication_quality": row["replication_quality"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    
    # ============= 通用胶囊接口 =============
    
    def save_capsule(self, capsule: Dict, capsule_type: str = "knowledge") -> bool:
        """
        通用保存胶囊接口
        
        Args:
            capsule: 胶囊数据
            capsule_type: 胶囊类型 ("knowledge" 或 "historical")
            
        Returns:
            是否保存成功
        """
        if capsule_type == "historical":
            return self.save_historical_capsule(capsule)
        else:
            return self.save_knowledge_capsule(capsule)
    
    def get_capsule(self, capsule_id: str, capsule_type: str = "knowledge") -> Optional[Dict]:
        """
        通用获取胶囊接口
        
        Args:
            capsule_id: 胶囊 ID
            capsule_type: 胶囊类型
            
        Returns:
            胶囊数据
        """
        if capsule_type == "historical":
            return self.get_historical_capsule(capsule_id)
        else:
            return self.get_knowledge_capsule(capsule_id)
    
    def list_capsules(
        self,
        capsule_type: str = "knowledge",
        **kwargs
    ) -> List[Dict]:
        """
        通用列出胶囊接口
        
        Args:
            capsule_type: 胶囊类型
            **kwargs: 其他过滤参数
            
        Returns:
            胶囊列表
        """
        if capsule_type == "historical":
            return self.list_historical_capsules(**kwargs)
        else:
            return self.list_knowledge_capsules(**kwargs)
    
    # ============= 搜索功能 =============
    
    def search_capsules(
        self,
        query: str,
        capsule_type: str = "knowledge",
        limit: int = 20
    ) -> List[Dict]:
        """
        搜索胶囊
        
        Args:
            query: 搜索关键词
            capsule_type: 胶囊类型
            limit: 返回数量限制
            
        Returns:
            匹配的胶囊列表
        """
        if capsule_type == "historical":
            table = "historical_replication_capsules"
            search_cols = ["title", "insight", "agent_name", "original_agent", "era"]
        else:
            table = "knowledge_capsules"
            search_cols = ["title", "insight", "category", "keywords"]
        
        # 构建搜索条件
        conditions = []
        params = []
        for col in search_cols:
            conditions.append(f"{col} LIKE ?")
            params.append(f"%{query}%")
        
        sql = f"""
            SELECT * FROM {table}
            WHERE {' OR '.join(conditions)}
            ORDER BY quality_score DESC
            LIMIT ?
        """
        params.append(limit)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            if capsule_type == "historical":
                return [self._row_to_historical_capsule_dict(row) for row in rows]
            else:
                return [self._row_to_capsule_dict(row) for row in rows]
    
    def get_capsules_by_topic(self, topic_id: str) -> List[Dict]:
        """获取指定话题的所有胶囊"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM knowledge_capsules WHERE topic_id = ? ORDER BY created_at DESC",
                (topic_id,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_capsule_dict(row) for row in rows]
    
    def get_top_capsules(self, limit: int = 10, min_quality: float = 0) -> List[Dict]:
        """获取高质量胶囊"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM knowledge_capsules
                WHERE quality_score >= ?
                ORDER BY quality_score DESC, created_at DESC
                LIMIT ?
            """, (min_quality, limit))
            
            rows = cursor.fetchall()
            
            return [self._row_to_capsule_dict(row) for row in rows]
    
    # ============= 统计功能 =============
    
    def get_stats(self) -> Dict:
        """获取存储统计信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 知识胶囊数量
            cursor.execute("SELECT COUNT(*) FROM knowledge_capsules")
            knowledge_count = cursor.fetchone()[0]
            
            # 历史复现胶囊数量
            cursor.execute("SELECT COUNT(*) FROM historical_replication_capsules")
            historical_count = cursor.fetchone()[0]
            
            # 平均质量分数
            cursor.execute("SELECT AVG(quality_score) FROM knowledge_capsules")
            avg_quality = cursor.fetchone()[0] or 0
            
            # 按分类统计
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM knowledge_capsules
                GROUP BY category
            """)
            category_stats = dict(cursor.fetchall())
            
            return {
                "knowledge_capsules_count": knowledge_count,
                "historical_capsules_count": historical_count,
                "total_capsules": knowledge_count + historical_count,
                "average_quality_score": round(avg_quality, 2),
                "category_distribution": category_stats,
                "db_path": self.db_path
            }
    
    # ============= 版本管理 =============
    
    def save_version(
        self,
        capsule_id: str,
        version: int,
        changes: str,
        editor: str = "system",
        content_snapshot: Dict = None
    ) -> bool:
        """
        保存胶囊版本
        
        Args:
            capsule_id: 胶囊 ID
            version: 版本号
            changes: 变更说明
            editor: 编辑者
            content_snapshot: 内容快照
            
        Returns:
            是否保存成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO capsule_versions
                (capsule_id, version, changes, editor, edited_at, content_snapshot)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                capsule_id,
                version,
                changes,
                editor,
                datetime.now().isoformat(),
                self._json_dumps(content_snapshot)
            ))
            
            logger.info(f"保存胶囊版本: {capsule_id} v{version}")
            return True
    
    def get_version_history(self, capsule_id: str) -> List[Dict]:
        """
        获取胶囊版本历史
        
        Args:
            capsule_id: 胶囊 ID
            
        Returns:
            版本历史列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM capsule_versions
                WHERE capsule_id = ?
                ORDER BY version DESC
            """, (capsule_id,))
            
            rows = cursor.fetchall()
            
            return [
                {
                    "id": row["id"],
                    "capsule_id": row["capsule_id"],
                    "version": row["version"],
                    "changes": row["changes"],
                    "editor": row["editor"],
                    "edited_at": row["edited_at"],
                    "content_snapshot": self._json_loads(row["content_snapshot"])
                }
                for row in rows
            ]
    
    # ============= 模板管理 =============
    
    def save_template(self, template: Dict) -> bool:
        """
        保存胶囊模板
        
        Args:
            template: 模板数据
            
        Returns:
            是否保存成功
        """
        if "id" not in template:
            template["id"] = f"tpl_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if "created_at" not in template:
            template["created_at"] = datetime.now().isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO capsule_templates
                (id, name, type, description, fields, example, usage_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                template.get("id"),
                template.get("name"),
                template.get("type"),
                template.get("description"),
                self._json_dumps(template.get("fields")),
                self._json_dumps(template.get("example")),
                template.get("usage_count", 0),
                template.get("created_at")
            ))
            
            return True
    
    def list_templates(self) -> List[Dict]:
        """列出所有模板"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM capsule_templates ORDER BY usage_count DESC")
            rows = cursor.fetchall()
            
            return [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "type": row["type"],
                    "description": row["description"],
                    "fields": self._json_loads(row["fields"]),
                    "example": self._json_loads(row["example"]),
                    "usage_count": row["usage_count"],
                    "created_at": row["created_at"]
                }
                for row in rows
            ]


# ============ 便捷函数 ============

def get_storage(db_path: str = None) -> CapsuleStorage:
    """获取存储实例"""
    return CapsuleStorage(db_path)


# ============ 演示 =============

if __name__ == "__main__":
    storage = CapsuleStorage()
    
    # 添加测试胶囊
    test_capsule = {
        "id": "test_001",
        "title": "测试知识胶囊",
        "summary": "这是一个测试胶囊",
        "insight": "测试洞见",
        "evidence": ["证据1", "证据2"],
        "action_items": ["行动1"],
        "questions": ["问题1"],
        "dimensions": {
            "truth_score": 80,
            "goodness_score": 70,
            "beauty_score": 60,
            "intelligence_score": 90
        },
        "source_agents": ["测试专家"],
        "keywords": ["测试"],
        "category": "交叉科学",
        "status": "draft",
        "confidence": 0.8,
        "quality_score": 75.0
    }
    
    storage.save_knowledge_capsule(test_capsule)
    
    # 读取测试
    capsule = storage.get_knowledge_capsule("test_001")
    print(f"获取胶囊: {capsule['title']}")
    
    # 列表测试
    capsules = storage.list_knowledge_capsules()
    print(f"胶囊总数: {len(capsules)}")
    
    # 统计测试
    stats = storage.get_stats()
    print(f"统计: {stats}")
