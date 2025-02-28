"""
数据库工具模块
"""
from sqlalchemy.exc import SQLAlchemyError
import logging

# 获取日志记录器
logger = logging.getLogger("hr_recruitment")

def safe_commit(db, error_msg="数据库操作失败"):
    """安全提交数据库事务"""
    try:
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"{error_msg}: {str(e)}")
        return False
