import os
import logging
from typing import Optional, BinaryIO

logger = logging.getLogger(__name__)

class StorageService:
    """阿里云OSS存储服务的模拟实现"""
    
    def __init__(self):
        """初始化存储服务"""
        self.mock_storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                             "tests", "mocks", "storage")
        # 确保模拟存储目录存在
        os.makedirs(self.mock_storage_path, exist_ok=True)
        logger.info(f"初始化模拟存储服务，存储路径: {self.mock_storage_path}")
    
    def upload_file(self, file_content: BinaryIO, file_name: str) -> str:
        """上传文件到存储服务（模拟实现）"""
        logger.info(f"模拟上传文件: {file_name}")
        
        # 检查文件大小
        file_size = self._get_file_size(file_content)
        if file_size > 100 * 1024 * 1024:  # 100MB
            logger.warning(f"文件过大: {file_size} bytes")
            raise ValueError("文件大小超过限制（最大100MB）")
        
        # 模拟文件存储
        try:
            file_path = os.path.join(self.mock_storage_path, file_name)
            with open(file_path, "wb") as f:
                f.write(file_content.read())
            
            # 返回模拟的文件URL
            return f"https://test-bucket.oss.aliyuncs.com/{file_name}"
        except Exception as e:
            logger.error(f"模拟文件上传失败: {str(e)}")
            raise
    
    def get_file_url(self, file_name: str) -> str:
        """获取文件URL（模拟实现）"""
        logger.info(f"模拟获取文件URL: {file_name}")
        return f"https://test-bucket.oss.aliyuncs.com/{file_name}"
    
    def delete_file(self, file_url: str) -> bool:
        """删除文件（模拟实现）"""
        logger.info(f"模拟删除文件: {file_url}")
        
        # 从URL中提取文件名
        file_name = file_url.split("/")[-1]
        file_path = os.path.join(self.mock_storage_path, file_name)
        
        # 检查文件是否存在
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                logger.error(f"模拟文件删除失败: {str(e)}")
                return False
        else:
            logger.warning(f"文件不存在: {file_path}")
            return False
    
    def _get_file_size(self, file_content: BinaryIO) -> int:
        """获取文件大小"""
        # 保存当前位置
        current_pos = file_content.tell()
        
        # 移动到文件末尾
        file_content.seek(0, os.SEEK_END)
        size = file_content.tell()
        
        # 恢复位置
        file_content.seek(current_pos)
        
        return size
