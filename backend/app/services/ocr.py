from typing import Optional
import os
import json
from fastapi import HTTPException

class OCRService:
    """OCR service for extracting text from resume files"""
    def __init__(self):
        """Initialize OCR service with environment-specific configuration"""
        if os.getenv("ENV") == "test":
            from .mock_ocr import MockOCRService
            self.service = MockOCRService()
        else:
            try:
                from aliyunsdkcore.client import AcsClient
                from aliyunsdkocr.request.v20191230 import RecognizeGeneralRequest
                self.client = AcsClient(
                    os.getenv("ALIYUN_ACCESS_KEY_ID"),
                    os.getenv("ALIYUN_ACCESS_KEY_SECRET"),
                    "cn-hangzhou"
                )
                self.RecognizeGeneralRequest = RecognizeGeneralRequest
            except ImportError:
                # Fallback to mock service if Aliyun SDK is not available
                from .mock_ocr import MockOCRService
                self.service = MockOCRService()

    def extract_text(self, file_content: bytes) -> str:
        """Extract text from file content using OCR service.

        Args:
            file_content: Binary content of the file to process

        Returns:
            str: Extracted text content

        Raises:
            HTTPException: If OCR processing fails
        """
        if hasattr(self, 'service'):
            return self.service.extract_text(file_content)
            
        try:
            request = self.RecognizeGeneralRequest()
            request.set_ImageURL(file_content)
            
            response = self.client.do_action_with_exception(request)
            result = json.loads(response)
            
            if result.get('Data') and result['Data'].get('Content'):
                return result['Data']['Content']
            else:
                raise HTTPException(status_code=500, detail="简历文本提取失败")
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"OCR服务调用失败: {str(e)}"
            )
