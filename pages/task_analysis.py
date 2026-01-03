"""
task_analysis.py - AI分析结果页面
显示智能AI的任务分析结果
"""

import streamlit as st
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(
    page_title="任务分析 | TaskSpark",
    page_icon="🔍",
    layout="wide"
)

# 复用app.py中的CSS样式
st.markdown("""
<style>
    /* 复用app.py中的所有CSS样式 */
    :root {
        --primary: #FF9A8B; --primary-light: #FFD6D0;
        --secondary: #93C5FD; --accent: #A78BFA;
        --background: #FAFAFA; --surface: #FFFFFF;
        --text-primary: #374151; --text-secondary: #6B7280;
        --border: #E5E7EB; --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        --radius-lg: 20px; --radius-md: 14px; --radius-sm: 10px;
    }
    .stApp { background: linear-gradient(135deg, var(--background) 0%, #FEF3C7 100%); min-height: 100vh; }
    h1 { font-weight: 700; font-size: 2.8rem; background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
    .ins-card { background: var(--surface); border-radius: var(--radius-lg); padding: 1.8rem; margin: 1rem 0; box-shadow: var(--shadow); border: 1px solid var(--border); }
    .step-card { background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary) 100%); color: white; border-radius: var(--radius-md); padding: 1rem; margin: 0.5rem 0; }
    .fade-in { animation: fadeIn 0.6s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔍 AI任务分析结果")
    st.markdown("基于你的状态和目标，这是为你定制的智能启动方案")
    
    # 检查是否有分析结果
    if 'task_analysis' not in st.session_state:
        st.warning("请先回到首页进行任务分析")
        if st.button("返回首页"):
            st.switch_page("../task_spark_home.py")
        return
    
    analysis = st.session_state.task_analysis
    
    # 显示AI模型信息
    ai_model = analysis.get('_meta', {}).get('ai_model', '智能AI')
    offline_mode = analysis.get('_meta', {}).get('offline_mode', True)
    
    st.caption(f"🤖 {ai_model} · {'完全离线运行' if offline_mode else '在线模式'}")
    
    # 任务概览卡片
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("任务类型", analysis.get('task_analysis', {}).get('task_type', '未知'))
    
    with col2:
        st.metric("难度级别", analysis.get('task_analysis', {}).get('difficulty_level', '未知'))
    
    with col3:
        time_estimate = analysis.get('task_analysis', {}).get('estimated_time', '未知')
        st.metric("预计时间", time_estimate)
    
    with col4:
        step_count = len(analysis.get('micro_steps', []))
        st.metric("步骤数量", f"{step_count}个")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 分隔线
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 策略和洞察
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.subheader("🎯 推荐策略")
        
        strategy = analysis.get('strategy', {})
        st.markdown(f"""
        <div class='ins-card'>
            <h3 style='color: var(--primary); margin-top: 0;'>{strategy.get('name', '微步骤启动法')}</h3>
            <p>{strategy.get('description', '')}</p>
            <div style='background: rgba(255, 154, 139, 0.1); padding: 1rem; border-radius: var(--radius-md); margin-top: 1rem;'>
                <strong>✨ 关键原则:</strong> {strategy.get('key_principle', '完成比完美重要')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("💡 核心洞察")
        key_insight = analysis.get('task_analysis', {}).get('key_insight', '')
        st.info(f"✨ {key_insight}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.subheader("🧠 心理障碍分析")
        
        mental_blocks = analysis.get('task_analysis', {}).get('mental_blocks', [])
        if mental_blocks:
            for block in mental_blocks:
                st.markdown(f"- 🔍 {block}")
        else:
            st.write("未识别到明显的心理障碍")
        
        st.subheader("💬 AI鼓励")
        encouragement = analysis.get('encouragement', '你可以做到的！')
        st.success(f"💖 {encouragement}")
        
        st.subheader("🏆 完成奖励")
        reward_ideas = analysis.get('adhd_specific', {}).get('reward_ideas', [])
        if reward_ideas:
            for reward in reward_ideas[:3]:
                st.markdown(f"- 🎁 {reward}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 分隔线
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 微步骤执行计划
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.subheader("📝 分步执行计划")
    st.markdown("<p style='color: var(--text-secondary);'>按照以下步骤开始，每个步骤都很小，容易完成</p>", unsafe_allow_html=True)
    
    micro_steps = analysis.get('micro_steps', [])
    if micro_steps:
        for i, step_info in enumerate(micro_steps, 1):
            with st.container():
                col_a, col_b, col_c = st.columns([1, 6, 2])
                with col_a:
                    st.markdown(f"### {i}")
                with col_b:
                    st.markdown(f"**{step_info.get('step', '步骤')}**")
                    if step_info.get('tip'):
                        st.markdown(f"<small style='color: var(--text-secondary);'>💡 {step_info.get('tip')}</small>", unsafe_allow_html=True)
                with col_c:
                    st.markdown(f"⏱️ {step_info.get('time', '')}")
                    energy = step_info.get('energy', '')
                    if energy:
                        energy_emoji = "⚡" if energy == "高" else "🔋" if energy == "中" else "🔋"
                        st.markdown(f"<small>{energy_emoji} {energy}能量</small>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("未生成微步骤，请返回重新分析")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 个性化建议
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.subheader("💡 个性化建议")
    
    suggestions = analysis.get('personalized_suggestions', [])
    if suggestions:
        cols = st.columns(2)
        for i, suggestion in enumerate(suggestions):
            col_idx = i % 2
            with cols[col_idx]:
                st.markdown(f"- ✅ {suggestion}")
    else:
        st.write("暂无个性化建议")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ADHD特定建议
    adhd_tips = analysis.get('adhd_specific', {})
    if adhd_tips:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.subheader("🌟 ADHD友好建议")
        
        col1, col2 = st.columns(2)
        
        with col1:
            focus_tips = adhd_tips.get('focus_tips', [])
            if focus_tips:
                st.markdown("**专注技巧:**")
                for tip in focus_tips[:3]:
                    st.markdown(f"- 🎯 {tip}")
        
        with col2:
            env_tips = adhd_tips.get('environment_tips', [])
            if env_tips:
                st.markdown("**环境调整:**")
                for tip in env_tips[:3]:
                    st.markdown(f"🏠 {tip}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 分隔线
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 行动按钮
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.subheader("🚀 开始执行")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ 开始执行第一步", type="primary", use_container_width=True):
            st.session_state.current_step = 0
            st.success("🎯 准备开始执行！")
            time.sleep(1)
            try:
             st.switch_page("micro_steps.py")
            except:
            # 尝试其他路径
             st.switch_page("./pages/micro_steps.py")
    
    with col2:
        if st.button("🔄 重新分析", type="secondary", use_container_width=True):
            st.switch_page("pages/task_spark_home.py")
    
    with col3:
        if st.button("🏠 返回首页", type="secondary", use_container_width=True):
            st.switch_page("app.py")
    
    # 底部信息
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: var(--text-secondary); padding: 1rem 0;'>
        <p style='margin-bottom: 0.5rem;'>
            🤖 智能AI分析 · 完全离线运行 · 保护隐私
        </p>
        <p style='font-size: 0.9rem; opacity: 0.7;'>
            基于心理学原理和任务管理最佳实践
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()