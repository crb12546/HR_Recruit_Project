"""API端点端到端测试"""
import pytest
import json
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db, Base, engine
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview
from app.models.onboarding import Onboarding
from app.models.user import User
from app.models.tag import Tag

# 创建测试客户端
client = TestClient(app)

class TestAPIEndpoints:
    """API端点测试类"""
    
    @pytest.fixture(scope="function")
    def setup_test_db(self):
        """设置测试数据库"""
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 创建测试数据
        db = next(get_db())
        
        # 创建简历
        resume1 = Resume(
            candidate_name="张三",
            file_url="https://example.com/resume1.pdf",
            file_type="pdf",
            ocr_content="简历内容1",
            parsed_content="解析内容1",
            talent_portrait="人才画像1"
        )
        resume2 = Resume(
            candidate_name="李四",
            file_url="https://example.com/resume2.pdf",
            file_type="pdf",
            ocr_content="简历内容2",
            parsed_content="解析内容2",
            talent_portrait="人才画像2"
        )
        
        # 创建职位
        job1 = JobRequirement(
            position_name="Python工程师",
            department="技术部",
            job_description="职位描述1",
            requirements="职位要求1",
            salary_range="20k-30k",
            status="open"
        )
        job2 = JobRequirement(
            position_name="前端工程师",
            department="技术部",
            job_description="职位描述2",
            requirements="职位要求2",
            salary_range="15k-25k",
            status="open"
        )
        
        # 创建用户
        user1 = User(
            username="admin",
            email="admin@example.com",
            role="admin",
            is_active=True
        )
        user2 = User(
            username="interviewer",
            email="interviewer@example.com",
            role="interviewer",
            is_active=True
        )
        
        db.add(resume1)
        db.add(resume2)
        db.add(job1)
        db.add(job2)
        db.add(user1)
        db.add(user2)
        db.commit()
        
        yield
        
        # 清理数据库
        Base.metadata.drop_all(bind=engine)
    
    def test_health_check(self):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_resume_endpoints(self, setup_test_db):
        """测试简历相关端点"""
        # 获取简历列表
        response = client.get("/api/v1/resumes")
        assert response.status_code == 200
        data = response.json()
        assert "resumes" in data
        assert len(data["resumes"]) >= 2
        
        # 获取单个简历
        resume_id = data["resumes"][0]["id"]
        response = client.get(f"/api/v1/resumes/{resume_id}")
        assert response.status_code == 200
        resume_data = response.json()
        assert resume_data["id"] == resume_id
        
        # 更新简历
        update_data = {
            "candidate_name": "张三(已更新)",
            "talent_portrait": "更新后的人才画像"
        }
        response = client.put(f"/api/v1/resumes/{resume_id}", json=update_data)
        assert response.status_code == 200
        updated_resume = response.json()
        assert updated_resume["candidate_name"] == "张三(已更新)"
        
        # 删除简历
        response = client.delete(f"/api/v1/resumes/{resume_id}")
        assert response.status_code == 200
        assert response.json() == {"success": True}
        
        # 确认已删除
        response = client.get(f"/api/v1/resumes/{resume_id}")
        assert response.status_code == 404
    
    def test_job_endpoints(self, setup_test_db):
        """测试职位相关端点"""
        # 获取职位列表
        response = client.get("/api/v1/jobs")
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert len(data["jobs"]) >= 2
        
        # 获取单个职位
        job_id = data["jobs"][0]["id"]
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        job_data = response.json()
        assert job_data["id"] == job_id
        
        # 更新职位
        update_data = {
            "position_name": "高级Python工程师",
            "status": "closed"
        }
        response = client.put(f"/api/v1/jobs/{job_id}", json=update_data)
        assert response.status_code == 200
        updated_job = response.json()
        assert updated_job["position_name"] == "高级Python工程师"
        assert updated_job["status"] == "closed"
        
        # 删除职位
        response = client.delete(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        assert response.json() == {"success": True}
        
        # 确认已删除
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 404
    
    def test_interview_endpoints(self, setup_test_db):
        """测试面试相关端点"""
        # 获取数据库中的简历和职位
        db = next(get_db())
        resume = db.query(Resume).first()
        job = db.query(JobRequirement).first()
        user = db.query(User).filter(User.role == "interviewer").first()
        
        # 创建面试
        from datetime import datetime, timedelta
        interview_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "interviewer_id": user.id,
            "interview_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "interview_type": "技术面试",
            "status": "scheduled"
        }
        
        response = client.post("/api/v1/interviews", json=interview_data)
        assert response.status_code == 200
        created_interview = response.json()
        assert "id" in created_interview
        assert created_interview["status"] == "scheduled"
        
        interview_id = created_interview["id"]
        
        # 获取面试列表
        response = client.get("/api/v1/interviews")
        assert response.status_code == 200
        data = response.json()
        assert "interviews" in data
        assert len(data["interviews"]) >= 1
        
        # 获取单个面试
        response = client.get(f"/api/v1/interviews/{interview_id}")
        assert response.status_code == 200
        interview_data = response.json()
        assert interview_data["id"] == interview_id
        
        # 更新面试
        update_data = {
            "status": "completed",
            "feedback": "面试表现良好",
            "evaluation_score": 85
        }
        response = client.put(f"/api/v1/interviews/{interview_id}", json=update_data)
        assert response.status_code == 200
        updated_interview = response.json()
        assert updated_interview["status"] == "completed"
        assert updated_interview["evaluation_score"] == 85
        
        # 删除面试
        response = client.delete(f"/api/v1/interviews/{interview_id}")
        assert response.status_code == 200
        assert response.json() == {"success": True}
        
        # 确认已删除
        response = client.get(f"/api/v1/interviews/{interview_id}")
        assert response.status_code == 404
    
    def test_onboarding_endpoints(self, setup_test_db):
        """测试入职相关端点"""
        # 获取数据库中的简历和职位
        db = next(get_db())
        resume = db.query(Resume).first()
        job = db.query(JobRequirement).first()
        
        # 创建入职记录
        from datetime import datetime, timedelta
        start_date = datetime.now() + timedelta(days=14)
        onboarding_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "department": "技术部",
            "position": "Python工程师",
            "salary": "25k",
            "offer_date": datetime.now().isoformat(),
            "start_date": start_date.isoformat(),
            "probation_end_date": (start_date + timedelta(days=90)).isoformat(),
            "status": "pending",
            "generate_tasks": True
        }
        
        response = client.post("/api/v1/onboardings", json=onboarding_data)
        assert response.status_code == 200
        created_onboarding = response.json()
        assert "id" in created_onboarding
        assert created_onboarding["status"] == "pending"
        
        onboarding_id = created_onboarding["id"]
        
        # 获取入职记录列表
        response = client.get("/api/v1/onboardings")
        assert response.status_code == 200
        data = response.json()
        assert "onboardings" in data
        assert len(data["onboardings"]) >= 1
        
        # 获取单个入职记录
        response = client.get(f"/api/v1/onboardings/{onboarding_id}")
        assert response.status_code == 200
        onboarding_data = response.json()
        assert onboarding_data["id"] == onboarding_id
        
        # 更新入职记录
        update_data = {
            "status": "in_progress",
            "notes": "已完成入职准备"
        }
        response = client.put(f"/api/v1/onboardings/{onboarding_id}", json=update_data)
        assert response.status_code == 200
        updated_onboarding = response.json()
        assert updated_onboarding["status"] == "in_progress"
        assert updated_onboarding["notes"] == "已完成入职准备"
        
        # 获取入职任务
        response = client.get(f"/api/v1/onboardings/{onboarding_id}/tasks")
        assert response.status_code == 200
        tasks_data = response.json()
        assert "tasks" in tasks_data
        
        # 删除入职记录
        response = client.delete(f"/api/v1/onboardings/{onboarding_id}")
        assert response.status_code == 200
        assert response.json() == {"success": True}
        
        # 确认已删除
        response = client.get(f"/api/v1/onboardings/{onboarding_id}")
        assert response.status_code == 404
