"""Test storage service implementation"""
import os
import pytest
from app.services.storage import StorageService

def test_storage_service_test_env():
    """Test storage service in test environment"""
    os.environ["ENV"] = "test"
    service = StorageService()
    
    # Test file upload in test environment
    file_content = b"test content"
    file_name = "test.pdf"
    url = service.upload_file(file_content, f"resumes/{file_name}")
    
    assert url.startswith("https://")
    assert "test-bucket" in url
    assert "resumes/test.pdf" in url

def test_storage_service_prod_env(mocker):
    """Test storage service in production environment"""
    os.environ["ENV"] = "production"
    os.environ["ALIYUN_ACCESS_KEY_ID"] = "test_key"
    os.environ["ALIYUN_ACCESS_KEY_SECRET"] = "test_secret"
    os.environ["ALIYUN_OSS_BUCKET"] = "hr-recruit-prod"
    os.environ["ALIYUN_OSS_ENDPOINT"] = "https://oss-cn-hangzhou.aliyuncs.com"
    
    # Mock oss2.Auth and oss2.Bucket
    mock_auth = mocker.patch("oss2.Auth")
    mock_bucket = mocker.patch("oss2.Bucket")
    mock_bucket.return_value.put_object.return_value.status = 200
    mock_bucket.return_value.bucket_name = "hr-recruit-prod"
    mock_bucket.return_value.endpoint = "oss-cn-hangzhou.aliyuncs.com"
    
    service = StorageService()
    
    # Test file upload in production environment
    file_content = b"test content"
    file_name = "test.pdf"
    url = service.upload_file(file_content, f"resumes/{file_name}")
    
    assert url.startswith("https://")
    assert "hr-recruit-prod" in url
    assert "resumes/test.pdf" in url
    mock_bucket.return_value.put_object.assert_called_once()

def test_storage_service_upload_error(mocker):
    """Test storage service error handling"""
    os.environ["ENV"] = "production"
    os.environ["ALIYUN_ACCESS_KEY_ID"] = "test_key"
    os.environ["ALIYUN_ACCESS_KEY_SECRET"] = "test_secret"
    os.environ["ALIYUN_OSS_BUCKET"] = "hr-recruit-prod"
    os.environ["ALIYUN_OSS_ENDPOINT"] = "https://oss-cn-hangzhou.aliyuncs.com"
    
    # Mock oss2.Auth and oss2.Bucket with error
    mock_auth = mocker.patch("oss2.Auth")
    mock_bucket = mocker.patch("oss2.Bucket")
    mock_bucket.return_value.put_object.side_effect = Exception("Upload failed")
    
    service = StorageService()
    
    # Test file upload error handling
    with pytest.raises(Exception) as exc:
        service.upload_file(b"test content", "resumes/test.pdf")
    assert "OSS服务错误" in str(exc.value)
