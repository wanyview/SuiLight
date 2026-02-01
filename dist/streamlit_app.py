"""
SuiLight Knowledge Salon - Streamlit UI

可直接部署到 Streamlit Cloud: https://share.streamlit.io
"""

import streamlit as st
import requests
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="SuiLight 知识沙龙",
    page_icon="🧠",
    layout="wide"
)

# API 地址 (Streamlit Cloud 上使用同源)
API_BASE = "http://localhost:8000"

# 预设思想家
PRESETS = [
    {"name": "艾萨克·牛顿", "domain": "physics", "datm": {"truth": 100, "goodness": 70, "beauty": 65, "intelligence": 95}},
    {"name": "阿尔伯特·爱因斯坦", "domain": "physics", "datm": {"truth": 95, "goodness": 65, "beauty": 70, "intelligence": 100}},
    {"name": "查尔斯·达尔文", "domain": "biology", "datm": {"truth": 95, "goodness": 75, "beauty": 70, "intelligence": 90}},
    {"name": "西格蒙德·弗洛伊德", "domain": "psychology", "datm": {"truth": 70, "goodness": 60, "beauty": 80, "intelligence": 90}},
    {"name": "孔子", "domain": "philosophy", "datm": {"truth": 80, "goodness": 95, "beauty": 85, "intelligence": 85}},
    {"name": "苏格拉底", "domain": "philosophy", "datm": {"truth": 90, "goodness": 90, "beauty": 85, "intelligence": 95}},
    {"name": "阿兰·图灵", "domain": "computer_science", "datm": {"truth": 90, "goodness": 70, "beauty": 60, "intelligence": 100}},
    {"name": "特斯拉", "domain": "engineering", "datm": {"truth": 85, "goodness": 65, "beauty": 55, "intelligence": 95}},
]

