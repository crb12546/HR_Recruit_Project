"""测试环境配置"""
from .base import BaseConfig

class TestingConfig(BaseConfig):
    """测试环境配置类"""
    ENV = "testing"
    DEBUG = True
    TESTING = True  # Make sure this is a boolean, not a string
    
    # 测试环境数据库配置
    DATABASE_URL = "sqlite:///:memory:"
    
    # 测试环境默认使用模拟服务
    SERVICE_MODE = "mock"
