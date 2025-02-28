from app.config.config import get_config

def get_ocr_service():
    """获取OCR服务实例"""
    config = get_config()
    
    if config["OCR_SERVICE"] == "mock" or config["MOCK_SERVICES"]:
        from app.services.ocr_mock import OCRService
    else:
        from app.services.ocr import OCRService
    
    return OCRService()

def get_storage_service():
    """获取存储服务实例"""
    config = get_config()
    
    if config["STORAGE_SERVICE"] == "mock" or config["MOCK_SERVICES"]:
        from app.services.storage_mock import StorageService
    else:
        from app.services.storage import StorageService
    
    return StorageService()

def get_gpt_service():
    """获取GPT服务实例"""
    config = get_config()
    
    if config["GPT_SERVICE"] == "mock" or config["MOCK_SERVICES"]:
        from app.services.gpt_mock import GPTService
    else:
        from app.services.gpt import GPTService
    
    return GPTService()
