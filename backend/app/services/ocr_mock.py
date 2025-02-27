class RecognizeGeneralRequest:
    def __init__(self):
        self.url = None
        self.body = None
    
    def set_Url(self, url):
        self.url = url
    
    def set_body(self, body):
        self.body = body

class Client:
    def __init__(self, region_id, access_key, access_secret):
        self.region_id = region_id
        self.access_key = access_key
        self.access_secret = access_secret
    
    def do_action_with_exception(self, request):
        # Return mock OCR result as string, not bytes
        return '{"Data": {"Content": "这是一份测试简历\\n姓名：张三\\n学历：本科\\n技能：Python, FastAPI, Vue.js"}}'.encode('utf-8')

def _is_file_empty(self, file_url):
    """检查文件是否为空"""
    # 模拟实现，实际应该检查文件内容
    return "empty" in file_url

def _get_file_type(self, file_url):
    """获取文件类型"""
    # 从URL中提取文件扩展名
    return file_url.split(".")[-1]
