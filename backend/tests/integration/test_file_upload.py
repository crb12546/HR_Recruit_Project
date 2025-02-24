"""集成测试：文件上传功能"""
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.services.storage import StorageService
from app.services.ocr import OCRService
from app.services.gpt import GPTService
from app.services.tag import TagService

pytestmark = pytest.mark.asyncio

def test_resume_upload_integration(client: TestClient, mocker):
    """测试简历上传集成流程"""
    os.environ["ENV"] = "test"
    
    # Mock storage service
    mock_storage = mocker.patch.object(StorageService, 'upload_file')
    mock_storage.return_value = "https://test-bucket.oss.aliyuncs.com/resumes/test.pdf"
    
    # Mock OCR service
    mock_ocr = mocker.patch.object(OCRService, 'extract_text')
    mock_ocr.return_value = "测试简历内容：\n张三，5年Python开发经验，精通FastAPI和Vue.js"
    
    # Mock GPT service
    mock_gpt_portrait = mocker.patch.object(GPTService, 'generate_talent_portrait')
    mock_gpt_portrait.return_value = "资深全栈工程师，在Python后端和Vue.js前端开发方面都有丰富经验"
    
    mock_gpt_name = mocker.patch.object(GPTService, 'extract_candidate_name')
    mock_gpt_name.return_value = "张三"
    
    # Mock tag service
    mock_tag = mocker.patch.object(TagService, 'generate_resume_tags')
    mock_tag.return_value = [
        {"id": 1, "name": "Python"},
        {"id": 2, "name": "FastAPI"},
        {"id": 3, "name": "Vue.js"}
    ]
    
    # 测试文件上传
    with open('tests/fixtures/resumes/fullstack_expert.pdf', 'rb') as f:
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    
    # 验证文件URL
    assert "file_url" in data
    assert data["file_url"].startswith("https://")
    assert data["file_url"].endswith(".pdf")
    
    # 验证简历内容
    assert data["ocr_content"] == "测试简历内容：\n张三，5年Python开发经验，精通FastAPI和Vue.js"
    assert data["talent_portrait"] == "资深全栈工程师，在Python后端和Vue.js前端开发方面都有丰富经验"
    assert data["candidate_name"] == "张三"
    
    # 验证标签
    assert len(data["tags"]) == 3
    assert data["tags"][0]["name"] == "Python"
    assert data["tags"][1]["name"] == "FastAPI"
    assert data["tags"][2]["name"] == "Vue.js"
    
    # 验证服务调用
    mock_storage.assert_called_once()
    mock_ocr.assert_called_once()
    mock_gpt_portrait.assert_called_once()
    mock_gpt_name.assert_called_once()
    mock_tag.assert_called_once()
