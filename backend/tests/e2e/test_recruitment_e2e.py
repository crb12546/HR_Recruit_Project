"""招聘流程端到端测试"""
import pytest
import json
import os
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db, Base, engine
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview
from app.models.onboarding import Onboarding, OnboardingTask
from app.models.user import User
from app.models.tag import Tag

# 创建测试客户端
client = TestClient(app)

class TestRecruitmentE2E:
    """招聘流程端到端测试类"""
    
    @pytest.fixture(scope="function")
    def setup_test_db(self):
        """设置测试数据库"""
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 创建测试用户
        db = next(get_db())
        admin_user = User(
            username="admin",
            email="admin@example.com",
            role="admin",
            is_active=True
        )
        interviewer = User(
            username="interviewer",
            email="interviewer@example.com",
            role="interviewer",
            is_active=True
        )
        hr_user = User(
            username="hr",
            email="hr@example.com",
            role="hr",
            is_active=True
        )
        
        db.add(admin_user)
        db.add(interviewer)
        db.add(hr_user)
        db.commit()
        
        yield
        
        # 清理数据库
        Base.metadata.drop_all(bind=engine)
    
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
        import app.services.service_factory as factory
        monkeypatch.setattr(factory, "get_ocr_service", lambda: mock_ocr)
        monkeypatch.setattr(factory, "get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr(factory, "get_storage_service", lambda: mock_storage)
        
        return {"ocr": mock_ocr, "gpt": mock_gpt, "storage": mock_storage}
    
    def test_complete_recruitment_workflow(self, setup_test_db, mock_services):
        """测试完整招聘流程"""
        # 步骤1：上传简历
        with open("tests/fixtures/resume_sample.pdf", "rb") as f:
            resume_content = f.read()
        
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", resume_content, "application/pdf")}
        )
        
        assert response.status_code == 200
        resume_data = response.json()
        assert "id" in resume_data
        assert resume_data["candidate_name"] == "张三"
        
        resume_id = resume_data["id"]
        
        # 步骤2：创建职位需求
        job_data = {
            "position_name": "Python高级工程师",
            "department": "技术部",
            "job_description": "负责后端系统开发和维护",
            "requirements": "5年以上Python开发经验，熟悉FastAPI框架",
            "salary_range": "25k-35k",
            "status": "open"
        }
        
        response = client.post(
            "/api/v1/jobs",
            json=job_data
        )
        
        assert response.status_code == 200
        job_data = response.json()
        assert "id" in job_data
        assert job_data["position_name"] == "Python高级工程师"
        
        job_id = job_data["id"]
        
        # 步骤3：匹配简历与职位
        response = client.get(
            f"/api/v1/jobs/{job_id}/match?resume_id={resume_id}"
        )
        
        assert response.status_code == 200
        match_data = response.json()
        assert "score" in match_data
        assert match_data["score"] >= 80
        
        # 步骤4：安排面试
        db = next(get_db())
        interviewer = db.query(User).filter(User.role == "interviewer").first()
        
        interview_time = datetime.now() + timedelta(days=1)
        interview_data = {
            "resume_id": resume_id,
            "job_requirement_id": job_id,
            "interviewer_id": interviewer.id,
            "interview_time": interview_time.isoformat(),
            "interview_type": "技术面试",
            "status": "scheduled"
        }
        
        response = client.post(
            "/api/v1/interviews",
            json=interview_data
        )
        
        assert response.status_code == 200
        interview_data = response.json()
        assert "id" in interview_data
        assert interview_data["status"] == "scheduled"
        
        interview_id = interview_data["id"]
        
        # 步骤5：更新面试结果
        feedback_data = {
            "status": "completed",
            "feedback": "面试表现良好，技术能力符合要求",
            "evaluation_score": 85
        }
        
        response = client.put(
            f"/api/v1/interviews/{interview_id}",
            json=feedback_data
        )
        
        assert response.status_code == 200
        updated_interview = response.json()
        assert updated_interview["status"] == "completed"
        assert updated_interview["evaluation_score"] == 85
        
        # 步骤6：创建入职记录
        start_date = datetime.now() + timedelta(days=14)
        onboarding_data = {
            "resume_id": resume_id,
            "job_requirement_id": job_id,
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
        
        response = client.post(
            "/api/v1/onboardings",
            json=onboarding_data
        )
        
        assert response.status_code == 200
        onboarding_data = response.json()
        assert "id" in onboarding_data
        assert onboarding_data["status"] == "pending"
        
        onboarding_id = onboarding_data["id"]
        
        # 步骤7：获取入职任务列表
        response = client.get(
            f"/api/v1/onboardings/{onboarding_id}/tasks"
        )
        
        assert response.status_code == 200
        tasks_data = response.json()
        assert "tasks" in tasks_data
        assert len(tasks_data["tasks"]) >= 2
        
        # 步骤8：更新入职状态
        update_data = {
            "status": "in_progress"
        }
        
        response = client.put(
            f"/api/v1/onboardings/{onboarding_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        updated_onboarding = response.json()
        assert updated_onboarding["status"] == "in_progress"
        
        # 步骤9：完成入职流程
        complete_data = {
            "status": "completed"
        }
        
        response = client.put(
            f"/api/v1/onboardings/{onboarding_id}",
            json=complete_data
        )
        
        assert response.status_code == 200
        completed_onboarding = response.json()
        assert completed_onboarding["status"] == "completed"
        
        # 验证整个流程的数据一致性
        response = client.get(f"/api/v1/resumes/{resume_id}")
        assert response.status_code == 200
        
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        
        response = client.get(f"/api/v1/interviews/{interview_id}")
        assert response.status_code == 200
        
        response = client.get(f"/api/v1/onboardings/{onboarding_id}")
        assert response.status_code == 200
