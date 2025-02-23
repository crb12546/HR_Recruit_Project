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
