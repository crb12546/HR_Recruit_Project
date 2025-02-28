"""OCR服务单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from app.services.ocr import OCRService, AliyunOCRService, MockOCRService

class TestOCRService:
    """OCR服务测试类"""
    
    def test_aliyun_ocr_service(self, monkeypatch):
        """测试阿里云OCR服务"""
        # 模拟阿里云SDK客户端
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.get_http_status.return_value = 200
        mock_response.get_response.return_value = {
            "Data": {
                "Content": "提取的文本内容"
            }
        }
        mock_client.do_action_with_exception.return_value = mock_response
        
        # 打补丁替换SDK客户端
        monkeypatch.setattr("app.services.ocr.AcsClient", lambda *args, **kwargs: mock_client)
        
        # 创建OCR服务
        ocr_service = AliyunOCRService(
            access_key="test_key",
            secret_key="test_secret",
            region="cn-hangzhou"
        )
        
        # 调用提取文本方法
        result = ocr_service.extract_text(file_content=b"测试文件内容", file_type="pdf")
        
        # 验证结果
        assert result == "提取的文本内容"
        assert mock_client.do_action_with_exception.called
    
    def test_mock_ocr_service(self):
        """测试模拟OCR服务"""
        # 创建模拟OCR服务
        ocr_service = MockOCRService()
        
        # 调用提取文本方法
        result = ocr_service.extract_text(file_content=b"测试文件内容", file_type="pdf")
        
        # 验证结果
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_ocr_service_factory(self, monkeypatch):
        """测试OCR服务工厂"""
        from app.services.service_factory import get_ocr_service
        
        # 模拟配置
        mock_config = {
            "OCR_SERVICE": "mock",
            "ALIYUN_ACCESS_KEY": "test_key",
            "ALIYUN_SECRET_KEY": "test_secret",
            "ALIYUN_REGION": "cn-hangzhou"
        }
        
        # 打补丁替换配置
        monkeypatch.setattr("app.services.service_factory.get_config", lambda: mock_config)
        
        # 获取OCR服务
        ocr_service = get_ocr_service()
        
        # 验证结果
        assert ocr_service is not None
        assert isinstance(ocr_service, OCRService)
        assert isinstance(ocr_service, MockOCRService)
        
        # 修改配置为阿里云
        mock_config["OCR_SERVICE"] = "aliyun"
        
        # 获取OCR服务
        ocr_service = get_ocr_service()
        
        # 验证结果
        assert ocr_service is not None
        assert isinstance(ocr_service, OCRService)
        assert isinstance(ocr_service, AliyunOCRService)
