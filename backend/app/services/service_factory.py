"""
服务工厂模块
用于创建和获取各种服务实例
"""
import os
import logging
from app.services.gpt import GPTService
from app.services.gpt_mock import GPTService as MockGPTService
from app.services.ocr import OCRService
from app.services.ocr_mock import MockOCRService
from app.services.storage import StorageService, LocalStorageService, AliyunOSSService

# 获取日志记录器
logger = logging.getLogger(__name__)

def get_gpt_service():
    """获取GPT服务实例"""
    # 在测试环境中使用模拟服务
    if os.getenv("MOCK_SERVICES", "False").lower() == "true" or os.getenv("ENV") == "test":
        logger.info("使用模拟GPT服务")
        return MockGPTService()
    logger.info("使用真实GPT服务")
    return GPTService()

def get_ocr_service():
    """获取OCR服务实例"""
    # 在测试环境中使用模拟服务
    if os.getenv("MOCK_SERVICES", "False").lower() == "true" or os.getenv("ENV") == "test":
        logger.info("使用模拟OCR服务")
        return MockOCRService()
    logger.info("使用真实OCR服务")
    return OCRService()

def get_storage_service():
    """获取存储服务实例"""
    storage_type = os.getenv("STORAGE_TYPE", "local")
    
    if storage_type == "local":
        storage_path = os.getenv("STORAGE_PATH", "./uploads")
        logger.info(f"使用本地存储服务，路径: {storage_path}")
        return LocalStorageService(storage_path)
    elif storage_type == "aliyun":
        logger.info("使用阿里云OSS存储服务")
        return AliyunOSSService()
    else:
        logger.error(f"不支持的存储类型: {storage_type}")
        raise ValueError(f"不支持的存储类型: {storage_type}")
