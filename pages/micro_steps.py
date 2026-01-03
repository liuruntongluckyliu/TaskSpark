"""
micro_steps.py - 微步骤执行页面
指导用户逐步完成任务
"""

import streamlit as st
import time

st.set_page_config(
    page_title="任务执行 | TaskSpark",
    page_icon="🚀",
    layout="wide"
)

# 复用app.py中的CSS样式
st.markdown("""
<style>
    :root {
        --primary: #FF9A8B; --primary-light: #FFD6D0;
        --secondary: #93C5FD; --accent: #A78BFA;
        --background: #FAFAFA; --surface: #FFFFFF;
        --text-primary: #374151; --text-secondary: #6B7280;
        --border: #E5E7EB; --radius-lg: 20px; --radius-md: 14px;
    }
    .current-step-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
    }
    .completed-step {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--primary);
        opacity: 0.8;
    }
    .fade-in { animation: fadeIn 0.6s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .celebration { animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🚀 任务执行中...")
    
    # 检查是否有分析结果
    if 'task_analysis' not in st.session_state:
        st.warning("请先进行任务分析")
        if st.button("返回分析页面"):
            st.switch_page("task_analysis.py")
        return
    
    analysis = st.session_state.task_analysis
    current_step = st.session_state.get('current_step', 0)
    
    # 获取步骤列表
    micro_steps = analysis.get('micro_steps', [])
    if not micro_steps:
        # 备用步骤
        micro_steps = [
            {"step": "准备好必要的工具", "time": "2分钟", "tip": "只是准备，不需要开始"},
            {"step": "设置5分钟倒计时", "time": "1分钟", "tip": "告诉自己只需坚持5分钟"},
            {"step": "从最简单的部分开始", "time": "5分钟", "tip": "完成后可以随时停止"},
            {"step": "完成后给自己奖励", "time": "2分钟", "tip": "庆祝小成就"}
        ]
    
    total_steps = len(micro_steps)
    
    # 进度显示
    progress = (current_step / total_steps) if total_steps > 0 else 0
    st.progress(progress, text=f"进度: {current_step}/{total_steps} ({int(progress*100)}%)")
    
    # 显示当前步骤
    if current_step < total_steps:
        current_task = micro_steps[current_step]
        
        st.markdown(f"""
        <div class='current-step-card fade-in'>
            <h2>当前步骤: {current_step + 1}/{total_steps}</h2>
            <h3 style='margin: 1rem 0;'>📌 {current_task.get('step', '步骤')}</h3>
            <p style='font-size: 1.2rem;'>⏱️ 预计时间: {current_task.get('time', '')}</p>
            {f"<p style='margin-top: 1rem; opacity: 0.9;'>💡 {current_task.get('tip', '')}</p>" if current_task.get('tip') else ""}
        </div>
        """, unsafe_allow_html=True)
        
        # 能量提示
        energy = current_task.get('energy', '')
        if energy:
            energy_messages = {
                "低": "这个步骤能量需求低，容易完成",
                "中": "中等能量需求，保持专注",
                "高": "这个步骤需要较多能量，完成后可以休息"
            }
            if energy in energy_messages:
                st.info(f"⚡ 能量提示: {energy_messages[energy]}")
        
        # 操作按钮
        st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ 完成这一步", type="primary", use_container_width=True):
                st.session_state.current_step = current_step + 1
                st.success("🎉 完成！")
                time.sleep(1)
                st.rerun()
        
        with col2:
            if st.button("⏸️ 暂停休息", type="secondary", use_container_width=True):
                st.info("休息5分钟，放松一下")
                # 这里可以添加计时器逻辑
                time.sleep(1)
        
        with col3:
            if st.button("🔄 重新开始", type="secondary", use_container_width=True):
                st.session_state.current_step = 0
                st.rerun()
        
        # 显示已完成步骤
        if current_step > 0:
            st.markdown("---")
            st.subheader("✅ 已完成步骤")
            for i in range(current_step):
                step = micro_steps[i]
                st.markdown(f"""
                <div class='completed-step'>
                    <strong>步骤 {i+1}:</strong> {step.get('step', '')}
                    <div style='font-size: 0.9rem; color: var(--text-secondary);'>
                        ⏱️ {step.get('time', '')} · ✅ 已完成
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # 所有步骤完成
        st.balloons()
        st.markdown("""
        <div class='current-step-card celebration' style='background: linear-gradient(135deg, #10B981 0%, #059669 100%);'>
            <h1>🎉 任务完成！</h1>
            <h3>你做得太棒了！</h3>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>为自己感到骄傲吧！</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示鼓励语
        encouragement = analysis.get('encouragement', '你太棒了！')
        st.markdown(f"### 💬 {encouragement}")
        
        # 显示奖励建议
        reward_ideas = analysis.get('adhd_specific', {}).get('reward_ideas', [])
        if reward_ideas:
            st.markdown("### 🏆 奖励时间")
            for reward in reward_ideas[:3]:
                st.markdown(f"- 🎁 {reward}")
        
        # 庆祝选项
        st.markdown("---")
        st.subheader("🎊 庆祝你的成就")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 查看统计", use_container_width=True):
                st.info("统计功能开发中...")
        
        with col2:
            if st.button("💾 保存记录", use_container_width=True):
                # 保存到历史记录
                if 'completed_tasks' not in st.session_state:
                    st.session_state.completed_tasks = []
                
                st.session_state.completed_tasks.append({
                    'task': analysis.get('task_analysis', {}).get('task_type', '任务'),
                    'time': time.strftime("%Y-%m-%d %H:%M"),
                    'steps': total_steps
                })
                
                st.success("记录已保存！")
        
        with col3:
            if st.button("🔄 新任务", use_container_width=True):
                # 清理状态
                if 'task_analysis' in st.session_state:
                    del st.session_state.task_analysis
                if 'current_step' in st.session_state:
                    del st.session_state.current_step
                
                st.switch_page("pages/task_spark_home.py")
        
        # 分享成就
        st.markdown("---")
        st.markdown("### ✨ 分享你的成就")
        st.markdown("""
        完成任务是值得庆祝的成就！你可以：
        - 告诉朋友或家人你完成了什么
        - 在日记中记录今天的进步
        - 给自己一个特别的奖励
        - 为明天的任务设定一个小目标
        """)

if __name__ == "__main__":
    main()