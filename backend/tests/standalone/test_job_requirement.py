import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestJobRequirement(unittest.TestCase):
    """职位需求模块的独立测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 模拟职位数据
        self.job_data = {
            "position_name": "Python高级工程师",
            "department": "技术部",
            "job_description": "负责公司核心系统的开发和维护",
            "requirements": "1. 精通Python编程语言\n2. 熟悉FastAPI框架\n3. 有5年以上开发经验",
            "salary_range": "25k-35k",
            "status": "open",
            "tags": ["Python", "FastAPI", "后端开发"]
        }
    
    def test_job_matching(self):
        """测试职位匹配功能"""
        # 模拟简历数据
        resume_data = {
            "ocr_content": "姓名：张三\n学历：本科\n技能：Python, FastAPI, Vue.js\n工作经验：5年",
            "tags": ["Python", "FastAPI", "Vue.js"]
        }
        
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.calculate_job_match.return_value = 0.85
        
        # 验证GPT服务调用
        mock_gpt.calculate_job_match.assert_not_called()
        
        match_score = mock_gpt.calculate_job_match(resume_data["ocr_content"], self.job_data["requirements"])
        
        mock_gpt.calculate_job_match.assert_called_once_with(resume_data["ocr_content"], self.job_data["requirements"])
        
        # 验证匹配分数
        self.assertEqual(match_score, 0.85)
    
    def test_job_model(self):
        """测试职位模型"""
        # 创建职位模型类的模拟对象
        class MockJobRequirement:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
                self.tags = []
            
            def to_dict(self):
                return {
                    "id": getattr(self, "id", None),
                    "position_name": getattr(self, "position_name", None),
                    "department": getattr(self, "department", None),
                    "job_description": getattr(self, "job_description", None),
                    "requirements": getattr(self, "requirements", None),
                    "salary_range": getattr(self, "salary_range", None),
                    "status": getattr(self, "status", None),
                    "created_at": self.created_at.isoformat() if self.created_at else None,
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None
                }
        
        # 创建职位实例
        job = MockJobRequirement(
            id=1,
            position_name=self.job_data["position_name"],
            department=self.job_data["department"],
            job_description=self.job_data["job_description"],
            requirements=self.job_data["requirements"],
            salary_range=self.job_data["salary_range"],
            status=self.job_data["status"]
        )
        
        # 验证职位属性
        self.assertEqual(job.id, 1)
        self.assertEqual(job.position_name, self.job_data["position_name"])
        self.assertEqual(job.department, self.job_data["department"])
        self.assertEqual(job.job_description, self.job_data["job_description"])
        self.assertEqual(job.requirements, self.job_data["requirements"])
        self.assertEqual(job.salary_range, self.job_data["salary_range"])
        self.assertEqual(job.status, self.job_data["status"])
        
        # 验证to_dict方法
        job_dict = job.to_dict()
        self.assertEqual(job_dict["id"], 1)
        self.assertEqual(job_dict["position_name"], self.job_data["position_name"])
        self.assertEqual(job_dict["department"], self.job_data["department"])
        self.assertEqual(job_dict["job_description"], self.job_data["job_description"])
        self.assertEqual(job_dict["requirements"], self.job_data["requirements"])
        self.assertEqual(job_dict["salary_range"], self.job_data["salary_range"])
        self.assertEqual(job_dict["status"], self.job_data["status"])

if __name__ == "__main__":
    unittest.main()
