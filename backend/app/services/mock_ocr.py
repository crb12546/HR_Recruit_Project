"""Mock OCR service for testing"""
import json

class AcsClient:
    def __init__(self, access_key_id, access_key_secret, region):
        pass

    def do_action_with_exception(self, request):
        return json.dumps({
            "Data": {
                "Content": "测试简历内容\n姓名：张三\n技能：Python, FastAPI, Vue.js\n工作经验：3年"
            }
        }).encode('utf-8')

class MockOCRService:
    def __init__(self):
        self.client = AcsClient("test", "test", "test")

    def extract_text(self, file_content: bytes) -> str:
        """Mock text extraction from file"""
        result = self.client.do_action_with_exception(None)
        return json.loads(result)["Data"]["Content"]
