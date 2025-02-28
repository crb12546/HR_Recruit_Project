import pytest
from fastapi.testclient import TestClient
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview
from app.services.ocr import OCRService
from app.services.gpt import GPTService

@pytest.fixture
def sample_job_requirement(db_session):
    job = JobRequirement(
        position_name="Python高级工程师",
        department="技术部",
        responsibilities="负责后端微服务架构设计和开发",
        requirements="1. 精通Python开发，5年以上经验\n2. 熟悉微服务架构\n3. 具有大型项目经验",
        salary_range="35k-50k",
        location="上海"
    )
    db_session.add(job)
    db_session.commit()
    return job

@pytest.fixture
def sample_resume(db_session):
    resume = Resume(
        candidate_name="李四",
        file_url="https://test-bucket.oss.aliyuncs.com/resumes/senior_dev.pdf",
        file_type="pdf",
        ocr_content="工作经验：8年Python开发\n主导过多个大型微服务项目\n精通分布式系统设计",
    )
    db_session.add(resume)
    db_session.commit()
    return resume

def test_complete_recruitment_flow(
    client,
    mocker,
    sample_job_requirement,
    sample_resume
):
    # 1. 上传并解析简历
    mock_ocr = mocker.patch.object(OCRService, 'extract_text')
    mock_ocr.return_value = sample_resume.ocr_content
    
    mock_gpt = mocker.patch.object(GPTService, 'generate_talent_portrait')
    mock_gpt.return_value = "具有8年Python开发经验的高级工程师，在微服务架构和分布式系统方面有丰富经验"
    
    # 解析简历
    response = client.post(f"/api/v1/resumes/{sample_resume.id}/parse")
    assert response.status_code == 200
    parsed_data = response.json()
    assert "tags" in parsed_data
    assert any(tag["name"] == "Python" for tag in parsed_data["tags"])
    assert any(tag["name"] == "微服务" for tag in parsed_data["tags"])
    
    # 2. 匹配职位
    response = client.get(f"/api/v1/jobs/{sample_job_requirement.id}/matches")
    assert response.status_code == 200
    matches = response.json()["matches"]
    assert len(matches) > 0
    assert any(match["resume_id"] == sample_resume.id for match in matches)
    
    # 3. 安排面试
    interview_data = {
        "resume_id": sample_resume.id,
        "job_requirement_id": sample_job_requirement.id,
        "interviewer_id": 1,  # 假设面试官ID为1
        "interview_time": "2025-03-01T14:00:00"
    }
    response = client.post("/api/v1/interviews", json=interview_data)
    assert response.status_code == 201
    interview = response.json()
    assert interview["status"] == "scheduled"
    
    # 4. 生成面试问题
    response = client.post(f"/api/v1/interviews/{interview['id']}/questions")
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert len(questions) > 0
    assert any("Python" in q["content"] for q in questions)
    assert any("微服务" in q["content"] for q in questions)
    
    # 5. 提交面试反馈
    feedback_data = {
        "score": 4.5,
        "feedback": "技术能力强，项目经验丰富，沟通良好",
        "status": "completed"
    }
    response = client.post(
        f"/api/v1/interviews/{interview['id']}/feedback",
        json=feedback_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_onboarding_flow(
    client,
    mocker,
    sample_job_requirement,
    sample_resume
):
    # 1. 创建入职记录
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
    
    # 模拟GPT服务生成入职任务
    mock_gpt = mocker.patch.object(GPTService, 'generate_onboarding_tasks')
    mock_gpt.return_value = [
        {"name": "完成入职文档", "description": "填写并签署所有入职文档"},
        {"name": "参加入职培训", "description": "参加公司文化和技术培训"},
        {"name": "配置开发环境", "description": "安装和配置所需的开发工具和环境"}
    ]
    
    response = client.post("/api/v1/onboardings", json=onboarding_data)
    assert response.status_code == 201
    onboarding = response.json()
    assert onboarding["status"] == "pending"
    assert len(onboarding["tasks"]) == 3
    
    # 2. 更新入职状态
    update_data = {
        "status": "in_progress",
        "notes": "入职流程已开始"
    }
    
    response = client.put(f"/api/v1/onboardings/{onboarding['id']}", json=update_data)
    assert response.status_code == 200
    updated_onboarding = response.json()
    assert updated_onboarding["status"] == "in_progress"
    
    # 3. 更新任务状态
    task_id = onboarding["tasks"][0]["id"]
    task_update = {
        "status": "completed"
    }
    
    response = client.put(f"/api/v1/onboardings/tasks/{task_id}", json=task_update)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["status"] == "completed"
    assert updated_task["completed_at"] is not None
    
    # 4. 完成入职流程
    final_update = {
        "status": "completed",
        "notes": "入职流程已完成"
    }
    
    response = client.put(f"/api/v1/onboardings/{onboarding['id']}", json=final_update)
    assert response.status_code == 200
    final_onboarding = response.json()
    assert final_onboarding["status"] == "completed"
