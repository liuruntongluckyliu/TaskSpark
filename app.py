"""
TaskSpark - 智能任务启动助手
简约温馨Ins风设计 · 专为ADHD/执行力困难者优化
"""

import streamlit as st

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="TaskSpark | 智能任务启动",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
        # TaskSpark
        **智能任务启动助手**
        
        专为ADHD/执行力困难人群设计的任务拆解与启动工具。
        通过AI智能分析，将大任务拆解为可执行的微步骤。
        
        ✨ 特色功能：
        - AI智能任务分析
        - 微步骤拆解
        - 个性化鼓励
        - 进度可视化
        """
    }
)

# ==================== 全局CSS样式 ====================
st.markdown("""
<style>
    /* 全局基础样式 */
    .main {
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Ins风字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 主色调：柔和暖色系（适合ADHD的舒缓色调） */
    :root {
        --primary: #FF9A8B;  /* 柔和的珊瑚粉 */
        --primary-light: #FFD6D0;
        --secondary: #93C5FD; /* 柔和的天空蓝 */
        --accent: #A78BFA;    /* 柔和的薰衣草紫 */
        --background: #FAFAFA; /* 极浅灰背景 */
        --surface: #FFFFFF;   /* 纯白卡片 */
        --text-primary: #374151; /* 深灰文字 */
        --text-secondary: #6B7280; /* 中灰文字 */
        --border: #E5E7EB;    /* 浅灰边框 */
        --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
        --radius-lg: 20px;
        --radius-md: 14px;
        --radius-sm: 10px;
    }
    
    /* 暗色模式支持 */
    @media (prefers-color-scheme: dark) {
        :root {
            --background: #0F172A;
            --surface: #1E293B;
            --text-primary: #F1F5F9;
            --text-secondary: #94A3B8;
            --border: #334155;
        }
    }
    
    /* 主容器 */
    .stApp {
        background: linear-gradient(135deg, var(--background) 0%, #FEF3C7 100%);
        min-height: 100vh;
    }
    
    /* 标题样式 */
    h1 {
        font-weight: 700;
        font-size: 2.8rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    h2 {
        font-weight: 600;
        color: var(--text-primary);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 500;
        color: var(--text-primary);
    }
    
    /* 卡片设计 */
    .ins-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .ins-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.08);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 0.8rem 2rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 154, 139, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 154, 139, 0.4);
    }
    
    /* 次要按钮 */
    .stButton > button:has(+ .secondary) {
        background: var(--surface);
        color: var(--primary);
        border: 2px solid var(--primary-light);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div {
        border-radius: var(--radius-md);
        border: 2px solid var(--border);
        background: var(--surface);
        color: var(--text-primary);
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(255, 154, 139, 0.1);
    }
    
    /* 进度条美化 */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: var(--radius-sm);
    }
    
    /* 侧边栏 */
    .css-1d391kg {
        background: linear-gradient(135deg, var(--surface) 0%, #FEF3C7 100%);
        border-right: 1px solid var(--border);
    }
    
    /* 分隔线 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }
    
    /* 徽章/标签 */
    .ins-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: linear-gradient(135deg, var(--secondary) 0%, var(--accent) 100%);
        color: white;
        border-radius: var(--radius-sm);
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    /* 心情图标 */
    .mood-option {
        text-align: center;
        padding: 1rem;
        border-radius: var(--radius-md);
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.3s ease;
        background: var(--surface);
    }
    
    .mood-option:hover {
        border-color: var(--primary-light);
        transform: scale(1.05);
    }
    
    .mood-option.selected {
        border-color: var(--primary);
        background: linear-gradient(135deg, rgba(255, 154, 139, 0.1) 0%, rgba(147, 197, 253, 0.1) 100%);
    }
    
    /* 加载动画 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2.2rem;
        }
        
        .ins-card {
            padding: 1.2rem;
        }
    }
    
    /* ADHD友好设计：减少视觉噪音 */
    * {
        transition: all 0.2s ease;
    }
    
    /* 聚焦指示（对ADHD用户很重要） */
    :focus {
        outline: 3px solid rgba(255, 154, 139, 0.5);
        outline-offset: 2px;
    }
    
    /* 平滑滚动 */
    html {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 主页内容 ====================
def main():
    # 主容器
    with st.container():
        # 顶部品牌区
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
            st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h1 style='margin-bottom: 0.5rem;'>✨ TaskSpark</h1>
                <p style='color: var(--text-secondary); font-size: 1.2rem; margin-top: 0;'>
                    智能任务启动助手
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 分隔线
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 功能介绍卡片
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.markdown("### 💡 如何使用TaskSpark")
        
        cols = st.columns(3)
        features = [
            {"icon": "📝", "title": "描述状态", "desc": "描述你现在的状态和感受"},
            {"icon": "🎯", "title": "设定目标", "desc": "告诉AI你想开始什么任务"},
            {"icon": "✨", "title": "获得方案", "desc": "AI会拆解任务并提供启动方案"}
        ]
        
        for i, feature in enumerate(features):
            with cols[i]:
                with st.container():
                    st.markdown(f"""
                    <div class='ins-card' style='text-align: center;'>
                        <div style='font-size: 2.5rem; margin-bottom: 1rem;'>{feature['icon']}</div>
                        <h3 style='margin-bottom: 0.5rem;'>{feature['title']}</h3>
                        <p style='color: var(--text-secondary);'>{feature['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # CTA区域
        st.markdown("<div class='fade-in' style='margin-top: 3rem;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style='text-align: center;'>
                <h2>准备好了吗？</h2>
                <p style='color: var(--text-secondary); margin-bottom: 2rem;'>
                    让我们开始你的第一个任务启动之旅
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 开始按钮
            if st.button("🚀 开始使用 TaskSpark", key="start_main", type="primary"):
                st.switch_page("pages/task_spark_home.py")
            
            # 或使用快捷方式
            st.markdown("<div style='text-align: center; margin-top: 1.5rem;'>", unsafe_allow_html=True)
            st.markdown("**或者试试快捷启动：**")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("📚 从刷手机到学习", use_container_width=True):
                    st.session_state.quick_start = "study"
                    st.switch_page("pages/task_spark_home.py")
            with col_b:
                if st.button("🧹 从躺床到整理", use_container_width=True):
                    st.session_state.quick_start = "clean"
                    st.switch_page("pages/task_spark_home.py")
            with col_c:
                if st.button("💼 从拖延到工作", use_container_width=True):
                    st.session_state.quick_start = "work"
                    st.switch_page("pages/task_spark_home.py")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 底部信息
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: var(--text-secondary); padding: 2rem 0;'>
            <p style='margin-bottom: 0.5rem;'>
                ✨ 专为ADHD/执行力困难人群设计 · 基于认知行为疗法与AI智能分析
            </p>
            <p style='font-size: 0.9rem; opacity: 0.7;'>
                安全 · 隐私 · 无评判 · 个性化支持
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== 运行主函数 ====================
if __name__ == "__main__":
    # 初始化session state
    if 'quick_start' not in st.session_state:
        st.session_state.quick_start = None
    
    # 运行主界面
    main()