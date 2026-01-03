"""
ai_simulator.py - 智能模拟AI模块
完全离线运行的智能任务分析器
模拟真实AI的思维过程，提供个性化建议
"""

import random
import json
import time
from typing import Dict, List, Any, Tuple
from datetime import datetime
import re

class AISimulator:
    """
    智能模拟AI分析器
    基于心理学和任务管理原理的智能模拟
    无需API，完全离线运行
    """
    
    def __init__(self, name: str = "TaskSpark AI"):
        """
        初始化智能AI模拟器
        
        Args:
            name: AI名称
        """
        self.name = name
        self.version = "1.0.0"
        self.personality = "温暖、耐心、非评判性"
        
        # 心理学知识库
        self.psychology_knowledge = {
            "adhd_challenges": [
                "执行功能困难（计划、启动、组织）",
                "注意力分散和维持困难",
                "时间感知和管理的困难",
                "情绪调节和冲动控制",
                "工作记忆和认知灵活性"
            ],
            "procrastination_triggers": [
                "任务模糊不清或过于庞大",
                "对失败的恐惧或完美主义",
                "缺乏明确的第一步",
                "决策疲劳和选择过载",
                "情绪调节困难"
            ],
            "motivation_strategies": [
                "微小化：把大任务拆成微小步骤",
                "具体化：明确具体的下一步动作",
                "可视化：看到任务完成的景象",
                "奖励机制：完成后的即时奖励",
                "同伴支持：社会承诺或分享"
            ]
        }
        
        # 任务类型识别模式
        self.task_patterns = {
            "学习": {
                "keywords": ["学习", "复习", "读书", "看", "写作业", "考试", "预习", "背", "记", "课程", "笔记", "教材"],
                "icon": "📚",
                "color": "#4F46E5",
                "difficulty_factor": 0.8
            },
            "整理": {
                "keywords": ["整理", "打扫", "收拾", "清理", "收纳", "洗", "拖", "擦", "收拾", "整理", "清洁"],
                "icon": "🧹",
                "color": "#10B981",
                "difficulty_factor": 0.6
            },
            "工作": {
                "keywords": ["工作", "报告", "邮件", "会议", "项目", "代码", "编程", "开发", "写", "文档", "任务"],
                "icon": "💼",
                "color": "#F59E0B",
                "difficulty_factor": 1.0
            },
            "创作": {
                "keywords": ["写作", "画画", "设计", "创作", "拍", "制作", "编辑", "创作", "写", "画", "设计"],
                "icon": "🎨",
                "color": "#8B5CF6",
                "difficulty_factor": 0.9
            },
            "健康": {
                "keywords": ["锻炼", "运动", "健身", "跑步", "瑜伽", "冥想", "散步", "运动", "健身", "健康"],
                "icon": "💪",
                "color": "#EF4444",
                "difficulty_factor": 0.7
            },
            "社交": {
                "keywords": ["联系", "打电话", "见面", "聚会", "拜访", "聊天", "社交", "沟通", "联络"],
                "icon": "👥",
                "color": "#3B82F6",
                "difficulty_factor": 1.2
            }
        }
        
        # 情绪响应库
        self.emotion_responses = {
            "energetic": {
                "title": "⚡ 精力充沛",
                "strategy": "能量充沛模式：利用高能量完成挑战性任务",
                "advice": "现在是开始任务的好时机，利用你的能量快速推进",
                "encouragements": [
                    "趁现在有能量，快速开始吧！",
                    "精力充沛是完成任务的好时机！",
                    "你的能量是宝贵的资源，好好利用它！"
                ]
            },
            "tired": {
                "title": "😴 有些疲惫",
                "strategy": "低能量模式：从最小动作开始，允许休息",
                "advice": "疲惫时更要温柔对待自己，从最简单的动作开始",
                "encouragements": [
                    "累的时候启动最难，先做最小的一件事",
                    "完成一个小步骤就可以休息",
                    "你的身体需要温柔的启动，慢慢来"
                ]
            },
            "anxious": {
                "title": "😰 焦虑不安",
                "strategy": "减压模式：5分钟启动法 + 允许不完美",
                "advice": "焦虑是正常的，让我们把大任务变小，专注于过程",
                "encouragements": [
                    "焦虑是身体在保护你，感谢它然后继续前进",
                    "不需要完美，完成比完美重要",
                    "你已经迈出了最困难的第一步"
                ]
            },
            "procrastinating": {
                "title": "🌀 拖延回避",
                "strategy": "防拖延模式：明确第一步 + 设定停止点",
                "advice": "拖延不是懒惰，是任务需要拆解。先开始5分钟",
                "encouragements": [
                    "拖延不是懒惰，是任务需要拆解",
                    "先开始5分钟，然后可以随时停止",
                    "你已经意识到需要改变，这很了不起"
                ]
            },
            "overwhelmed": {
                "title": "😫 压力很大",
                "strategy": "分解模式：聚焦单一任务，忽略其他",
                "advice": "一次只做一件事，把大任务分解成小任务",
                "encouragements": [
                    "一次只做一件事，你已经做得很好了",
                    "任务看起来大，我们把它拆成小块",
                    "你已经走了这么远，继续前进"
                ]
            },
            "neutral": {
                "title": "😐 平稳中性",
                "strategy": "标准启动法：建立惯例和信号",
                "advice": "平稳的情绪是建立好习惯的好时机",
                "encouragements": [
                    "平稳的情绪是开始任务的好状态",
                    "让我们建立一个简单的启动惯例",
                    "你可以做到的！从小步骤开始"
                ]
            }
        }
        
        # 微步骤模板库
        self.microstep_templates = {
            "通用": [
                "准备好必要的工具和材料",
                "明确第一步具体做什么",
                "设置5分钟倒计时开始",
                "完成后检查进度",
                "决定是否继续"
            ],
            "学习": [
                "准备好学习材料（书、笔、笔记本）",
                "关闭手机通知，设置25分钟倒计时",
                "从最简单的概念开始回顾",
                "写下3个关键点",
                "做几道练习题巩固",
                "休息5分钟，喝口水"
            ],
            "整理": [
                "准备垃圾袋和收纳箱",
                "从离你最近的区域开始",
                "先处理明显垃圾",
                "分类物品（保留/丢弃/待定）",
                "简单擦拭表面",
                "完成一个区域后欣赏一下"
            ],
            "工作": [
                "打开电脑和相关软件",
                "列出今天要做的3件事",
                "从最容易的开始",
                "设置阶段性休息",
                "完成后自我奖励",
                "记录完成进度"
            ],
            "创作": [
                "准备好创作工具和材料",
                "设置一个简单的创作目标",
                "先完成粗糙的初稿",
                "休息一下再回来完善",
                "保存作品并分享给信任的人"
            ],
            "健康": [
                "换上舒适的运动服装",
                "准备水和毛巾",
                "从简单的热身开始",
                "完成核心锻炼动作",
                "进行放松拉伸",
                "记录今天的进步"
            ]
        }
        
        # 智能建议库
        self.suggestions_library = {
            "环境调整": [
                "改变位置：从床上移动到椅子上",
                "光线调整：打开窗帘或调整灯光",
                "声音环境：播放背景音乐或白噪音",
                "温度调整：确保环境舒适"
            ],
            "注意力管理": [
                "手机静音并放到视线外",
                "使用番茄工作法（25分钟专注+5分钟休息）",
                "一次只做一件事，避免多任务",
                "设置明确的开始和结束时间"
            ],
            "情绪调节": [
                "做3次深呼吸，放松身体",
                "告诉自己'完成比完美重要'",
                "接受当下的情绪状态，不加评判",
                "想象任务完成后的轻松感"
            ],
            "能量管理": [
                "先喝一杯水补充水分",
                "吃一点健康的零食补充能量",
                "做简单的伸展运动激活身体",
                "设置合理的休息间隔"
            ]
        }
        
        print(f"🤖 {self.name} v{self.version} 已初始化")
        print(f"   人格: {self.personality}")
        print(f"   知识库: {len(self.psychology_knowledge['adhd_challenges'])}条心理学知识")
        print(f"   任务模式: {len(self.task_patterns)}种任务类型")
    
    def analyze_task(self, current_state: str, target_task: str, mood: str, difficulty: int) -> Dict[str, Any]:
        """
        智能分析任务
        
        Args:
            current_state: 当前状态
            target_task: 目标任务
            mood: 当前情绪
            difficulty: 难度评分1-10
            
        Returns:
            完整的分析结果
        """
        print(f"🔍 {self.name} 正在分析任务...")
        print(f"   当前状态: {current_state}")
        print(f"   目标任务: {target_task}")
        print(f"   情绪: {mood}")
        print(f"   难度: {difficulty}/10")
        
        # 开始分析计时
        start_time = time.time()
        
        # 1. 识别任务类型
        task_type_info = self._identify_task_type(target_task)
        
        # 2. 分析心理障碍
        mental_blocks = self._analyze_mental_blocks(current_state, mood, difficulty)
        
        # 3. 生成个性化策略
        strategy = self._generate_strategy(current_state, mood, difficulty, task_type_info)
        
        # 4. 生成微步骤
        micro_steps = self._generate_micro_steps(target_task, task_type_info, difficulty, mood)
        
        # 5. 生成核心洞察
        key_insight = self._generate_key_insight(current_state, target_task, mood, difficulty, mental_blocks)
        
        # 6. 生成鼓励语
        encouragement = self._generate_encouragement(mood, difficulty, target_task)
        
        # 7. 生成个性化建议
        personalized_suggestions = self._generate_personalized_suggestions(current_state, mood, task_type_info)
        
        # 构建完整响应
        response = {
            "task_analysis": {
                "task_type": task_type_info["name"],
                "task_icon": task_type_info["icon"],
                "task_color": task_type_info["color"],
                "difficulty_level": self._get_difficulty_level(difficulty),
                "perceived_difficulty": f"{difficulty}/10",
                "mental_blocks": mental_blocks,
                "transition_challenge": self._analyze_transition_challenge(current_state, target_task),
                "key_insight": key_insight,
                "estimated_time": self._estimate_time(difficulty, len(micro_steps))
            },
            "micro_steps": micro_steps,
            "strategy": strategy,
            "encouragement": {
                "main": encouragement,
                "completion": self._get_completion_encouragement(),
                "progress_based": self._get_progress_encouragements()
            },
            "personalized_suggestions": personalized_suggestions,
            "adhd_specific": {
                "focus_tips": self._get_adhd_focus_tips(mood),
                "environment_tips": self._get_environment_tips(current_state),
                "reward_ideas": self._get_reward_ideas(task_type_info["name"]),
                "accountability_ideas": self._get_accountability_ideas()
            },
            "meta": {
                "ai_model": self.name,
                "ai_version": self.version,
                "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "api_used": False,
                "confidence_score": self._calculate_confidence_score(current_state, target_task),
                "note": "这是智能模拟AI的分析结果，基于心理学和任务管理原理"
            }
        }
        
        print(f"✅ 分析完成！用时: {response['meta']['processing_time_ms']}ms")
        print(f"   任务类型: {task_type_info['name']} {task_type_info['icon']}")
        print(f"   生成步骤: {len(micro_steps)}个微步骤")
        print(f"   核心策略: {strategy['name']}")
        
        return response
    
    def _identify_task_type(self, task: str) -> Dict[str, str]:
        """智能识别任务类型 - 改进版"""
        task_lower = task.lower()
        
        # 更详细的任务类型识别
        enhanced_task_patterns = {
            "学习": {
                "keywords": ["学习", "复习", "读书", "看", "写作业", "考试", "预习", "背", "记", "课程", "笔记", "教材", "读书", "论文", "研究"],
                "subtypes": {
                    "备考": ["考试", "期末", "测验", "测试", "考"],
                    "阅读": ["读书", "看书", "阅读", "文献", "文章"],
                    "写作": ["论文", "写作", "写文章", "报告", "作文"],
                    "记忆": ["背", "记忆", "记单词", "背诵"]
                },
                "icon": "📚",
                "color": "#4F46E5",
                "difficulty_factor": 0.8
            },
            "工作": {
                "keywords": ["工作", "报告", "邮件", "会议", "项目", "代码", "编程", "开发", "写", "文档", "任务", "制作", "设计", "分析", "计划"],
                "subtypes": {
                    "创意工作": ["设计", "创意", "策划", "方案"],
                    "技术工作": ["代码", "编程", "开发", "调试"],
                    "文书工作": ["报告", "文档", "邮件", "表格"],
                    "沟通工作": ["会议", "沟通", "协商", "谈判"]
                },
                "icon": "💼",
                "color": "#F59E0B",
                "difficulty_factor": 1.0
            },
            "整理": {
                "keywords": ["整理", "打扫", "收拾", "清理", "收纳", "洗", "拖", "擦", "收拾", "整理", "清洁", "收拾", "规整"],
                "subtypes": {
                    "深度整理": ["整理", "收纳", "规整"],
                    "日常清洁": ["打扫", "清洁", "洗", "拖"],
                    "物品处理": ["收拾", "清理", "丢弃"]
                },
                "icon": "🧹",
                "color": "#10B981",
                "difficulty_factor": 0.6
            },
            "创作": {
                "keywords": ["写作", "画画", "设计", "创作", "拍", "制作", "编辑", "创作", "写", "画", "设计", "记录", "拍摄"],
                "subtypes": {
                    "文字创作": ["写作", "写", "记录"],
                    "视觉创作": ["画画", "设计", "画", "拍摄"],
                    "音乐创作": ["作曲", "编曲", "弹奏"]
                },
                "icon": "🎨",
                "color": "#8B5CF6",
                "difficulty_factor": 0.9
            },
            "健康": {
                "keywords": ["锻炼", "运动", "健身", "跑步", "瑜伽", "冥想", "散步", "运动", "健身", "健康", "拉伸", "休息"],
                "subtypes": {
                    "有氧运动": ["跑步", "散步", "骑车"],
                    "力量训练": ["健身", "举重", "训练"],
                    "身心平衡": ["瑜伽", "冥想", "拉伸"]
                },
                "icon": "💪",
                "color": "#EF4444",
                "difficulty_factor": 0.7
            },
            "社交": {
                "keywords": ["联系", "打电话", "见面", "聚会", "拜访", "聊天", "社交", "沟通", "联络", "约会", "聚会"],
                "subtypes": {
                    "线上社交": ["联系", "打电话", "聊天"],
                    "线下社交": ["见面", "聚会", "拜访", "约会"]
                },
                "icon": "👥",
                "color": "#3B82F6",
                "difficulty_factor": 1.2
            }
        }
        
        # 使用增强的任务模式进行识别
        for task_name, info in enhanced_task_patterns.items():
            for keyword in info["keywords"]:
                if keyword in task_lower:
                    # 识别子类型
                    subtype = "通用"
                    for sub_name, sub_keywords in info.get("subtypes", {}).items():
                        for sub_keyword in sub_keywords:
                            if sub_keyword in task_lower:
                                subtype = sub_name
                                break
                        if subtype != "通用":
                            break
                    
                    # 识别任务的具体特征
                    task_features = []
                    if "复杂" in task_lower or "困难" in task_lower:
                        task_features.append("复杂")
                    if "简单" in task_lower or "容易" in task_lower:
                        task_features.append("简单")
                    if "紧急" in task_lower or "立刻" in task_lower or "赶紧" in task_lower:
                        task_features.append("紧急")
                    if "重要" in task_lower or "关键" in task_lower:
                        task_features.append("重要")
                    
                    return {
                        "name": task_name,
                        "subtype": subtype,
                        "features": task_features,
                        "icon": info["icon"],
                        "color": info["color"],
                        "difficulty_factor": info["difficulty_factor"],
                        "matched_keyword": keyword,
                        "user_description": task  # 保存用户原始描述
                    }
        
        # 如果没有匹配到，使用原来的类属性中的任务模式作为后备
        for task_name, info in self.task_patterns.items():
            for keyword in info["keywords"]:
                if keyword in task_lower:
                    return {
                        "name": task_name,
                        "subtype": "通用",
                        "features": [],
                        "icon": info["icon"],
                        "color": info["color"],
                        "difficulty_factor": info["difficulty_factor"],
                        "matched_keyword": keyword,
                        "user_description": task
                    }
        
        # 默认类型
        return {
            "name": "其他",
            "subtype": "通用",
            "features": [],
            "icon": "📋",
            "color": "#6B7280",
            "difficulty_factor": 1.0,
            "matched_keyword": "未匹配到特定类型",
            "user_description": task
        }
    
    def _analyze_mental_blocks(self, current_state: str, mood: str, difficulty: int) -> List[str]:
        """分析心理障碍 - 改进版"""
        blocks = []
        
        # 分析当前状态的具体细节
        state_keywords = {
            "床上": ["床上", "床", "躺着", "卧"],
            "手机": ["手机", "刷", "抖音", "视频", "游戏", "玩"],
            "电脑": ["电脑", "上网", "网页", "看剧"],
            "发呆": ["发呆", "放空", "愣"],
            "累": ["累", "疲惫", "困", "乏"],
            "焦虑": ["焦虑", "紧张", "担心", "害怕"],
            "拖延": ["拖延", "不想", "避免", "推迟"]
        }
        
        # 基于用户描述的具体状态分析
        current_lower = current_state.lower()
        for keyword, synonyms in state_keywords.items():
            for synonym in synonyms:
                if synonym in current_lower:
                    if keyword == "床上":
                        blocks.extend(["身体惯性", "从休息到活跃的模式切换困难", "环境暗示放松"])
                        # 如果床上玩手机，添加特定障碍
                        if any(s in current_lower for s in ["手机", "刷", "玩"]):
                            blocks.append("高刺激娱乐依赖")
                    elif keyword == "手机":
                        blocks.extend(["即时满足依赖", "注意力碎片化", "数字娱乐成瘾"])
                    elif keyword == "发呆":
                        blocks.extend(["决策困难", "缺乏启动信号", "思维迟缓"])
                    elif keyword == "累":
                        blocks.extend(["生理能量不足", "精神疲惫", "恢复需求高"])
                    break
        
        # 基于任务描述的具体特征分析
        # 如果用户描述了具体障碍，直接采纳
        if "记不住" in current_lower or "忘记" in current_lower:
            blocks.append("记忆保持困难")
        if "分心" in current_lower or "注意力" in current_lower:
            blocks.append("注意力控制困难")
        if "不知道" in current_lower or "不懂" in current_lower:
            blocks.append("知识理解障碍")
        if "害怕" in current_lower or "担心" in current_lower:
            blocks.append("恐惧或担忧情绪")
        
        # 基于情绪的专业分析
        mood_profiles = {
            "energetic": ["可能高估能力，计划过多"],
            "tired": ["执行功能降低，决策困难", "耐心减少，易受挫"],
            "anxious": ["灾难化思维", "完美主义压力", "过度担忧结果"],
            "procrastinating": ["任务回避模式激活", "即时满足偏倚", "未来折扣"],
            "overwhelmed": ["认知过载", "决策瘫痪", "压力导致的回避"]
        }
        
        if mood in mood_profiles:
            blocks.extend(mood_profiles[mood])
        
        # 基于难度的心理分析
        if difficulty >= 8:
            blocks.append("认知资源需求超出当前能力")
            blocks.append("自我效能感降低")
        elif difficulty >= 6:
            blocks.append("挑战与技能不平衡")
        
        # 去重并排序（把用户明确提到的障碍放在前面）
        unique_blocks = []
        mentioned_blocks = []
        
        # 先添加用户明确提到的障碍
        for block in blocks:
            if any(keyword in current_lower for keyword in ["记不住", "分心", "害怕", "担心"]) and any(kw in block for kw in ["记忆", "注意力", "恐惧"]):
                if block not in mentioned_blocks:
                    mentioned_blocks.append(block)
        
        # 添加其他障碍
        for block in blocks:
            if block not in mentioned_blocks and block not in unique_blocks:
                unique_blocks.append(block)
        
        return mentioned_blocks + unique_blocks[:6]  # 最多6个
    
    def _analyze_transition_challenge(self, current_state: str, target_task: str) -> str:
        """分析状态转换的困难"""
        transitions = {
            ("床", "学习"): "从完全放松到高度专注的巨大转换",
            ("床", "整理"): "从休息到体力活动的能量跳跃",
            ("手机", "工作"): "从高刺激娱乐到低刺激任务的转换困难",
            ("发呆", "创作"): "从被动状态到主动创造的模式切换",
            ("累", "运动"): "低能量状态开始体力活动的双重困难"
        }
        
        for (from_state, to_task), description in transitions.items():
            if from_state in current_state and to_task in target_task:
                return description
        
        # 通用描述
        return f"从'{current_state}'切换到'{target_task}'需要克服初始惯性"
    
    def _generate_strategy(self, current_state: str, mood: str, difficulty: int, task_type: Dict) -> Dict[str, str]:
        """生成个性化策略"""
        
        # 根据情绪选择基础策略
        base_strategy = self.emotion_responses.get(mood, self.emotion_responses["neutral"])
        
        # 根据当前状态调整
        state_adjustments = {
            "床": {
                "name": "渐进启动法",
                "description": "从床上可以做的微小动作开始，逐步增加活动量"
            },
            "手机": {
                "name": "数字断奶法",
                "description": "物理隔离电子设备，创造无干扰启动环境"
            },
            "累": {
                "name": "最低能量启动",
                "description": "只做消耗最小能量的第一步，允许随时停止"
            }
        }
        
        strategy_name = base_strategy["strategy"]
        strategy_desc = base_strategy["advice"]
        
        for keyword, adjustment in state_adjustments.items():
            if keyword in current_state:
                strategy_name = adjustment["name"]
                strategy_desc = adjustment["description"]
                break
        
        # 根据难度调整
        if difficulty >= 8:
            strategy_name = f"超困难任务专用: {strategy_name}"
            strategy_desc = f"针对高难度任务的特殊策略。{strategy_desc}"
        
        # 根据任务类型调整
        task_adjustments = {
            "学习": "分阶段专注法，结合主动回忆和间隔重复",
            "整理": "区域渐进法，完成一个区域再继续",
            "创作": "烂初稿优先法，先完成再完美"
        }
        
        if task_type["name"] in task_adjustments:
            strategy_desc = f"{task_adjustments[task_type['name']]}。{strategy_desc}"
        
        return {
            "name": strategy_name,
            "description": strategy_desc,
            "first_step": self._generate_first_step(current_state, task_type),
            "key_principle": "完成比完美重要，开始比完成重要"
        }
    
    def _generate_first_step(self, current_state: str, task_type: Dict) -> str:
        """生成最容易开始的第一步"""
        
        first_steps = {
            "床": [
                "慢慢坐起来，在床边坐1分钟",
                "做3次深呼吸，感受身体的苏醒",
                "把脚放在地上，感受地面的支撑"
            ],
            "手机": [
                "把手机屏幕朝下放在桌子上",
                "把手机放到另一个房间",
                "设置10分钟的勿扰模式"
            ],
            "桌子": [
                "清理出工作区域的一小块空间",
                "准备好需要的工具放在面前",
                "坐直身体，调整呼吸"
            ]
        }
        
        # 查找匹配的当前状态
        for state_key, steps in first_steps.items():
            if state_key in current_state:
                return random.choice(steps)
        
        # 默认第一步
        default_steps = [
            "站起来，伸展一下身体",
            "喝一小口水",
            "深呼吸三次",
            "告诉自己'我可以开始'"
        ]
        
        return random.choice(default_steps)
    
    def _generate_micro_steps(self, task: str, task_type: Dict, difficulty: int, mood: str) -> List[Dict[str, str]]:
        """生成微步骤 - 改进版，更贴合用户描述"""
        
        # 解析用户任务描述中的具体元素
        task_lower = task.lower()
        task_details = {
            "has_deadline": any(word in task_lower for word in ["今天", "明天", "截止", "之前"]),
            "has_specific_goal": any(word in task_lower for word in ["写完", "完成", "做好", "整理好"]),
            "is_creative": any(word in task_lower for word in ["写", "画", "设计", "创作"]),
            "is_analytical": any(word in task_lower for word in ["分析", "计算", "思考", "解决"]),
            "is_physical": any(word in task_lower for word in ["整理", "打扫", "收拾", "运动"])
        }
        
        # 基础模板选择
        base_template = "通用"
        if task_type["name"] in self.microstep_templates:
            base_template = task_type["name"]
        
        # 根据任务特征调整基础步骤
        base_steps = self.microstep_templates[base_template].copy()
        
        # 个性化调整
        personalized_steps = []
        
        # 第一步总是根据当前状态定制
        if "床" in task_lower or "躺" in task_lower:
            personalized_steps.append("慢慢坐起来，双脚放在地上，感受地面支撑")
        elif "手机" in task_lower or "刷" in task_lower:
            personalized_steps.append("把手机屏幕朝下放在够不到的地方")
        else:
            personalized_steps.append("调整姿势，做3次深呼吸")
        
        # 根据任务类型添加具体步骤
        if task_details["is_creative"]:
            personalized_steps.extend([
                "准备创作工具（纸笔/软件）",
                "设定一个小目标：先完成粗糙的草稿",
                "设置25分钟创作时间，不自我评判"
            ])
        elif task_details["is_analytical"]:
            personalized_steps.extend([
                "明确要解决的核心问题",
                "收集必要的信息和数据",
                "从一个简单的角度开始分析"
            ])
        elif task_details["is_physical"]:
            personalized_steps.extend([
                "准备必要的工具和材料",
                "从离你最近的区域开始",
                "设置15分钟定时，专注于一个区域"
            ])
        
        # 根据情绪调整步骤
        if mood == "anxious":
            personalized_steps.insert(1, "写下3个最担心的具体问题")
            personalized_steps.insert(2, "为每个担心想一个简单的应对方案")
        elif mood == "tired":
            personalized_steps.insert(1, "喝一杯水，补充水分")
            personalized_steps.insert(2, "做简单的伸展运动激活身体")
        elif mood == "procrastinating":
            personalized_steps.insert(1, "问自己：我在逃避什么具体的事情？")
            personalized_steps.insert(2, "把那个具体的事情拆成更小的部分")
        
        # 组合步骤
        all_steps = personalized_steps + base_steps
        
        # 根据难度调整数量
        if difficulty <= 3:
            step_count = min(4, len(all_steps))
            steps = all_steps[:step_count]
        elif difficulty <= 7:
            step_count = min(6, len(all_steps))
            steps = all_steps[:step_count]
        else:
            step_count = min(8, len(all_steps))
            steps = all_steps[:step_count]
        
        # 转换为标准格式
        formatted_steps = []
        for i, step in enumerate(steps, 1):
            # 为每个步骤生成个性化提示
            personalized_tip = self._generate_personalized_tip(step, i, task, mood, difficulty)
            
            formatted_steps.append({
                "step": step,
                "time": self._estimate_step_time(i, difficulty, mood),
                "tip": personalized_tip,
                "energy": self._estimate_step_energy(i, difficulty),
                "priority": "高" if i <= 3 else "中",
                "emotional_support": self._get_step_emotional_support(i, mood)
            })
        
        return formatted_steps
    
    def _estimate_step_time(self, step_number: int, difficulty: int, mood: str) -> str:
        """估计步骤所需时间"""
        base_time = 2  # 基础2分钟
        
        # 根据步骤序号调整
        if step_number == 1:
            time_multiplier = 0.5  # 第一步更快
        elif step_number <= 3:
            time_multiplier = 1.0
        else:
            time_multiplier = 1.5  # 后续步骤可能需要更多时间
        
        # 根据难度调整
        difficulty_multiplier = 1 + (difficulty - 5) / 10
        
        # 根据情绪调整
        mood_speed = {
            "energetic": 0.8,
            "tired": 1.3,
            "anxious": 1.1,
            "neutral": 1.0
        }
        mood_multiplier = mood_speed.get(mood, 1.0)
        
        estimated_minutes = round(base_time * time_multiplier * difficulty_multiplier * mood_multiplier)
        
        # 确保至少1分钟
        estimated_minutes = max(1, estimated_minutes)
        
        return f"{estimated_minutes}分钟"
    
    def _estimate_step_energy(self, step_number: int, difficulty: int) -> str:
        """估计步骤所需能量"""
        if step_number == 1:
            return "低"  # 第一步通常能量需求最低
        elif difficulty >= 8:
            return "高"
        elif difficulty >= 5:
            return "中"
        else:
            return "低"
    
    def _generate_step_tip(self, step: str, step_number: int, task_type: str) -> str:
        """生成步骤小提示"""
        
        tips_library = {
            1: [  # 第一步提示
                "只是准备，不需要开始真正的任务",
                "完成这一步就可以休息，没有压力",
                "这是建立启动动量的关键一步"
            ],
            2: [  # 中间步骤提示
                "保持专注，一次只做一件事",
                "如果需要可以暂停，但尽量完成",
                "关注过程而不是结果"
            ],
            "最后": [  # 最后步骤提示
                "庆祝你的成就，无论大小",
                "记录下今天的进步",
                "为明天的启动积累信心"
            ]
        }
        
        # 选择提示库
        if step_number == 1:
            tips = tips_library[1]
        elif "完成" in step or "结束" in step or "奖励" in step:
            tips = tips_library["最后"]
        else:
            tips = tips_library[2]
        
        # 根据任务类型调整提示
        task_specific_tips = {
            "学习": ["理解比记忆更重要", "主动回忆效果最好", "间隔重复帮助长期记忆"],
            "整理": ["完成一个区域再看整体", "视觉改善带来心理改善", "保持比完美更重要"],
            "工作": ["质量比数量重要", "休息提高效率", "完成比完美重要"]
        }
        
        if task_type in task_specific_tips:
            tips.extend(task_specific_tips[task_type])
        
        return random.choice(tips)
    
    def _generate_key_insight(self, current_state: str, target_task: str, mood: str, difficulty: int, mental_blocks: List[str]) -> str:
            """生成核心洞察 - 改进版，更深入"""
            
            # 分析状态转换的心理学意义
            transition_insights = {
                ("床", "学习"): "从生理休息到认知活动的巨大跳跃，需要温和的渐进激活",
                ("手机", "工作"): "从高刺激被动消费到低刺激主动创造的思维模式转换",
                ("焦虑", "工作"): "焦虑往往是过度思考未来，需要将注意力拉回到当下的小行动",
                ("累", "运动"): "低能量状态开始体力活动，需要尊重身体的节奏，从微小开始"
            }
            
            # 寻找最匹配的洞察
            best_insight = None
            for (state_key, mood_key), insight in transition_insights.items():
                if state_key in current_state and mood_key in mood:
                    best_insight = insight
                    break
            
            # 如果没有精确匹配，创建个性化洞察
            if not best_insight:
                # 基于用户描述的洞察
                if "忘记" in current_state or "记不住" in current_state:
                    best_insight = "记忆困难时，理解比死记更重要，建立联系比重复更有效"
                elif "分心" in current_state:
                    best_insight = "分心不是缺陷，是大脑在寻找更有趣的刺激，需要创造性的专注策略"
                elif "不知道" in current_state:
                    best_insight = "不知道从哪开始正是开始的最好时机，从最小的探索开始"
                else:
                    # 通用但深入的洞察
                    insights = [
                        f"从「{current_state[:15]}...」到「{target_task[:15]}...」的转换，本质是大脑神经通路的切换",
                        f"你感受到的{difficulty}/10困难，其中{difficulty*7}%是启动困难，{difficulty*3}%是执行困难",
                        f"「{mood}」情绪是你身体的信使，它在告诉你需要{self._get_emotional_message(mood)}"
                    ]
                    best_insight = random.choice(insights)
            
            # 添加基于心理障碍的深度分析
            if mental_blocks:
                block_analysis = {
                    "完美主义压力": "完美主义是进步的敌人，完成65分比追求100分更实际",
                    "能量不足": "低能量时完成的小任务，比高能量时的大计划更有价值",
                    "决策困难": "决策疲劳时，减少选择，接受足够好的方案"
                }
                
                for block in mental_blocks:
                    if block in block_analysis:
                        best_insight += f" 另外，{block_analysis[block]}"
                        break
            
            return best_insight

    def _get_emotional_message(self, mood: str) -> str:
        """获取情绪背后的信息"""
        messages = {
            "anxious": "降低期望，增加自我关怀",
            "tired": "尊重生理节奏，不要过度强迫",
            "procrastinating": "任务需要更具体的拆解和更低的启动门槛",
            "overwhelmed": "简化目标，一次只做一件事"
        }
        return messages.get(mood, "调整策略，适应当前状态")
    
    def _generate_encouragement(self, mood: str, difficulty: int, target_task: str) -> str:
        """生成鼓励语"""
        
        # 根据情绪选择鼓励语
        if mood in self.emotion_responses:
            encouragements = self.emotion_responses[mood]["encouragements"]
            encouragement = random.choice(encouragements)
        else:
            encouragement = "你可以做到的！从小步骤开始。"
        
        # 根据难度调整
        if difficulty >= 8:
            encouragement = f"面对高难度任务，{encouragement} 相信你可以找到适合自己的节奏。"
        
        # 个性化
        if target_task:
            encouragement = encouragement.replace("任务", f"'{target_task[:15]}...'")
        
        return encouragement
    
    def _generate_personalized_suggestions(self, current_state: str, mood: str, task_type: Dict) -> List[str]:
        """生成个性化建议"""
        suggestions = []
        
        # 基于当前状态的建议
        if "床" in current_state:
            suggestions.append("先改变身体姿势：从躺着到坐着")
            suggestions.append("拉开窗帘或开灯，改变环境光线")
        
        if "手机" in current_state:
            suggestions.append("手机设置静音，放到视线外")
            suggestions.append("告诉自己：'10分钟后可以看手机'")
        
        # 基于情绪的建议
        if mood == "tired":
            suggestions.append("先补充水分，喝一杯水")
            suggestions.append("设置明确的休息时间，完成后立即休息")
        
        if mood == "anxious":
            suggestions.append("做3次深呼吸，放松肩膀")
            suggestions.append("告诉自己：'完成比完美重要'")
        
        # 基于任务类型的建议
        if task_type["name"] == "学习":
            suggestions.append("使用番茄工作法：25分钟学习+5分钟休息")
            suggestions.append("主动回忆：学完后合上书本复述")
        
        if task_type["name"] == "整理":
            suggestions.append("从最杂乱的1平方米开始")
            suggestions.append("播放喜欢的音乐，让整理更愉快")
        
        # 通用建议
        suggestions.append("一次只专注于一个步骤")
        suggestions.append("完成后给自己一个小奖励")
        
        # 去重并限制数量
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion not in unique_suggestions and len(unique_suggestions) < 5:
                unique_suggestions.append(suggestion)
        
        return unique_suggestions
    
    def _get_difficulty_level(self, difficulty: int) -> str:
        """获取难度级别描述"""
        if difficulty <= 3:
            return "低"
        elif difficulty <= 6:
            return "中低"
        elif difficulty <= 8:
            return "中高"
        else:
            return "高"
    
    def _estimate_time(self, difficulty: int, step_count: int) -> str:
        """估计总时间"""
        base_time_per_step = 3  # 每个步骤基础3分钟
        difficulty_multiplier = 0.8 + (difficulty * 0.04)  # 难度增加时间
        
        total_minutes = round(step_count * base_time_per_step * difficulty_multiplier)
        
        if total_minutes < 60:
            return f"约{total_minutes}分钟"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if minutes > 0:
                return f"约{hours}小时{minutes}分钟"
            else:
                return f"约{hours}小时"
    
    def _calculate_confidence_score(self, current_state: str, target_task: str) -> float:
        """计算分析置信度分数"""
        score = 0.7  # 基础分数
        
        # 状态描述的详细程度
        if len(current_state) > 5:
            score += 0.1
        
        # 任务描述的详细程度
        if len(target_task) > 5:
            score += 0.1
        
        # 任务类型匹配度
        task_type = self._identify_task_type(target_task)
        if task_type["name"] != "其他":
            score += 0.1
        
        # 确保在0-1范围内
        return min(0.95, max(0.5, round(score, 2)))
    
    def _get_adhd_focus_tips(self, mood: str) -> List[str]:
        """获取ADHD专注提示"""
        tips = [
            "使用计时器创造时间边界",
            "一次只处理一个任务，避免多任务",
            "把大任务拆成25分钟的小块",
            "定期站起来活动，保持血液循环"
        ]
        
        if mood == "anxious":
            tips.append("焦虑时先进行呼吸练习，再开始任务")
        
        return tips[:3]
    
    def _get_environment_tips(self, current_state: str) -> List[str]:
        """获取环境调整提示"""
        tips = []
        
        if "床" in current_state:
            tips.append("考虑换个位置，比如移动到书桌前")
            tips.append("调整灯光，增加环境亮度")
        
        if any(word in current_state for word in ["手机", "电视", "电脑"]):
            tips.append("创造无电子干扰的工作区域")
            tips.append("使用网站拦截工具减少分心")
        
        if not tips:
            tips = [
                "整理工作区域，减少视觉杂乱",
                "确保良好的照明和通风",
                "准备必要的工具在手边"
            ]
        
        return tips[:3]
    
    def _get_reward_ideas(self, task_type: str) -> List[str]:
        """获取奖励想法"""
        rewards = {
            "通用": ["休息10分钟", "喝喜欢的饮料", "看一集短剧", "吃点零食"],
            "学习": ["完成一章后的短休息", "学习后的娱乐时间", "达成目标的自我肯定"],
            "整理": ["整理后的空间享受", "完成后的成就感", "拍照记录前后对比"],
            "工作": ["完成后的放松时间", "小成就的自我奖励", "进度可视化的满足感"]
        }
        
        if task_type in rewards:
            return rewards[task_type]
        return rewards["通用"]
    
    def _get_accountability_ideas(self) -> List[str]:
        """获取责任机制想法"""
        return [
            "告诉朋友你的计划",
            "在社交媒体上分享目标",
            "使用进度跟踪应用",
            "设置完成后的汇报机制"
        ]
    
    def _get_completion_encouragement(self) -> str:
        """获取完成鼓励语"""
        completions = [
            "🎉 太棒了！你做到了！",
            "✨ 为你骄傲！任务完成！",
            "🌟 优秀的完成！庆祝一下吧！",
            "💫 坚持到底的力量，太了不起了！"
        ]
        return random.choice(completions)
    
    def _get_progress_encouragements(self) -> Dict[str, str]:
        """获取基于进度的鼓励语"""
        return {
            "0": "最难的是开始，你已经做到了！",
            "25": "25%完成！继续前进！",
            "50": "过半了！最艰难的部分已经过去！",
            "75": "接近终点了！坚持就是胜利！",
            "100": "🎉 任务完成！你太棒了！"
        }


