"""测试配置模块"""
import os
import pytest
from unittest.mock import patch, MagicMock

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
            assert "sqlite" in config.DATABASE_URL.lower()
    
    def test_load_testing_config(self):
        """测试加载测试环境配置"""
        with patch.dict(os.environ, {"APP_ENV": "testing"}):
            config = load_config()
            assert config.ENV == "testing"
            assert isinstance(config, TestingConfig)
            assert config.TESTING is True
            assert "sqlite" in config.DATABASE_URL.lower() or "memory" in config.DATABASE_URL.lower()
    
    def test_load_production_config(self):
        """测试加载生产环境配置"""
        with patch.dict(os.environ, {"APP_ENV": "production"}):
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
        test_db_url = "mysql+pymysql://test:test@localhost/test_db"
        with patch.dict(os.environ, {"APP_ENV": "development", "DATABASE_URL": test_db_url}):
            config = load_config()
            assert config.DATABASE_URL == test_db_url
    
    def test_get_config_singleton(self):
        """测试获取配置单例"""
        with patch.dict(os.environ, {"APP_ENV": "testing"}):
            config1 = get_config()
            config2 = get_config()
            assert config1 is config2  # 应该是同一个实例
    
    def test_service_mode_config(self):
        """测试服务模式配置"""
        # 测试默认模式
        with patch.dict(os.environ, {"APP_ENV": "development"}):
            config = load_config()
            assert config.SERVICE_MODE == "production"  # 默认为生产模式
        
        # 测试模拟模式
        with patch.dict(os.environ, {"APP_ENV": "testing", "SERVICE_MODE": "mock"}):
            config = load_config()
            assert config.SERVICE_MODE == "mock"
        
        # 测试生产模式
        with patch.dict(os.environ, {"APP_ENV": "production", "SERVICE_MODE": "production"}):
            config = load_config()
            assert config.SERVICE_MODE == "production"
    
    def test_api_keys_config(self):
        """测试API密钥配置"""
        test_openai_key = "test-openai-key"
        test_aliyun_key = "test-aliyun-key"
        
        with patch.dict(os.environ, {
            "APP_ENV": "production",
            "OPENAI_API_KEY": test_openai_key,
            "ALIYUN_ACCESS_KEY": test_aliyun_key
        }):
            config = load_config()
            assert config.OPENAI_API_KEY == test_openai_key
            assert config.ALIYUN_ACCESS_KEY == test_aliyun_key
