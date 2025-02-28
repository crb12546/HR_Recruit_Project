import json
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OCRService:
    """阿里云OCR服务的模拟实现"""
    
    def __init__(self):
        """初始化OCR服务"""
        self.mock_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          "tests", "mocks", "data")
        logger.info(f"初始化模拟OCR服务，数据路径: {self.mock_data_path}")
    
    def extract_text_from_file(self, file_url: str) -> str:
        """从文件中提取文本（模拟实现）"""
        logger.info(f"模拟从文件提取文本: {file_url}")
        
        # 检查文件是否为空
        if self._is_file_empty(file_url):
            logger.warning(f"文件为空: {file_url}")
            return ""
        
        # 获取文件类型
        file_type = self._get_file_type(file_url)
        if file_type not in ["pdf", "docx", "doc", "jpg", "png"]:
            logger.warning(f"不支持的文件类型: {file_type}")
            return f"不支持的文件类型: {file_type}"
        
        # 从模拟数据中获取OCR内容
        try:
            with open(os.path.join(self.mock_data_path, "mock_resume.json"), "r", encoding="utf-8") as f:
                mock_data = json.load(f)
                
            for resume in mock_data.get("resumes", []):
                if resume.get("file_url") == file_url:
                    return resume.get("ocr_content", "")
                
            # 如果没有找到匹配的文件，返回默认内容
            return "姓名：测试用户\n学历：本科\n技能：Python, Java\n工作经验：3年\n联系电话：13800000000"
        except Exception as e:
            logger.error(f"读取模拟数据失败: {str(e)}")
            return "模拟OCR提取的文本内容"
    
    def _is_file_empty(self, file_url: str) -> bool:
        """检查文件是否为空"""
        # 模拟实现，实际应该检查文件内容
        return "empty" in file_url
    
    def _get_file_type(self, file_url: str) -> str:
        """获取文件类型"""
        # 从URL中提取文件扩展名
        return file_url.split(".")[-1]
