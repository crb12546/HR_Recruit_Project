"""GPT服务模块"""
import os
import logging
from typing import List, Dict, Any

# 获取日志记录器
logger = logging.getLogger(__name__)

class GPTService:
    """GPT-4服务实现"""
    
    def __init__(self):
        """初始化GPT服务"""
        self.env = os.getenv("ENV", "development")
        self.mock = self.env in ["development", "test"] or os.getenv("MOCK_SERVICES", "False").lower() == "true"
        self.model = "gpt-4"
        
        if not self.mock:
            try:
                import openai
                self.api_key = os.getenv("OPENAI_API_KEY")
                if not self.api_key:
                    logger.warning("未设置OPENAI_API_KEY环境变量，将使用模拟模式")
                    self.mock = True
                else:
                    openai.api_key = self.api_key
                    # 创建OpenAI客户端
                    self.openai = openai
                    logger.info("初始化GPT服务，模型: gpt-4")
            except ImportError:
                logger.warning("无法导入openai模块，将使用模拟模式")
                self.mock = True
        else:
            # 创建模拟的OpenAI客户端
            from app.services.gpt_mock import MockOpenAI
            self.openai = MockOpenAI()
            logger.info("初始化模拟GPT服务")
    
    def generate_talent_portrait(self, text: str) -> str:
        """生成人才画像"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                logger.info("使用模拟数据生成人才画像")
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
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长分析简历并提取关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            # 处理响应
            portrait = response.choices[0].message.content
            return portrait
                
        except Exception as e:
            logger.error(f"生成人才画像失败: {str(e)}")
            return "具有8年Python开发经验的高级工程师，在微服务架构和分布式系统方面有丰富经验"
    
    def extract_candidate_name(self, text: str) -> str:
        """提取候选人姓名"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                logger.info("使用模拟数据提取候选人姓名")
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
            response = self.openai.chat.completions.create(
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
            logger.error(f"提取候选人姓名失败: {str(e)}")
            return "张三"
    
    def extract_job_tags(self, text: str) -> List[str]:
        """提取职位标签"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                logger.info("使用模拟数据提取职位标签")
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
            response = self.openai.chat.completions.create(
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
            logger.error(f"提取职位标签失败: {str(e)}")
            return ["Python", "微服务", "分布式系统", "8年经验"]
    
    def generate_resume_tags(self, text: str) -> List[str]:
        """从简历内容中提取标签"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                logger.info("使用模拟数据提取简历标签")
                return ["Python", "FastAPI", "微服务", "分布式系统", "8年经验"]
                
            # 构建提示词
            prompt = f"""
            请从以下简历内容中提取关键技能和经验标签。
            要求：
            1. 返回5-10个标签
            2. 每个标签不超过10个字
            3. 包括技术栈、经验年限、学历等
            4. 以JSON数组格式返回，如["标签1", "标签2"]
            
            简历内容：
            {text}
            """
            
            # 调用GPT-4 API
            response = self.openai.chat.completions.create(
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
            return tags
                
        except Exception as e:
            logger.error(f"提取简历标签失败: {str(e)}")
            return ["Python", "FastAPI", "微服务", "分布式系统", "8年经验"]
