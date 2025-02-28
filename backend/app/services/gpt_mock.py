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
    
    def generate_interview_questions(self, job_requirements: str, candidate_skills: List[str], 
                                    count: int = 5) -> List[str]:
        """生成面试问题（模拟实现）"""
        logger.info(f"模拟生成面试问题，数量: {count}")
        
        # 基于职位要求和候选人技能生成面试问题
        questions = []
        
        # 从模拟数据中获取面试问题
        try:
            with open(os.path.join(self.mock_data_path, "mock_interviews.json"), "r", encoding="utf-8") as f:
                mock_data = json.load(f)
                
            for interview in mock_data.get("interviews", []):
                if interview.get("interview_questions"):
                    questions.extend(interview.get("interview_questions"))
                    
            # 如果没有足够的问题，添加一些通用问题
            general_questions = [
                "请介绍一下你的工作经历和技术专长",
                "你认为自己最大的优势是什么？",
                "你如何处理工作中的压力和挑战？",
                "你对我们公司/职位有什么了解？",
                "你为什么想加入我们团队？"
            ]
            
            questions.extend(general_questions)
            
            # 确保返回指定数量的问题
            return questions[:count]
        except Exception as e:
            logger.error(f"读取模拟数据失败: {str(e)}")
            return general_questions[:count]
    
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
