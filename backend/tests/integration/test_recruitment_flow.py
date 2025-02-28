"""招聘流程集成测试"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch

from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview
from app.models.onboarding import Onboarding, OnboardingTask
from app.models.user import User
from app.models.tag import Tag

from app.routers.resumes import create_resume, get_resume
from app.routers.jobs import create_job_requirement, get_job_requirement
from app.routers.interviews import create_interview, update_interview
from app.routers.onboardings import create_onboarding, update_onboarding

class TestRecruitmentFlow:
    """招聘流程集成测试类"""
    
    @pytest.fixture
    def mock_services(self, monkeypatch):
        """模拟服务"""
        # 模拟OCR服务
        mock_ocr = MagicMock()
        mock_ocr.extract_text.return_value = "姓名：张三\n技能：Python, FastAPI, Vue.js, MySQL, Docker"
        
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.parse_resume.return_value = {"name": "张三", "skills": ["Python", "FastAPI"]}
        mock_gpt.generate_talent_portrait.return_value = "张三是一名Python开发工程师"
        mock_gpt.generate_interview_questions.return_value = ["问题1", "问题2"]
        mock_gpt.match_job_requirements.return_value = {"score": 85, "analysis": "匹配度高"}
        mock_gpt.generate_onboarding_tasks.return_value = [
            {"title": "完成入职文档", "description": "填写文档", "deadline": 1},
            {"title": "参加培训", "description": "参加培训", "deadline": 3}
        ]
        
        # 模拟存储服务
        mock_storage = MagicMock()
        mock_storage.upload_file.return_value = "https://example.com/resume.pdf"
        
        # 打补丁替换服务
        monkeypatch.setattr("app.routers.resumes.get_ocr_service", lambda: mock_ocr)
        monkeypatch.setattr("app.routers.resumes.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.routers.resumes.get_storage_service", lambda: mock_storage)
        monkeypatch.setattr("app.routers.jobs.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.routers.interviews.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.routers.onboardings.get_gpt_service", lambda: mock_gpt)
        
        return {"ocr": mock_ocr, "gpt": mock_gpt, "storage": mock_storage}
    def test_complete_recruitment_flow(self, db: Session, mock_services):
        """测试完整招聘流程"""
        # 步骤1：上传简历
        file_content = b"测试简历内容"
        file_type = "pdf"
        
        resume = create_resume(db=db, file_content=file_content, file_type=file_type)
        assert resume is not None
        assert resume.candidate_name == "张三"
        
        # 步骤2：创建职位需求
        job_data = {
            "position_name": "Python高级工程师",
            "department": "技术部",
            "job_description": "负责后端系统开发和维护",
            "requirements": "5年以上Python开发经验，熟悉FastAPI框架",
            "salary_range": "25k-35k",
            "status": "open"
        }
        
        job = create_job_requirement(db=db, job_data=job_data)
        assert job is not None
        assert job.position_name == "Python高级工程师"
        
        # 步骤3：安排面试
        interviewer = User(username="interviewer", email="test@example.com", role="interviewer")
        db.add(interviewer)
        db.commit()
        
        interview_time = datetime.now() + timedelta(days=1)
        interview_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "interviewer_id": interviewer.id,
            "interview_time": interview_time.isoformat(),
            "interview_type": "技术面试",
            "status": "scheduled"
        }
        
        interview = create_interview(db=db, interview_data=interview_data)
        assert interview is not None
        assert interview.status == "scheduled"
        
        # 步骤4：更新面试结果
        feedback_data = {
            "status": "completed",
            "feedback": "面试表现良好，技术能力符合要求",
            "evaluation_score": 85
        }
        
        updated_interview = update_interview(db=db, interview_id=interview.id, interview_data=feedback_data)
        assert updated_interview is not None
        assert updated_interview.status == "completed"
        assert updated_interview.evaluation_score == 85
        
        # 步骤5：创建入职记录
        start_date = datetime.now() + timedelta(days=14)
        onboarding_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "department": "技术部",
            "position": "Python高级工程师",
            "salary": "30k",
            "offer_date": datetime.now().isoformat(),
            "start_date": start_date.isoformat(),
            "probation_end_date": (start_date + timedelta(days=90)).isoformat(),
            "status": "pending",
            "notes": "优秀候选人，尽快入职",
            "generate_tasks": True
        }
        
        onboarding = create_onboarding(db=db, onboarding_data=onboarding_data)
        assert onboarding is not None
        assert onboarding.status == "pending"
        assert len(onboarding.tasks) >= 2
        
        # 步骤6：更新入职状态
        update_data = {
            "status": "in_progress"
        }
        
        updated_onboarding = update_onboarding(db=db, onboarding_id=onboarding.id, onboarding_data=update_data)
        assert updated_onboarding is not None
        assert updated_onboarding.status == "in_progress"
        
        # 验证整个流程的数据一致性
        final_resume = get_resume(db=db, resume_id=resume.id)
        final_job = get_job_requirement(db=db, job_id=job.id)
        
        assert final_resume.id == resume.id
        assert final_job.id == job.id
        assert updated_interview.resume_id == resume.id
        assert updated_interview.job_requirement_id == job.id
        assert updated_onboarding.resume_id == resume.id
        assert updated_onboarding.job_requirement_id == job.id
