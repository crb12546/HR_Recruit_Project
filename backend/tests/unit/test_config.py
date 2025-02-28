"""配置模块测试"""
import os
import pytest
from unittest.mock import patch

from app.config.config import load_config, get_config
from app.config.environments.development import DevelopmentConfig
from app.config.environments.testing import TestingConfig
from app.config.environments.production import ProductionConfig

class TestConfig:
    """配置测试类"""
    
    def test_load_development_config(self):
        """测试加载开发环境配置"""
        with patch.dict(os.environ, {"APP_ENV": "development"}):
            config = load_config()
            assert config.ENV == "development"
            assert isinstance(config, DevelopmentConfig)
            assert config.DEBUG is True
    
    def test_load_testing_config(self):
        """测试加载测试环境配置"""
        with patch.dict(os.environ, {"APP_ENV": "testing"}):
            config = load_config()
            assert config.ENV == "testing"
            assert isinstance(config, TestingConfig)
            assert config.TESTING is True
    
    def test_load_production_config(self):
        """测试加载生产环境配置"""
        # 清除配置单例
        from app.config.config import _config_instance
        import app.config.config
        app.config.config._config_instance = None
        
        # 确保环境变量不会干扰测试
        with patch.dict(os.environ, {"APP_ENV": "production"}, clear=True):
            config = load_config()
            assert config.ENV == "production"
            assert isinstance(config, ProductionConfig)
            assert config.DEBUG is False
            assert config.TESTING is False
    
    def test_default_config(self):
        """测试默认配置"""
        with patch.dict(os.environ, {}, clear=True):
            config = load_config()
            assert config.ENV == "development"  # 默认为开发环境
    
    def test_database_url_override(self):
        """测试数据库URL环境变量覆盖"""
        test_db_url = "mysql+mysqlconnector://test:test@localhost/test_db"
        
        # 清除配置单例
        from app.config.config import _config_instance
        import app.config.config
        app.config.config._config_instance = None
        
        # 模拟环境变量
        with patch.dict(os.environ, {"APP_ENV": "development", "DATABASE_URL": test_db_url}, clear=True):
            config = load_config()
            assert config.DATABASE_URL == test_db_url
    
    def test_get_config_singleton(self):
        """测试获取配置单例"""
        with patch.dict(os.environ, {"APP_ENV": "testing"}):
            config1 = get_config()
            config2 = get_config()
            assert config1 is config2  # 应该是同一个实例
