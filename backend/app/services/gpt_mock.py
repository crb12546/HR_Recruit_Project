class GPTService:
    def __init__(self):
        pass
    
    async def generate_resume_tags(self, resume_text):
        """生成简历标签"""
        return ["Python", "FastAPI", "Vue.js", "前端开发", "后端开发"]
    
    async def generate_talent_portrait(self, resume_text):
        """生成人才画像"""
        return "张三是一名有5年经验的全栈开发工程师，精通Python和Vue.js，有丰富的FastAPI开发经验。"
    
    async def calculate_job_match(self, resume_text, job_requirement):
        """计算职位匹配度"""
        return 0.85
    
    async def generate_interview_questions(self, resume_text, job_requirement):
        """生成面试问题"""
        return [
            "请描述您使用FastAPI开发的项目经验",
            "您如何处理Vue.js中的状态管理",
            "您如何确保代码质量和测试覆盖率"
        ]
    
    async def generate_onboarding_tasks(self, candidate_name, position, department):
        """生成入职任务"""
        return [
            {"name": "完成入职文档", "description": "填写并签署所有入职文档"},
            {"name": "参加入职培训", "description": "参加公司文化和技术培训"},
            {"name": "配置开发环境", "description": "安装和配置所需的开发工具和环境"}
        ]
