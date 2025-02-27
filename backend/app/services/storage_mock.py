class StorageService:
    def __init__(self):
        self.files = {}
    
    async def upload_file(self, file_content, file_name, content_type):
        """模拟文件上传"""
        file_url = f"https://test-bucket.oss.aliyuncs.com/{file_name}"
        self.files[file_name] = {
            "content": file_content,
            "url": file_url,
            "content_type": content_type
        }
        return file_url
    
    async def get_file_url(self, file_name):
        """获取文件URL"""
        if file_name in self.files:
            return self.files[file_name]["url"]
        return None
