import os
import sys
import json
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入需要测试的模块
from app.models.onboarding import Onboarding, OnboardingTask
from app.services.gpt_mock import GPTService

class TestOnboardingModule(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.gpt_service = GPTService()
        
        # 模拟数据
        self.resume_id = 1
        self.job_requirement_id = 1
        self.onboarding_data = {
            "resume_id": self.resume_id,
            "job_requirement_id": self.job_requirement_id,
            "status": "pending",
            "offer_date": datetime.utcnow().isoformat(),
            "start_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "department": "技术部",
            "position": "Python开发工程师",
            "salary": "30k",
            "generate_tasks": True
        }
    
    async def test_generate_onboarding_tasks(self):
        """测试生成入职任务"""
        tasks = await self.gpt_service.generate_onboarding_tasks(
            "张三", 
            "Python开发工程师", 
            "技术部"
        )
        
        # 验证任务生成
        self.assertIsInstance(tasks, list)
        self.assertTrue(len(tasks) > 0)
        self.assertIn("name", tasks[0])
        self.assertIn("description", tasks[0])
    
    def test_onboarding_model(self):
        """测试入职模型"""
        # 创建入职记录
        onboarding = Onboarding(
            resume_id=self.resume_id,
            job_requirement_id=self.job_requirement_id,
            status="pending",
            offer_date=datetime.utcnow(),
            start_date=datetime.utcnow() + timedelta(days=30),
            department="技术部",
            position="Python开发工程师",
            salary="30k"
        )
        
        # 验证入职记录属性
        self.assertEqual(onboarding.resume_id, self.resume_id)
        self.assertEqual(onboarding.job_requirement_id, self.job_requirement_id)
        self.assertEqual(onboarding.status, "pending")
        self.assertEqual(onboarding.department, "技术部")
        self.assertEqual(onboarding.position, "Python开发工程师")
        self.assertEqual(onboarding.salary, "30k")
        
        # 创建入职任务
        task = OnboardingTask(
            onboarding_id=1,
            name="完成入职文档",
            description="填写并签署所有入职文档",
            deadline=datetime.utcnow() + timedelta(days=7),
            status="pending"
        )
        
        # 验证任务属性
        self.assertEqual(task.onboarding_id, 1)
        self.assertEqual(task.name, "完成入职文档")
        self.assertEqual(task.description, "填写并签署所有入职文档")
        self.assertEqual(task.status, "pending")

if __name__ == "__main__":
    unittest.main()
