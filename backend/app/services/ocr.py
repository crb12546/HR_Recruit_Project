import os
import json
import base64
import logging
from typing import Optional

# 根据环境变量决定是否使用模拟实现
if os.getenv("TESTING", "False").lower() == "true":
    from app.services.ocr_mock import Client, RecognizeGeneralRequest
else:
    try:
        from aliyunsdkcore.client import AcsClient as Client
        from aliyunsdkocr.request.v20191230.RecognizeGeneralRequest import RecognizeGeneralRequest
    except ImportError:
        # 如果无法导入，使用模拟实现
        from app.services.ocr_mock import Client, RecognizeGeneralRequest

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.client = Client(
            os.getenv("ALIYUN_REGION_ID", "cn-shanghai"),
            os.getenv("ALIYUN_ACCESS_KEY", "test_access_key"),
            os.getenv("ALIYUN_ACCESS_SECRET", "test_access_secret")
        )
    
    async def extract_text_from_url(self, file_url: str) -> Optional[str]:
        """
        从文件URL中提取文本内容
        
        Args:
            file_url: 文件的URL地址
            
        Returns:
            提取的文本内容，如果失败则返回None
        """
        try:
            request = RecognizeGeneralRequest()
            request.set_Url(file_url)
            
            # 调用阿里云OCR服务
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            # 提取文本内容
            if "Data" in response_json and "Content" in response_json["Data"]:
                return response_json["Data"]["Content"]
            
            logger.error(f"OCR服务返回格式错误: {response_json}")
            return None
        except Exception as e:
            logger.error(f"OCR文本提取失败: {str(e)}")
            return None
    
    async def extract_text_from_base64(self, base64_content: str) -> Optional[str]:
        """
        从Base64编码的内容中提取文本
        
        Args:
            base64_content: Base64编码的文件内容
            
        Returns:
            提取的文本内容，如果失败则返回None
        """
        try:
            request = RecognizeGeneralRequest()
            request.set_body(base64_content)
            
            # 调用阿里云OCR服务
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            # 提取文本内容
            if "Data" in response_json and "Content" in response_json["Data"]:
                return response_json["Data"]["Content"]
            
            logger.error(f"OCR服务返回格式错误: {response_json}")
            return None
        except Exception as e:
            logger.error(f"OCR文本提取失败: {str(e)}")
            return None
