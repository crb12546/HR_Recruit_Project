"""配置模块"""
import os
from importlib import import_module

_config_instance = None

def _convert_value(current_value, new_value):
    """根据当前值的类型转换新值"""
    if isinstance(current_value, bool):
        # 将字符串转换为布尔值
        if isinstance(new_value, str):
            return new_value.lower() in ('true', 'yes', '1', 'y')
        return bool(new_value)
    elif isinstance(current_value, int):
        # 将字符串转换为整数
        try:
            return int(new_value)
        except (ValueError, TypeError):
            return current_value
    elif isinstance(current_value, float):
        # 将字符串转换为浮点数
        try:
            return float(new_value)
        except (ValueError, TypeError):
            return current_value
    else:
        # 其他类型直接返回
        return new_value

def load_config():
    """加载配置"""
    env = os.environ.get("APP_ENV", "development").lower()
    
    # 导入对应环境的配置类
    try:
        config_module = import_module(f"app.config.environments.{env}")
        config_class = getattr(config_module, f"{env.capitalize()}Config")
        config = config_class()
        
        # 应用环境变量覆盖
        for key, value in os.environ.items():
            if hasattr(config, key):
                current_value = getattr(config, key)
                converted_value = _convert_value(current_value, value)
                setattr(config, key, converted_value)
        
        # 特殊处理数据库URL
        if "DATABASE_URL" in os.environ:
            config.DATABASE_URL = os.environ["DATABASE_URL"]
            
        return config
    except (ImportError, AttributeError):
        # 默认使用开发环境配置
        from app.config.environments.development import DevelopmentConfig
        config = DevelopmentConfig()
        
        # 应用环境变量覆盖
        for key, value in os.environ.items():
            if hasattr(config, key):
                current_value = getattr(config, key)
                converted_value = _convert_value(current_value, value)
                setattr(config, key, converted_value)
        
        # 特殊处理数据库URL
        if "DATABASE_URL" in os.environ:
            config.DATABASE_URL = os.environ["DATABASE_URL"]
            
        return config

def get_config():
    """获取配置单例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = load_config()
    return _config_instance
