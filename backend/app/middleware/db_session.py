"""
数据库会话中间件
用于确保每个请求都有一个有效的数据库会话
"""
from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import SessionLocal
import logging

# 获取日志记录器
logger = logging.getLogger("hr_recruitment")

class DBSessionMiddleware(BaseHTTPMiddleware):
    """数据库会话中间件"""
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        # 创建数据库会话
        db = SessionLocal()
        
        # 将数据库会话添加到请求状态
        request.state.db = db
        
        try:
            # 处理请求
            response = await call_next(request)
            return response
        except SQLAlchemyError as e:
            # 记录数据库错误
            logger.error(f"数据库错误: {str(e)}")
            # 回滚事务
            db.rollback()
            raise
        except Exception as e:
            # 记录其他错误
            logger.error(f"请求处理错误: {str(e)}")
            raise
        finally:
            # 关闭数据库会话
            db.close()
