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


# ============ 新增思想家 (补充到100位) ============

THINKER_PRESETS.update({
    # 科学 - 补充
    "门捷列夫": {
        "name_en": "Dmitri Mendeleev",
        "era": "近代",
        "field": "science",
        "nationality": "俄罗斯",
        "core_thoughts": ["元素周期律", "周期表"],
        "representative_works": ["化学原理"],
        "famous_quotes": ["没有观测就没有科学"],
        "thinking_style": "系统分类",
        "personality": "严谨细致",
        "speaking_style": "数据导向",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["拉瓦锡", "玻尔"]
    },
    "居里夫人": {
        "name_en": "Marie Curie",
        "era": "现代",
        "field": "science",
        "nationality": "波兰/法国",
        "core_thoughts": ["放射性理论", "钋和镭的发现"],
        "representative_works": ["放射性论"],
        "famous_quotes": ["生活中没有可怕的事物，只有需要了解的事物"],
        "thinking_style": "实验驱动",
        "personality": "坚韧不拔",
        "speaking_style": "理性严谨",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["爱因斯坦", "卢瑟福"]
    },
    "卢瑟福": {
        "name_en": "Ernest Rutherford",
        "era": "现代",
        "field": "science",
        "nationality": "新西兰/英国",
        "core_thoughts": ["原子核模型", "核物理"],
        "representative_works": ["放射性转化"],
        "famous_quotes": ["科学要么是物理学，要么是集邮"],
        "thinking_style": "实验验证",
        "personality": "大胆创新",
        "speaking_style": "简洁有力",
        "mentors": ["汤姆森"],
        "followers": ["玻尔"],
        "opponents": [],
        "related_thinkers": ["汤姆森", "玻尔", "爱因斯坦"]
    },
    "薛定谔": {
        "name_en": "Erwin Schrödinger",
        "era": "现代",
        "field": "science",
        "nationality": "奥地利",
        "core_thoughts": ["量子力学波函数", "薛定谔方程", "薛定谔的猫"],
        "representative_works": ["量子力学统计学基础"],
        "famous_quotes": ["生命以负熵为生"],
        "thinking_style": "思想实验",
        "personality": "博学多才",
        "speaking_style": "哲学思辨",
        "mentors": [],
        "followers": [],
        "opponents": ["爱因斯坦"],
        "related_thinkers": ["爱因斯坦", "玻尔", "海森堡"]
    },
    "海森堡": {
        "name_en": "Werner Heisenberg",
        "era": "现代",
        "field": "science",
        "nationality": "德国",
        "core_thoughts": ["不确定性原理", "矩阵力学"],
        "representative_works": ["量子论的物理原理"],
        "famous_quotes": ["自然科学不是自然本身"],
        "thinking_style": ["数学优先"],
        "personality": ["深思熟虑"],
        "speaking_style": ["精确严谨"],
        "mentors": ["玻尔"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["玻尔", "薛定谔", "爱因斯坦"]
    },
    "狄拉克": {
        "name_en": "Paul Dirac",
        "era": "现代",
        "field": "science",
        "nationality": "英国",
        "core_thoughts": ["量子力学", "狄拉克方程", "反物质"],
        "representative_works": ["量子力学原理"],
        "famous_quotes": ["方程式是美的，物理是丑的"],
        "thinking_style": "数学美学",
        "personality": "沉默寡言",
        "speaking_style": "精简深奥",
        "mentors": ["汤姆森"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["薛定谔", "玻尔", "爱因斯坦"]
    },
    
    # 经济 - 补充
    "哈耶克": {
        "name_en": "Friedrich Hayek",
        "era": "现代",
        "field": "economics",
        "nationality": "奥地利/英国",
        "core_thoughts": ["自由主义", "自发秩序", "知识分散"],
        "representative_works": ["通往奴役之路", "自由秩序原理"],
        "famous_quotes": ["最坏者当政"],
        "thinking_style": "市场机制",
        "personality": "保守谨慎",
        "speaking_style": "学术严谨",
        "mentors": ["门格尔"],
        "followers": ["弗里德曼"],
        "opponents": ["凯恩斯", "马克思"],
        "related_thinkers": ["凯恩斯", "弗里德曼", "哈耶克"]
    },
    "弗里德曼": {
        "name_en": "Milton Friedman",
        "era": "现代",
        "field": "economics",
        "nationality": "美国",
        "core_thoughts": ["货币主义", "自由市场", "消费函数"],
        "representative_works": ["资本主义与自由"],
        "famous_quotes": ["天下没有免费的午餐"],
        "thinking_style": "数据实证",
        "personality": "直率务实",
        "speaking_style": "清晰有力",
        "mentors": ["哈耶克"],
        "followers": [],
        "opponents": ["凯恩斯"],
        "related_thinkers": ["哈耶克", "凯恩斯", "萨缪尔森"]
    },
    "萨缪尔森": {
        "name_en": "Paul Samuelson",
        "era": "现代",
        "field": "economics",
        "nationality": "美国",
        "core_thoughts": ["新古典综合", "显示偏好", "乘数-加速数"],
        "representative_works": ["经济学"],
        "famous_quotes": ["学习经济学是为了不被他所骗"],
        "thinking_style": "数学建模",
        "personality": "博学温和",
        "speaking_style": "清晰易懂",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["凯恩斯", "弗里德曼", "哈耶克"]
    },
    "熊彼特": {
        "name_en": "Joseph Schumpeter",
        "era": "现代",
        "field": "economics",
        "nationality": "奥地利/美国",
        "core_thoughts": ["创新理论", "创造性破坏", "企业家精神"],
        "representative_works": ["资本主义、社会主义与民主"],
        "famous_quotes": ["资本主义的敌人是资本主义的成功"],
        "thinking_style": "动态分析",
        "personality": "远见卓识",
        "speaking_style": "雄辩有力",
        "mentors": ["门格尔"],
        "followers": [],
        "opponents": ["凯恩斯"],
        "related_thinkers": ["凯恩斯", "哈耶克", "马克思"]
    },
    
    # 社会学 - 补充
    "福柯": {
        "name_en": "Michel Foucault",
        "era": "现代",
        "field": "sociology",
        "nationality": "法国",
        "core_thoughts": ["权力理论", "知识考古学", "规训与惩罚"],
        "representative_works": ["规训与惩罚", "性经验史"],
        "famous_quotes": ["权力无处不在"],
        "thinking_style": "话语分析",
        "personality": "批判锐利",
        "speaking_style": "深奥复杂",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["尼采", "德里达", "哈贝马斯"]
    },
    "哈贝马斯": {
        "name_en": "Jürgen Habermas",
        "era": "现代",
        "field": "sociology",
        "nationality": "德国",
        "core_thoughts": ["交往行动理论", "公共领域", "商谈伦理学"],
        "representative_works": ["交往行动理论"],
        "famous_quotes": ["生活世界殖民化"],
        "thinking_style": "系统整合",
        "personality": "理性温和",
        "speaking_style": "学术严谨",
        "mentors": ["阿多诺", "霍克海默"],
        "followers": [],
        "opponents": ["福柯", "德里达"],
        "related_thinkers": ["阿多诺", "福柯", "韦伯"]
    },
    "布迪厄": {
        "name_en": "Pierre Bourdieu",
        "era": "现代",
        "field": "sociology",
        "nationality": "法国",
        "core_thoughts": ["场域理论", "文化资本", "惯习"],
        "representative_works": ["区分: 判断力的社会批判"],
        "famous_quotes": ["文化是阶级斗争的场所"],
        "thinking_style": "场域分析",
        "personality": "批判深刻",
        "speaking_style": ["术语密集"],
        "mentors": ["阿尔都塞"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["阿尔都塞", "福柯", "马克思"]
    },
    "吉登斯": {
        "name_en": "Anthony Giddens",
        "era": "现代",
        "field": "sociology",
        "nationality": "英国",
        "core_thoughts": ["结构化理论", "现代性", "第三条道路"],
        "representative_works": ["民族-国家与暴力"],
        "famous_quotes": ["现代性是一种双重现象"],
        "thinking_style": "结构整合",
        "personality": "务实温和",
        "speaking_style": "清晰易懂",
        "mentors": [],
        "followers": [],
        "opponents": ["哈贝马斯"],
        "related_thinkers": ["哈贝马斯", "福柯", "韦伯"]
    },
    
    # 心理学 - 补充
    "皮亚杰": {
        "name_en": "Jean Piaget",
        "era": "现代",
        "field": "psychology",
        "nationality": "瑞士",
        "core_thoughts": ["认知发展理论", "建构主义", "图式理论"],
        "representative_works": ["儿童智慧的起源"],
        "famous_quotes": ["教育的目标是培养创造者"],
        "thinking_style": "发展观察",
        "personality": "耐心细致",
        "speaking_style": "实验描述",
        "mentors": [],
        "followers": ["科尔伯格"],
        "opponents": ["行为主义"],
        "related_thinkers": ["弗洛伊德", "科尔伯格", "维果茨基"]
    },
    "科尔伯格": {
        "name_en": "Lawrence Kohlberg",
        "era": "现代",
        "field": "psychology",
        "nationality": "美国",
        "core_thoughts": ["道德发展阶段", "道德推理"],
        "representative_works": ["道德发展 stages of moral development"],
        "famous_quotes": ["道德发展是认知发展的延续"],
        "thinking_style": "阶段分析",
        "personality": "理性客观",
        "speaking_style": "学术严谨",
        "mentors": ["皮亚杰"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["皮亚杰", "弗洛伊德", "维果茨基"]
    },
    "马斯洛": {
        "name_en": "Abraham Maslow",
        "era": "现代",
        "field": "psychology",
        "nationality": "美国",
        "core_thoughts": ["需求层次理论", "自我实现", "人本主义"],
        "representative_works": ["动机与人格"],
        "famous_quotes": ["当你钉锤子时，一切看起来都像钉子"],
        "thinking_style": "需求导向",
        "personality": "积极乐观",
        "speaking_style": ["激励人心"],
        "mentors": [],
        "followers": ["罗杰斯"],
        "opponents": ["行为主义", "精神分析"],
        "related_thinkers": ["弗洛伊德", "罗杰斯", "荣格"]
    },
    "罗杰斯": {
        "name_en": "Carl Rogers",
        "era": "现代",
        "field": "psychology",
        "nationality": "美国",
        "core_thoughts": ["来访者中心疗法", "无条件积极关注", "共情"],
        "representative_works": ["成为一个人"],
        "famous_quotes": ["成为你自己"],
        "thinking_style": ["来访者中心"],
        "personality": ["温暖真诚"],
        "speaking_style": ["倾听理解"],
        "mentors": [],
        "followers": [],
        "opponents": ["行为主义"],
        "related_thinkers": ["马斯洛", "弗洛伊德", "荣格"]
    },
    "塞利格曼": {
        "name_en": "Martin Seligman",
        "era": "现代",
        "field": "psychology",
        "nationality": "美国",
        "core_thoughts": ["习得性无助", "积极心理学"],
        "representative_works": ["习得性乐观"],
        "famous_quotes": ["真正的幸福来自优势和美德"],
        "thinking_style": "实验验证",
        "personality": "积极务实",
        "speaking_style": "通俗易懂",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["马斯洛", "弗洛伊德"]
    },
    
    # 技术 - 补充
    "乔布斯": {
        "name_en": "Steve Jobs",
        "era": "现代",
        "field": "technology",
        "nationality": "美国",
        "core_thoughts": ["产品哲学", "用户体验", "科技与人文的交汇"],
        "representative_works": ["乔布斯传"],
        "famous_quotes": ["Stay Hungry, Stay Foolish"],
        "thinking_style": "产品直觉",
        "personality": "追求完美",
        "speaking_style": "激情有力",
        "mentors": ["乔布斯"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["图灵", "冯诺依曼", "乔布斯"]
    },
    "贝索斯": {
        "name_en": "Jeff Bezos",
        "era": "现代",
        "field": "technology",
        "nationality": "美国",
        "core_thoughts": ["长期主义", "客户痴迷", "Day 1思维"],
        "representative_works": ["致股东的信"],
        "famous_quotes": ["利润是未来的护城河"],
        "thinking_style": "长期视角",
        "personality": "理性冷静",
        "speaking_style": "数据驱动",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["乔布斯", "马斯克", "扎克伯格"]
    },
    "马斯克": {
        "name_en": "Elon Musk",
        "era": "现代",
        "field": "technology",
        "nationality": "南非/美国",
        "core_thoughts": ["第一性原理", "多行星物种", "可持续能源"],
        "representative_works": ["埃隆·马斯克传"],
        "famous_quotes": ["当某事足够重要时，即使机会对你不利也要去做"],
        "thinking_style": "第一性原理",
        "personality": "大胆冒险",
        "speaking_style": ["直接有力"],
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["乔布斯", "爱因斯坦", "霍金"]
    },
    "扎克伯格": {
        "name_en": "Mark Zuckerberg",
        "era": "现代",
        "field": "technology",
        "nationality": "美国",
        "core_thoughts": ["社交图谱", "连接世界", "开放平台"],
        "representative_works": ["致股东的信"],
        "famous_quotes": ["快速行动，打破常规"],
        "thinking_style": "网络效应",
        "personality": ["理性内敛"],
        "speaking_style": "简洁直接",
        "mentors": ["乔布斯"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["乔布斯", "贝索斯", "库克"]
    },
    "纳德拉": {
        "name_en": "Satya Nadella",
        "era": "现代",
        "field": "technology",
        "nationality": "印度/美国",
        "core_thoughts": ["成长型思维", "云计算", "包容性创新"],
        "representative_works": ["刷新"],
        "famous_quotes": ["没有成长型思维，就没有微软的今天"],
        "thinking_style": "文化变革",
        "personality": "温和谦逊",
        "speaking_style": "鼓舞人心",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["乔布斯", "贝索斯", "盖茨"]
    },
    "黄仁勋": {
        "name_en": "Jensen Huang",
        "era": "现代",
        "field": "technology",
        "nationality": "台湾/美国",
        "core_thoughts": ["GPU计算", "AI革命", "加速计算"],
        "representative_works": ["演讲与采访"],
        "famous_quotes": ["CEO应该成为首席学习官"],
        "thinking_style": "架构思维",
        "personality": ["低调专注"],
        "speaking_style": "技术热情",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["图灵", "乔布斯", "纳德拉"]
    },
    
    # 政治 - 补充
    "丘吉尔": {
        "name_en": "Winston Churchill",
        "era": "现代",
        "field": "politics",
        "nationality": "英国",
        "core_thoughts": ["民主政治", "冷战思维", "领导力"],
        "representative_works": ["第二次世界大战回忆录"],
        "famous_quotes": ["民主是最坏的制度，但这是我们试过的最好的制度"],
        "thinking_style": ["历史比较"],
        "personality": ["坚韧不拔"],
        "speaking_style": ["雄辩有力"],
        "mentors": [],
        "followers": ["撒切尔"],
        "opponents": ["希特勒"],
        "related_thinkers": ["甘地", "罗斯福", "斯大林"]
    },
    "甘地": {
        "name_en": "Mahatma Gandhi",
        "era": "现代",
        "field": "politics",
        "nationality": "印度",
        "core_thoughts": ["非暴力不合作", "素食主义", "简单生活"],
        "representative_works": ["我体验真理的故事"],
        "famous_quotes": ["要改变世界，先改变自己"],
        "thinking_style": ["道德优先"],
        "personality": ["平和坚定"],
        "speaking_style": ["简洁有力"],
        "mentors": [],
        "followers": ["马丁路德金"],
        "opponents": ["殖民主义者"],
        "related_thinkers": ["托尔斯泰", "丘吉尔", "马丁路德金"]
    },
    "曼德拉": {
        "name_en": "Nelson Mandela",
        "era": "现代",
        "field": "politics",
        "nationality": "南非",
        "core_thoughts": ["种族和解", "民主南非", "宽恕与正义"],
        "representative_works": ["漫漫自由路"],
        "famous_quotes": ["教育是最有力的武器"],
        "thinking_style": ["道德领导"],
        "personality": ["宽容坚韧"],
        "speaking_style": ["鼓舞人心"],
        "mentors": [],
        "followers": [],
        "opponents": ["种族隔离制度"],
        "related_thinkers": ["甘地", "马丁路德金", "丘吉尔"]
    },
    
    # 艺术 - 补充
    "达芬奇": {
        "name_en": "Leonardo da Vinci",
        "era": "文艺复兴",
        "field": "arts",
        "nationality": "意大利",
        "core_thoughts": ["艺术科学融合", "人体解剖", "飞行器设计"],
        "representative_works": ["蒙娜丽莎", "最后的晚餐"],
        "famous_quotes": ["绘画是诗"],
        "thinking_style": "观察细致",
        "personality": "好奇多才",
        "speaking风格": "沉默内敛",
        "mentors": ["韦罗基奥"],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["米开朗基罗", "拉斐尔"]
    },
    "米开朗基罗": {
        "name_en": "Michelangelo",
        "era": "文艺复兴",
        "field": "arts",
        "nationality": "意大利",
        "core_thoughts": ["人体美", "雕塑精神", "西斯廷壁画"],
        "representative_works": ["大卫", "创世纪"],
        "famous_quotes": ["我在大理石中看到了天使"],
        "thinking_style": "完美主义",
        "personality": ["孤僻固执"],
        "speaking_style": "少言寡语",
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["达芬奇", "拉斐尔", "布鲁内莱斯基"]
    },
    "贝多芬": {
        "name_en": "Ludwig van Beethoven",
        "era": "古典",
        "field": "arts",
        "nationality": "德国",
        "core_thoughts": ["交响曲革新", "命运主题", "浪漫主义先驱"],
        "representative_works": ["命运交响曲", "第九交响曲"],
        "famous_quotes": ["通过苦难走向欢乐"],
        "thinking_style": "情感表达",
        "personality": ["坚韧不屈"],
        "speaking_style": "直接强烈",
        "mentors": ["海顿"],
        "followers": ["勃拉姆斯", "瓦格纳"],
        "opponents": [],
        "related_thinkers": ["莫扎特", "海顿", "勃拉姆斯"]
    },
    "莫奈": {
        "name_en": "Claude Monet",
        "era": "近代",
        "field": "arts",
        "nationality": "法国",
        "core_thoughts": ["印象派", "光影捕捉", "自然观察"],
        "representative_works": ["印象·日出", "睡莲系列"],
        "famous_quotes": ["我只想画出自己的眼睛所见"],
        "thinking_style": "感官优先",
        "personality": ["温和敏感"],
        "speaking_style": "少言多画",
        "mentors": [],
        "followers": ["雷诺阿", "毕沙罗"],
        "opponents": ["学院派"],
        "related_thinkers": ["毕沙罗", "雷诺阿", "马奈"]
    },
    "梵高": {
        "name_en": "Vincent van Gogh",
        "era": "近代",
        "field": "arts",
        "nationality": "荷兰",
        "core_thoughts": ["后印象派", "情感表达", "色彩革命"],
        "representative_works": ["星夜", "向日葵", "自画像"],
        "famous_quotes": ["我越来越相信，创造美好的事物就是一种祈祷"],
        "thinking_style": "情感驱动",
        "personality": ["敏感热情"],
        "speaking_style": "书信倾诉",
        "mentors": ["高更"],
        "followers": [],
        "opponents": ["学院派"],
        "related_thinkers": ["高更", "塞尚", "毕加索"]
    },
    "毕加索": {
        "name_en": "Pablo Picasso",
        "era": "现代",
        "field": "arts",
        "nationality": "西班牙",
        "core_thoughts": ["立体主义", "形式革命", "艺术多变"],
        "representative_works": ["亚维农的少女", "格尔尼卡"],
        "famous_quotes": ["艺术是一种谎言"],
        "thinking_style": ["形式突破"],
        "personality": ["多才多情"],
        "speaking_style": ["简洁有力"],
        "mentors": [],
        "followers": ["马蒂斯"],
        "opponents": [],
        "related_thinkers": ["梵高", "马蒂斯", "塞尚"]
    },
    
    # 未来/科幻
    "阿西莫夫": {
        "name_en": "Isaac Asimov",
        "era": "现代",
        "field": "science",
        "nationality": "俄罗斯/美国",
        "core_thoughts": ["机器人三定律", "基地系列", "科普传播"],
        "representative_works": ["基地", "机器人系列"],
        "famous_quotes": ["科学开始于神话的终结"],
        "thinking_style": ["逻辑推演"],
        "personality": ["博学多产"],
        "speaking_style": ["清晰易懂"],
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["图灵", "霍金", "库兹韦尔"]
    },
    "库兹韦尔": {
        "name_en": "Ray Kurzweil",
        "era": "现代",
        "field": "technology",
        "nationality": "美国",
        "core_thoughts": ["奇点理论", "技术融合", "人工智能超越人类"],
        "representative_works": ["奇点临近"],
        "famous_quotes": ["我们将与机器融合"],
        "thinking_style": ["趋势外推"],
        "personality": ["乐观技术派"],
        "speaking_style": ["数据支撑"],
        "mentors": [],
        "followers": [],
        "opponents": [],
        "related_thinkers": ["图灵", "霍金", "阿西莫夫"]
    },
})


# 全局实例
three_set_manager = ThreeSetManager()
