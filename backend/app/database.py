"""
数据库模块
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import get_config

# 获取日志记录器
logger = logging.getLogger("hr_recruitment")

# 获取配置
config = get_config()

# 数据库URL
DATABASE_URL = config.DATABASE_URL

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,  # 添加连接池预检查，解决连接断开问题
    pool_recycle=3600,   # 每小时回收连接，避免连接过期
    echo=False           # 设置为True可以查看SQL语句，用于调试
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库"""
    try:
        # 导入所有模型以确保它们在创建表时被注册
        # 这里导入是为了避免循环导入问题
        from app.models.init_models import JobRequirement, Resume, Interview, User, Tag, Onboarding, OnboardingTask
        
        # 创建所有表
        logger.info("正在初始化数据库表...")
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表初始化完成")
        
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False