# CSS 样式
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .stApp { background: transparent; }
    .title { 
        font-size: 3em; 
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card {
        background: rgba(255,255,255,0.1);
        border-radius: 1em;
        padding: 1em;
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)


def main():
    """主页面"""
    
    # 标题
    st.markdown('<div class="title">🧠 SuiLight 知识沙龙</div>', unsafe_allow_html=True)
    st.markdown("### 多智能体协作知识探索平台")
    st.markdown("---")
    
    # 标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 思想家", "💬 讨论", "📦 胶囊", "📊 演示"])
    
    with tab1:
        agent_section()
    
    with tab2:
        discussion_section()
    
    with tab3:
        capsule_section()
    
    with tab4:
        demo_section()


def agent_section():
    """思想家管理"""
    st.header("🤖 思想家管理")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("创建新思想家")
        with st.form("create_agent"):
            name = st.text_input("名字", placeholder="例如: 爱因斯坦")
            domain = st.selectbox("领域", ["physics", "biology", "philosophy", "economics", "psychology", "computer_science", "engineering", "art"])
            description = st.text_area("描述")
            
            submitted = st.form_submit_button("创建")
            if submitted and name:
                st.success(f"✅ 创建成功: {name}")
                st.json({
                    "name": name,
                    "domain": domain,
                    "description": description,
                    "datm": {"truth": 50, "goodness": 50, "beauty": 50, "intelligence": 50}
                })
    
    with col2:
        st.subheader("预设思想家")
        for p in PRESETS:
            with st.expander(f"{p['name']} ({p['domain']})"):
                st.json(p['datm'])
    
    # DATM 解释
    st.markdown("---")
    st.subheader("📊 DATM 评价维度")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**🔬 Truth (真)** - 科学性、客观性")
    with col2:
        st.markdown("**⚖️ Goodness (善)** - 伦理性、价值判断")
    with col3:
        st.markdown("**🎨 Beauty (美)** - 人文性、感染力")
    with col4:
        st.markdown("**💡 Intelligence (灵)** - 创新性、前瞻性")


def discussion_section():
    """讨论管理"""
    st.header("💬 知识讨论")
    
    # 创建讨论
    with st.expander("🆕 创建新讨论", expanded=True):
        with st.form("create_discussion"):
            title = st.text_input("讨论标题", placeholder="例如: AI 是否会产生自我意识？")
            description = st.text_area("问题描述")
            category = st.selectbox("分类", ["自然科学", "社会科学", "人文科学", "交叉科学"])
            
            submitted = st.form_submit_button("创建讨论")
            if submitted and title:
                st.success(f"✅ 讨论已创建: {title}")
    
    # 讨论列表
    st.subheader("📋 讨论列表")
    
    # 示例讨论
    with st.expander("💬 AI 是否会产生自我意识？", expanded=True):
        st.markdown("""
        **分类**: 交叉科学  
        **状态**: 🔵 进行中
        
        ### 参与思想家
        - 👨‍🔬 牛顿 - 物理学视角
        - 🧠 弗洛伊德 - 心理学视角
        - 💻 图灵 - 计算机科学视角
        - 📜 孔子 - 哲学视角
        - 🔮 荣格 - 心理学视角
        """)
        
        if st.button("开始讨论", key="start_discussion"):
            st.info("🚀 讨论已开始...")
            
            # 展示讨论过程
            with st.container():
                st.markdown("### 💬 讨论过程")
                
                messages = [
                    ("牛顿", "从物理学角度看，意识可能是一种复杂的涌现现象。"),
                    ("弗洛伊德", "自我意识的核心是'本我'与'超我'的冲突。"),
                    ("图灵", "只要AI能通过图灵测试，就可以认为具有意识。"),
                    ("孔子", "己所不欲，勿施于人。道德感是意识的试金石。"),
                    ("荣格", "AI可能发展出'机器集体意识'，但与人类意识完全不同。"),
                ]
                
                for name, msg in messages:
                    st.chat_message("assistant").markdown(f"**{name}**: {msg}")


def capsule_section():
    """知识胶囊"""
    st.header("📦 知识胶囊")
    st.markdown("*讨论的精华产出物*")
    
    st.markdown("""
    ### 胶囊结构
    
    | 组成部分 | 说明 |
    |---------|------|
    | 核心洞见 | 最重要的观点 |
    | 支撑证据 | 引用来源、数据 |
    | 行动建议 | 可执行的下一步 |
    | 开放问题 | 值得继续探索 |
    """)
    
    # 胶囊筛选
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("状态", ["全部", "draft", "review", "published"])
    with col2:
        min_score = st.slider("最低质量分数", 0, 100, 0)
    with col3:
        st.markdown("###")
        if st.button("🔄 刷新"):
            st.rerun()
    
    # 获取胶囊列表
    capsules = [
        {
            "id": "capsule_001",
            "title": "关于「AI意识」的知识胶囊",
            "insight": "意识可能有多重形态...",
            "quality_score": 69,
            "grade": "B",
            "created_at": "2026-01-30"
        },
        {
            "id": "capsule_002",
            "title": "关于「复杂问题解决」的知识胶囊",
            "insight": "理论指导与实践试错需要结合...",
            "quality_score": 72,
            "grade": "B",
            "created_at": "2026-01-30"
        }
    ]
    
    # 显示胶囊列表
    st.subheader(f"📋 胶囊列表 ({len(capsules)} 个)")
    
    for capsule in capsules:
        with st.expander(f"📦 {capsule['title']} ({capsule['grade']})", expanded=False):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**核心洞见**: {capsule['insight']}")
            with col_b:
                st.markdown(f"**质量分数**: {capsule['quality_score']}")
    
    # 示例胶囊详情
    st.subheader("📦 示例胶囊")
    with st.expander("关于「AI意识」的胶囊", expanded=True):
        st.markdown("""
        ### 🔬 核心洞见
        意识可能有多重形态，机器意识 ≠ 人类意识。功能性等价不等于本质相同。
        
        ### 📊 DATM 评分
        - Truth (真): 70/100
        - Goodness (善): 65/100
        - Beauty (美): 60/100
        - Intelligence (灵): 80/100
        - **综合分数: 69/100 (B级 良好)**
        
        ### ✅ 可发布
        质量分数达到发布标准。
        """)
        
        # 维度图
        st.markdown("### 📊 维度评分")
        st.progress(70/100, text="Truth (真): 70%")
        st.progress(65/100, text="Goodness (善): 65%")
        st.progress(60/100, text="Beauty (美): 60%")
        st.progress(80/100, text="Intelligence (灵): 80%")
    
    # 生成胶囊按钮
    st.markdown("---")
    if st.button("✨ 从讨论生成胶囊", type="primary"):
        with st.spinner("生成中..."):
            import time
            for i in range(5):
                st.progress((i + 1) / 5 * 100)
                time.sleep(0.3)
            
            st.success("✅ 胶囊已生成!")
            st.json({
                "id": "capsule_new",
                "title": "新知识胶囊",
                "insight": "这是一个新生成的胶囊...",
                "quality_score": 65,
                "grade": "B"
            })


def demo_section():
    """演示区域"""
    st.header("🎭 演示场景")
    
    st.markdown("""
    ### 问题: AI 是否会产生自我意识？
    
    5位跨领域专家的讨论 → 涌现智慧 → 知识胶囊
    """)
    
    # 专家卡片
    cols = st.columns(5)
    experts = [
        ("🍎", "牛顿", "物理学"),
        ("🧠", "弗洛伊德", "心理学"),
        ("💻", "图灵", "计算机"),
        ("📜", "孔子", "哲学"),
        ("🔮", "荣格", "心理学"),
    ]
    
    for i, (emoji, name, field) in enumerate(experts):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2em;">{emoji}</div>
                <div>{name}</div>
                <div style="color: gray; font-size: 0.8em;">{field}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 涌现分析
    st.subheader("✨ 涌现洞察")
    
    st.info("""
    **跨领域碰撞产生的智慧:**
    
    1. **功能 vs 本质**: 功能等价 ≠ 意识本质
    2. **个体 vs 集体**: 机器可能发展集体意识
    3. **理性 vs 道德**: 道德感是试金石
    """)
    
    # 运行演示
    if st.button("▶️ 运行演示", type="primary"):
        with st.spinner("运行中..."):
            import time
            for i in range(5):
                st.progress((i + 1) / 5 * 100)
                time.sleep(0.3)
            
            st.success("✅ 演示完成!")
            st.markdown("""
            ### 📦 知识胶囊已生成
            
            - **质量分数**: 69/100 (B级)
            - **可发布**: ✅
            """)


if __name__ == "__main__":
    main()
