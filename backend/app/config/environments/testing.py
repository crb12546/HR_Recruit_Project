"""
测试环境配置模块
"""
from .base import BaseConfig

class TestingConfig(BaseConfig):
    """测试环境配置类"""
    ENV = "testing"
    DEBUG = True
    TESTING = True
    
    # 测试环境数据库配置
    DATABASE_URL = "sqlite:///./hr_recruitment_test.db"
    
    # 测试环境默认使用模拟服务
    SERVICE_MODE = "mock"
