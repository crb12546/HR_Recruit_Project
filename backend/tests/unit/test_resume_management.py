"""简历管理模块单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.models.tag import Tag
from app.services.ocr import OCRService
from app.services.gpt import GPTService
from app.services.storage import StorageService
from app.routers.resumes import create_resume, get_resume, get_resumes, update_resume, delete_resume

class TestResumeManagement:
    """简历管理测试类"""
    
    def test_create_resume(self, db: Session, monkeypatch):
        """测试创建简历"""
        # 模拟服务
        mock_ocr = MagicMock()
        mock_ocr.extract_text.return_value = "提取的简历文本"
        
        mock_gpt = MagicMock()
        mock_gpt.parse_resume.return_value = {"name": "张三", "skills": ["Python", "FastAPI"]}
        mock_gpt.generate_talent_portrait.return_value = "人才画像内容"
        
        mock_storage = MagicMock()
        mock_storage.upload_file.return_value = "https://example.com/resume.pdf"
        
        # 打补丁替换服务
        monkeypatch.setattr("app.routers.resumes.get_ocr_service", lambda: mock_ocr)
        monkeypatch.setattr("app.routers.resumes.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.routers.resumes.get_storage_service", lambda: mock_storage)
        
        # 创建测试数据
        file_content = b"测试文件内容"
        file_type = "pdf"
        
        # 调用创建简历函数
        resume = create_resume(db=db, file_content=file_content, file_type=file_type)
        
        # 验证结果
        assert resume is not None
        assert resume.file_type == "pdf"
        assert resume.file_url == "https://example.com/resume.pdf"
        assert resume.ocr_content == "提取的简历文本"
        assert "张三" in resume.parsed_content
        assert resume.talent_portrait == "人才画像内容"
        
        # 验证服务调用
        mock_storage.upload_file.assert_called_once()
        mock_ocr.extract_text.assert_called_once()
        mock_gpt.parse_resume.assert_called_once()
        mock_gpt.generate_talent_portrait.assert_called_once()
    
    def test_get_resume(self, db: Session):
        """测试获取单个简历"""
        # 创建测试数据
        resume = Resume(
            candidate_name="李四",
            file_url="https://example.com/resume2.pdf",
            file_type="pdf",
            ocr_content="简历内容",
            parsed_content="解析后的内容",
            talent_portrait="人才画像"
        )
        db.add(resume)
        db.commit()
        
        # 获取简历
        retrieved_resume = get_resume(db=db, resume_id=resume.id)
        
        # 验证结果
        assert retrieved_resume is not None
        assert retrieved_resume.id == resume.id
        assert retrieved_resume.candidate_name == "李四"
        assert retrieved_resume.file_url == "https://example.com/resume2.pdf"
    
    def test_get_resumes(self, db: Session):
        """测试获取简历列表"""
        # 创建测试数据
        resume1 = Resume(candidate_name="王五", file_url="url1", file_type="pdf")
        resume2 = Resume(candidate_name="赵六", file_url="url2", file_type="docx")
        db.add(resume1)
        db.add(resume2)
        db.commit()
        
        # 获取简历列表
        resumes = get_resumes(db=db, skip=0, limit=10)
        
        # 验证结果
        assert len(resumes) >= 2
        assert any(r.candidate_name == "王五" for r in resumes)
        assert any(r.candidate_name == "赵六" for r in resumes)
    
    def test_update_resume(self, db: Session):
        """测试更新简历"""
        # 创建测试数据
        resume = Resume(
            candidate_name="张三",
            file_url="https://example.com/resume.pdf",
            file_type="pdf",
            ocr_content="原始内容",
            parsed_content="原始解析",
            talent_portrait="原始画像"
        )
        db.add(resume)
        db.commit()
        
        # 更新数据
        updated_data = {
            "candidate_name": "张三(已更新)",
            "talent_portrait": "更新后的人才画像"
        }
        
        # 更新简历
        updated_resume = update_resume(db=db, resume_id=resume.id, resume_data=updated_data)
        
        # 验证结果
        assert updated_resume is not None
        assert updated_resume.candidate_name == "张三(已更新)"
        assert updated_resume.talent_portrait == "更新后的人才画像"
        assert updated_resume.file_url == "https://example.com/resume.pdf"  # 未更新的字段保持不变
    
    def test_delete_resume(self, db: Session):
        """测试删除简历"""
        # 创建测试数据
        resume = Resume(candidate_name="待删除", file_url="url", file_type="pdf")
        db.add(resume)
        db.commit()
        
        resume_id = resume.id
        
        # 删除简历
        result = delete_resume(db=db, resume_id=resume_id)
        
        # 验证结果
        assert result is True
        
        # 确认已删除
        deleted_resume = db.query(Resume).filter(Resume.id == resume_id).first()
        assert deleted_resume is None
    
    def test_resume_tag_relationship(self, db: Session):
        """测试简历与标签的关联关系"""
        # 创建测试数据
        resume = Resume(candidate_name="测试标签", file_url="url", file_type="pdf")
        tag1 = Tag(name="Python")
        tag2 = Tag(name="FastAPI")
        
        # 建立关联
        resume.tags.append(tag1)
        resume.tags.append(tag2)
        
        db.add(resume)
        db.add(tag1)
        db.add(tag2)
        db.commit()
        
        # 获取简历及其标签
        retrieved_resume = db.query(Resume).filter(Resume.id == resume.id).first()
        
        # 验证结果
        assert retrieved_resume is not None
        assert len(retrieved_resume.tags) == 2
        assert any(tag.name == "Python" for tag in retrieved_resume.tags)
        assert any(tag.name == "FastAPI" for tag in retrieved_resume.tags)
        
        # 验证反向关联
        python_tag = db.query(Tag).filter(Tag.name == "Python").first()
        assert any(r.id == resume.id for r in python_tag.resumes)
