"""配置模块"""
import os
from typing import Dict, Any

# 默认环境
DEFAULT_ENV = "development"

def get_config() -> Dict[str, Any]:
    """获取应用配置"""
    # 获取当前环境
    env = os.environ.get("APP_ENV", DEFAULT_ENV)
    
    # 检查是否在测试模式
    if os.environ.get("TESTING") == "True":
        env = "testing"
    
    # 根据环境加载配置
    if env == "development":
        from app.config.environments.development import get_development_config
        config = get_development_config()
    elif env == "testing":
        from app.config.environments.testing import get_testing_config
        config = get_testing_config()
    elif env == "production":
        from app.config.environments.production import get_production_config
        config = get_production_config()
    else:
        from app.config.environments.development import get_development_config
        config = get_development_config()
    
    # 从环境变量覆盖配置
    for key in config:
        env_value = os.environ.get(key)
        if env_value:
            # 处理布尔值
            if env_value.lower() in ["true", "false"]:
                config[key] = env_value.lower() == "true"
            else:
                config[key] = env_value
    
    return config
