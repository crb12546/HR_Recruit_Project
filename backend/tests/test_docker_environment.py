"""Docker环境测试"""
import os
import pytest
from app.config.config import get_config

def test_environment_variables():
    """测试环境变量是否正确设置"""
    # 检查测试模式是否启用
    assert os.environ.get("TESTING") == "True"
    
    # 检查模拟服务是否启用
    assert os.environ.get("MOCK_SERVICES") == "True"
    
    # 获取配置
    config = get_config()
    
    # 检查配置是否正确
    assert config["TESTING"] is True
    assert config["MOCK_SERVICES"] is True
    assert config["OCR_SERVICE"] == "mock"
    assert config["STORAGE_SERVICE"] == "mock"
    assert config["GPT_SERVICE"] == "mock"

def test_database_connection(db):
    """测试数据库连接是否正常"""
    # 如果数据库连接正常，这个测试应该通过
    assert db is not None

def test_service_factory():
    """测试服务工厂是否正常工作"""
    from app.services.service_factory import get_ocr_service, get_storage_service, get_gpt_service
    
    # 获取服务实例
    ocr_service = get_ocr_service()
    storage_service = get_storage_service()
    gpt_service = get_gpt_service()
    
    # 检查服务实例是否正确
    assert ocr_service is not None
    assert storage_service is not None
    assert gpt_service is not None
    
    # 检查是否使用了模拟服务
    assert "mock" in ocr_service.__class__.__module__.lower()
    assert "mock" in storage_service.__class__.__module__.lower()
    assert "mock" in gpt_service.__class__.__module__.lower()
