"""
配置模块
"""
import os
import importlib
from typing import Dict, Any, Optional

# 配置实例
_config_instance = None

def load_config():
    """
    加载配置
    根据环境变量APP_ENV加载对应环境的配置
    """
    # 获取环境变量
    env = os.getenv("APP_ENV", "development").lower()
    
    # 导入对应环境的配置模块
    try:
        # 尝试导入配置类
        config_module = importlib.import_module(f"app.config.environments.{env}")
        config_class = getattr(config_module, f"{env.capitalize()}Config")
        return config_class()
    except (ImportError, AttributeError) as e:
        # 如果找不到配置类，尝试导入配置字典
        try:
            config_func = getattr(config_module, f"get_{env}_config")
            config_dict = config_func()
            
            # 创建一个配置类实例
            from app.config.environments.base import BaseConfig
            config = BaseConfig()
            
            # 将字典中的配置项设置到配置类实例中
            for key, value in config_dict.items():
                setattr(config, key, value)
            
            return config
        except (AttributeError, ImportError) as e:
            # 如果还是找不到，使用默认配置
            print(f"警告: 无法加载{env}环境配置，使用默认配置。错误: {str(e)}")
            from app.config.environments.base import BaseConfig
            return BaseConfig()

def get_config():
    """
    获取配置实例
    单例模式
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = load_config()
    return _config_instance

def reload_config():
    """
    重新加载配置
    """
    global _config_instance
    _config_instance = load_config()
    return _config_instance
