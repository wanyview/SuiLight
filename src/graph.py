"""
SuiLight Knowledge Salon - 知识图谱模块
胶囊关系可视化、领域聚类、时间线
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GraphNode:
    """图谱节点"""
    id: str
    type: str  # capsule/topic/agent/category
    label: str
    properties: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "properties": self.properties
        }


@dataclass
class GraphEdge:
    """图谱边"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source: str = ""
    target: str = ""
    type: str = "related"  # related/cites/evolves/from_topic/from_agent
    weight: float = 1.0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "weight": self.weight
        }


@dataclass
class KnowledgeGraph:
    """知识图谱"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    nodes: Dict[str, GraphNode] = field(default_factory=dict)
    edges: Dict[str, GraphEdge] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "edges": {k: v.to_dict() for k, v in self.edges.items()},
            "stats": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges)
            }
        }
    
    def add_node(self, node: GraphNode):
        self.nodes[node.id] = node
        self.updated_at = datetime.now()
    
    def add_edge(self, edge: GraphEdge):
        self.edges[edge.id] = edge
        self.updated_at = datetime.now()
    
    def get_neighbors(self, node_id: str, edge_type: str = None) -> List[Dict]:
        """获取邻居节点"""
        neighbors = []
        for edge in self.edges.values():
            if edge.source == node_id:
                if edge_type is None or edge.type == edge_type:
                    target = self.nodes.get(edge.target)
                    if target:
                        neighbors.append({
                            "node": target.to_dict(),
                            "edge": edge.to_dict()
                        })
            elif edge.target == node_id:
                if edge_type is None or edge.type == edge_type:
                    source = self.nodes.get(edge.source)
                    if source:
                        neighbors.append({
                            "node": source.to_dict(),
                            "edge": edge.to_dict()
                        })
        return neighbors
    
    def get_shortest_path(self, start_id: str, end_id: str) -> List[str]:
        """获取最短路径"""
        if start_id not in self.nodes or end_id not in self.nodes:
            return []
        
        # BFS
        queue = [[start_id]]
        visited = {start_id}
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node == end_id:
                return path
            
            for edge in self.edges.values():
                if edge.source == node and edge.target not in visited:
                    visited.add(edge.target)
                    queue.append(path + [edge.target])
                elif edge.target == node and edge.source not in visited:
                    visited.add(edge.source)
                    queue.append(path + [edge.source])
        
        return []


class KnowledgeGraphManager:
    """
    知识图谱管理器
    
    功能:
    - 构建图谱
    - 计算关联
    - 聚类分析
    - 时间线生成
    """
    
    def __init__(self, storage=None):
        self.storage = storage
        self.graphs: Dict[str, KnowledgeGraph] = {}
        self.main_graph = KnowledgeGraph(name="主图谱", description="SuiLight 知识图谱主图")
        
        logger.info("知识图谱管理器初始化完成")
    
    def build_from_capsules(self, capsules: List[Dict]) -> KnowledgeGraph:
        """从胶囊列表构建图谱"""
        graph = KnowledgeGraph(name="胶囊图谱", description=f"包含 {len(capsules)} 个胶囊")
        
        # 添加胶囊节点
        category_nodes = {}  # 分类节点
        
        for capsule in capsules:
            # 添加胶囊节点
            node = GraphNode(
                id=capsule.get("id", f"capsule_{uuid.uuid4().hex[:8]}"),
                type="capsule",
                label=capsule.get("title", "未命名胶囊"),
                properties={
                    "quality_score": capsule.get("quality_score", 0),
                    "grade": capsule.get("grade", "C"),
                    "category": capsule.get("category", "general")
                }
            )
            graph.add_node(node)
            
            # 添加/关联分类节点
            category = capsule.get("category", "general")
            if category not in category_nodes:
                cat_node = GraphNode(
                    id=f"category_{category}",
                    type="category",
                    label=self._get_category_label(category),
                    properties={"count": 0}
                )
                category_nodes[category] = cat_node
                graph.add_node(cat_node)
            else:
                category_nodes[category].properties["count"] += 1
            
            # 连接胶囊到分类
            edge = GraphEdge(
                source=node.id,
                target=cat_node.id,
                type="from_category",
                weight=0.8
            )
            graph.add_edge(edge)
            
            # 添加 Agent 节点和连接
            for agent in capsule.get("source_agents", []):
                agent_id = f"agent_{agent}"
                if agent_id not in graph.nodes:
                    agent_node = GraphNode(
                        id=agent_id,
                        type="agent",
                        label=agent,
                        properties={}
                    )
                    graph.add_node(agent_node)
                
                edge = GraphEdge(
                    source=node.id,
                    target=agent_id,
                    type="from_agent",
                    weight=1.0
                )
                graph.add_edge(edge)
            
            # 添加关键词节点
            for keyword in capsule.get("keywords", [])[:3]:
                kw_id = f"keyword_{keyword}"
                if kw_id not in graph.nodes:
                    kw_node = GraphNode(
                        id=kw_id,
                        type="keyword",
                        label=keyword,
                        properties={}
                    )
                    graph.add_node(kw_node)
                
                edge = GraphEdge(
                    source=node.id,
                    target=kw_id,
                    type="has_keyword",
                    weight=0.5
                )
                graph.add_edge(edge)
        
        # 胶囊之间的关联 (基于关键词)
        for i, c1 in enumerate(capsules):
            for j, c2 in enumerate(capsules[i+1:], i+1):
                kw1 = set(c1.get("keywords", [])[:10])
                kw2 = set(c2.get("keywords", [])[:10])
                intersection = kw1 & kw2
                
                if intersection:
                    weight = len(intersection) / max(len(kw1), len(kw2), 1)
                    if weight > 0.2:  # 至少20%重叠
                        edge = GraphEdge(
                            source=c1.get("id"),
                            target=c2.get("id"),
                            type="related",
                            weight=weight
                        )
                        graph.add_edge(edge)
        
        logger.info(f"图谱构建完成: {len(graph.nodes)} 节点, {len(graph.edges)} 边")
        
        return graph
    
    def _get_category_label(self, category: str) -> str:
        """获取分类标签"""
        labels = {
            "自然科学": "🔬 自然科学",
            "社会科学": "⚖️ 社会科学",
            "人文科学": "🎨 人文科学",
            "交叉科学": "🔗 交叉科学",
            "ai": "🤖 AI",
            "philosophy": "🤔 哲学",
            "general": "📦 综合"
        }
        return labels.get(category, f"📦 {category}")
    
    def get_cluster_analysis(self, capsules: List[Dict]) -> Dict:
        """获取聚类分析"""
        # 按分类聚类
        clusters = defaultdict(list)
        for capsule in capsules:
            category = capsule.get("category", "general")
            clusters[category].append(capsule)
        
        result = {
            "clusters": [],
            "total": len(capsules)
        }
        
        for category, items in clusters.items():
            result["clusters"].append({
                "id": category,
                "label": self._get_category_label(category),
                "count": len(items),
                "avg_quality": sum(c.get("quality_score", 0) for c in items) / len(items) if items else 0
            })
        
        # 按质量排序
        result["clusters"].sort(key=lambda x: x["count"], reverse=True)
        
        return result
    
    def get_timeline(self, capsules: List[Dict]) -> Dict:
        """获取时间线数据"""
        # 按时间排序
        sorted_capsules = sorted(
            capsules,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
        
        # 按周分组
        weeks = defaultdict(list)
        for capsule in sorted_capsules:
            created = capsule.get("created_at", "")
            if created:
                date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                week_key = date.strftime("%Y-W%U")
                weeks[week_key].append(capsule)
        
        timeline = []
        for week_key in sorted(weeks.keys(), reverse=True):
            week_capsules = weeks[week_key]
            timeline.append({
                "week": week_key,
                "count": len(week_capsules),
                "avg_quality": sum(c.get("quality_score", 0) for c in week_capsules) / len(week_capsules),
                "capsules": [c.get("title", "未命名") for c in week_capsules[:5]]
            })
        
        return {
            "timeline": timeline,
            "total_capsules": len(sorted_capsules),
            "total_weeks": len(timeline)
        }
    
    def get_related_capsules(self, capsule_id: str, capsules: List[Dict], limit: int = 5) -> List[Dict]:
        """获取相关胶囊"""
        target = None
        for c in capsules:
            if c.get("id") == capsule_id:
                target = c
                break
        
        if not target:
            return []
        
        kw1 = set(target.get("keywords", [])[:10])
        category = target.get("category", "")
        
        related = []
        for capsule in capsules:
            if capsule.get("id") == capsule_id:
                continue
            
            score = 0
            
            # 分类匹配
            if capsule.get("category") == category:
                score += 0.5
            
            # 关键词重叠
            kw2 = set(capsule.get("keywords", [])[:10])
            intersection = kw1 & kw2
            if kw1 or kw2:
                score += len(intersection) / max(len(kw1), len(kw2), 1)
            
            if score > 0:
                related.append({
                    "capsule": capsule,
                    "score": score
                })
        
        # 排序并返回
        related.sort(key=lambda x: x["score"], reverse=True)
        return [r["capsule"] for r in related[:limit]]
    
    def get_statistics(self, capsules: List[Dict]) -> Dict:
        """获取图谱统计"""
        return {
            "total_capsules": len(capsules),
            "total_keywords": len(set(
                kw for c in capsules 
                for kw in c.get("keywords", [])[:10]
            )),
            "total_agents": len(set(
                agent for c in capsules 
                for agent in c.get("source_agents", [])
            )),
            "categories": len(set(c.get("category", "general") for c in capsules)),
            "avg_quality": sum(c.get("quality_score", 0) for c in capsules) / len(capsules) if capsules else 0,
            "a_grade_count": len([c for c in capsules if c.get("grade") == "A"]),
            "b_grade_count": len([c for c in capsules if c.get("grade") == "B"]),
            "c_grade_count": len([c for c in capsules if c.get("grade") == "C"])
        }
    
    def export_graph_json(self, capsules: List[Dict]) -> Dict:
        """导出图谱 JSON (D3.js 可用格式)"""
        graph = self.build_from_capsules(capsules)
        
        nodes = []
        for node in graph.nodes.values():
            nodes.append({
                "id": node.id,
                "type": node.type,
                "label": node.label,
                **node.properties
            })
        
        edges = []
        for edge in graph.edges.values():
            edges.append({
                "source": edge.source,
                "target": edge.target,
                "type": edge.type,
                "weight": edge.weight
            })
        
        return {
            "nodes": nodes,
            "links": edges,
            "stats": graph.to_dict()["stats"]
        }


# 全局实例
graph_manager = KnowledgeGraphManager()
