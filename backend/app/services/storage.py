"""存储服务"""
import os
import oss2

class StorageService:
    """阿里云OSS存储服务"""
    
    def __init__(self):
        self.env = os.getenv("ENV", "test")
        if self.env == "test":
            self.mock = True
            self.bucket_name = os.getenv("ALIYUN_OSS_BUCKET", "test-bucket")
            self.endpoint = os.getenv("ALIYUN_OSS_ENDPOINT", "oss-cn-hangzhou.aliyuncs.com")
        else:
            self.mock = False
            self.access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
            self.access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
            self.bucket_name = os.getenv("ALIYUN_OSS_BUCKET")
            self.endpoint = os.getenv("ALIYUN_OSS_ENDPOINT")
            
            # 初始化OSS客户端
            auth = oss2.Auth(self.access_key_id, self.access_key_secret)
            self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
    
    def upload_file(self, file_content: bytes, file_name: str) -> str:
        """上传文件到OSS"""
        try:
            if self.mock:
                return f"https://{self.bucket_name}.{self.endpoint}/{file_name}"
                
            # 上传文件
            result = self.bucket.put_object(file_name, file_content)
            
            if result.status != 200:
                raise Exception("OSS服务错误：上传失败")
                
            # 生成文件URL
            return f"https://{self.bucket_name}.{self.endpoint}/{file_name}"
            
        except Exception as e:
            if not self.mock:
                raise Exception(f"OSS服务错误：{str(e)}")
            return f"https://{self.bucket_name}.{self.endpoint}/{file_name}"
