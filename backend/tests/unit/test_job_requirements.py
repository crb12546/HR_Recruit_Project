import pytest
from fastapi.testclient import TestClient
from app.models.job_requirement import JobRequirement
from app.services.gpt import GPTService

def test_create_job_requirement(client, mocker):
    # Mock GPT service for tag extraction
    mock_gpt = mocker.patch.object(GPTService, 'extract_job_tags')
    mock_gpt.return_value = ["Python", "FastAPI", "3年经验"]
    
    job_data = {
        "position_name": "Python后端工程师",
        "department": "技术部",
        "responsibilities": "负责后端API开发和维护",
        "requirements": "熟悉Python, FastAPI框架\n3年以上相关开发经验",
        "salary_range": "25k-35k",
        "location": "上海"
    }
    
    response = client.post("/api/v1/jobs", json=job_data)
    assert response.status_code == 201
    data = response.json()
    assert data["position_name"] == "Python后端工程师"
    assert "tags" in data
    assert "Python" in data["tags"]
    assert "FastAPI" in data["tags"]

def test_match_resumes(client, db_session):
    # Create a test job requirement
    job = JobRequirement(
        position_name="Python后端工程师",
        responsibilities="负责后端API开发和维护",
        requirements="熟悉Python, FastAPI框架\n3年以上相关开发经验",
        tags=["Python", "FastAPI", "3年经验"]
    )
    db_session.add(job)
    db_session.commit()
    
    response = client.get(f"/api/v1/jobs/{job.id}/matches")
    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
    assert isinstance(data["matches"], list)
    for match in data["matches"]:
        assert "resume_id" in match
        assert "match_score" in match
        assert "match_explanation" in match
