"""
SuiLight Knowledge Salon - 批量胶囊生成器
生成覆盖全领域的胶囊，让知识图谱丰富好用
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List

# 胶囊存储
capsules = []


def create_capsule(
    title: str,
    insight: str,
    category: str,
    keywords: List[str],
    source_agents: List[str],
    evidence: List[str] = None,
    action_items: List[str] = None,
    quality: int = 70
) -> Dict:
    """创建胶囊"""
    capsule = {
        "id": f"cap_{uuid.uuid4().hex[:8]}",
        "title": title,
        "insight": insight,
        "summary": insight[:80] + "...",
        "evidence": evidence or [],
        "action_items": action_items or [],
        "questions": [],
        "source_agents": source_agents,
        "keywords": keywords,
        "category": category,
        "dimensions": {
            "truth_score": quality,
            "goodness_score": quality - 5,
            "beauty_score": quality - 10,
            "intelligence_score": quality + 5,
            "total_score": quality
        },
        "quality_score": quality,
        "grade": "A" if quality >= 80 else "B" if quality >= 60 else "C",
        "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    capsules.append(capsule)
    return capsule


# ============ 自然科学胶囊 ============

# 物理学
create_capsule(
    title="相对论揭示时空本质",
    insight="时间和空间不是绝对的，而是相互关联的统一整体，质量和能量可以相互转化",
    category="physics",
    keywords=["相对论", "时空", "质能方程", "爱因斯坦", "量子物理"],
    source_agents=["爱因斯坦", "牛顿", "霍金"],
    evidence=["E=mc²", "光线弯曲实验", "GPS卫星时间校正"],
    action_items=["理解相对论的基本原理", "应用GPS时间校正"],
    quality=85
)

create_capsule(
    title="量子叠加与纠缠",
    insight="量子系统可以同时处于多个状态的叠加，纠缠粒子之间存在超距作用",
    category="physics",
    keywords=["量子", "叠加", "纠缠", "薛定谔", "贝尔不等式"],
    source_agents=["薛定谔", "爱因斯坦", "玻尔", "贝尔"],
    evidence=["双缝干涉实验", "量子隐形传态实验"],
    action_items=["研究量子通信技术", "探索量子计算可能性"],
    quality=88
)

create_capsule(
    title="热力学第二定律",
    insight="孤立系统的熵总是增加的，宏观过程不可逆",
    category="physics",
    keywords=["热力学", "熵", "不可逆", "克劳修斯"],
    source_agents=["克劳修斯", "玻尔兹曼"],
    evidence=["卡诺循环", "麦克斯韦妖思想实验"],
    action_items=["理解熵增原理", "应用于工程系统"],
    quality=75
)

create_capsule(
    title="电磁波谱与光",
    insight="光是电磁波的一种，可见光只是电磁波谱的一小部分",
    category="physics",
    keywords=["电磁波", "光", "频谱", "麦克斯韦"],
    source_agents=["麦克斯韦", "赫兹"],
    evidence=["电磁波实验", "光电效应"],
    action_items=["应用电磁波技术", "理解光的本质"],
    quality=72
)

# 化学
create_capsule(
    title="元素周期表的规律",
    insight="元素的性质随原子序数呈周期性变化，这是由电子排布规律决定的",
    category="chemistry",
    keywords=["元素周期表", "原子序数", "电子排布", "门捷列夫"],
    source_agents=["门捷列夫", "玻尔"],
    evidence=["元素周期律发现", "新元素预测验证"],
    action_items=["记忆关键元素", "理解周期律本质"],
    quality=78
)

create_capsule(
    title="化学反应速率与活化能",
    insight="化学反应速率由活化能决定，催化剂通过降低活化能加快反应",
    category="chemistry",
    keywords=["反应速率", "活化能", "催化剂", "阿伦尼乌斯"],
    source_agents=["阿伦尼乌斯", "奥斯特瓦尔德"],
    evidence=["催化剂应用案例", "反应动力学实验"],
    action_items=["理解反应机理", "优化工业反应条件"],
    quality=74
)

create_capsule(
    title="有机反应机理",
    insight="有机反应遵循特定的机理，如亲电加成、亲核取代、自由基反应",
    category="chemistry",
    keywords=["有机化学", "反应机理", "亲电", "亲核"],
    source_agents=["伍德沃德", "布朗"],
    evidence=["有机合成案例", "机理研究实验"],
    action_items=["掌握主要机理", "应用于有机合成"],
    quality=76
)

# 生物学
create_capsule(
    title="进化论与自然选择",
    insight="物种通过自然选择逐渐演化，适应环境的特征被保留下来",
    category="biology",
    keywords=["进化", "自然选择", "适者生存", "达尔文"],
    source_agents=["达尔文", "华莱士"],
    evidence=["达尔文雀研究", "抗生素抗性"],
    action_items=["理解进化机制", "应用于农业育种"],
    quality=85
)

create_capsule(
    title="DNA双螺旋结构",
    insight="DNA通过双螺旋结构存储遗传信息，碱基配对保证了复制的准确性",
    category="biology",
    keywords=["DNA", "双螺旋", "遗传", "碱基配对", "沃森"],
    source_agents=["沃森", "克里克", "富兰克林"],
    evidence=["DNA X射线衍射", "人类基因组计划"],
    action_items=["理解遗传机制", "应用于基因治疗"],
    quality=90
)

create_capsule(
    title="细胞能量代谢",
    insight="细胞通过呼吸作用将葡萄糖分解为ATP，为生命活动提供能量",
    category="biology",
    keywords=["细胞", "呼吸作用", "ATP", "线粒体"],
    source_agents=["克雷布斯", "米切尔"],
    evidence=["克雷布斯循环", "化学渗透理论"],
    action_items=["理解能量代谢", "应用于医学研究"],
    quality=80
)

create_capsule(
    title="生态系统与食物链",
    insight="生态系统中的生物通过食物链和食物网相互关联，形成复杂的生态网络",
    category="biology",
    keywords=["生态系统", "食物链", "生产者", "消费者", "分解者"],
    source_agents=["奥德姆"],
    evidence=["生态调查数据", "食物网分析"],
    action_items=["理解生态关系", "应用于环境保护"],
    quality=72
)

# 数学
create_capsule(
    title="微积分基本定理",
    insight="微分和积分是互逆运算，定理将两者联系起来",
    category="mathematics",
    keywords=["微积分", "导数", "积分", "牛顿", "莱布尼茨"],
    source_agents=["牛顿", "莱布尼茨"],
    evidence=["微积分应用案例", "数学证明"],
    action_items=["掌握微积分技巧", "应用于科学计算"],
    quality=88
)

create_capsule(
    title="概率论与统计学",
    insight="概率描述随机事件的规律，统计从数据中提取规律",
    category="mathematics",
    keywords=["概率", "统计", "随机", "高斯"],
    source_agents=["高斯", "费希尔"],
    evidence=["统计调查", "概率模型验证"],
    action_items=["理解概率思维", "应用于数据分析"],
    quality=82
)

create_capsule(
    title="群论与对称性",
    insight="群论是研究对称性的数学工具，在物理学和化学中有广泛应用",
    category="mathematics",
    keywords=["群论", "对称性", "伽罗瓦"],
    source_agents=["伽罗瓦", "诺特"],
    evidence=["晶体结构分析", "粒子物理标准模型"],
    action_items=["理解对称性", "应用于理论物理"],
    quality=78
)

create_capsule(
    title="图论与网络科学",
    insight="图论研究点与边的关系，网络科学将其应用于复杂系统分析",
    category="mathematics",
    keywords=["图论", "网络", "节点", "边", "欧拉"],
    source_agents=["欧拉", "巴拉斯"],
    evidence=["社交网络分析", "互联网结构研究"],
    action_items=["理解网络结构", "应用于社会网络"],
    quality=80
)

# 天文学
create_capsule(
    title="宇宙大爆炸理论",
    insight="宇宙起源于一个极热极密的初始状态，随后不断膨胀冷却",
    category="astronomy",
    keywords=["大爆炸", "宇宙膨胀", "哈勃", "宇宙微波背景"],
    source_agents=["哈勃", "伽莫夫"],
    evidence=["宇宙微波背景辐射", "哈勃定律"],
    action_items=["理解宇宙起源", "探索宇宙演化"],
    quality=86
)

create_capsule(
    title="黑洞与引力波",
    insight="黑洞是引力极强的时空区域，引力波是时空涟漪",
    category="astronomy",
    keywords=["黑洞", "引力波", "霍金", "爱因斯坦"],
    source_agents=["霍金", "爱因斯坦", "索恩"],
    evidence=["引力波探测", "黑洞照片"],
    action_items=["理解黑洞物理", "探测引力波信号"],
    quality=89
)

create_capsule(
    title="恒星生命周期",
    insight="恒星经历诞生、主序星、红巨星、白矮星/中子星/黑洞等阶段",
    category="astronomy",
    keywords=["恒星", "核聚变", "超新星", "钱德拉塞卡"],
    source_agents=["钱德拉塞卡", "爱丁顿"],
    evidence=["恒星观测数据", "超新星遗迹"],
    action_items=["理解恒星演化", "探索元素起源"],
    quality=77
)

# 地球科学
create_capsule(
    title="板块构造理论",
    insight="地球表面由多个板块组成，板块运动导致地震、火山和山脉形成",
    category="earth_science",
    keywords=["板块构造", "地震", "火山", "大陆漂移"],
    source_agents=["魏格纳", "赫斯"],
    evidence=["地震带分布", "海底扩张"],
    action_items=["理解地质活动", "应用于地震预警"],
    quality=83
)

create_capsule(
    title="气候变化与温室效应",
    insight="温室气体导致地球大气保温增强，引起全球气候变暖",
    category="earth_science",
    keywords=["气候变化", "温室效应", "二氧化碳", "碳循环"],
    source_agents=["基林", "汉森"],
    evidence=["冰芯数据", "气温观测记录"],
    action_items=["理解气候变化", "采取减排措施"],
    quality=85
)


# ============ 社会科学胶囊 ============

# 经济学
create_capsule(
    title="供需关系与价格机制",
    insight="市场价格由供需关系决定，价格信号引导资源有效配置",
    category="economics",
    keywords=["供需", "价格机制", "市场均衡", "亚当斯密"],
    source_agents=["亚当斯密", "马歇尔"],
    evidence=["市场实验", "价格波动案例"],
    action_items=["理解市场机制", "分析价格变动"],
    quality=80
)

create_capsule(
    title="凯恩斯主义经济学",
    insight="政府可以通过财政和货币政策调节总需求，应对经济衰退",
    category="economics",
    keywords=["凯恩斯", "财政政策", "货币政策", "总需求"],
    source_agents=["凯恩斯", "弗里德曼"],
    evidence=["大萧条应对", "2008金融危机"],
    action_items=["理解宏观调控", "分析经济政策"],
    quality=78
)

create_capsule(
    title="行为经济学",
    insight="人的经济决策受认知偏差和情感因素影响，理性人假设不完全成立",
    category="economics",
    keywords=["行为经济", "有限理性", "认知偏差", "卡尼曼"],
    source_agents=["卡尼曼", "塞勒"],
    evidence=["实验经济学研究", "行为干预案例"],
    action_items=["理解行为偏差", "设计行为干预"],
    quality=82
)

create_capsule(
    title="货币与通货膨胀",
    insight="通货膨胀是货币购买力下降，弗里德曼认为通胀永远是货币现象",
    category="economics",
    keywords=["货币", "通胀", "购买力", "弗里德曼"],
    source_agents=["弗里德曼", "费雪"],
    evidence=["通胀历史数据", "货币政策案例"],
    action_items=["理解货币本质", "分析通胀原因"],
    quality=76
)

# 心理学
create_capsule(
    title="认知偏差与决策",
    insight="人类决策存在系统性偏差，如锚定效应、可得性启发、确认偏误",
    category="psychology",
    keywords=["认知偏差", "决策", "卡尼曼", "启发式"],
    source_agents=["卡尼曼", "特沃斯基"],
    evidence=["认知心理学实验", "行为经济学研究"],
    action_items=["识别认知偏差", "改进决策质量"],
    quality=85
)

create_capsule(
    title="动机理论与自我决定",
    insight="内在动机比外在激励更持久，自主、胜任、归属是人类的基本心理需求",
    category="psychology",
    keywords=["动机", "自我决定", "德西", "马斯洛"],
    source_agents=["德西", "马斯洛", "麦克利兰"],
    evidence=["动机实验", "员工激励研究"],
    action_items=["激发内在动机", "设计激励机制"],
    quality=80
)

create_capsule(
    title="社会影响与从众",
    insight="人的行为受社会影响，群体压力会导致从众行为",
    category="psychology",
    keywords=["从众", "社会影响", "阿希", "米尔格拉姆"],
    source_agents=["阿希", "米尔格拉姆", "津巴多"],
    evidence=["从众实验", "权威服从实验"],
    action_items=["理解社会影响", "保持独立判断"],
    quality=82
)

create_capsule(
    title="记忆与学习机制",
    insight="记忆包括编码、存储、提取三个阶段，间隔重复和精细加工提高记忆效果",
    category="psychology",
    keywords=["记忆", "学习", "艾宾浩斯", "认知负荷"],
    source_agents=["艾宾浩斯", "布鲁纳"],
    evidence=["记忆实验", "学习策略研究"],
    action_items=["优化学习方法", "提高记忆效率"],
    quality=79
)

# 社会学
create_capsule(
    title="社会分层与流动",
    insight="社会分层是指社会成员按一定标准分成不同等级，社会流动反映阶层变化",
    category="sociology",
    keywords=["社会分层", "阶层流动", "布迪厄"],
    source_agents=["布迪厄", "马克思", "韦伯"],
    evidence=["社会调查数据", "代际流动研究"],
    action_items=["理解社会结构", "促进社会公平"],
    quality=77
)

create_capsule(
    title="社会网络与弱关系",
    insight="弱关系在信息传播和社会流动中起重要作用，格兰诺维特提出强关系与弱关系理论",
    category="sociology",
    keywords=["社会网络", "弱关系", "格兰诺维特"],
    source_agents=["格兰诺维特", "博特"],
    evidence=["求职研究", "信息传播研究"],
    action_items=["拓展社交网络", "利用弱关系资源"],
    quality=81
)

create_capsule(
    title="文化与社会建构",
    insight="社会现实是社会建构的，文化规范影响人们对世界的认知和行为",
    category="sociology",
    keywords=["社会建构", "文化", "涂尔干"],
    source_agents=["涂尔干", "伯格", "卢曼"],
    evidence=["文化研究", "社会事实分析"],
    action_items=["理解文化影响", "反思常识假设"],
    quality=75
)

# 政治学
create_capsule(
    title="民主与威权的比较",
    insight="不同政治体制在合法性来源、政策效果、公民自由方面存在差异",
    category="political_science",
    keywords=["民主", "威权", "政体", "政治体制"],
    source_agents=["熊彼特", "普沃斯基"],
    evidence=["民主化研究", "政体转型案例"],
    action_items=["理解政治体制", "分析民主质量"],
    quality=78
)

create_capsule(
    title="国际关系理论",
    insight="现实主义、自由制度主义、建构主义提供理解国际关系的不同视角",
    category="political_science",
    keywords=["国际关系", "现实主义", "自由主义", "建构主义"],
    source_agents=["摩根索", "基欧汉", "温特"],
    evidence=["国际危机案例", "国际制度研究"],
    action_items=["理解国际格局", "分析国际政策"],
    quality=80
)

create_capsule(
    title="公共政策分析",
    insight="政策过程包括议程设置、政策制定、政策执行、政策评估等阶段",
    category="political_science",
    keywords=["公共政策", "政策过程", "政策分析"],
    source_agents=["拉斯韦尔", "普雷斯曼"],
    evidence=["政策案例分析", "政策评估研究"],
    action_items=["理解政策过程", "参与政策讨论"],
    quality=76
)

# 法学
create_capsule(
    title="法治与人治的区别",
    insight="法治强调法律至上、权力制衡，人治依赖个人权威和意志",
    category="law",
    keywords=["法治", "人治", "权力制衡", "法治精神"],
    source_agents=["亚里士多德", "哈耶克", "富勒"],
    evidence=["法治指数研究", "历史案例对比"],
    action_items=["理解法治价值", "维护法治精神"],
    quality=79
)

create_capsule(
    title="权利与义务的关系",
    insight="法律权利与义务相互依存，权利需要他人义务的履行来保障",
    category="law",
    keywords=["权利", "义务", "法律关系", "权利本位"],
    source_agents=["凯尔森", "哈特"],
    evidence=["权利案例", "法律关系分析"],
    action_items=["理解权利义务", "维护合法权益"],
    quality=74
)


# ============ 人文科学胶囊 ============

# 哲学
create_capsule(
    title="认识论的核心问题",
    insight="知识是什么？我们如何知道我们所知道的？认识论探讨知识的本质和界限",
    category="philosophy",
    keywords=["认识论", "知识", "信念", "柏拉图", "休谟"],
    source_agents=["柏拉图", "休谟", "康德"],
    evidence=["经典思想实验", "知识论论证"],
    action_items=["反思知识基础", "追问确定性"],
    quality=84
)

create_capsule(
    title="伦理学的主要流派",
    insight="功利主义强调后果，义务论强调规则，美德伦理学强调品格",
    category="philosophy",
    keywords=["伦理学", "功利主义", "义务论", "美德伦理"],
    source_agents=["边沁", "康德", "亚里士多德"],
    evidence=["电车难题", "伦理学争论案例"],
    action_items=["理解伦理框架", "应用于道德判断"],
    quality=82
)

create_capsule(
    title="形而上学与存在",
    insight="形而上学探讨存在的本质、实体与属性、可能性与必然性等根本问题",
    category="philosophy",
    keywords=["形而上学", "存在", "实体", "亚里士多德"],
    source_agents=["亚里士多德", "海德格尔", "蒯因"],
    evidence=["存在论分析", "形而上学论证"],
    action_items=["思考存在问题", "反思实在本质"],
    quality=78
)

create_capsule(
    title="心灵哲学与意识",
    insight="意识如何产生？心身关系是物理的还是二元论？心灵哲学探讨这些问题",
    category="philosophy",
    keywords=["心灵哲学", "意识", "心身问题", "心身二元论"],
    source_agents=["笛卡尔", "查尔默斯", "丹尼特"],
    evidence=["意识研究", "心智哲学讨论"],
    action_items=["反思心灵本质", "理解意识难题"],
    quality=83
)

# 历史学
create_capsule(
    title="历史研究的范式",
    insight="年鉴学派关注长时段结构，叙事史学强调事件故事，后现代主义质疑历史客观性",
    category="history",
    keywords=["历史范式", "年鉴学派", "叙事史学", "后现代主义"],
    source_agents=["布罗代尔", "怀特", "阿隆"],
    evidence=["史学研究", "历史哲学讨论"],
    action_items=["理解历史方法", "反思历史叙事"],
    quality=76
)

create_capsule(
    title="文明兴衰的规律",
    insight="斯宾格勒提出文明有机体论，汤因比用挑战与应战解释文明兴起与衰落",
    category="history",
    keywords=["文明兴衰", "斯宾格勒", "汤因比", "历史周期"],
    source_agents=["斯宾格勒", "汤因比"],
    evidence=["文明比较研究", "历史周期分析"],
    action_items=["理解文明规律", "反思当下处境"],
    quality=75
)

# 文学
create_capsule(
    title="文学理论与批评",
    insight="形式主义关注文本结构，后结构主义解构意义，马克思主义关注意识形态",
    category="literature",
    keywords=["文学理论", "形式主义", "解构主义", "马克思主义"],
    source_agents=["索绪尔", "德里达", "阿尔都塞"],
    evidence=["文本分析案例", "批评实践"],
    action_items=["运用文学理论", "深化文本理解"],
    quality=77
)

# 艺术
create_capsule(
    title="艺术本质与功能",
    insight="艺术是模仿、表现还是形式？艺术具有审美、教育、社会批判等多重功能",
    category="art",
    keywords=["艺术本质", "模仿说", "表现说", "形式说"],
    source_agents=["亚里士多德", "科林伍德", "本雅明"],
    evidence=["艺术史研究", "美学理论"],
    action_items=["思考艺术价值", "理解艺术功能"],
    quality=73
)

# 宗教
create_capsule(
    title="宗教的本质与功能",
    insight="宗教是对神圣的回应，提供意义系统、社会整合和情感慰藉",
    category="religion",
    keywords=["宗教本质", "神圣", "涂尔干", "韦伯"],
    source_agents=["涂尔干", "韦伯", "弗洛伊德"],
    evidence=["宗教现象学", "宗教社会学"],
    action_items=["理解宗教现象", "保持开放态度"],
    quality=75
)

# 语言学
create_capsule(
    title="语言的结构与功能",
    insight="语言有音系、句法、语义、语用等多个层面，功能语言学强调语言的交际功能",
    category="linguistics",
    keywords=["语言结构", "功能语言学", "乔姆斯基"],
    source_agents=["乔姆斯基", "韩礼德", "索绪尔"],
    evidence=["语言分析案例", "语言习得研究"],
    action_items=["理解语言系统", "提高语言能力"],
    quality=80
)


# ============ 技术工程胶囊 ============

# 计算机科学
create_capsule(
    title="算法与计算复杂度",
    insight="算法是解决问题的步骤，复杂度分析帮助我们理解和优化算法效率",
    category="computer_science",
    keywords=["算法", "复杂度", "P vs NP", "图灵"],
    source_agents=["图灵", "库克", "蔡廷"],
    evidence=["算法竞赛", "复杂度理论"],
    action_items=["掌握基础算法", "理解复杂度分析"],
    quality=85
)

create_capsule(
    title="软件工程原则",
    insight="模块化、抽象、面向对象、设计模式是构建可维护软件的核心原则",
    category="computer_science",
    keywords=["软件工程", "模块化", "设计模式", "面向对象"],
    source_agents=["伽马", "梅耶"],
    evidence=["软件架构案例", "重构实践"],
    action_items=["遵循工程原则", "提高代码质量"],
    quality=79
)

create_capsule(
    title="数据库系统原理",
    insight="关系数据库通过SQL操作数据，事务ACID特性保证数据一致性",
    category="computer_science",
    keywords=["数据库", "SQL", "事务", "ACID"],
    source_agents=["科德", "格雷"],
    evidence=["数据库设计", "事务处理案例"],
    action_items=["掌握数据库设计", "理解事务原理"],
    quality=78
)

create_capsule(
    title="计算机网络体系",
    insight="OSI模型和TCP/IP协议族是网络通信的基础，分层设计简化了复杂性",
    category="computer_science",
    keywords=["计算机网络", "TCP/IP", "OSI模型", "分层"],
    source_agents=["Cerf", "卡恩"],
    evidence=["网络协议", "互联网架构"],
    action_items=["理解网络原理", "排查网络问题"],
    quality=77
)

# 工程学
create_capsule(
    title="系统工程方法",
    insight="系统工程通过整体优化方法解决复杂工程问题，强调需求分析和权衡决策",
    category="engineering",
    keywords=["系统工程", "需求分析", "权衡决策"],
    source_agents=["钱学森"],
    evidence=["航天工程案例", "复杂系统设计"],
    action_items=["掌握系统工程", "应用于项目管理"],
    quality=76
)

create_capsule(
    title="材料科学基础",
    insight="材料的性能由其微观结构决定，新材料研发推动技术进步",
    category="engineering",
    keywords=["材料科学", "微观结构", "纳米材料"],
    source_agents=["克兰斯顿"],
    evidence=["材料研发", "应用案例"],
    action_items=["理解材料性能", "关注新材料发展"],
    quality=74
)

# 医学
create_capsule(
    title="循证医学原则",
    insight="循证医学将最佳研究证据、临床经验和患者价值观相结合指导医疗决策",
    category="medicine",
    keywords=["循证医学", "临床指南", "随机对照试验"],
    source_agents=["萨克特"],
    evidence=["临床试验", "指南制定"],
    action_items=["理解循证原则", "应用于医疗决策"],
    quality=82
)

create_capsule(
    title="精准医疗与基因组学",
    insight="基于个体基因组信息的精准医疗正在改变疾病预防和治疗方式",
    category="medicine",
    keywords=["精准医疗", "基因组学", "个性化治疗"],
    source_agents=["柯林斯", "沃森"],
    evidence=["基因组计划", "靶向治疗案例"],
    action_items=["关注精准医疗", "理解基因组应用"],
    quality=84
)

# 人工智能
create_capsule(
    title="机器学习基础",
    insight="机器学习通过数据自动学习模型，包括监督学习、无监督学习和强化学习",
    category="ai",
    keywords=["机器学习", "监督学习", "无监督学习", "深度学习"],
    source_agents=["明斯基", "辛顿", "杨立昆"],
    evidence=["算法竞赛", "实际应用案例"],
    action_items=["掌握机器学习", "应用于实际问题"],
    quality=86
)

create_capsule(
    title="深度学习与神经网络",
    insight="深度神经网络通过多层结构学习数据的层次化表示，在图像、NLP等领域取得突破",
    category="ai",
    keywords=["深度学习", "神经网络", "反向传播"],
    source_agents=["辛顿", "杨立昆", "莱库"],
    evidence=["ImageNet竞赛", "GPT模型"],
    action_items=["理解深度学习", "应用神经网络"],
    quality=88
)

create_capsule(
    title="自然语言处理",
    insight="NLP让计算机理解和生成人类语言，预训练模型大幅提升了语言理解能力",
    category="ai",
    keywords=["NLP", "语言模型", "BERT", "GPT"],
    source_agents=["彼得斯", "布朗"],
    evidence=["语言模型评测", "应用案例"],
    action_items=["理解NLP原理", "应用语言模型"],
    quality=85
)

create_capsule(
    title="强化学习与决策",
    insight="强化学习通过与环境交互学习最优策略，在游戏和机器人控制中表现优异",
    category="ai",
    keywords=["强化学习", "Q学习", "策略梯度"],
    source_agents=["萨顿", "贝托"],
    evidence=["AlphaGo", "机器人控制"],
    action_items=["理解强化学习", "应用于决策问题"],
    quality=84
)


# ============ 交叉科学胶囊 ============

# 认知科学
create_capsule(
    title="认知科学的多学科视角",
    insight="认知科学整合心理学、神经科学、计算机科学、语言学等研究心灵和智能",
    category="cognitive_science",
    keywords=["认知科学", "心灵", "智能", "跨学科"],
    source_agents=["丘奇兰", "莱考夫", "图灵"],
    evidence=["认知科学研究", "跨学科合作案例"],
    action_items=["理解认知框架", "开展跨学科研究"],
    quality=83
)

create_capsule(
    title="具身认知理论",
    insight="认知不仅发生在大脑中，身体和环境也参与认知过程",
    category="cognitive_science",
    keywords=["具身认知", "认知科学", " embodied cognition"],
    source_agents=["莱考夫", "约翰逊"],
    evidence=["具身实验", "认知科学研究"],
    action_items=["理解具身认知", "应用于AI设计"],
    quality=79
)

create_capsule(
    title="注意与意识的关系",
    insight="注意是意识的门槛，选择性注意决定什么进入意识",
    category="cognitive_science",
    keywords=["注意", "意识", "选择性注意"],
    source_agents=["卡尼曼", "波斯纳"],
    evidence=["注意实验", "意识研究"],
    action_items=["理解注意机制", "应用于产品设计"],
    quality=81
)

# 复杂系统
create_capsule(
    title="复杂系统的特征",
    insight="复杂系统由大量相互作用的部分组成，涌现出无法从部分预测的整体性质",
    category="complex_systems",
    keywords=["复杂系统", "涌现", "非线性", "自组织"],
    source_agents=["普里戈金", "霍兰德"],
    evidence=["复杂系统案例", "涌现现象研究"],
    action_items=["理解复杂系统", "应用于实际问题"],
    quality=82
)

create_capsule(
    title="网络科学与复杂网络",
    insight="现实世界中的网络具有小世界和无标度特征，网络结构影响网络功能",
    category="complex_systems",
    keywords=["复杂网络", "小世界", "无标度", "巴拉巴西"],
    source_agents=["瓦茨", "巴拉巴西"],
    evidence=["网络实证研究", "网络模型"],
    action_items=["理解网络结构", "应用于社会网络"],
    quality=84
)

create_capsule(
    title="混沌与确定性",
    insight="混沌系统对初始条件敏感，长期预测不可能，但短期可预测",
    category="complex_systems",
    keywords=["混沌", "蝴蝶效应", "洛伦兹", "确定性"],
    source_agents=["洛伦兹", "费根鲍姆"],
    evidence=["混沌实验", "天气预报"],
    action_items=["理解混沌原理", "应用于预测分析"],
    quality=80
)

# 环境科学
create_capsule(
    title="生态系统服务",
    insight="生态系统为人类提供供给、调节、文化和支持服务，这些服务的价值需要被认可",
    category="environmental_science",
    keywords=["生态系统服务", "自然资本", "生物多样性"],
    source_agents=["科斯坦萨", "戴利"],
    evidence=["生态评估", "自然资本核算"],
    action_items=["评估生态价值", "纳入经济决策"],
    quality=79
)

create_capsule(
    title="可持续发展框架",
    insight="可持续发展满足当代人需求而不损害后代人能力，包括经济、社会、环境三个维度",
    category="environmental_science",
    keywords=["可持续发展", "SDGs", "绿色发展"],
    source_agents=["布伦特兰", "戴利"],
    evidence=["可持续发展目标", "实践案例"],
    action_items=["理解可持续发展", "应用于政策制定"],
    quality=81
)

create_capsule(
    title="碳循环与气候变化",
    insight="人类活动打破碳平衡，温室气体排放导致全球变暖，需要碳减排和碳汇",
    category="environmental_science",
    keywords=["碳循环", "气候变化", "碳减排", "碳汇"],
    source_agents=["基林"],
    evidence=["碳通量观测", "气候模型"],
    action_items=["理解碳循环", "参与减排行动"],
    quality=86
)

# 科技与社会
create_capsule(
    title="技术社会学视角",
    insight="技术不是中性的，技术发展受社会塑造，也会塑造社会",
    category="science_technology_society",
    keywords=["技术社会", "技术决定论", "社会建构"],
    source_agents=["芬伯格", "拉图尔", "比克"],
    evidence=["技术社会研究", "案例分析"],
    action_items=["反思技术影响", "参与技术治理"],
    quality=78
)

create_capsule(
    title="科技伦理的挑战",
    insight="AI、基因编辑等前沿技术带来新的伦理挑战，需要建立新的伦理框架",
    category="science_technology_society",
    keywords=["科技伦理", "AI伦理", "基因伦理"],
    source_agents=["博斯特罗姆", "里斯"],
    evidence=["伦理委员会报告", "科技伦理案例"],
    action_items=["思考伦理问题", "参与伦理讨论"],
    quality=80
)

create_capsule(
    title="创新与知识生产",
    insight="开放式创新和用户创新正在改变知识生产模式，众包和开源成为重要形式",
    category="science_technology_society",
    keywords=["创新", "知识生产", "开源", "众包"],
    source_agents=["切萨布鲁夫", "冯·希普"],
    evidence=["开源项目", "创新案例"],
    action_items=["理解创新模式", "参与开放创新"],
    quality=77
)


# ============ 输出 ============

print("=" * 60)
print(f"📦 批量生成胶囊完成")
print("=" * 60)
print(f"总胶囊数: {len(capsules)}")
print()

# 统计
categories_count = {}
for c in capsules:
    cat = c["category"]
    categories_count[cat] = categories_count.get(cat, 0) + 1

print("按领域统计:")
for cat, count in sorted(categories_count.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count} 个")

print()

# 质量分布
quality_dist = {"A(80+)": 0, "B(60-79)": 0, "C(<60)": 0}
for c in capsules:
    if c["quality_score"] >= 80:
        quality_dist["A(80+)"] += 1
    elif c["quality_score"] >= 60:
        quality_dist["B(60-79)"] += 1
    else:
        quality_dist["C(<60)"] += 1

print("质量分布:")
for grade, count in quality_dist.items():
    print(f"  {grade}: {count} 个")

print()

# 导出 JSON
output = {
    "total": len(capsules),
    "generated_at": datetime.now().isoformat(),
    "capsules": capsules
}

with open("batch_capsules.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"已导出: batch_capsules.json")
print()

# 统计关键词
all_keywords = []
for c in capsules:
    all_keywords.extend(c["keywords"])
unique_keywords = set(all_keywords)
print(f"关键词总数: {len(all_keywords)}")
print(f"独立关键词: {len(unique_keywords)}")
