from typing import Optional
import os
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkocr.request.v20191230 import RecognizeGeneralRequest
from fastapi import HTTPException

class OCRService:
    def __init__(self):
        self.client = AcsClient(
            os.getenv('ALIYUN_ACCESS_KEY_ID'),
            os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
            'cn-shanghai'
        )

    def extract_text(self, file_content: bytes) -> str:
        """
        使用阿里云OCR服务提取简历文本内容
        
        Args:
            file_content: 文件二进制内容
            
        Returns:
            str: 提取的文本内容
            
        Raises:
            HTTPException: OCR服务调用失败时抛出异常
        """
        try:
            request = RecognizeGeneralRequest.RecognizeGeneralRequest()
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
