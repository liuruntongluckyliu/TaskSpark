"""
ai_engine.py - 统一的AI分析引擎
使用智能模拟AI提供完整的任务分析功能
完全离线，无需网络，无需API密钥
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from ai_simulator import AISimulator
import json
import time
from typing import Dict, Any

class TaskAnalyzer:
    """
    统一的任务分析器
    包装智能模拟AI，提供简单的接口
    """
    
    def __init__(self):
        """初始化AI分析器"""
        self.ai = AISimulator(name="TaskSpark AI")
        print(f"🤖 {self.ai.name} v{self.ai.version} 已就绪")
    
    def analyze_task(self, current_state: str, target_task: str, mood: str, difficulty: int) -> Dict[str, Any]:
        """
        分析任务并返回结果
        
        Args:
            current_state: 当前状态
            target_task: 目标任务
            mood: 当前情绪
            difficulty: 难度评分1-10
            
        Returns:
            分析结果字典
        """
        try:
            # 调用智能AI分析
            result = self.ai.analyze_task(current_state, target_task, mood, difficulty)
            
            # 添加分析元数据
            result["_meta"] = {
                "ai_model": "smart-simulator",
                "ai_version": self.ai.version,
                "analysis_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "offline_mode": True,
                "confidence": result.get("meta", {}).get("confidence_score", 0.85)
            }
            
            # 标准化输出格式
            standardized_result = {
                "task_analysis": result.get("task_analysis", {}),
                "micro_steps": result.get("micro_steps", []),
                "strategy": result.get("strategy", {}),
                "encouragement": result.get("encouragement", {}).get("main", "你可以做到的！"),
                "personalized_suggestions": result.get("personalized_suggestions", []),
                "adhd_specific": result.get("adhd_specific", {}),
                "_meta": result["_meta"]
            }
            
            return standardized_result
            
        except Exception as e:
            print(f"AI分析出错: {e}")
            return self._get_fallback_response(current_state, target_task, mood, difficulty)
    
    def _get_fallback_response(self, current_state: str, target_task: str, mood: str, difficulty: int) -> Dict[str, Any]:
        """备用响应（当AI模拟器出错时）"""
        return {
            "task_analysis": {
                "task_type": "通用任务",
                "difficulty_level": "中等",
                "mental_blocks": ["启动困难", "分心易", "能量不足"],
                "key_insight": "从小步骤开始建立动量",
                "estimated_time": "15-25分钟"
            },
            "micro_steps": [
                {"step": "准备好必要的工具材料", "time": "2分钟", "tip": "只是准备，不需要开始"},
                {"step": "设置5分钟倒计时", "time": "1分钟", "tip": "告诉自己只需坚持5分钟"},
                {"step": "从最简单的部分开始", "time": "5分钟", "tip": "完成后可以随时停止"},
                {"step": "完成后给自己一个奖励", "time": "2分钟", "tip": "庆祝小成就"}
            ],
            "strategy": {
                "name": "5分钟启动法",
                "description": "先做5分钟，然后可以决定是否继续",
                "first_step": "准备好需要的工具",
                "key_principle": "完成比完美重要"
            },
            "encouragement": "你已经迈出了第一步，这很了不起！",
            "personalized_suggestions": [
                "一次只专注于一个步骤",
                "完成后给自己一个小奖励",
                "记录今天的进步"
            ],
            "adhd_specific": {
                "focus_tips": ["使用计时器", "一次只做一件事", "定期休息"],
                "environment_tips": ["整理工作区域", "确保良好照明", "准备必要工具"],
                "reward_ideas": ["休息10分钟", "喝喜欢的饮料", "吃点零食"]
            },
            "_meta": {
                "ai_model": "fallback",
                "ai_version": "1.0",
                "analysis_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "offline_mode": True,
                "confidence": 0.7,
                "note": "使用备用方案，AI模拟器可能遇到问题"
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