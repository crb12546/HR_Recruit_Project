"""初始化测试数据"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine, Base
from app.models.tag import Tag
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview

def init_database():
    """初始化数据库表结构"""
    print("正在初始化数据库表结构...")
    Base.metadata.create_all(bind=engine)
    print("数据库表结构初始化完成！")

if __name__ == "__main__":
    init_database()
