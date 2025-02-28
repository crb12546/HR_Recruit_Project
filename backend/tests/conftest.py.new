import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from app.config.config import get_config

# 设置测试环境
os.environ["TESTING"] = "True"
os.environ["MOCK_SERVICES"] = "True"

# 获取测试配置
config = get_config()

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """创建测试数据库会话"""
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # 清理数据库表
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    
    # 清理依赖覆盖
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def test_data(db):
    """创建测试数据"""
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.job_requirement import JobRequirement
    from app.models.tag import Tag
    
    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
        is_hr=True
    )
    db.add(user)
    
    # 创建测试标签
    tags = []
    for tag_name in ["Python", "FastAPI", "Vue.js", "前端开发", "后端开发"]:
        tag = Tag(name=tag_name)
        db.add(tag)
        tags.append(tag)
    
    # 创建测试简历
    resume = Resume(
        candidate_name="张三",
        file_url="https://test-bucket.oss.aliyuncs.com/resume.pdf",
        file_type="pdf",
        ocr_content="姓名：张三\n学历：本科\n技能：Python, FastAPI, Vue.js",
        parsed_content={"name": "张三", "education": "本科", "skills": ["Python", "FastAPI", "Vue.js"]},
        talent_portrait="张三是一名有5年经验的全栈开发工程师，精通Python和Vue.js，有丰富的FastAPI开发经验。"
    )
    resume.tags = tags[:3]  # 添加标签
    db.add(resume)
    
    # 创建测试职位
    job = JobRequirement(
        position_name="Python高级工程师",
        department="技术部",
        job_description="负责公司核心系统的开发和维护",
        requirements="1. 精通Python编程语言\n2. 熟悉FastAPI框架\n3. 有5年以上开发经验",
        salary_range="25k-35k",
        status="open"
    )
    job.tags = tags[1:4]  # 添加标签
    db.add(job)
    
    db.commit()
    
    return {
        "user": user,
        "resume": resume,
        "job": job,
        "tags": tags
    }
