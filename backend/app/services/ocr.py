"""阿里云OCR服务"""
import os
import base64
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkocr.request.v20191230.RecognizeGeneralRequest import RecognizeGeneralRequest

class OCRService:
    """阿里云OCR服务实现"""
    
    def __init__(self):
        self.env = os.getenv("ENV", "test")
        if self.env == "test":
            self.mock = True
        else:
            self.mock = False
            self.access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
            self.access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
            self.region_id = os.getenv("ALIYUN_REGION_ID", "cn-shanghai")
            
            # 初始化ACS客户端
            self.client = AcsClient(
                self.access_key_id,
                self.access_key_secret,
                self.region_id
            )
    
    def extract_text(self, file_content: bytes) -> str:
        """从文件内容中提取文本"""
        try:
            if self.mock:
                # 测试环境使用模拟数据
                return "工作经验：5年\n技能：Python, FastAPI\n教育背景：计算机科学学士"
                
            # 将文件内容转换为Base64编码
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            
            # 创建OCR请求
            request = RecognizeGeneralRequest()
            request.set_accept_format('json')
            
            # 设置请求参数
            request.set_ImageURL(encoded_content)
            
            # 发送请求
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response.decode('utf-8'))
            
            # 提取文本内容
            if 'Data' in response_json and 'Content' in response_json['Data']:
                return response_json['Data']['Content']
            else:
                raise Exception("OCR识别失败：无法提取文本内容")
                
        except (ClientException, ServerException) as e:
            if not self.mock:
                raise Exception(f"阿里云OCR服务错误：{str(e)}")
            return "工作经验：5年\n技能：Python, FastAPI\n教育背景：计算机科学学士"
