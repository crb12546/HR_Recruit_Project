"""
生产环境配置模块
"""
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    """生产环境配置类"""
    ENV = "production"
    DEBUG = False
    TESTING = False
    
    # 生产环境数据库配置
    DATABASE_URL = "sqlite:///./hr_recruitment.db"
    
    # 生产环境默认使用模拟服务
    SERVICE_MODE = "mock"
