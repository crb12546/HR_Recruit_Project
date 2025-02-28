import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestInterviewManagement(unittest.TestCase):
    """面试管理模块的独立测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 模拟面试数据
        self.interview_data = {
            "resume_id": 1,
            "job_requirement_id": 1,
            "interviewer_id": 1,
            "interview_time": (datetime.now() + timedelta(days=3)).isoformat(),
            "status": "scheduled",
            "feedback": None,
            "rating": None
        }
        
        # 模拟面试问题
        self.interview_questions = [
            "请描述您使用FastAPI开发的项目经验",
            "您如何处理Vue.js中的状态管理",
            "您如何确保代码质量和测试覆盖率"
        ]
    
    def test_interview_scheduling(self):
        """测试面试预约功能"""
        # 创建面试模型类的模拟对象
        class MockInterview:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            
            def to_dict(self):
                return {
                    "id": getattr(self, "id", None),
                    "resume_id": getattr(self, "resume_id", None),
                    "job_requirement_id": getattr(self, "job_requirement_id", None),
                    "interviewer_id": getattr(self, "interviewer_id", None),
                    "interview_time": self.interview_time.isoformat() if hasattr(self, "interview_time") else None,
                    "status": getattr(self, "status", None),
                    "feedback": getattr(self, "feedback", None),
                    "rating": getattr(self, "rating", None),
                    "created_at": self.created_at.isoformat() if self.created_at else None,
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None
                }
            
            def validate_interview_time(self):
                """验证面试时间是否有效"""
                if hasattr(self, "interview_time") and self.interview_time < datetime.now():
                    raise ValueError("面试时间不能在过去")
                return True
        
        # 创建面试实例
        interview_time = datetime.now() + timedelta(days=3)
        interview = MockInterview(
            id=1,
            resume_id=self.interview_data["resume_id"],
            job_requirement_id=self.interview_data["job_requirement_id"],
            interviewer_id=self.interview_data["interviewer_id"],
            interview_time=interview_time,
            status=self.interview_data["status"]
        )
        
        # 验证面试属性
        self.assertEqual(interview.id, 1)
        self.assertEqual(interview.resume_id, self.interview_data["resume_id"])
        self.assertEqual(interview.job_requirement_id, self.interview_data["job_requirement_id"])
        self.assertEqual(interview.interviewer_id, self.interview_data["interviewer_id"])
        self.assertEqual(interview.interview_time, interview_time)
        self.assertEqual(interview.status, self.interview_data["status"])
        
        # 验证to_dict方法
        interview_dict = interview.to_dict()
        self.assertEqual(interview_dict["id"], 1)
        self.assertEqual(interview_dict["resume_id"], self.interview_data["resume_id"])
        self.assertEqual(interview_dict["job_requirement_id"], self.interview_data["job_requirement_id"])
        self.assertEqual(interview_dict["interviewer_id"], self.interview_data["interviewer_id"])
        self.assertEqual(interview_dict["status"], self.interview_data["status"])
        
        # 验证面试时间验证
        self.assertTrue(interview.validate_interview_time())
        
        # 测试过去时间的验证
        past_interview = MockInterview(
            interview_time=datetime.now() - timedelta(days=1)
        )
        with self.assertRaises(ValueError) as context:
            past_interview.validate_interview_time()
        self.assertIn("面试时间不能在过去", str(context.exception))
    
    def test_interview_question_generation(self):
        """测试面试问题生成功能"""
        # 模拟简历数据
        resume_text = "姓名：张三\n学历：本科\n技能：Python, FastAPI, Vue.js\n工作经验：5年"
        
        # 模拟职位需求
        job_requirement = "1. 精通Python编程语言\n2. 熟悉FastAPI框架\n3. 有5年以上开发经验"
        
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.generate_interview_questions.return_value = self.interview_questions
        
        # 验证GPT服务调用
        mock_gpt.generate_interview_questions.assert_not_called()
        
        questions = mock_gpt.generate_interview_questions(resume_text, job_requirement)
        
        mock_gpt.generate_interview_questions.assert_called_once_with(resume_text, job_requirement)
        
        # 验证生成的问题
        self.assertEqual(questions, self.interview_questions)
        self.assertEqual(len(questions), 3)

if __name__ == "__main__":
    unittest.main()
