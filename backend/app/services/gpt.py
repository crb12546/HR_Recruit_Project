"""GPT服务"""
import os
import openai
from typing import List, Dict, Any

class GPTService:
    """GPT-4服务实现"""
    
    def __init__(self):
        self.env = os.getenv("ENV", "test")
        if self.env == "test":
            self.mock = True
        else:
            self.mock = False
            self.api_key = os.getenv("OPENAI_API_KEY")
            openai.api_key = self.api_key
            self.model = "gpt-4"
    
    def generate_talent_portrait(self, text: str) -> str:
        """生成人才画像"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                return "具有8年Python开发经验的高级工程师，在微服务架构和分布式系统方面有丰富经验"
                
            # 构建提示词
            prompt = f"""
            请根据以下简历内容，生成一段简短的人才画像，描述候选人的核心能力、经验和专长。
            要求：
            1. 不超过100字
            2. 突出关键技能和经验年限
            3. 使用中文回答
            
            简历内容：
            {text}
            """
            
            # 调用GPT-4 API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长分析简历并提取关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200,
                stream=True
            )
            
            # 处理流式响应
            portrait = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    portrait += chunk.choices[0].delta.content
            
            return portrait
                
        except Exception as e:
            if not self.mock:
                raise Exception(f"GPT服务错误：{str(e)}")
            return "具有8年Python开发经验的高级工程师，在微服务架构和分布式系统方面有丰富经验"
    
    def extract_candidate_name(self, text: str) -> str:
        """提取候选人姓名"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                return "张三"
                
            # 构建提示词
            prompt = f"""
            请从以下简历内容中提取候选人的姓名。
            要求：
            1. 只返回姓名，不要有其他内容
            2. 如果找不到姓名，返回"未知"
            
            简历内容：
            {text}
            """
            
            # 调用GPT-4 API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长分析简历并提取关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            return response.choices[0].message.content.strip()
                
        except Exception as e:
            if not self.mock:
                raise Exception(f"GPT服务错误：{str(e)}")
            return "张三"
    
    def extract_job_tags(self, text: str) -> List[str]:
        """提取职位标签"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                return ["Python", "微服务", "分布式系统", "8年经验"]
                
            # 构建提示词
            prompt = f"""
            请从以下职位描述中提取关键技能和要求标签。
            要求：
            1. 返回5-10个标签
            2. 每个标签不超过10个字
            3. 包括技术栈、经验要求、学历要求等
            4. 以JSON数组格式返回，如["标签1", "标签2"]
            
            职位描述：
            {text}
            """
            
            # 调用GPT-4 API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长分析职位描述并提取关键标签。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            import json
            content = response.choices[0].message.content
            tags = json.loads(content).get("tags", [])
            return tags
                
        except Exception as e:
            if not self.mock:
                raise Exception(f"GPT服务错误：{str(e)}")
            return ["Python", "微服务", "分布式系统", "8年经验"]
    
    def extract_resume_tags(self, text: str) -> List[Dict[str, str]]:
        """提取简历标签"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                return [{"name": "Python"}, {"name": "FastAPI"}]
                
            # 构建提示词
            prompt = f"""
            请从以下简历内容中提取关键技能和经验标签。
            要求：
            1. 返回5-10个标签
            2. 每个标签不超过10个字
            3. 包括技术栈、经验年限、学历等
            4. 以JSON数组格式返回，如[{{"name": "标签1"}}, {{"name": "标签2"}}]
            
            简历内容：
            {text}
            """
            
            # 调用GPT-4 API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长分析简历并提取关键标签。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            import json
            content = response.choices[0].message.content
            tags = json.loads(content).get("tags", [])
            return [{"name": tag} for tag in tags]
                
        except Exception as e:
            if not self.mock:
                raise Exception(f"GPT服务错误：{str(e)}")
            return [{"name": "Python"}, {"name": "FastAPI"}]
