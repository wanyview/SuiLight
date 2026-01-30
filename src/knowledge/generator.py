"""
SuiLight Knowledge Salon - Knowledge Engine
知识引擎: 文档解析、知识图谱、Agent 生成器

冷启动系统: 知识 → Agent
"""

import re
import json
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
from pathlib import Path

from .base import Agent, AgentConfig, DATM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KnowledgeDocument:
    """知识文档"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    content: str = ""
    source: str = ""
    domain: str = ""
    keywords: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content[:500] if len(self.content) > 500 else self.content,
            "source": self.source,
            "domain": self.domain,
            "keywords": self.keywords,
            "created_at": self.created_at.isoformat()
        }


class KnowledgeParser:
    """
    知识解析器
    
    将各种格式的文档解析为结构化知识
    """
    
    SUPPORTED_FORMATS = ['.txt', '.md', '.pdf', '.docx', '.html']
    
    def __init__(self):
        self.chunk_size = 1000  # 知识块大小
        self.chunk_overlap = 200  # 块重叠
    
    def parse(self, file_path: str, domain: str = "general") -> List[KnowledgeDocument]:
        """
        解析文档
        
        Args:
            file_path: 文件路径
            domain: 领域分类
            
        Returns:
            知识文档列表
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"文件不存在: {file_path}")
            return []
        
        suffix = path.suffix.lower()
        
        if suffix not in self.SUPPORTED_FORMATS:
            logger.warning(f"不支持的格式: {suffix}")
            return []
        
        # 读取内容
        content = self._read_file(file_path)
        if not content:
            return []
        
        # 提取关键词
        keywords = self._extract_keywords(content)
        
        # 分割为块
        chunks = self._split_into_chunks(content)
        
        # 创建文档
        documents = []
        for i, chunk in enumerate(chunks):
            doc = KnowledgeDocument(
                title=f"{path.stem} - Part {i+1}",
                content=chunk,
                source=str(file_path),
                domain=domain,
                keywords=keywords
            )
            documents.append(doc)
        
        logger.info(f"解析完成: {len(documents)} 个知识块")
        return documents
    
    def _read_file(self, file_path: str) -> str:
        """读取文件内容"""
        path = Path(file_path)
        
        try:
            if path.suffix == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif path.suffix == '.md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif path.suffix == '.html':
                # 简单 HTML 解析
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 移除 HTML 标签
                    text = re.sub(r'<[^>]+>', '', content)
                    return text.strip()
            
            else:
                # 其他格式需要额外处理
                logger.warning(f"需要安装额外库处理 {path.suffix} 格式")
                return ""
                
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            return ""
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词 (简单版)"""
        # 移除标点
        text = re.sub(r'[^\w\s]', ' ', content)
        words = text.lower().split()
        
        # 停用词
        stopwords = {'的', '是', '在', '和', '与', '或', '这', '那', '有', '没有',
                    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at'}
        
        # 过滤
        keywords = [w for w in words if len(w) > 2 and w not in stopwords]
        
        # 词频统计
        from collections import Counter
        word_counts = Counter(keywords)
        
        # 返回 top 10
        return [word for word, _ in word_counts.most_common(10)]
    
    def _split_into_chunks(self, content: str) -> List[str]:
        """分割为知识块"""
        # 按段落分割
        paragraphs = content.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # 处理重叠
        if len(chunks) > 1 and self.chunk_overlap > 0:
            overlapped_chunks = []
            for i, chunk in enumerate(chunks):
                if i > 0:
                    prev_chunk = chunks[i-1]
                    overlap = prev_chunk[-self.chunk_overlap:] if len(prev_chunk) > self.chunk_overlap else prev_chunk
                    chunk = overlap + chunk
                overlapped_chunks.append(chunk)
            chunks = overlapped_chunks
        
        return chunks


class AgentGenerator:
    """
    Agent 生成器
    
    从知识文档自动构建专家 Agent
    """
    
    def __init__(self):
        self.parser = KnowledgeParser()
    
    def generate_from_knowledge(
        self,
        name: str,
        domain: str,
        knowledge_documents: List[KnowledgeDocument],
        datm_config: Dict = None
    ) -> Agent:
        """
        从知识文档生成 Agent
        
        Args:
            name: Agent 名称
            domain: 领域
            knowledge_documents: 知识文档列表
            datm_config: DATM 配置
            
        Returns:
            生成的 Agent
        """
        # 合并所有知识
        all_content = "\n\n".join([doc.content for doc in knowledge_documents])
        all_keywords = []
        for doc in knowledge_documents:
            all_keywords.extend(doc.keywords)
        all_keywords = list(set(all_keywords))[:20]  # 去重
        
        # 提取专长领域
        expertise = self._extract_expertise(all_content, all_keywords)
        
        # 生成描述
        description = f"{name}是一个{domain}领域的专家，擅长{', '.join(expertise[:5])}。"
        
        # 配置 DATM
        if datm_config is None:
            datm_config = self._estimate_datm(domain, expertise)
        
        datm = DATM.from_dict(datm_config)
        
        # 创建配置
        config = AgentConfig(
            name=name,
            domain=domain,
            description=description,
            expertise=expertise,
            datm=datm
        )
        
        # 创建 Agent
        agent = Agent(config)
        
        # 注入知识
        for doc in knowledge_documents:
            agent.learn(doc.content, source=doc.source)
        
        logger.info(f"Agent {name} 从 {len(knowledge_documents)} 个知识文档生成")
        
        return agent
    
    def generate_from_files(
        self,
        name: str,
        domain: str,
        file_paths: List[str],
        datm_config: Dict = None
    ) -> Agent:
        """
        从文件列表生成 Agent
        
        Args:
            name: Agent 名称
            domain: 领域
            file_paths: 文件路径列表
            datm_config: DATM 配置
            
        Returns:
            生成的 Agent
        """
        # 解析所有文件
        all_documents = []
        for file_path in file_paths:
            documents = self.parser.parse(file_path, domain)
            all_documents.extend(documents)
        
        # 生成 Agent
        return self.generate_from_knowledge(name, domain, all_documents, datm_config)
    
    def _extract_expertise(self, content: str, keywords: List[str]) -> List[str]:
        """提取专长领域"""
        # 基于关键词和内容分析
        expertise = []
        
        # 简单规则匹配
        expertise_indicators = {
            'science': ['研究', '实验', '理论', '科学'],
            'technology': ['技术', '开发', '实现', '系统'],
            'business': ['商业', '管理', '运营', '市场'],
            'education': ['教育', '学习', '教学', '培训'],
            'culture': ['文化', '艺术', '历史', '哲学'],
            'health': ['健康', '医学', '养生', '医疗']
        }
        
        content_lower = content.lower()
        
        for field, indicators in expertise_indicators.items():
            for indicator in indicators:
                if indicator in content:
                    expertise.append(field)
                    break
        
        # 添加关键词
        expertise.extend(keywords[:5])
        
        # 去重
        expertise = list(set(expertise))
        
        if not expertise:
            expertise = ['general']
        
        return expertise[:8]  # 限制数量
    
    def _estimate_datm(self, domain: str, expertise: List[str]) -> Dict:
        """估算 DATM 配置"""
        # 基于领域默认值
        domain_defaults = {
            'science': {'truth': 90, 'goodness': 50, 'beauty': 50, 'intelligence': 80},
            'technology': {'truth': 85, 'goodness': 60, 'beauty': 50, 'intelligence': 90},
            'business': {'truth': 70, 'goodness': 70, 'beauty': 60, 'intelligence': 85},
            'education': {'truth': 85, 'goodness': 80, 'beauty': 60, 'intelligence': 75},
            'culture': {'truth': 60, 'goodness': 75, 'beauty': 95, 'intelligence': 70},
            'health': {'truth': 90, 'goodness': 85, 'beauty': 60, 'intelligence': 70},
            'coffee': {'truth': 85, 'goodness': 60, 'beauty': 50, 'intelligence': 75},
            'reading': {'truth': 70, 'goodness': 80, 'beauty': 90, 'intelligence': 75},
            'general': {'truth': 70, 'goodness': 60, 'beauty': 60, 'intelligence': 70}
        }
        
        default = domain_defaults.get(domain.lower(), domain_defaults['general'])
        
        # 根据 expertise 调整
        if 'art' in expertise or 'culture' in expertise:
            default['beauty'] = min(100, default['beauty'] + 20)
        if 'innovation' in expertise or 'technology' in expertise:
            default['intelligence'] = min(100, default['intelligence'] + 15)
        
        return default


class KnowledgeGraph:
    """
    知识图谱
    
    存储和管理知识的关联关系
    """
    
    def __init__(self):
        self.entities: Dict[str, Dict] = {}  # 实体
        self.relations: List[Dict] = []     # 关系
        self.vectors: Dict[str, List[float]] = {}  # 向量 (简化版)
    
    def add_entity(self, entity_id: str, entity_type: str, properties: Dict):
        """添加实体"""
        self.entities[entity_id] = {
            "type": entity_type,
            "properties": properties,
            "created_at": datetime.now().isoformat()
        }
    
    def add_relation(self, from_id: str, to_id: str, relation_type: str, weight: float = 1.0):
        """添加关系"""
        self.relations.append({
            "from": from_id,
            "to": to_id,
            "type": relation_type,
            "weight": weight,
            "created_at": datetime.now().isoformat()
        })
    
    def query(self, entity_type: str = None, keyword: str = None) -> List[Dict]:
        """查询"""
        results = []
        
        for eid, entity in self.entities.items():
            if entity_type and entity['type'] != entity_type:
                continue
            
            # 简单关键词匹配
            if keyword:
                properties_str = json.dumps(entity.get('properties', {}))
                if keyword.lower() not in properties_str.lower():
                    continue
            
            results.append({
                "id": eid,
                **entity
            })
        
        return results
    
    def to_dict(self) -> Dict:
        return {
            "entity_count": len(self.entities),
            "relation_count": len(self.relations),
            "entities": self.entities,
            "relations": self.relations
        }
