import pytest
from fastapi.testclient import TestClient
from app.models.resume import Resume
from app.services.ocr import OCRService
from app.services.gpt import GPTService

def test_resume_upload(client, mocker):
    # Mock OCR service
    mock_ocr = mocker.patch.object(OCRService, 'extract_text')
    mock_ocr.return_value = "工作经验：5年\n技能：Python, FastAPI\n教育背景：计算机科学学士"
    
    # Mock GPT service
    mock_gpt = mocker.patch.object(GPTService, 'generate_talent_portrait')
    mock_gpt.return_value = "具有5年Python开发经验的后端工程师，擅长FastAPI框架"
    
    # Test file upload
    with open('tests/fixtures/test_resume.txt', 'rb') as f:
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("test_resume.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "talent_portrait" in data
    assert data["talent_portrait"] == "具有5年Python开发经验的后端工程师，擅长FastAPI框架"

def test_resume_parse(client, db_session, mocker):
    # Create a test resume
    resume = Resume(
        candidate_name="张三",
        file_url="https://test-bucket.oss.aliyuncs.com/resumes/test.pdf",
        file_type="pdf",
        ocr_content="工作经验：5年\n技能：Python, FastAPI",
    )
    db_session.add(resume)
    db_session.commit()
    
    # Mock GPT service
    mock_gpt = mocker.patch.object(GPTService, 'extract_resume_tags')
    mock_gpt.return_value = [{"name": "Python"}, {"name": "FastAPI"}]

    response = client.post(f"/api/v1/resumes/{resume.id}/parse")
    assert response.status_code == 200
    data = response.json()
    assert "tags" in data
    assert any(tag["name"] == "Python" for tag in data["tags"])
    assert any(tag["name"] == "FastAPI" for tag in data["tags"])
