import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.models.onboarding import Onboarding, OnboardingTask
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement

@pytest.fixture
def sample_resume(db_session):
    resume = Resume(
        candidate_name="张三",
        file_url="https://test-bucket.oss.aliyuncs.com/resumes/test_resume.pdf",
        file_type="pdf",
        ocr_content="工作经验：5年Python开发\n熟悉FastAPI和Vue.js",
    )
    db_session.add(resume)
    db_session.commit()
    return resume

@pytest.fixture
def sample_job_requirement(db_session):
    job = JobRequirement(
        position_name="Python开发工程师",
        department="技术部",
        responsibilities="负责后端API开发",
        requirements="熟悉Python、FastAPI",
        salary_range="25k-35k",
        location="北京"
    )
    db_session.add(job)
    db_session.commit()
    return job

@pytest.fixture
def sample_onboarding(db_session, sample_resume, sample_job_requirement):
    onboarding = Onboarding(
        resume_id=sample_resume.id,
        job_requirement_id=sample_job_requirement.id,
        status="pending",
        offer_date=datetime.utcnow(),
        start_date=datetime.utcnow() + timedelta(days=30),
        department="技术部",
        position="Python开发工程师",
        salary="30k"
    )
    db_session.add(onboarding)
    db_session.commit()
    return onboarding

def test_create_onboarding(client, sample_resume, sample_job_requirement):
    onboarding_data = {
        "resume_id": sample_resume.id,
        "job_requirement_id": sample_job_requirement.id,
        "status": "pending",
        "offer_date": datetime.utcnow().isoformat(),
        "start_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "department": "技术部",
        "position": "Python开发工程师",
        "salary": "30k",
        "generate_tasks": True
    }
    
    response = client.post("/api/v1/onboardings", json=onboarding_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["department"] == "技术部"
    assert "tasks" in data
    assert len(data["tasks"]) > 0

def test_get_onboarding(client, sample_onboarding):
    response = client.get(f"/api/v1/onboardings/{sample_onboarding.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_onboarding.id
    assert data["status"] == sample_onboarding.status
    assert data["department"] == sample_onboarding.department

def test_update_onboarding(client, sample_onboarding):
    update_data = {
        "status": "in_progress",
        "notes": "入职流程已开始"
    }
    
    response = client.put(f"/api/v1/onboardings/{sample_onboarding.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["notes"] == "入职流程已开始"

def test_add_onboarding_task(client, sample_onboarding):
    task_data = {
        "name": "完成入职文档",
        "description": "填写并签署所有入职文档",
        "deadline": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "status": "pending"
    }
    
    response = client.post(f"/api/v1/onboardings/{sample_onboarding.id}/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "完成入职文档"
    assert data["status"] == "pending"

def test_update_task_status(client, sample_onboarding, db_session):
    # 创建一个任务
    task = OnboardingTask(
        onboarding_id=sample_onboarding.id,
        name="完成入职文档",
        description="填写并签署所有入职文档",
        deadline=datetime.utcnow() + timedelta(days=7),
        status="pending"
    )
    db_session.add(task)
    db_session.commit()
    
    update_data = {
        "status": "completed"
    }
    
    response = client.put(f"/api/v1/onboardings/tasks/{task.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None
