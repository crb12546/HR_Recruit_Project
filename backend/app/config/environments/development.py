"""
开发环境配置模块
"""
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """开发环境配置类"""
    ENV = "development"
    DEBUG = True
    TESTING = False
    
    # 开发环境数据库配置
    DATABASE_URL = "sqlite:///./hr_recruitment_dev.db"
    
    # 开发环境默认使用模拟服务
    SERVICE_MODE = "mock"
