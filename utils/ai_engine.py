import openai
import streamlit as st  # 用于安全读取密钥
import sys
import os
sys.path.append(os.path.dirname(__file__))

from ai_simulator import AISimulator
import json
import time
from typing import Dict, Any

class TaskAnalyzer:
    """统一的任务分析器"""
    
    def __init__(self):
        """初始化AI分析器"""
        self.ai = AISimulator(name="TaskSpark AI")
        print(f"🤖 {self.ai.name} v{self.ai.version} 已就绪")
    
    def analyze_task(self, current_state: str, target_task: str, mood: str, difficulty: int) -> dict:
        """分析任务的核心方法"""
        try:
            print(f"🔍 开始分析任务: {target_task}")
            result = self.ai.analyze_task(
                current_state=current_state,
                target_task=target_task,
                mood=mood,
                difficulty=difficulty
            )
            print(f"✅ 分析完成，返回 {len(result.get('micro_steps', []))} 个步骤")
            return result
        except Exception as e:
            print(f"❌ AI分析失败: {e}")
            import traceback
            traceback.print_exc()
            return self._get_default_analysis(current_state, target_task, mood, difficulty)
    
    def _get_default_analysis(self, current_state, target_task, mood, difficulty):
        """获取默认分析结果"""
        return {
            "task_analysis": {
                "task_type": "自定义任务",
                "difficulty_level": f"{difficulty}/10",
                "estimated_time": "30分钟",
                "key_insight": f"从{current_state}到{target_task}的转变需要逐步过渡",
                "mental_blocks": ["启动惯性", "注意力转移困难"]
            },
            "micro_steps": [
                {"step": f"从{current_state}中慢慢脱离", "time": "3分钟", "tip": "温和过渡"},
                {"step": f"准备开始{target_task}的环境", "time": "5分钟", "tip": "环境准备"},
                {"step": "从最小的一步开始执行", "time": "10分钟", "tip": "建立动力"},
                {"step": "检查进度，调整节奏", "time": "3分钟", "tip": "灵活应对"}
            ],
            "strategy": {
                "name": "渐进启动法",
                "description": "从小动作开始建立执行动量",
                "key_principle": "开始比完成更重要"
            },
            "encouragement": "你已经意识到了需要改变，这是最重要的第一步！",
            "_meta": {
                "ai_model": "TaskSpark AI",
                "offline_mode": True
            }
        }
    
    
    
    def get_progress_encouragement(self, progress: int) -> str:
        """根据进度获取鼓励语"""
        if progress <= 25:
            return "最难的是开始，你已经做到了！"
        elif progress <= 50:
            return "25%完成！继续前进！"
        elif progress <= 75:
            return "过半了！最艰难的部分已经过去！"
        elif progress < 100:
            return "75%了！胜利在望！"
        else:
            return "🎉 任务完成！你太棒了！"


# 单例实例
_analyzer_instance = None

def get_analyzer() -> TaskAnalyzer:
    """获取分析器实例（单例模式）"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = TaskAnalyzer()
    return _analyzer_instance


# 测试函数
def test_ai_engine():
    """测试AI引擎"""
    print("🧪 测试AI引擎")
    print("=" * 60)
    
    analyzer = get_analyzer()
    
    # 测试用例
    test_cases = [
        ("躺在床上刷抖音", "复习期末考试", "procrastinating", 8),
        ("刚睡醒躺在床上", "整理房间", "tired", 6),
        ("坐在桌前发呆", "写工作报告", "anxious", 7)
    ]
    
    for current, task, mood, difficulty in test_cases:
        print(f"\n📋 测试: {current} → {task}")
        
        # 分析任务
        result = analyzer.analyze_task(current, task, mood, difficulty)
        
        # 显示结果
        print(f"   🎯 任务类型: {result['task_analysis']['task_type']}")
        print(f"   📊 难度: {result['task_analysis']['difficulty_level']}")
        print(f"   ⚡ 策略: {result['strategy']['name']}")
        print(f"   💬 鼓励: {result['encouragement'][:50]}...")
        print(f"   🔢 步骤数: {len(result['micro_steps'])}")
        print(f"   🤖 AI模型: {result['_meta']['ai_model']}")
        print(f"   📡 离线模式: {result['_meta']['offline_mode']}")
    
    print("\n" + "=" * 60)
    print("✅ AI引擎测试完成！")
    return True


if __name__ == "__main__":
    test_ai_engine()