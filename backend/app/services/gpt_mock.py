import json
import os
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class GPTService:
    """GPT-4服务的模拟实现"""
    
    def __init__(self):
        """初始化GPT服务"""
        self.mock_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          "tests", "mocks", "data")
        logger.info(f"初始化模拟GPT服务，数据路径: {self.mock_data_path}")
    
    def parse_resume(self, ocr_content: str) -> Dict[str, Any]:
        """解析简历内容（模拟实现）"""
        logger.info("模拟解析简历内容")
        
        # 如果OCR内容为空，返回空结果
        if not ocr_content:
            return {}
        
        # 简单解析OCR内容
        parsed_content = {}
        lines = ocr_content.split("\n")
        
        for line in lines:
            if "：" in line:
                key, value = line.split("：", 1)
                if key == "姓名":
                    parsed_content["name"] = value
                elif key == "学历":
                    parsed_content["education"] = value
                elif key == "技能":
                    parsed_content["skills"] = [skill.strip() for skill in value.split(",")]
                elif key == "工作经验":
                    parsed_content["experience"] = value
                elif key == "联系电话":
                    parsed_content["contact"] = value
        
        return parsed_content
    
    def generate_talent_portrait(self, parsed_content: Dict[str, Any]) -> str:
        """生成人才画像（模拟实现）"""
        logger.info("模拟生成人才画像")
        
        # 如果解析内容为空，返回空结果
        if not parsed_content:
            return ""
        
        # 根据解析内容生成人才画像
        name = parsed_content.get("name", "候选人")
        education = parsed_content.get("education", "")
        skills = parsed_content.get("skills", [])
        experience = parsed_content.get("experience", "")
        
        skills_str = "、".join(skills) if skills else "相关技能"
        
        return f"{name}是一名有{experience}经验的开发工程师，{education}学历，精通{skills_str}。"
    
    def generate_resume_tags(self, resume_content: str) -> List[str]:
        """从简历内容中提取标签（模拟实现）"""
        logger.info("模拟从简历内容中提取标签")
        
        # 如果简历内容为空，返回空列表
        if not resume_content:
            return []
        
        # 模拟标签提取
        default_tags = ["Python", "Java", "SQL", "FastAPI", "Vue.js", "React", "Docker", "Kubernetes"]
        
        # 根据简历内容选择相关标签
        selected_tags = []
        for tag in default_tags:
            if tag.lower() in resume_content.lower() or len(selected_tags) < 3:
                selected_tags.append(tag)
                if len(selected_tags) >= 5:  # 最多返回5个标签
                    break
        
        return selected_tags
    
    def extract_skills(self, text: str) -> List[str]:
        """从文本中提取技能（模拟实现）"""
        logger.info("模拟从文本中提取技能")
        
        # 如果文本为空，返回空列表
        if not text:
            return []
        
        # 模拟技能提取
        default_skills = ["Python", "Java", "SQL", "FastAPI", "Vue.js", "React", "Docker", "Kubernetes"]
        
        # 根据文本内容选择相关技能
        selected_skills = []
        for skill in default_skills:
            if skill.lower() in text.lower() or len(selected_skills) < 3:
                selected_skills.append(skill)
                if len(selected_skills) >= 5:  # 最多返回5个技能
                    break
        
        return selected_skills
    
    def generate_interview_questions(self, job_requirements: str, resume: Optional[str] = None, 
                                    candidate_skills: List[str] = None, count: int = 5) -> List[str]:
        """生成面试问题（模拟实现）"""
        logger.info(f"模拟生成面试问题，数量: {count}")
        
        # 基于职位要求和候选人技能生成面试问题
        questions = []
        
        # 通用问题
        general_questions = [
            "请介绍一下你的工作经历和技术专长",
            "你认为自己最大的优势是什么？",
            "你如何处理工作中的压力和挑战？",
            "你对我们公司/职位有什么了解？",
            "你为什么想加入我们团队？"
        ]
        
        # 从模拟数据中获取面试问题
        try:
            with open(os.path.join(self.mock_data_path, "mock_interviews.json"), "r", encoding="utf-8") as f:
                mock_data = json.load(f)
                
            for interview in mock_data.get("interviews", []):
                if interview.get("interview_questions"):
                    questions.extend(interview.get("interview_questions"))
                    
            questions.extend(general_questions)
            
            # 确保返回指定数量的问题
            return questions[:count]
        except Exception as e:
            logger.error(f"读取模拟数据失败: {str(e)}")
            return general_questions[:count]
    
    def analyze_interview_feedback(self, feedback: str) -> Dict[str, Any]:
        """分析面试反馈（模拟实现）"""
        logger.info(f"模拟分析面试反馈: {feedback[:30]}...")
        
        # 简单分析反馈内容
        result = {
            "strengths": ["技术能力强", "沟通能力好"],
            "weaknesses": ["项目经验不足"],
            "recommendation": "建议录用",
            "fit_score": 85
        }
        
        # 根据反馈内容调整分析结果
        if "技术" in feedback:
            result["strengths"].append("技术知识扎实")
        if "经验" in feedback:
            result["strengths"].append("经验丰富")
        if "不足" in feedback or "欠缺" in feedback:
            result["weaknesses"].append("需要进一步培训")
        if "推荐" in feedback:
            result["recommendation"] = "强烈推荐录用"
            result["fit_score"] = 90
        
        return result
    
    def match_job_requirements(self, resume_content: str = None, job_requirements: str = None, 
                                    talent_portrait: str = None) -> Dict[str, Any]:
        """匹配简历与职位需求（模拟实现）"""
        logger.info("模拟匹配简历与职位需求")
        
        # 简单匹配分析
        result = {
            "score": 75,
            "analysis": "候选人基本符合职位要求，但在某些方面需要进一步提升",
            "matching_points": ["技术技能匹配", "教育背景符合"],
            "missing_points": ["项目经验不足", "行业经验欠缺"]
        }
        
        # 使用任何可用的内容进行匹配
        content_to_check = resume_content or talent_portrait or ""
        requirements_to_check = job_requirements or ""
        
        # 根据内容调整匹配结果
        if len(content_to_check) > 500 and len(requirements_to_check) > 200:
            result["score"] = 85
            result["analysis"] = "候选人非常符合职位要求，建议安排面试"
            result["matching_points"].append("工作经验丰富")
            result["missing_points"] = ["可能需要适应新团队文化"]
        
        return result
    
    def generate_onboarding_tasks(self, position: str, department: str) -> List[Dict[str, Any]]:
        """生成入职任务（模拟实现）"""
        logger.info(f"模拟生成入职任务，职位: {position}, 部门: {department}")
        
        # 从模拟数据中获取入职任务
        try:
            with open(os.path.join(self.mock_data_path, "mock_onboardings.json"), "r", encoding="utf-8") as f:
                mock_data = json.load(f)
                
            for onboarding in mock_data.get("onboardings", []):
                if onboarding.get("position") == position and onboarding.get("department") == department:
                    return onboarding.get("tasks", [])
            
            # 如果没有找到匹配的任务，返回默认任务
            return [
                {
                    "task_name": "准备办公设备",
                    "description": "配置电脑、显示器等办公设备",
                    "assignee": "IT部门",
                    "deadline": "入职前1天",
                    "status": "pending"
                },
                {
                    "task_name": "配置开发环境",
                    "description": "安装必要的开发软件和工具",
                    "assignee": "技术部门",
                    "deadline": "入职当天",
                    "status": "pending"
                },
                {
                    "task_name": "安排入职培训",
                    "description": "公司制度、文化和业务培训",
                    "assignee": "HR部门",
                    "deadline": "入职第1天",
                    "status": "pending"
                }
            ]
        except Exception as e:
            logger.error(f"读取模拟数据失败: {str(e)}")
            return []
