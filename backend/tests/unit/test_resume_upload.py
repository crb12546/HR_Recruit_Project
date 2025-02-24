"""测试简历上传功能"""
import os
from unittest.mock import MagicMock, patch
import pytest
from app.services.ocr import OCRService
from app.routers.resumes import upload_resume

@pytest.fixture
def mock_file():
    """Mock file fixture"""
    mock = MagicMock()
    mock.filename = "test.pdf"
    mock.content_type = "application/pdf"
    return mock

@pytest.fixture
def mock_db():
    """Mock database fixture"""
    return MagicMock()

async def test_upload_resume_success(mock_file, mock_db, mocker):
    """Test successful resume upload"""
    os.environ["ENV"] = "test"

    # Mock file content
    mock_file.read.return_value = b"test content"

    # Mock services
    with patch('app.services.storage.StorageService') as MockStorage, \
         patch('app.services.mock_storage.MockStorageService') as MockStorageService, \
         patch('app.services.mock_ocr.MockOCRService') as MockOCRService, \
         patch('app.services.ocr.OCRService') as MockOCR, \
         patch('app.services.gpt.GPTService') as MockGPT, \
         patch('app.routers.resumes.TagService') as MockTag, \
         patch('app.routers.resumes.Resume') as MockResume:

        # Configure mock services
        mock_storage = MockStorage.return_value
        mock_storage_service = MockStorageService.return_value
        mock_storage_service.upload_file = MagicMock()
        mock_storage_service.upload_file.return_value = "https://test-bucket.oss-cn-hangzhou.aliyuncs.com/resumes/test.pdf"
        mock_storage.service = mock_storage_service

        mock_ocr = MockOCR.return_value
        mock_ocr_service = MockOCRService.return_value
        mock_ocr_service.extract_text = MagicMock()
        mock_ocr_service.extract_text.return_value = "测试简历内容"
        mock_ocr.service = mock_ocr_service

        # Mock GPT service
        mock_gpt = MockGPT.return_value
        mock_gpt.generate_talent_portrait = MagicMock(return_value="具有5年Python开发经验的后端工程师，擅长FastAPI框架")
        mock_gpt.extract_candidate_name = MagicMock(return_value="张三")

        # Mock tag service
        mock_tag = MockTag.return_value
        mock_tag.generate_resume_tags = MagicMock()
        mock_tag.generate_resume_tags.return_value = [
            {"name": "Python", "category": "技能"},
            {"name": "FastAPI", "category": "技能"},
            {"name": "5年", "category": "经验"}
        ]

        # Mock resume object
        mock_resume = MagicMock()
        mock_resume.id = 1
        mock_resume.file_url = "https://test-bucket.oss-cn-hangzhou.aliyuncs.com/resumes/test.pdf"
        mock_resume.file_type = "pdf"
        mock_resume.talent_portrait = "具有5年Python开发经验的后端工程师，擅长FastAPI框架"
        mock_resume.candidate_name = "张三"
        mock_resume.ocr_content = "测试简历内容"
        mock_resume.tags = []  # Tags will be added by the route handler in test env
        MockResume.return_value = mock_resume

        # Mock database operations
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh.return_value = mock_resume

        # Execute upload
        result = await upload_resume(mock_file, mock_db)

        # Verify result
        assert result["file_url"].startswith("https://")
        assert "test.pdf" in result["file_url"]
        assert result["file_type"] == "pdf"
        assert result["talent_portrait"] == "具有5年Python开发经验的后端工程师，擅长FastAPI框架"
        assert result["candidate_name"] == "张三"
        assert result["ocr_content"] == "测试简历内容"
        assert len(result["tags"]) == 3

async def test_upload_resume_error(mock_file, mock_db):
    """Test resume upload with error"""
    os.environ["ENV"] = "test"

    # Mock file read error
    mock_file.read.side_effect = Exception("文件读取失败")

    with pytest.raises(Exception) as exc:
        await upload_resume(mock_file, mock_db)
    assert "文件读取失败" in str(exc.value)
