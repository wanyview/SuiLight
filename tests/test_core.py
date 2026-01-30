"""
SuiLight Knowledge Salon - 测试套件
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDATM:
    """DATM 知识矩阵测试"""
    
    def test_datm_creation(self):
        from src.agents.base import DATM
        
        datm = DATM(truth=80, goodness=70, beauty=60, intelligence=90)
        assert datm.truth == 80
        assert datm.goodness == 70
        assert datm.beauty == 60
        assert datm.intelligence == 90
    
    def test_datm_to_dict(self):
        from src.agents.base import DATM
        
        datm = DATM(truth=80, goodness=70, beauty=60, intelligence=90)
        result = datm.to_dict()
        
        assert result["truth"] == 80
        assert result["goodness"] == 70
        assert result["beauty"] == 60
        assert result["intelligence"] == 90
    
    def test_datm_from_dict(self):
        from src.agents.base import DATM
        
        data = {"truth": 85, "goodness": 75, "beauty": 65, "intelligence": 95}
        datm = DATM.from_dict(data)
        
        assert datm.truth == 85
        assert datm.goodness == 75
        assert datm.beauty == 65
        assert datm.intelligence == 95
    
    def test_datm_default_values(self):
        from src.agents.base import DATM
        
        datm = DATM()
        assert datm.truth == 50
        assert datm.goodness == 50
        assert datm.beauty == 50
        assert datm.intelligence == 50
    
    def test_datm_radar_data(self):
        from src.agents.base import DATM
        
        datm = DATM(truth=80, goodness=70, beauty=60, intelligence=90)
        radar = datm.to_radar_data()
        
        assert "labels" in radar
        assert "datasets" in radar
        assert len(radar["datasets"]) == 1
        assert len(radar["datasets"][0]["data"]) == 4


class TestAgent:
    """Agent 测试"""
    
    def test_agent_creation(self):
        from src.agents.base import Agent, AgentConfig, DATM
        
        config = AgentConfig(
            name="测试专家",
            domain="test",
            description="测试描述",
            expertise=["测试1", "测试2"],
            datm=DATM(truth=80, goodness=70, beauty=60, intelligence=90)
        )
        
        agent = Agent(config)
        
        assert agent.config.name == "测试专家"
        assert agent.config.domain == "test"
        assert len(agent.config.expertise) == 2
        assert agent.status.value == "idle"
    
    def test_agent_chat_mock(self):
        from src.agents.base import Agent, AgentConfig
        
        config = AgentConfig(
            name="测试",
            domain="test"
        )
        
        agent = Agent(config)
        response = agent.chat("你好")
        
        assert response is not None
        assert "测试" in response
    
    def test_agent_learn(self):
        from src.agents.base import Agent, AgentConfig
        
        config = AgentConfig(name="测试", domain="test")
        agent = Agent(config)
        
        success = agent.learn("新知识内容", source="test")
        assert success is True
        assert len(agent.knowledge_base) == 1
    
    def test_agent_to_dict(self):
        from src.agents.base import Agent, AgentConfig, DATM
        
        config = AgentConfig(
            name="测试",
            domain="test",
            datm=DATM(truth=80, goodness=70, beauty=60, intelligence=90)
        )
        
        agent = Agent(config)
        data = agent.to_dict()
        
        assert data["name"] == "测试"
        assert data["domain"] == "test"
        assert "datm" in data
        assert data["status"] == "idle"


class TestAgentRegistry:
    """Agent 注册表测试"""
    
    def test_registry_operations(self):
        from src.agents.base import Agent, AgentConfig, AgentRegistry
        
        registry = AgentRegistry()
        
        # 创建 Agent
        config = AgentConfig(name="测试1", domain="test")
        agent1 = Agent(config)
        
        config2 = AgentConfig(name="测试2", domain="test")
        agent2 = Agent(config2)
        
        # 注册
        assert registry.register(agent1) is True
        assert registry.register(agent2) is True
        
        # 重复注册
        assert registry.register(agent1) is False
        
        # 获取
        assert registry.get(agent1.id) is not None
        
        # 列表
        agents = registry.list_all()
        assert len(agents) == 2
        
        # 注销
        assert registry.unregister(agent1.id) is True
        assert registry.unregister(agent1.id) is False  # 重复注销


class TestPresets:
    """预设 Agent 测试"""
    
    def test_great_minds_exists(self):
        from src.agents.presets import GREAT_MINDS
        
        assert len(GREAT_MINDS) > 0
    
    def test_create_agent_configs(self):
        from src.agents.presets import create_agent_configs
        
        configs = create_agent_configs()
        assert len(configs) > 0
        
        # 检查至少有一个牛顿
        names = [c.name for c in configs]
        assert "艾萨克·牛顿" in names or "Isaac Newton" in names
    
    def test_get_domains(self):
        from src.agents.presets import get_domains
        
        domains = get_domains()
        assert len(domains) > 0
        assert "physics" in domains


class TestDiscussion:
    """讨论系统测试"""
    
    def test_discussion_manager(self):
        from src.knowledge.discussion import DiscussionManager
        from src.agents.base import AgentRegistry
        
        registry = AgentRegistry()
        dm = DiscussionManager(registry)
        
        # 创建讨论
        topic = dm.create_topic(
            title="测试讨论",
            description="测试描述",
            category="交叉科学"
        )
        
        assert topic.title == "测试讨论"
        assert topic.phase.value == "setup"
    
    def test_great_discussions(self):
        from src.knowledge.discussion import get_great_discussions
        
        discussions = get_great_discussions()
        assert len(discussions) > 0


class TestStorage:
    """存储测试"""
    
    def test_storage_creation(self):
        import tempfile
        import os
        from src.storage import StorageManager
        
        # 使用临时文件
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            storage = StorageManager(db_path)
            assert storage is not None
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


class TestIntegration:
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        from src.agents.base import Agent, AgentConfig, DATM, AgentRegistry
        from src.knowledge.discussion import DiscussionManager
        
        # 创建组件
        registry = AgentRegistry()
        dm = DiscussionManager(registry)
        
        # 创建 Agent
        config = AgentConfig(
            name="测试专家",
            domain="test",
            datm=DATM(truth=80, goodness=70, beauty=60, intelligence=90)
        )
        agent = Agent(config)
        registry.register(agent)
        
        # 创建讨论
        topic = dm.create_topic(
            title="集成测试讨论",
            description="测试描述",
            category="交叉科学"
        )
        
        # 验证
        assert topic is not None
        assert len(registry.list_all()) == 1


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
