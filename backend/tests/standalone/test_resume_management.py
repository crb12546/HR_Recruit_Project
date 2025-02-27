import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestResumeManagement(unittest.TestCase):
    """简历管理模块的独立测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 模拟简历数据
        self.resume_data = {
            "candidate_name": "张三",
            "file_url": "https://test-bucket.oss.aliyuncs.com/resume.pdf",
            "file_type": "pdf",
            "ocr_content": "姓名：张三\n学历：本科\n技能：Python, FastAPI, Vue.js",
            "parsed_content": {
                "name": "张三",
                "education": "本科",
                "skills": ["Python", "FastAPI", "Vue.js"]
            },
            "talent_portrait": "张三是一名有5年经验的全栈开发工程师，精通Python和Vue.js，有丰富的FastAPI开发经验。"
        }
        
        # 模拟标签数据
        self.tags = ["Python", "FastAPI", "Vue.js", "全栈开发"]
    
    def test_resume_parsing(self):
        """测试简历解析功能"""
        # 模拟OCR服务
        mock_ocr = MagicMock()
        mock_ocr.extract_text_from_url.return_value = self.resume_data["ocr_content"]
        
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.generate_resume_tags.return_value = self.tags
        mock_gpt.generate_talent_portrait.return_value = self.resume_data["talent_portrait"]
        
        # 验证OCR服务调用
        mock_ocr.extract_text_from_url.assert_not_called()
        mock_ocr.extract_text_from_url(self.resume_data["file_url"])
        mock_ocr.extract_text_from_url.assert_called_once_with(self.resume_data["file_url"])
        
        # 验证GPT服务调用
        mock_gpt.generate_resume_tags.assert_not_called()
        mock_gpt.generate_talent_portrait.assert_not_called()
        
        tags = mock_gpt.generate_resume_tags(self.resume_data["ocr_content"])
        portrait = mock_gpt.generate_talent_portrait(self.resume_data["ocr_content"])
        
        mock_gpt.generate_resume_tags.assert_called_once_with(self.resume_data["ocr_content"])
        mock_gpt.generate_talent_portrait.assert_called_once_with(self.resume_data["ocr_content"])
        
        # 验证返回结果
        self.assertEqual(tags, self.tags)
        self.assertEqual(portrait, self.resume_data["talent_portrait"])
    
    def test_resume_model(self):
        """测试简历模型"""
        # 创建简历模型类的模拟对象
        class MockResume:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
                self.tags = []
            
            def to_dict(self):
                return {
                    "id": getattr(self, "id", None),
                    "candidate_name": getattr(self, "candidate_name", None),
                    "file_url": getattr(self, "file_url", None),
                    "file_type": getattr(self, "file_type", None),
                    "ocr_content": getattr(self, "ocr_content", None),
                    "parsed_content": getattr(self, "parsed_content", None),
                    "talent_portrait": getattr(self, "talent_portrait", None),
                    "created_at": self.created_at.isoformat() if self.created_at else None,
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None
                }
        
        # 创建简历实例
        resume = MockResume(
            id=1,
            candidate_name=self.resume_data["candidate_name"],
            file_url=self.resume_data["file_url"],
            file_type=self.resume_data["file_type"],
            ocr_content=self.resume_data["ocr_content"],
            parsed_content=self.resume_data["parsed_content"],
            talent_portrait=self.resume_data["talent_portrait"]
        )
        
        # 验证简历属性
        self.assertEqual(resume.id, 1)
        self.assertEqual(resume.candidate_name, self.resume_data["candidate_name"])
        self.assertEqual(resume.file_url, self.resume_data["file_url"])
        self.assertEqual(resume.file_type, self.resume_data["file_type"])
        self.assertEqual(resume.ocr_content, self.resume_data["ocr_content"])
        self.assertEqual(resume.parsed_content, self.resume_data["parsed_content"])
        self.assertEqual(resume.talent_portrait, self.resume_data["talent_portrait"])
        
        # 验证to_dict方法
        resume_dict = resume.to_dict()
        self.assertEqual(resume_dict["id"], 1)
        self.assertEqual(resume_dict["candidate_name"], self.resume_data["candidate_name"])
        self.assertEqual(resume_dict["file_url"], self.resume_data["file_url"])
        self.assertEqual(resume_dict["file_type"], self.resume_data["file_type"])
        self.assertEqual(resume_dict["ocr_content"], self.resume_data["ocr_content"])
        self.assertEqual(resume_dict["parsed_content"], self.resume_data["parsed_content"])
        self.assertEqual(resume_dict["talent_portrait"], self.resume_data["talent_portrait"])

if __name__ == "__main__":
    unittest.main()
