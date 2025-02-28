"""简历与职位匹配集成测试"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.tag import Tag
from app.services.gpt import GPTService
from app.routers.resumes import create_resume
from app.routers.jobs import create_job_requirement
from app.services.matching import match_resume_to_job

class TestResumeJobMatching:
    """简历与职位匹配测试类"""
    
    @pytest.fixture
    def mock_services(self, monkeypatch):
        """模拟服务"""
        # 模拟OCR服务
        mock_ocr = MagicMock()
        mock_ocr.extract_text.return_value = "姓名：李四\n技能：Python, Django, Vue.js, PostgreSQL"
        
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.parse_resume.return_value = {"name": "李四", "skills": ["Python", "Django", "Vue.js"]}
        mock_gpt.generate_talent_portrait.return_value = "李四是一名全栈开发工程师"
        mock_gpt.match_job_requirements.return_value = {
            "score": 75, 
            "analysis": "候选人具备Python和前端开发能力，但缺乏FastAPI经验",
            "matching_points": ["Python开发", "前端开发"],
            "missing_points": ["FastAPI经验"]
        }
        
        # 模拟存储服务
        mock_storage = MagicMock()
        mock_storage.upload_file.return_value = "https://example.com/resume.pdf"
        
        # 打补丁替换服务
        monkeypatch.setattr("app.routers.resumes.get_ocr_service", lambda: mock_ocr)
        monkeypatch.setattr("app.routers.resumes.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.routers.resumes.get_storage_service", lambda: mock_storage)
        monkeypatch.setattr("app.routers.jobs.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.services.matching.get_gpt_service", lambda: mock_gpt)
        
        return {"ocr": mock_ocr, "gpt": mock_gpt, "storage": mock_storage}
    
    def test_resume_job_matching(self, db: Session, mock_services):
        """测试简历与职位匹配"""
        # 创建简历
        file_content = b"测试简历内容"
        file_type = "pdf"
        
        resume = create_resume(db=db, file_content=file_content, file_type=file_type)
        assert resume is not None
        assert resume.candidate_name == "李四"
        
        # 创建职位需求
        job_data = {
            "position_name": "Python后端工程师",
            "department": "技术部",
            "job_description": "负责后端系统开发和维护",
            "requirements": "3年以上Python开发经验，熟悉FastAPI框架",
            "salary_range": "20k-30k",
            "status": "open"
        }
        
        job = create_job_requirement(db=db, job_data=job_data)
        assert job is not None
        assert job.position_name == "Python后端工程师"
        
        # 匹配简历与职位
        match_result = match_resume_to_job(db=db, resume_id=resume.id, job_id=job.id)
        
        # 验证结果
        assert match_result is not None
        assert "score" in match_result
        assert match_result["score"] == 75
        assert "analysis" in match_result
        assert "matching_points" in match_result
        assert "missing_points" in match_result
        assert len(match_result["matching_points"]) >= 1
        assert len(match_result["missing_points"]) >= 1
        
        # 验证GPT服务调用
        mock_services["gpt"].match_job_requirements.assert_called_once()
    
    def test_tag_based_matching(self, db: Session):
        """测试基于标签的匹配"""
        # 创建简历
        resume = Resume(
            candidate_name="王五",
            file_url="https://example.com/resume.pdf",
            file_type="pdf",
            ocr_content="技能：Python, FastAPI, Vue.js",
            parsed_content="解析后的内容",
            talent_portrait="人才画像"
        )
        
        # 创建职位
        job = JobRequirement(
            position_name="全栈工程师",
            department="技术部",
            job_description="负责全栈开发",
            requirements="熟悉Python和前端开发",
            status="open"
        )
        
        # 创建标签
        python_tag = Tag(name="Python")
        fastapi_tag = Tag(name="FastAPI")
        vue_tag = Tag(name="Vue.js")
        
        # 建立关联
        resume.tags.append(python_tag)
        resume.tags.append(fastapi_tag)
        resume.tags.append(vue_tag)
        
        job.tags.append(python_tag)
        job.tags.append(vue_tag)
        
        db.add(resume)
        db.add(job)
        db.add(python_tag)
        db.add(fastapi_tag)
        db.add(vue_tag)
        db.commit()
        
        # 计算标签匹配度
        resume_tags = set(tag.name for tag in resume.tags)
        job_tags = set(tag.name for tag in job.tags)
        
        common_tags = resume_tags.intersection(job_tags)
        match_percentage = len(common_tags) / len(job_tags) * 100 if job_tags else 0
        
        # 验证结果
        assert len(common_tags) == 2
        assert "Python" in common_tags
        assert "Vue.js" in common_tags
        assert match_percentage == 100.0  # 职位要求的所有标签都匹配
