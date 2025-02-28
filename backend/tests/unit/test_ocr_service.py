import os
import pytest
from app.services.ocr import OCRService

# 设置测试环境变量
os.environ["TESTING"] = "True"

@pytest.mark.asyncio
async def test_ocr_service_extract_text():
    """测试OCR服务文本提取功能"""
    ocr_service = OCRService()
    
    # 测试从URL提取文本
    text = await ocr_service.extract_text_from_url("https://example.com/test.pdf")
    assert text is not None
    assert "张三" in text
    assert "Python" in text
    
    # 测试从Base64提取文本
    base64_content = "base64_encoded_content"
    text = await ocr_service.extract_text_from_base64(base64_content)
    assert text is not None
    assert "张三" in text
    assert "Python" in text
