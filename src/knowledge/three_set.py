"""
SuiLight Knowledge Salon - 三设机制
思想家 + 思想 + 实验
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field as dc_field, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Era(Enum):
    """思想家时代"""
    ANCIENT = "古代"          # 古希腊、春秋战国
    CLASSICAL = "古典"        # 中世纪、秦汉
    MODERN = "近代"           # 文艺复兴、启蒙
    CONTEMPORARY = "现代"     # 19-20世纪
    FUTURE = "未来"           # 科幻/预测


class Field(Enum):
    """学科领域"""
    PHILOSOPHY = "philosophy"
    SCIENCE = "science"
    ECONOMICS = "economics"
    PSYCHOLOGY = "psychology"
    SOCIOLOGY = "sociology"
    TECHNOLOGY = "technology"
    ARTS = "arts"
    POLITICS = "politics"


@dataclass
class ThinkerProfile:
    """
    思想家设定档案
    
    包含:
    - 基本信息
    - 核心思想
    - 代表著作
    - 思想风格
    - 关联思想家
    """
    id: str = dc_field(default_factory=lambda: f"thinker_{uuid.uuid4().hex[:8]}")
    name: str = ""                    # 姓名
    name_en: str = ""                 # 英文名
    era: str = ""                     # 时代
    field: str = ""                   # 领域
    nationality: str = ""             # 国籍
    
    # 核心设定
    core_thoughts: List[str] = dc_field(default_factory=list)  # 核心思想
    representative_works: List[str] = dc_field(default_factory=list)  # 代表作
    famous_quotes: List[str] = dc_field(default_factory=list)  # 名言
    
    # 思想风格
    thinking_style: str = ""          # 思维方式
    personality: str = ""             # 性格特点
    speaking_style: str = ""          # 说话风格
    
    # 关联
    mentors: List[str] = dc_field(default_factory=list)      # 导师/师承
    followers: List[str] = dc_field(default_factory=list)    # 继承者
    opponents: List[str] = dc_field(default_factory=list)    # 对手/批评者
    related_thinkers: List[str] = dc_field(default_factory=list)  # 相关
    
    # 统计
    appearances: int = 0              # 出现次数
    capsules_generated: int = 0       # 生成的胶囊数
    
    created_at: str = dc_field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = dc_field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ThoughtDesign:
    """
    思想设计
    
    记录:
    - 思想的定义
    - 发展脉络
    - 核心论点
    - 争议和批评
    """
    id: str = dc_field(default_factory=lambda: f"thought_{uuid.uuid4().hex[:8]}")
    title: str = ""                   # 思想名称
    description: str = ""             # 思想描述
    
    # 思想家
    primary_thinker: str = ""         # 主要思想家
    associated_thinkers: List[str] = dc_field(default_factory=list)
    
    # 内容
    core_arguments: List[str] = dc_field(default_factory=list)  # 核心论点
    key_concepts: List[str] = dc_field(default_factory=list)   # 关键概念
    historical_context: str = ""      # 历史背景
    
    # 发展
    origins: str = ""                 # 思想起源
    evolution: str = ""               # 思想演变
    milestones: List[str] = dc_field(default_factory=list)     # 里程碑
    
    # 争议
    criticisms: List[str] = dc_field(default_factory=list)     # 批评
    counterarguments: List[str] = dc_field(default_factory=list)  # 反论
    limitations: str = ""             # 局限性
    
    # 关联
    related_thoughts: List[str] = dc_field(default_factory=list)  # 相关思想
    related_capsules: List[str] = dc_field(default_factory=list)  # 相关胶囊
    
    # 领域
    fields: List[str] = dc_field(default_factory=list)         # 涉及领域
    
    created_at: str = dc_field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = dc_field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ExperimentDesign:
    """
    实验验证设计
    
    用案例/数据验证思想
    """
    id: str = dc_field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    title: str = ""                   # 实验名称
    thought_id: str = ""              # 关联的思想
    
    # 类型
    experiment_type: str = ""         # 类型: case_study / data / thought
    methodology: str = ""             # 方法论
    
    # 内容
    hypothesis: str = ""              # 假设
    setup: str = ""                   # 实验设计
    results: str = ""                 # 实验结果
    analysis: str = ""                # 分析
    
    # 证据
    evidence: List[str] = dc_field(default_factory=list)  # 证据列表
    data_sources: List[str] = dc_field(default_factory=list)  # 数据来源
    
    # 结论
    conclusion: str = ""              # 结论
    implications: str = ""            # 启示
    limitations: str = ""             # 局限性
    
    # 验证的思想
    supported_claims: List[str] = dc_field(default_factory=list)  # 支持的主张
    challenged_claims: List[str] = dc_field(default_factory=list)  # 挑战的主张
    
    created_at: str = dc_field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = dc_field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 100位思想家预设 ============

THINKER_PRESETS = {
    # 哲学
    "苏格拉底": {
        "name_en": "Socrates",
        "era": "古代",
        "field": "philosophy",
        "nationality": "古希腊",
        "core_thoughts": ["产婆术", "认识你自己", "德即知识"],
        "representative_works": ["柏拉图对话录"],
        "famous_quotes": ["我唯一知道的，就是我一无所知"],
        "thinking_style": "问答式辩证",
        "personality": "追问质疑",
        "speaking_style": "提问引导",
        "mentors": [],
        "followers": ["柏拉图", "亚里士多德"],
        "opponents": ["诡辩学派"],
        "related_thinkers": ["柏拉图", "亚里士多德"]
    },
    "柏拉图": {
        "name_en": "Plato",
        "era": "古代",
        "field": "philosophy",
        "nationality": "古希腊",
        "core_thoughts": ["理念论", "理想国", "哲学王"],
        "representative_works": ["理想国", "斐多篇", "会饮篇"],
        "famous_quotes": ["哲学开始于惊异"],
        "thinking_style": "理念构建",
        "personality": "理想主义",
        "speaking_style": "对话体",
        "mentors": ["苏格拉底"],
        "followers": ["亚里士多德"],
        "opponents": ["亚里士多德"],
        "related_thinkers": ["苏格拉底", "亚里士多德"]
    },
    "亚里士多德": {
        "name_en": "Aristotle",
        "era": "古代",
        "field": "philosophy",
        "nationality": "古希腊",
        "core_thoughts": ["形而上学", "四因说", "中庸之道"],
        "representative_works": ["形而上学", "尼各马可伦理学", "政治学"],
        "famous_quotes": ["求知是人类的本性"],
        "thinking_style": "分类归纳",
        "personality": "务实理性",
        "speaking_style": "系统论述",
        "mentors": ["柏拉图"],
        "followers": ["阿奎那", "康德"],
        "opponents": ["柏拉图"],
        "related_thinkers": ["柏拉图", "苏格拉底"]
    },
    "孔子": {
        "name_en": "Confucius",
        "era": "古代",
        "field": "philosophy",
        "nationality": "中国",
        "core_thoughts": ["仁", "礼", "君子", "大同"],
        "representative_works": ["论语", "大学", "中庸"],
        "famous_quotes": ["己所不欲，勿施于人"],
        "thinking_style": "伦理教化",
        "personality": "温文尔雅",
        "speaking_style": "格言体",
        "mentors": [],
        "followers": ["孟子", "荀子"],
        "opponents": ["墨子", "法家"],
        "related_thinkers": ["孟子", "荀子"]
    },
    "康德": {
        "name_en": "Immanuel Kant",
        "era": "近代",
        "field": "philosophy",
        "nationality": "德国",
        "core_thoughts": ["纯粹理性批判", "实践理性", "人为自然立法"],
        "representative_works": ["纯粹理性批判", "实践理性批判", "判断力批判"],
        "famous_quotes": ["有两种东西，我对它们的思考越是深沉和持久，它们在我心灵中唤起的惊奇和敬畏就会日新月异，这就是我头顶的星空和心中的道德律"],
        "thinking_style": "批判哲学",
        "personality": "严谨自律",
        "speaking_style": "体系化",
        "mentors": ["休谟", "莱布尼茨"],
        "followers": ["黑格尔", "费希特"],
        "opponents": [],
        "related_thinkers": ["休谟", "黑格尔"]
    },
    "尼采": {
        "name_en": "Friedrich Nietzsche",
        "era": "现代",
        "field": "philosophy",
        "nationality": "德国",
        "core_thoughts": ["超人哲学", "权力意志", "上帝已死", "永恒轮回"],
        "representative_works": ["查拉图斯特拉如是说", "权力意志", "道德的谱系"],
        "famous_quotes": ["那些知道自己为何而活的人，能承受任何一种活法"],
        "thinking_style": "价值重估",
        "personality": "反叛激进",
        "speaking_style": "格言警句",
        "mentors": ["叔本华"],
        "followers": ["海德格尔", "萨特"],
        "opponents": ["基督教伦理"],
        "related_thinkers": ["叔本华", "海德格尔"]
    },
    # 科学
    "牛顿": {
        "name_en": "Isaac Newton",
        "era": "近代",
        "field": "science",
        "nationality": "英国",
        "core_thoughts": ["万有引力", "三大运动定律", "微积分"],
        "representative_works": ["自然哲学的数学原理", "光学"],
        "famous_quotes": ["如果说我看得更远，那是因为我站在巨人的肩膀上"],
        "thinking_style": "数学演绎",
        "personality": "专注执着",
        "speaking_style": "精确简洁",
        "mentors": ["笛卡尔", "伽利略"],
        "followers": ["拉格朗日", "哈密顿"],
        "opponents": ["莱布尼茨"],
        "related_thinkers": ["爱因斯坦", "莱布尼茨"]
    },
    "爱因斯坦": {
        "name_en": "Albert Einstein",
        "era": "现代",
        "field": "science",
        "nationality": "德国/美国",
        "core_thoughts": ["相对论", "质能方程", "光量子"],
        "representative_works": ["狭义相对论", "广义相对论"],
        "famous_quotes": ["想象力比知识更重要"],
        "thinking_style": "思想实验",
        "personality": "好奇谦逊",
        "speaking_style": "通俗深刻",
        "mentors": [],
        "followers": ["玻尔", "霍金"],
        "opponents": ["玻尔"],
        "related_thinkers": ["牛顿", "玻尔"]
    },
    "达尔文": {
        "name_en": "Charles Darwin",
        "era": "近代",
        "field": "science",
        "nationality": "英国",
        "core_thoughts": ["自然选择", "进化论", "共同祖先"],
        "representative_works": ["物种起源", "人类的由来"],
        "famous_quotes": ["物竞天择，适者生存"],
        "thinking_style": "观察归纳",
        "personality": "谨慎细致",
        "speaking_style": "平实严谨",
        "mentors": ["莱尔"],
        "followers": ["华莱士", "道金斯"],
        "opponents": ["教会"],
        "related_thinkers": ["华莱士", "孟德尔"]
    },
    # 经济学
    "亚当斯密": {
        "name_en": "Adam Smith",
        "era": "近代",
        "field": "economics",
        "nationality": "英国",
        "core_thoughts": ["看不见的手", "分工理论", "自由市场"],
        "representative_works": ["国富论", "道德情操论"],
        "famous_quotes": ["我们有指望于晚餐，并非因为屠夫、酿酒商的仁慈"],
        "thinking_style": "经济分析",
        "personality": "理性温和",
        "speaking_style": "论述详尽",
        "mentors": ["休谟"],
        "followers": ["李嘉图", "凯恩斯"],
        "opponents": ["马克思"],
        "related_thinkers": ["凯恩斯", "马克思"]
    },
    "凯恩斯": {
        "name_en": "John Maynard Keynes",
        "era": "现代",
        "field": "economics",
        "nationality": "英国",
        "core_thoughts": ["凯恩斯主义", "政府干预", "总需求管理"],
        "representative_works": ["就业、利息和货币通论"],
        "famous_quotes": ["从长期来看，我们都死了"],
        "thinking_style": "宏观分析",
        "personality": "务实灵活",
        "speaking_style": "雄辩有力",
        "mentors": ["马歇尔"],
        "followers": ["萨缪尔森", "弗里德曼"],
        "opponents": ["弗里德曼", "哈耶克"],
        "related_thinkers": ["亚当斯密", "弗里德曼"]
    },
    "马克思": {
        "name_en": "Karl Marx",
        "era": "近代",
        "field": "economics",
        "nationality": "德国",
        "core_thoughts": ["剩余价值", "历史唯物主义", "阶级斗争"],
        "representative_works": ["资本论", "共产党宣言"],
        "famous_quotes": ["哲学家们只是用不同的方式解释世界，问题在于改变世界"],
        "thinking_style": "辩证唯物",
        "personality": "批判激进",
        "speaking_style": "号召动员",
        "mentors": ["黑格尔", "费尔巴哈"],
        "followers": ["列宁", "毛泽东"],
        "opponents": ["亚当斯密", "哈耶克"],
        "related_thinkers": ["恩格斯", "列宁"]
    },
    # 心理学
    "弗洛伊德": {
        "name_en": "Sigmund Freud",
        "era": "现代",
        "field": "psychology",
        "nationality": "奥地利",
        "core_thoughts": ["精神分析", "潜意识", "本我自我超我"],
        "representative_works": ["梦的解析", "精神分析引论"],
        "famous_quotes": ["没有被表达的情绪永远不会消失，它们只是被活埋了，有朝一日会以更丑恶的方式爆发出来"],
        "thinking_style": "临床分析",
        "personality": "洞察敏锐",
        "speaking_style": "案例叙述",
        "mentors": ["布洛伊尔"],
        "followers": ["荣格", "拉康"],
        "opponents": ["荣格"],
        "related_thinkers": ["荣格", "阿德勒"]
    },
    "荣格": {
        "name_en": "Carl Jung",
        "era": "现代",
        "field": "psychology",
        "nationality": "瑞士",
        "core_thoughts": ["集体潜意识", "原型", "人格类型"],
        "representative_works": ["原型与集体潜意识", "人及其象征"],
        "famous_quotes": ["直到你使潜意识变为意识，它将一直主宰你的生活，而你称之为命运"],
        "thinking_style": "原型分析",
        "personality": "神秘深邃",
        "speaking_style": "象征隐喻",
        "mentors": ["弗洛伊德"],
        "followers": ["坎贝尔"],
        "opponents": ["弗洛伊德"],
        "related_thinkers": ["弗洛伊德", "阿德勒"]
    },
    "行为经济学"
    "卡尼曼": {
        "name_en": "Daniel Kahneman",
        "era": "当代",
        "field": "economics/psychology",
        "nationality": "以色列/美国",
        "core_thoughts": ["前景理论", "有限理性", "认知偏差"],
        "representative_works": ["思考，快与慢"],
        "famous_quotes": ["我们对自己不了解的东西做出预测是非常困难的"],
        "thinking_style": "实验验证",
        "personality": "实证严谨",
        "speaking_style": "数据说话",
        "mentors": ["特沃斯基"],
        "followers": ["塞勒"],
        "opponents": [],
        "related_thinkers": ["塞勒", "特沃斯基"]
    },
    # 物理学
    "霍金": {
        "name_en": "Stephen Hawking",
        "era": "现代",
        "field": "science",
        "nationality": "英国",
        "core_thoughts": ["黑洞辐射", "宇宙大爆炸", "时间箭头"],
        "representative_works": ["时间简史", "果壳中的宇宙"],
        "famous_quotes": ["如果生活没有了乐趣，那将是一场悲剧"],
        "thinking_style": "理论物理",
        "personality": "幽默坚韧",
        "speaking_style": "通俗科普",
        "mentors": ["彭罗斯"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["爱因斯坦", "彭罗斯"]
    },
    "玻尔": {
        "name_en": "Niels Bohr",
        "era": "现代",
        "field": "science",
        "nationality": "丹麦",
        "core_thoughts": ["互补原理", "量子力学", "哥本哈根诠释"],
        "representative_works": ["玻尔文集"],
        "famous_quotes": ["如果量子力学没有让你感到震惊，那说明你还没理解它"],
        "thinking_style": "辩证思维",
        "personality": "开放谦逊",
        "speaking_style": "对话讨论",
        "mentors": ["卢瑟福"],
        "followers": ["海森堡"],
        "opponents": ["爱因斯坦"],
        "related_thinkers": ["爱因斯坦", "海森堡"]
    },
    # 计算机/AI
    "图灵": {
        "name_en": "Alan Turing",
        "era": "现代",
        "field": "technology",
        "nationality": "英国",
        "core_thoughts": ["图灵机", "人工智能", "图灵测试"],
        "representative_works": ["论可计算数及其在判定问题上的应用", "计算机器与智能"],
        "famous_quotes": ["我们只能看见前方很短的距离，但我们能够看到那里有很多需要去做的事情"],
        "thinking_style": "抽象计算",
        "personality": "天才内敛",
        "speaking_style": ["数学证明"],
        "mentors": ["丘奇"],
        "followers": ["冯诺依曼"],
        "opponents": [],
        "related_thinkers": ["冯诺依曼", "维特根斯坦"]
    },
    "冯诺依曼": {
        "name_en": "John von Neumann",
        "era": "现代",
        "field": "technology",
        "nationality": "匈牙利/美国",
        "core_thoughts": ["冯诺依曼架构", "博弈论", "计算机科学"],
        "representative_works": ["博弈论与经济行为", "计算机与人脑"],
        "famous_quotes": ["如果有人不相信数学是简单的，那是因为他们没有意识到人生有多复杂"],
        "thinking_style": ["数学建模"],
        "personality": ["博学多才"],
        "speaking_style": ["精确高效"],
        "mentors": ["希尔伯特"],
        "followers": ["图灵"],
        "opponents": [],
        "related_thinkers": ["图灵", "哥德尔"]
    },
    # 复杂系统
    "巴拉巴西": {
        "name_en": "Albert-László Barabási",
        "era": "当代",
        "field": "science/complex_systems",
        "nationality": "匈牙利",
        "core_thoughts": ["无标度网络", "复杂网络", "爆发"],
        "representative_works": ["链接", "爆发"],
        "famous_quotes": ["复杂网络无处不在"],
        "thinking_style": ["网络科学"],
        "personality": ["创新探索"],
        "speaking_style": ["案例驱动"],
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["瓦茨", "克劳塞特"]
    },
    # 社会学
    "韦伯": {
        "name_en": "Max Weber",
        "era": "近代",
        "field": "sociology",
        "nationality": "德国",
        "core_thoughts": ["官僚制", "新教伦理与资本主义", "理性化"],
        "representative_works": ["经济与社会", "新教伦理与资本主义精神"],
        "famous_quotes": ["人是悬挂在自己编织的意义之网上的动物"],
        "thinking_style": ["类型学"],
        "personality": ["严谨客观"],
        "speaking_style": ["概念分析"],
        "mentors": [],
        "followers": ["帕森斯"],
        "opponents": ["马克思"],
        "related_thinkers": ["涂尔干", "马克思"]
    },
    "涂尔干": {
        "name_en": "Émile Durkheim",
        "era": "近代",
        "field": "sociology",
        "nationality": "法国",
        "core_thoughts": ["社会分工论", "自杀论", "社会事实"],
        "representative_works": ["社会分工论", "自杀论"],
        "famous_quotes": ["社会是高于个人的实在"],
        "thinking_style": ["实证主义"],
        "personality": ["理性客观"],
        "speaking_style": ["社会事实"],
        "mentors": [],
        "followers": ["帕森斯"],
        "opponents": [],
        "related_thinkers": ["韦伯", "马克思"]
    },
}


# ============ 三设管理器 ============

class ThreeSetManager:
    """
    三设管理器
    
    管理:
    - 思想家设定
    - 思想设计
    - 实验验证
    """
    
    def __init__(self, storage=None):
        self.storage = storage
        self.thinkers: Dict[str, ThinkerProfile] = {}
        self.thoughts: Dict[str, ThoughtDesign] = {}
        self.experiments: Dict[str, ExperimentDesign] = {}
        
        self._init_presets()
        logger.info("三设管理器初始化完成")
    
    def _init_presets(self):
        """初始化思想家预设"""
        for name, data in THINKER_PRESETS.items():
            profile = ThinkerProfile(
                name=name,
                **data
            )
            self.thinkers[name] = profile
        logger.info(f"已初始化 {len(self.thinkers)} 位思想家")
    
    # ============ 思想家管理 ============
    
    def get_thinker(self, name: str) -> Optional[ThinkerProfile]:
        """获取思想家"""
        return self.thinkers.get(name)
    
    def list_thinkers(self, field: str = None, era: str = None) -> List[Dict]:
        """列出思想家 (支持筛选)"""
        result = list(self.thinkers.values())
        
        if field:
            result = [t for t in result if t.field == field]
        
        if era:
            result = [t for t in result if t.era == era]
        
        return [t.to_dict() for t in result]
    
    def add_thinker(self, profile: ThinkerProfile):
        """添加思想家"""
        self.thinkers[profile.name] = profile
        logger.info(f"添加思想家: {profile.name}")
    
    def generate_thinker_response(
        self,
        thinker_name: str,
        topic: str,
        style: str = "dialogue"
    ) -> str:
        """
        生成思想家风格的回复
        
        用于模拟思想家参与讨论
        """
        profile = self.thinkers.get(thinker_name)
        if not profile:
            return f"未知思想家: {thinker_name}"
        
        # 根据说话风格生成回复
        if style == "question":
            # 苏格拉底式提问
            return f"关于「{topic}」，让我先问你一个问题：{profile.famous_quotes[0] if profile.famous_quotes else '...'} 你怎么看？"
        elif style == "quote":
            # 名言式
            return f"这个问题让我想起{profile.name}的话：「{profile.famous_quotes[0] if profile.famous_quotes else '...'}」"
        elif style == "argument":
            # 论点式
            return f"我的核心观点是：{'；'.join(profile.core_thoughts[:2])}. 应用到「{topic}」，我认为..."
        else:
            # 对话式
            return f"{profile.name}曾说：「{profile.famous_quotes[0] if profile.famous_quotes else '...'}」. 至于「{topic}」，从{profile.thinking_style}的角度来看..."
    
    # ============ 思想管理 ============
    
    def get_thought(self, thought_id: str) -> Optional[ThoughtDesign]:
        """获取思想"""
        return self.thoughts.get(thought_id)
    
    def add_thought(self, thought: ThoughtDesign):
        """添加思想"""
        self.thoughts[thought.id] = thought
        logger.info(f"添加思想: {thought.title}")
    
    # ============ 实验管理 ============
    
    def get_experiment(self, exp_id: str) -> Optional[ExperimentDesign]:
        """获取实验"""
        return self.experiments.get(exp_id)
    
    def add_experiment(self, experiment: ExperimentDesign):
        """添加实验"""
        self.experiments[experiment.id] = experiment
        logger.info(f"添加实验: {experiment.title}")
    
    def verify_thought(self, thought_id: str) -> Dict:
        """
        验证思想
        
        收集相关实验，返回验证结果
        """
        relevant_exps = [
            e for e in self.experiments.values()
            if e.thought_id == thought_id
        ]
        
        supported = []
        challenged = []
        
        for exp in relevant_exps:
            supported.extend(exp.supported_claims)
            challenged.extend(exp.challenged_claims)
        
        return {
            "thought_id": thought_id,
            "experiment_count": len(relevant_exps),
            "supported_claims": list(set(supported)),
            "challenged_claims": list(set(challenged)),
            "evidence_strength": "strong" if len(relevant_exps) >= 3 else "moderate" if len(relevant_exps) >= 1 else "weak"
        }
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_thinkers": len(self.thinkers),
            "total_thoughts": len(self.thoughts),
            "total_experiments": len(self.experiments),
            "fields": list(set(t.field for t in self.thinkers.values())),
            "eras": list(set(t.era for t in self.thinkers.values()))
        }


# 全局实例
three_set_manager = ThreeSetManager()
