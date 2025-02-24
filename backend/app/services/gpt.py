import os
from typing import List, Dict
from openai import OpenAI
from fastapi import HTTPException

class GPTService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4"

    def _call_gpt(self, prompt: str) -> str:
        """调用GPT-4模型进行推理"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的HR助手，擅长分析简历和职位需求。请用中文回复。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"GPT服务调用失败: {str(e)}"
            )

    def generate_talent_portrait(self, text: str) -> str:
        """
        生成人才画像
        
        Args:
            text: 简历文本内容
            
        Returns:
            str: 人才画像描述
        """
        prompt = f"""
        请根据以下简历内容，生成一段专业的人才画像描述：
        
        {text}
        
        要求：
        1. 突出关键技能和经验
        2. 描述专业领域的专长
        3. 总结职业发展阶段
        4. 使用专业的HR语言
        """
        return self._call_gpt(prompt)

    def extract_job_info(self, text: str) -> dict:
        """
        从职位描述文档中提取结构化信息
        
        Args:
            text: 职位描述文本
            
        Returns:
            dict: 职位信息字典
        """
        prompt = f"""
        请从以下职位描述文档中提取关键信息，并以JSON格式返回：
        
        {text}
        
        要求提取以下字段：
        1. position_name: 职位名称
        2. department: 所属部门
        3. responsibilities: 岗位职责
        4. skills: 技能要求（数组）
        5. education: 学历要求
        6. experience: 工作年限要求
        7. salary_min: 最低薪资（数字）
        8. salary_max: 最高薪资（数字）
        9. location: 工作地点（数组，如["北京", "海淀区"]）
        
        示例格式：
        {
          "position_name": "高级Python工程师",
          "department": "技术部",
          "responsibilities": "负责核心系统开发...",
          "skills": ["Python", "FastAPI", "MySQL"],
          "education": "本科及以上",
          "experience": "3-5年",
          "salary_min": 25000,
          "salary_max": 35000,
          "location": ["北京", "海淀区"]
        }
        """
        response = self._call_gpt(prompt)
        try:
            return eval(response)
        except:
            raise ValueError("职位信息解析失败")

    def calculate_match_score(self, resume: dict, job: dict) -> dict:
        """
        计算简历与职位的匹配度
        
        Args:
            resume: 简历信息
            job: 职位需求信息
            
        Returns:
            dict: 包含总分和各维度得分的字典
        """
        prompt = f"""
        请分析以下简历和职位需求的匹配程度，并给出详细评分：

        简历信息：
        {resume}

        职位需求：
        {job}

        请从以下维度进行评分（0-100分）并给出评分理由：
        1. 技能匹配度：技能要求的覆盖程度
        2. 经验匹配度：工作年限和相关经验
        3. 教育匹配度：学历要求的满足程度
        4. 职责匹配度：是否具备完成岗位职责的能力

        返回格式：
        {{
            "total_score": 85,  # 总分（各维度加权平均）
            "skill_score": {{
                "score": 90,
                "reason": "掌握所需的核心技能..."
            }},
            "experience_score": {{
                "score": 80,
                "reason": "工作年限符合要求..."
            }},
            "education_score": {{
                "score": 100,
                "reason": "学历超过要求..."
            }},
            "responsibility_score": {{
                "score": 85,
                "reason": "具有相关项目经验..."
            }}
        }}
        """
        response = self._call_gpt(prompt)
        try:
            return eval(response)
        except:
            raise ValueError("匹配度计算失败")

    def extract_job_tags(self, text: str) -> List[str]:
        """
        从职位描述中提取关键标签
        
        Args:
            text: 职位描述文本
            
        Returns:
            List[str]: 职位标签列表
        """
        prompt = f"""
        请从以下职位描述中提取关键标签：
        
        {text}
        
        要求：
        1. 提取技能要求
        2. 提取经验要求
        3. 提取专业领域
        4. 以JSON数组格式返回
        """
        response = self._call_gpt(prompt)
        try:
            return eval(response)
        except:
            return []

    def extract_resume_tags(self, text: str) -> List[Dict[str, str]]:
        """
        从简历中提取技能标签
        
        Args:
            text: 简历文本内容
            
        Returns:
            List[Dict[str, str]]: 技能标签列表
        """
        prompt = f"""
        请从以下简历内容中提取关键技能标签：
        
        {text}
        
        要求：
        1. 提取技术技能
        2. 提取专业领域
        3. 提取经验年限
        4. 以JSON数组格式返回，每个标签包含name字段
        """
        response = self._call_gpt(prompt)
        try:
            return eval(response)
        except:
            return []