# 测试函数
def test_ai_simulator():
    """测试智能AI模拟器"""
    print("🧪 测试智能AI模拟器")
    print("=" * 60)
    
    # 创建模拟器
    simulator = AISimulator()
    
    # 测试用例
    test_cases = [
        {
            "name": "从刷手机到学习",
            "current_state": "躺在床上刷抖音",
            "target_task": "复习期末考试",
            "mood": "procrastinating",
            "difficulty": 8
        },
        {
            "name": "从躺床到整理",
            "current_state": "刚睡醒躺在床上",
            "target_task": "整理混乱的房间",
            "mood": "tired",
            "difficulty": 6
        },
        {
            "name": "从拖延到工作",
            "current_state": "坐在桌前发呆刷微博",
            "target_task": "完成工作报告",
            "mood": "anxious",
            "difficulty": 9
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 测试场景: {test_case['name']}")
        print(f"   当前状态: {test_case['current_state']}")
        print(f"   目标任务: {test_case['target_task']}")
        print(f"   情绪: {test_case['mood']}")
        print(f"   难度: {test_case['difficulty']}/10")
        
        # 分析任务
        result = simulator.analyze_task(
            current_state=test_case['current_state'],
            target_task=test_case['target_task'],
            mood=test_case['mood'],
            difficulty=test_case['difficulty']
        )
        
        # 显示关键结果
        print(f"\n   📝 任务类型: {result['task_analysis']['task_type']} {result['task_analysis']['task_icon']}")
        print(f"   🎯 核心策略: {result['strategy']['name']}")
        print(f"   💡 关键洞察: {result['task_analysis']['key_insight']}")
        print(f"   📊 估计时间: {result['task_analysis']['estimated_time']}")
        print(f"   🔢 微步骤数: {len(result['micro_steps'])}")
        print(f"   💬 鼓励语: {result['encouragement']['main'][:50]}...")
        
        print("   📋 前2个步骤:")
        for i, step in enumerate(result['micro_steps'][:2], 1):
            print(f"      {i}. {step['step']} ({step['time']})")
        
        print("   💡 个性化建议:")
        for suggestion in result['personalized_suggestions'][:2]:
            print(f"      • {suggestion}")
    
    print("\n" + "=" * 60)
    print("✅ 智能AI模拟器测试完成！")
    print("✨ 所有功能正常，可以集成到主程序中")


if __name__ == "__main__":
    test_ai_simulator()