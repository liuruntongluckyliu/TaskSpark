"""
TaskSpark 首页 - 用户任务输入界面
简约温馨Ins风设计 · 专为ADHD用户优化
"""

import streamlit as st
import sys
import os
import time

# 添加utils到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="任务输入 | TaskSpark",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 复用app.py中的CSS样式
st.markdown("""
<style>
    /* 复用app.py中的所有CSS样式 */
    .main { padding: 1rem 2rem; max-width: 1200px; margin: 0 auto; }
    :root {
        --primary: #FF9A8B; --primary-light: #FFD6D0;
        --secondary: #93C5FD; --accent: #A78BFA;
        --background: #FAFAFA; --surface: #FFFFFF;
        --text-primary: #374151; --text-secondary: #6B7280;
        --border: #E5E7EB; --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
        --radius-lg: 20px; --radius-md: 14px; --radius-sm: 10px;
    }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .stApp { background: linear-gradient(135deg, var(--background) 0%, #FEF3C7 100%); min-height: 100vh; }
    h1 { font-weight: 700; font-size: 2.8rem; background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; letter-spacing: -0.02em; }
    .ins-card { background: var(--surface); border-radius: var(--radius-lg); padding: 1.8rem; margin: 1rem 0; box-shadow: var(--shadow); border: 1px solid var(--border); transition: all 0.3s ease; }
    .stButton > button { background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%); color: white; border: none; border-radius: var(--radius-md); padding: 0.8rem 2rem; font-weight: 500; font-size: 1rem; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(255, 154, 139, 0.3); width: 100%; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(255, 154, 139, 0.4); }
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stSlider > div { border-radius: var(--radius-md); border: 2px solid var(--border); background: var(--surface); color: var(--text-primary); padding: 0.8rem; font-size: 1rem; }
    .stTextInput > div > div > input:focus, .stSelectbox > div > div > select:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(255, 154, 139, 0.1); }
    .mood-option { text-align: center; padding: 1rem; border-radius: var(--radius-md); border: 2px solid transparent; cursor: pointer; transition: all 0.3s ease; background: var(--surface); margin: 0.2rem; }
    .mood-option:hover { border-color: var(--primary-light); transform: scale(1.02); }
    .mood-option.selected { border-color: var(--primary); background: linear-gradient(135deg, rgba(255, 154, 139, 0.1) 0%, rgba(147, 197, 253, 0.1) 100%); }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    .pulse { animation: pulse 2s infinite; }
    .fade-in { animation: fadeIn 0.6s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化session state ====================
def init_session_state():
    """初始化session state"""
    if 'user_state' not in st.session_state:
        st.session_state.user_state = {
            'current_activity': '',
            'target_task': '',
            'mood': '',
            'difficulty': 5,
            'history': []
        }
    
    if 'task_analysis' not in st.session_state:
        st.session_state.task_analysis = None
    
    # 处理快捷启动
    if 'quick_start' in st.session_state and st.session_state.quick_start:
        handle_quick_start(st.session_state.quick_start)
        st.session_state.quick_start = None

def handle_quick_start(quick_type):
    """处理快捷启动"""
    quick_presets = {
        'study': {
            'current_activity': '刷手机/看视频',
            'target_task': '学习/复习考试',
            'mood': 'procrastinating',  # 改为英文ID
            'difficulty': 7
        },
        'clean': {
            'current_activity': '躺在床上',
            'target_task': '整理房间/打扫卫生',
            'mood': 'tired',  # 改为英文ID
            'difficulty': 6
        },
        'work': {
            'current_activity': '坐在桌前发呆',
            'target_task': '写报告/完成工作',
            'mood': 'anxious',  # 改为英文ID
            'difficulty': 8
        }
    }
    
    if quick_type in quick_presets:
        preset = quick_presets[quick_type]
        st.session_state.user_state.update(preset)

# ==================== 情绪选择器 ====================
def mood_selector(selected_mood):
    """创建情绪选择器"""
    moods = [
        {"id": "energetic", "emoji": "⚡", "name": "精力充沛", "color": "#10B981"},
        {"id": "neutral", "emoji": "😐", "name": "平稳中性", "color": "#6B7280"},
        {"id": "tired", "emoji": "😴", "name": "有些疲惫", "color": "#F59E0B"},
        {"id": "anxious", "emoji": "😰", "name": "焦虑不安", "color": "#EF4444"},
        {"id": "procrastinating", "emoji": "🌀", "name": "拖延回避", "color": "#8B5CF6"},
        {"id": "overwhelmed", "emoji": "😫", "name": "压力很大", "color": "#DC2626"}
    ]
    
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.markdown("#### 🎭 选择当前情绪")
    st.markdown("<p style='color: var(--text-secondary); margin-bottom: 1rem;'>选择最符合你现在感受的情绪</p>", unsafe_allow_html=True)
    
    # 创建3列布局
    cols = st.columns(3)
    
    for idx, mood in enumerate(moods):
        col_idx = idx % 3
        is_selected = selected_mood == mood["id"]
        
        with cols[col_idx]:
            button_html = f"""
            <div class='mood-option {'selected' if is_selected else ''}' 
                 onclick="this.parentNode.querySelector('button').click()"
                 style='border-color: {mood['color'] if is_selected else 'transparent'};'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{mood['emoji']}</div>
                <div style='font-weight: {'600' if is_selected else '400'}; color: var(--text-primary);'>
                    {mood['name']}
                </div>
            </div>
            """
            
            # 创建隐藏的按钮
            if st.button(mood["name"], key=f"mood_{mood['id']}", 
                        use_container_width=True, 
                        type="primary" if is_selected else "secondary",
                        help=f"选择 {mood['name']}"):
                st.session_state.user_state['mood'] = mood['id']
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    return selected_mood

# ==================== 难度选择器 ====================
def difficulty_selector():
    """创建难度选择器"""
    current_difficulty = st.session_state.user_state.get('difficulty', 5)
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.markdown("#### 🎯 评估任务难度")
    st.markdown("<p style='color: var(--text-secondary); margin-bottom: 1rem;'>你觉得开始这个任务有多困难？</p>", unsafe_allow_html=True)
    
    # 难度描述
    difficulty_descriptions = {
        1: {"label": "很简单", "desc": "有信心轻松开始"},
        3: {"label": "有点挑战", "desc": "需要一点努力"},
        5: {"label": "中等难度", "desc": "需要一些决心"},
        7: {"label": "相当困难", "desc": "需要很大动力"},
        10: {"label": "极其困难", "desc": "感觉几乎不可能开始"}
    }

    # 创建滑块
    difficulty = st.slider(
        "难度评分 (1-10)",
        min_value=1,
        max_value=10,
        value=current_difficulty,
        step=1,
        label_visibility="collapsed",
    )

    # 更新 user_state
    if difficulty != current_difficulty:
        st.session_state.user_state['difficulty'] = difficulty

    # 显示难度描述
    closest = min(difficulty_descriptions.keys(), key=lambda x: abs(x - difficulty))
    desc = difficulty_descriptions[closest]
    
    st.markdown(f"""
    <div style='text-align: center; margin-top: 1rem;'>
        <div style='font-size: 2rem; font-weight: 700; color: var(--primary);'>{difficulty}/10</div>
        <div style='font-weight: 600; color: var(--text-primary); margin-top: 0.5rem;'>{desc['label']}</div>
        <div style='color: var(--text-secondary); font-size: 0.9rem;'>{desc['desc']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return difficulty

# ==================== AI分析函数 ====================
def analyze_with_ai(current_state, target_task, mood, difficulty):
    """调用智能AI分析任务"""
    try:
        # 导入AI引擎
        from utils.ai_engine import get_analyzer
        
        # 获取分析器实例
        analyzer = get_analyzer()
        
        # 显示分析状态
        with st.spinner("🤖 AI正在分析你的任务..."):
            # 添加一点延迟让用户看到加载状态
            time.sleep(1)
            
            # 调用AI分析
            analysis = analyzer.analyze_task(
                current_state=current_state,
                target_task=target_task,
                mood=mood,
                difficulty=difficulty
            )
            
            # 显示分析来源
            if analysis.get('_meta', {}).get('ai_model') == 'smart-simulator':
                st.success("✅ 智能AI分析完成！")
            else:
                st.info("🤖 AI分析完成！")
            
            return analysis
            
    except ImportError as e:
        st.error(f"无法加载AI模块: {str(e)}")
        st.info("请确保已正确创建AI模块文件")
        return None
    except Exception as e:
        st.error(f"AI分析失败: {str(e)}")
        st.info("请稍后重试")
        return None

# ==================== 保存历史记录 ====================
def save_to_history(user_state, analysis_result):
    """保存任务到历史记录"""
    if 'history' not in st.session_state.user_state:
        st.session_state.user_state['history'] = []
    
    history_entry = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M"),
        'from': user_state['current_activity'],
        'to': user_state['target_task'],
        'mood': user_state['mood'],
        'difficulty': user_state['difficulty'],
        'analysis': analysis_result
    }
    
    st.session_state.user_state['history'].insert(0, history_entry)
    
    # 只保留最近10条记录
    if len(st.session_state.user_state['history']) > 10:
        st.session_state.user_state['history'] = st.session_state.user_state['history'][:10]

# ==================== 主页面 ====================
def main():
    # 初始化session state
    init_session_state()
    
    # 处理快捷启动
    if 'quick_start' in st.session_state and st.session_state.quick_start:
        handle_quick_start(st.session_state.quick_start)
        st.session_state.quick_start = None
    
    # 标题区域
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(""" 
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin-bottom: 0.5rem;'>📝 任务启动分析</h1>
            <p style='color: var(--text-secondary); font-size: 1.2rem; margin-top: 0;'>
                让我们了解你现在的状态，AI会帮你制定启动策略
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 分隔线
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 创建两列布局
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        # 当前状态输入 - 直接使用user_state中的值
        st.markdown("#### 📱 你现在在做什么？")
        current_activity = st.text_input(
            "描述你当前的活动状态",
            value=st.session_state.user_state.get('current_activity', ''),
            placeholder="例如：躺在床上刷手机、坐在桌前发呆、刚睡醒...",
            # 不要添加key，让value参数控制显示
            help="如实描述你现在在做什么，这有助于AI理解你的启动困难"
        )

        # 在输入后立即更新 user_state
        if current_activity != st.session_state.user_state.get('current_activity', ''):
            st.session_state.user_state['current_activity'] = current_activity

        # 同理处理目标任务
        st.markdown("#### 🎯 你想要做什么？")
        target_task = st.text_input(
            "描述你想要开始的任务",
            value=st.session_state.user_state.get('target_task', ''),
            placeholder="例如：整理房间、复习期末考试、写工作报告...",
            # 不要添加key，让value参数控制显示
            help="明确描述你想要开始的任务，越具体越好"
        )

        if target_task != st.session_state.user_state.get('target_task', ''):
            st.session_state.user_state['target_task'] = target_task
        
        # 分隔线
        st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
        
        # 情绪选择
        selected_mood = st.session_state.user_state.get('mood', '')
        mood_selector(selected_mood)
        
        # 难度选择
        difficulty = difficulty_selector()

        # 确保 user_state 中有最新的难度值
        if 'difficulty' not in st.session_state.user_state:
            st.session_state.user_state['difficulty'] = difficulty

        # 更新session state
        st.session_state.user_state.update({
            'current_activity': current_activity,
            'target_task': target_task,
        })
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 分析按钮
        st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
        
        # 检查必要输入
        can_analyze = current_activity and target_task and selected_mood
        
        if st.button("🚀 开始AI智能分析", 
                    type="primary", 
                    use_container_width=True,
                    disabled=not can_analyze,
                    help="请填写所有必要信息"):
            
            if can_analyze:
                # 调用AI分析
                analysis_result = analyze_with_ai(
                    current_state=current_activity,
                    target_task=target_task,
                    mood=selected_mood,
                    difficulty=difficulty
                )
                
                if analysis_result:
                    # 保存分析结果
                    st.session_state.task_analysis = analysis_result
                    
                    # 保存到历史记录
                    save_to_history(st.session_state.user_state, analysis_result)
                    
                    # 成功消息
                    st.success("✅ AI分析完成！正在跳转到分析页面...")
                    time.sleep(1)
                    
                    # 跳转到分析页面
                    st.switch_page("pages/task_analysis.py")
                else:
                    st.error("AI分析失败，请稍后重试或检查配置")
            else:
                st.warning("请填写所有必要信息")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with right_col:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        # 历史记录卡片
        st.markdown("#### 📚 历史记录")
        
        history = st.session_state.user_state.get('history', [])
        
        if history:
            for i, record in enumerate(history[:5]):  # 只显示最近5条
                with st.expander(f"{record['from']} → {record['to']}", expanded=(i==0)):
                    st.caption(f"时间: {record['timestamp']}")
                    
                    # 情绪显示
                    mood_map = {
                        "energetic": "⚡ 精力充沛",
                        "neutral": "😐 平稳中性",
                        "tired": "😴 有些疲惫",
                        "anxious": "😰 焦虑不安",
                        "procrastinating": "🌀 拖延回避",
                        "overwhelmed": "😫 压力很大"
                    }
                    mood_text = mood_map.get(record.get('mood', ''), record.get('mood', '未知'))
                    st.write(f"**情绪:** {mood_text}")
                    
                    st.write(f"**难度:** {record.get('difficulty', '?')}/10")
                    
                    # 快速重试按钮
                    if st.button("🔄 快速重试", key=f"retry_{i}", use_container_width=True):
                        # 获取记录中的难度
                        record_difficulty = record.get('difficulty', 5)
                        # 处理情绪ID映射（从显示文本映射回ID）
                        mood_id = record.get('mood', '')
                        
                        # 如果mood是中文（来自预设），需要映射回ID
                        chinese_to_english = {
                            "拖延回避": "procrastinating",
                            "有些疲惫": "tired", 
                            "焦虑不安": "anxious",
                            "精力充沛": "energetic",
                            "平稳中性": "neutral", 
                            "压力很大": "overwhelmed"
                        }
                        
                        if mood_id in chinese_to_english:
                            mood_id = chinese_to_english[mood_id]
                        
                        # 更新所有状态
                        st.session_state.user_state.update({
                            'current_activity': record['from'],
                            'target_task': record['to'],
                            'mood': mood_id,  # 使用处理后的情绪值
                            'difficulty': record_difficulty
                        })
                        
                        # 不要直接修改小部件的session_state
                        # st.session_state['current_activity_input'] = record['from']  # 删除这行
                        # st.session_state['target_task_input'] = record['to']  # 删除这行
                        
                        # 直接重新运行，让输入框从更新后的user_state中获取值
                        st.rerun()
        else:
            st.info("暂无历史记录")
            st.caption("完成的任务会显示在这里")
        
        st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # 使用提示卡片
        st.markdown("#### 💡 使用提示")
        
        tips = [
            "✨ **诚实描述**：越真实的状态，分析越准确",
            "🎯 **具体任务**：把模糊任务变成具体动作",
            "😌 **接纳情绪**：所有情绪都是正常的",
            "⚡ **微小开始**：从最小的步骤开始建立动量",
            "🔄 **允许调整**：随时可以修改或重新开始"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
        
        st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # 常见场景快捷入口
        st.markdown("#### 🚀 快速开始")
        
        quick_scenarios = [
            {"label": "📱 → 📚", "desc": "从娱乐到学习", "key": "quick_study"},
            {"label": "🛏️ → 🧹", "desc": "从躺床到整理", "key": "quick_clean"},
            {"label": "🌀 → 💼", "desc": "从拖延到工作", "key": "quick_work"}
        ]
        
        for scenario in quick_scenarios:
            if st.button(f"{scenario['label']} {scenario['desc']}", 
                        key=scenario['key'],
                        use_container_width=True,
                        type="secondary"):
                # 设置对应的快捷启动
                quick_map = {
                    "quick_study": "study",
                    "quick_clean": "clean",
                    "quick_work": "work"
                }
                st.session_state.quick_start = quick_map.get(scenario['key'])
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 底部导航
    st.markdown("<hr style='margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← 返回主页", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button("🔄 重置表单", use_container_width=True, type="secondary"):
            st.session_state.user_state = {
                'current_activity': '',
                'target_task': '',
                'mood': '',
                'difficulty': 5,
                'history': st.session_state.user_state.get('history', [])
            }
            # 不要直接修改小部件的session_state
            # st.session_state['current_activity_input'] = ''  # 删除这行
            # st.session_state['target_task_input'] = ''  # 删除这行
            st.rerun()
    with col3:
        st.markdown("""
        <div style='text-align: center; color: var(--text-secondary);'>
            <p style='margin: 0; font-size: 0.9rem;'>步骤 1/3</p>
            <p style='margin: 0; font-weight: 500;'>任务输入 → 分析 → 执行</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== 运行主函数 ====================
if __name__ == "__main__":
    main()