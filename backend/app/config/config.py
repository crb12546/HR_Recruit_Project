import os
from typing import Dict, Any

# 默认配置
DEFAULT_CONFIG: Dict[str, Any] = {
    "TESTING": False,
    "DATABASE_URL": "mysql+mysqlconnector://root:password@localhost:3306/hr_recruit",
    "MOCK_SERVICES": False,
    "OCR_SERVICE": "aliyun",
    "STORAGE_SERVICE": "aliyun",
    "GPT_SERVICE": "openai",
    "ALIYUN_ACCESS_KEY": "",
    "ALIYUN_SECRET_KEY": "",
    "ALIYUN_REGION": "cn-hangzhou",
    "ALIYUN_BUCKET": "hr-recruit",
    "OPENAI_API_KEY": ""
}

def get_config() -> Dict[str, Any]:
    """获取应用配置"""
    # 检查是否在测试模式
    if os.environ.get("TESTING") == "True":
        from app.config.test_config import get_test_config
        return get_test_config()
    
    config = DEFAULT_CONFIG.copy()
    
    # 从环境变量覆盖配置
    for key in config:
        env_value = os.environ.get(key)
        if env_value:
            config[key] = env_value
    
    return config
