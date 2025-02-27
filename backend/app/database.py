from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "mysql://root:test_password@localhost:3306/hr_recruit_test"

# Import models to ensure they're registered with Base
from .models.job_requirement import JobRequirement
from .models.resume import Resume
from .models.interview import Interview
from .models.user import User
from .models.tag import Tag

Base = declarative_base()

def init_db(db_url=None):
    if db_url:
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    Base.metadata.create_all(bind=engine)
    return engine

def get_db() -> Session:
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
