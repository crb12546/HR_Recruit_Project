"""存储服务单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from app.services.storage import StorageService, AliyunStorageService, MockStorageService

class TestStorageService:
    """存储服务测试类"""
    
    def test_aliyun_storage_service(self, monkeypatch):
        """测试阿里云存储服务"""
        # 模拟阿里云OSS客户端
        mock_bucket = MagicMock()
        mock_bucket.put_object.return_value = None
        mock_bucket.sign_url.return_value = "https://example.com/signed_url"
        
        mock_oss = MagicMock()
        mock_oss.Bucket.return_value = mock_bucket
        
        # 打补丁替换OSS客户端
        monkeypatch.setattr("app.services.storage.oss2.Bucket", mock_bucket)
        monkeypatch.setattr("app.services.storage.oss2.Auth", lambda *args: MagicMock())
        
        # 创建存储服务
        storage_service = AliyunStorageService(
            access_key="test_key",
            secret_key="test_secret",
            bucket_name="test-bucket",
            region="cn-hangzhou"
        )
        
        # 调用上传文件方法
        result = storage_service.upload_file(file_content=b"测试文件内容", file_name="test.pdf")
        
        # 验证结果
        assert result == "https://example.com/signed_url"
        assert mock_bucket.put_object.called
        assert mock_bucket.sign_url.called
    
    def test_mock_storage_service(self):
        """测试模拟存储服务"""
        # 创建模拟存储服务
        storage_service = MockStorageService()
        
        # 调用上传文件方法
        result = storage_service.upload_file(file_content=b"测试文件内容", file_name="test.pdf")
        
        # 验证结果
        assert result is not None
        assert isinstance(result, str)
        assert result.startswith("http")
        assert "test.pdf" in result
    
    def test_storage_service_factory(self, monkeypatch):
        """测试存储服务工厂"""
        from app.services.service_factory import get_storage_service
        
        # 模拟配置
        mock_config = {
            "STORAGE_SERVICE": "mock",
            "ALIYUN_ACCESS_KEY": "test_key",
            "ALIYUN_SECRET_KEY": "test_secret",
            "ALIYUN_REGION": "cn-hangzhou",
            "ALIYUN_BUCKET": "test-bucket"
        }
        
        # 打补丁替换配置
        monkeypatch.setattr("app.services.service_factory.get_config", lambda: mock_config)
        
        # 获取存储服务
        storage_service = get_storage_service()
        
        # 验证结果
        assert storage_service is not None
        assert isinstance(storage_service, StorageService)
        assert isinstance(storage_service, MockStorageService)
        
        # 修改配置为阿里云
        mock_config["STORAGE_SERVICE"] = "aliyun"
        
        # 获取存储服务
        storage_service = get_storage_service()
        
        # 验证结果
        assert storage_service is not None
        assert isinstance(storage_service, StorageService)
        assert isinstance(storage_service, AliyunStorageService)
