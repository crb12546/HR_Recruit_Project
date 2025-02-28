"""
日志配置模块
用于配置应用程序的日志记录
"""
import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 日志目录
LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
LOG_LEVEL = LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO)

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志文件
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
ACCESS_LOG_FILE = os.path.join(LOG_DIR, "access.log")

def setup_logger(name, log_file, level=logging.INFO, max_bytes=10485760, backup_count=5):
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 文件处理器（按大小轮转）
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(console_handler)
    
    return logger

def setup_access_logger(name, log_file, level=logging.INFO):
    """设置访问日志记录器（按日期轮转）"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 文件处理器（按日期轮转）
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=30
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    file_handler.suffix = "%Y-%m-%d"
    logger.addHandler(file_handler)
    
    return logger

# 应用日志记录器
app_logger = setup_logger("hr_recruitment", APP_LOG_FILE, LOG_LEVEL)

# 错误日志记录器
error_logger = setup_logger("hr_recruitment.error", ERROR_LOG_FILE, logging.ERROR)

# 访问日志记录器
access_logger = setup_access_logger("hr_recruitment.access", ACCESS_LOG_FILE, logging.INFO)

def get_logger(name=None):
    """获取日志记录器"""
    if name is None:
        return app_logger
    return logging.getLogger(f"hr_recruitment.{name}")
