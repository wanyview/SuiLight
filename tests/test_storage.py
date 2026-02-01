"""
SuiLight Knowledge Salon - 胶囊存储单元测试
"""

import pytest
import sys
import os
import tempfile
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage.capsule_storage import CapsuleStorage


class TestCapsuleStorage:
    """胶囊存储测试类"""
    
    @pytest.fixture
    def storage(self):
        """创建临时存储实例"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        storage = CapsuleStorage(db_path)
        yield storage
        
        # 清理
        os.unlink(db_path)
    
    @pytest.fixture
    def sample_knowledge_capsule(self):
        """示例知识胶囊"""
        return {
            "id": "test_kc_001",
            "topic_id": "topic_001",
            "title": "测试知识胶囊",
            "summary": "这是一个测试胶囊摘要",
            "insight": "测试核心洞见",
            "evidence": ["证据1", "证据2", "证据3"],
            "action_items": ["行动建议1", "行动建议2"],
            "questions": ["问题1", "问题2"],
            "dimensions": {
                "truth_score": 80,
                "goodness_score": 70,
                "beauty_score": 60,
                "intelligence_score": 90
            },
            "source_agents": ["测试专家1", "测试专家2"],
            "keywords": ["测试", "知识胶囊"],
            "category": "交叉科学",
            "status": "draft",
            "confidence": 0.85,
            "quality_score": 75.0
        }
    
    @pytest.fixture
    def sample_historical_capsule(self):
        """示例历史复现胶囊"""
        return {
            "id": "test_hc_001",
            "original_agent": "艾萨克·牛顿",
            "agent_name": "牛顿",
            "era": "17-18世纪",
            "topic_id": "topic_002",
            "title": "牛顿谈物理学发展",
            "summary": "关于物理学发展方向的讨论",
            "insight": "实验与理论相结合",
            "evidence": ["实验验证", "数学推导"],
            "action_items": ["开展实验"],
            "questions": ["下一步研究方向"],
            "dimensions": {
                "truth_score": 90,
                "goodness_score": 60,
                "beauty_score": 70,
                "intelligence_score": 85
            },
            "source_agents": ["牛顿"],
            "keywords": ["物理学", "实验"],
            "category": "自然科学",
            "status": "approved",
            "confidence": 0.9,
            "quality_score": 76.25,
            "replication_quality": 0.95
        }
    
    # ============= 知识胶囊测试 =============
    
    def test_save_knowledge_capsule(self, storage, sample_knowledge_capsule):
        """测试保存知识胶囊"""
        result = storage.save_knowledge_capsule(sample_knowledge_capsule)
        assert result is True
    
    def test_get_knowledge_capsule(self, storage, sample_knowledge_capsule):
        """测试获取知识胶囊"""
        # 先保存
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        # 再获取
        capsule = storage.get_knowledge_capsule("test_kc_001")
        
        assert capsule is not None
        assert capsule["id"] == "test_kc_001"
        assert capsule["title"] == "测试知识胶囊"
        assert capsule["insight"] == "测试核心洞见"
        assert len(capsule["evidence"]) == 3
    
    def test_get_nonexistent_capsule(self, storage):
        """测试获取不存在的胶囊"""
        capsule = storage.get_knowledge_capsule("nonexistent")
        assert capsule is None
    
    def test_list_knowledge_capsules(self, storage, sample_knowledge_capsule):
        """测试列出知识胶囊"""
        # 保存多个胶囊
        for i in range(3):
            capsule = sample_knowledge_capsule.copy()
            capsule["id"] = f"test_kc_{i}"
            capsule["title"] = f"测试胶囊 {i}"
            storage.save_knowledge_capsule(capsule)
        
        # 列出
        capsules = storage.list_knowledge_capsules(limit=10)
        
        assert len(capsules) >= 3
    
    def test_list_with_category_filter(self, storage, sample_knowledge_capsule):
        """测试按分类筛选"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        capsules = storage.list_knowledge_capsules(category="交叉科学")
        assert len(capsules) >= 1
        assert capsules[0]["category"] == "交叉科学"
    
    def test_delete_knowledge_capsule(self, storage, sample_knowledge_capsule):
        """测试删除知识胶囊"""
        # 保存
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        # 删除
        result = storage.delete_knowledge_capsule("test_kc_001")
        assert result is True
        
        # 验证删除
        capsule = storage.get_knowledge_capsule("test_kc_001")
        assert capsule is None
    
    # ============= 历史复现胶囊测试 =============
    
    def test_save_historical_capsule(self, storage, sample_historical_capsule):
        """测试保存历史复现胶囊"""
        result = storage.save_historical_capsule(sample_historical_capsule)
        assert result is True
    
    def test_get_historical_capsule(self, storage, sample_historical_capsule):
        """测试获取历史复现胶囊"""
        storage.save_historical_capsule(sample_historical_capsule)
        
        capsule = storage.get_historical_capsule("test_hc_001")
        
        assert capsule is not None
        assert capsule["id"] == "test_hc_001"
        assert capsule["original_agent"] == "艾萨克·牛顿"
        assert capsule["era"] == "17-18世纪"
    
    def test_list_historical_capsules(self, storage, sample_historical_capsule):
        """测试列出历史复现胶囊"""
        storage.save_historical_capsule(sample_historical_capsule)
        
        capsules = storage.list_historical_capsules()
        
        assert len(capsules) >= 1
        assert capsules[0]["agent_name"] == "牛顿"
    
    # ============= 通用接口测试 =============
    
    def test_save_capsule_generic(self, storage, sample_knowledge_capsule, sample_historical_capsule):
        """测试通用保存接口"""
        result = storage.save_capsule(sample_knowledge_capsule, capsule_type="knowledge")
        assert result is True
        
        result = storage.save_capsule(sample_historical_capsule, capsule_type="historical")
        assert result is True
    
    def test_get_capsule_generic(self, storage, sample_knowledge_capsule):
        """测试通用获取接口"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        capsule = storage.get_capsule("test_kc_001", capsule_type="knowledge")
        assert capsule is not None
        assert capsule["title"] == "测试知识胶囊"
    
    def test_list_capsules_generic(self, storage, sample_knowledge_capsule, sample_historical_capsule):
        """测试通用列表接口"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        storage.save_historical_capsule(sample_historical_capsule)
        
        knowledge_capsules = storage.list_capsules(capsule_type="knowledge")
        historical_capsules = storage.list_capsules(capsule_type="historical")
        
        assert len(knowledge_capsules) >= 1
        assert len(historical_capsules) >= 1
    
    # ============= 搜索功能测试 =============
    
    def test_search_capsules(self, storage, sample_knowledge_capsule):
        """测试搜索胶囊"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        results = storage.search_capsules("测试")
        
        assert len(results) >= 1
    
    def test_get_capsules_by_topic(self, storage, sample_knowledge_capsule):
        """测试按话题获取胶囊"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        capsules = storage.get_capsules_by_topic("topic_001")
        
        assert len(capsules) >= 1
        assert capsules[0]["topic_id"] == "topic_001"
    
    def test_get_top_capsules(self, storage, sample_knowledge_capsule):
        """测试获取高质量胶囊"""
        # 保存一个高质量胶囊
        capsule = sample_knowledge_capsule.copy()
        capsule["quality_score"] = 80.0
        storage.save_knowledge_capsule(capsule)
        
        top_capsules = storage.get_top_capsules(limit=10, min_quality=60)
        
        assert len(top_capsules) >= 1
        assert top_capsules[0]["quality_score"] >= 60
    
    # ============= 版本管理测试 =============
    
    def test_save_version(self, storage, sample_knowledge_capsule):
        """测试保存版本"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        result = storage.save_version(
            capsule_id="test_kc_001",
            version=2,
            changes="更新内容",
            editor="test_user",
            content_snapshot={"insight": "新洞见"}
        )
        
        assert result is True
    
    def test_get_version_history(self, storage, sample_knowledge_capsule):
        """测试获取版本历史"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        # 保存多个版本
        for v in range(1, 4):
            storage.save_version(
                capsule_id="test_kc_001",
                version=v,
                changes=f"版本 {v} 变更"
            )
        
        history = storage.get_version_history("test_kc_001")
        
        assert len(history) >= 3
    
    # ============= 模板管理测试 =============
    
    def test_save_template(self, storage):
        """测试保存模板"""
        template = {
            "id": "test_tpl_001",
            "name": "测试模板",
            "type": "discussion_output",
            "description": "测试描述",
            "fields": [{"name": "title", "label": "标题"}],
            "usage_count": 0
        }
        
        result = storage.save_template(template)
        assert result is True
    
    def test_list_templates(self, storage):
        """测试列出模板"""
        templates = storage.list_templates()
        
        # 可能为空或包含预设模板
        assert isinstance(templates, list)
    
    # ============= 统计功能测试 =============
    
    def test_get_stats(self, storage, sample_knowledge_capsule, sample_historical_capsule):
        """测试获取统计信息"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        storage.save_historical_capsule(sample_historical_capsule)
        
        stats = storage.get_stats()
        
        assert "knowledge_capsules_count" in stats
        assert "historical_capsules_count" in stats
        assert "total_capsules" in stats
        assert stats["knowledge_capsules_count"] >= 1
        assert stats["historical_capsules_count"] >= 1
    
    # ============= 数据完整性测试 =============
    
    def test_capsule_json_integrity(self, storage, sample_knowledge_capsule):
        """测试胶囊 JSON 数据完整性"""
        storage.save_knowledge_capsule(sample_knowledge_capsule)
        
        capsule = storage.get_knowledge_capsule("test_kc_001")
        
        # 验证 JSON 数组
        assert isinstance(capsule["evidence"], list)
        assert len(capsule["evidence"]) == 3
        
        # 验证 JSON 对象
        assert isinstance(capsule["dimensions"], dict)
        assert capsule["dimensions"]["truth_score"] == 80
    
    def test_empty_list_handling(self, storage):
        """测试空列表处理"""
        capsule = {
            "id": "test_empty_001",
            "title": "空列表胶囊",
            "insight": "测试",
            "evidence": [],
            "action_items": [],
            "questions": [],
            "dimensions": {}
        }
        
        storage.save_knowledge_capsule(capsule)
        
        retrieved = storage.get_knowledge_capsule("test_empty_001")
        
        assert retrieved["evidence"] == []
        assert retrieved["action_items"] == []
        assert retrieved["questions"] == []
    
    def test_special_characters(self, storage):
        """测试特殊字符处理"""
        capsule = {
            "id": "test_special_001",
            "title": "特殊字符测试: \"quotes\" 和 中文",
            "insight": "包含\n换行和'tick'标记",
            "evidence": ["包含\"双引号\"和'单引号'"],
            "action_items": ["换行\n测试"],
            "dimensions": {
                "truth_score": 50,
                "goodness_score": 50,
                "beauty_score": 50,
                "intelligence_score": 50
            }
        }
        
        storage.save_knowledge_capsule(capsule)
        
        retrieved = storage.get_knowledge_capsule("test_special_001")
        
        assert "quotes" in retrieved["title"]
        assert "换行" in retrieved["insight"]


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
