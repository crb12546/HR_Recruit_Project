import os
from typing import Dict, Any

# 测试环境配置
TEST_CONFIG: Dict[str, Any] = {
    "TESTING": True,
    "DATABASE_URL": "sqlite:///:memory:",
    "MOCK_SERVICES": True,
    "OCR_SERVICE": "mock",
    "STORAGE_SERVICE": "mock",
    "GPT_SERVICE": "mock"
}

def get_test_config() -> Dict[str, Any]:
    """获取测试环境配置"""
    config = TEST_CONFIG.copy()
    
    # 从环境变量覆盖配置
    for key in config:
        env_value = os.environ.get(key)
        if env_value:
            config[key] = env_value
    
    return config
