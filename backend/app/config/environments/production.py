"""生产环境配置"""
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    """生产环境配置类"""
    ENV = "production"
    DEBUG = False
    TESTING = False
    
    # 生产环境数据库配置
    DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/hr_recruitment"
    
    # 生产环境默认使用真实服务
    SERVICE_MODE = "production"
