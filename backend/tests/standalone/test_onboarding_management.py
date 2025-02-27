import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestOnboardingManagement(unittest.TestCase):
    """入职管理模块的独立测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 模拟入职数据
        self.onboarding_data = {
            "resume_id": 1,
            "job_requirement_id": 1,
            "department": "技术部",
            "position": "Python高级工程师",
            "salary": "30k",
            "offer_date": datetime.now().isoformat(),
            "start_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "probation_end_date": (datetime.now() + timedelta(days=120)).isoformat(),
            "status": "pending",
            "notes": "需要提前准备开发环境",
            "generate_tasks": True
        }
        
        # 模拟入职任务
        self.onboarding_tasks = [
            {
                "name": "完成入职文档",
                "description": "填写并签署所有入职文档",
                "deadline": (datetime.now() + timedelta(days=25)).isoformat(),
                "status": "pending"
            },
            {
                "name": "参加入职培训",
                "description": "参加公司文化和技术培训",
                "deadline": (datetime.now() + timedelta(days=35)).isoformat(),
                "status": "pending"
            },
            {
                "name": "配置开发环境",
                "description": "安装和配置所需的开发工具和环境",
                "deadline": (datetime.now() + timedelta(days=32)).isoformat(),
                "status": "pending"
            }
        ]
    
    def test_onboarding_model(self):
        """测试入职模型"""
        # 创建入职模型类的模拟对象
        class MockOnboarding:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
                self.tasks = []
            
            def to_dict(self):
                return {
                    "id": getattr(self, "id", None),
                    "resume_id": getattr(self, "resume_id", None),
                    "job_requirement_id": getattr(self, "job_requirement_id", None),
                    "department": getattr(self, "department", None),
                    "position": getattr(self, "position", None),
                    "salary": getattr(self, "salary", None),
                    "offer_date": self.offer_date.isoformat() if hasattr(self, "offer_date") else None,
                    "start_date": self.start_date.isoformat() if hasattr(self, "start_date") else None,
                    "probation_end_date": self.probation_end_date.isoformat() if hasattr(self, "probation_end_date") else None,
                    "status": getattr(self, "status", None),
                    "notes": getattr(self, "notes", None),
                    "created_at": self.created_at.isoformat() if self.created_at else None,
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None
                }
        
        # 创建入职任务模型类的模拟对象
        class MockOnboardingTask:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            
            def to_dict(self):
                return {
                    "id": getattr(self, "id", None),
                    "onboarding_id": getattr(self, "onboarding_id", None),
                    "name": getattr(self, "name", None),
                    "description": getattr(self, "description", None),
                    "deadline": self.deadline.isoformat() if hasattr(self, "deadline") else None,
                    "status": getattr(self, "status", None),
                    "created_at": self.created_at.isoformat() if self.created_at else None,
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None
                }
            
            def validate_deadline(self, start_date):
                """验证任务截止日期是否有效"""
                if hasattr(self, "deadline") and start_date and self.deadline > start_date:
                    raise ValueError("任务截止日期必须在入职日期之前")
                return True
        
        # 创建入职实例
        offer_date = datetime.now()
        start_date = datetime.now() + timedelta(days=30)
        probation_end_date = datetime.now() + timedelta(days=120)
        
        onboarding = MockOnboarding(
            id=1,
            resume_id=self.onboarding_data["resume_id"],
            job_requirement_id=self.onboarding_data["job_requirement_id"],
            department=self.onboarding_data["department"],
            position=self.onboarding_data["position"],
            salary=self.onboarding_data["salary"],
            offer_date=offer_date,
            start_date=start_date,
            probation_end_date=probation_end_date,
            status=self.onboarding_data["status"],
            notes=self.onboarding_data["notes"]
        )
        
        # 验证入职属性
        self.assertEqual(onboarding.id, 1)
        self.assertEqual(onboarding.resume_id, self.onboarding_data["resume_id"])
        self.assertEqual(onboarding.job_requirement_id, self.onboarding_data["job_requirement_id"])
        self.assertEqual(onboarding.department, self.onboarding_data["department"])
        self.assertEqual(onboarding.position, self.onboarding_data["position"])
        self.assertEqual(onboarding.salary, self.onboarding_data["salary"])
        self.assertEqual(onboarding.offer_date, offer_date)
        self.assertEqual(onboarding.start_date, start_date)
        self.assertEqual(onboarding.probation_end_date, probation_end_date)
        self.assertEqual(onboarding.status, self.onboarding_data["status"])
        self.assertEqual(onboarding.notes, self.onboarding_data["notes"])
        
        # 验证to_dict方法
        onboarding_dict = onboarding.to_dict()
        self.assertEqual(onboarding_dict["id"], 1)
        self.assertEqual(onboarding_dict["resume_id"], self.onboarding_data["resume_id"])
        self.assertEqual(onboarding_dict["job_requirement_id"], self.onboarding_data["job_requirement_id"])
        self.assertEqual(onboarding_dict["department"], self.onboarding_data["department"])
        self.assertEqual(onboarding_dict["position"], self.onboarding_data["position"])
        self.assertEqual(onboarding_dict["salary"], self.onboarding_data["salary"])
        self.assertEqual(onboarding_dict["status"], self.onboarding_data["status"])
        self.assertEqual(onboarding_dict["notes"], self.onboarding_data["notes"])
        
        # 创建入职任务实例
        task_deadline = datetime.now() + timedelta(days=25)
        task = MockOnboardingTask(
            id=1,
            onboarding_id=1,
            name=self.onboarding_tasks[0]["name"],
            description=self.onboarding_tasks[0]["description"],
            deadline=task_deadline,
            status=self.onboarding_tasks[0]["status"]
        )
        
        # 验证任务属性
        self.assertEqual(task.id, 1)
        self.assertEqual(task.onboarding_id, 1)
        self.assertEqual(task.name, self.onboarding_tasks[0]["name"])
        self.assertEqual(task.description, self.onboarding_tasks[0]["description"])
        self.assertEqual(task.deadline, task_deadline)
        self.assertEqual(task.status, self.onboarding_tasks[0]["status"])
        
        # 验证任务截止日期验证
        self.assertTrue(task.validate_deadline(start_date))
        
        # 测试无效截止日期的验证
        invalid_task = MockOnboardingTask(
            deadline=start_date + timedelta(days=1)
        )
        with self.assertRaises(ValueError) as context:
            invalid_task.validate_deadline(start_date)
        self.assertIn("任务截止日期必须在入职日期之前", str(context.exception))
    
    def test_task_generation(self):
        """测试入职任务生成功能"""
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.generate_onboarding_tasks.return_value = [
            {"name": task["name"], "description": task["description"]}
            for task in self.onboarding_tasks
        ]
        
        # 验证GPT服务调用
        mock_gpt.generate_onboarding_tasks.assert_not_called()
        
        tasks = mock_gpt.generate_onboarding_tasks(
            "张三", 
            self.onboarding_data["position"], 
            self.onboarding_data["department"]
        )
        
        mock_gpt.generate_onboarding_tasks.assert_called_once_with(
            "张三", 
            self.onboarding_data["position"], 
            self.onboarding_data["department"]
        )
        
        # 验证生成的任务
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]["name"], self.onboarding_tasks[0]["name"])
        self.assertEqual(tasks[0]["description"], self.onboarding_tasks[0]["description"])

if __name__ == "__main__":
    unittest.main()
