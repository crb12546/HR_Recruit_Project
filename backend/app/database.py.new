from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import get_config

config = get_config()
DATABASE_URL = config["DATABASE_URL"]

# 创建SQLAlchemy引擎
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 导入模型以便Alembic可以检测到它们
from .models.resume import Resume
from .models.job_requirement import JobRequirement
from .models.interview import Interview
from .models.user import User
from .models.tag import Tag
from .models.onboarding import Onboarding, OnboardingTask
