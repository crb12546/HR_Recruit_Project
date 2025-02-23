from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import SQLALCHEMY_DATABASE_URL
from app.models import Base
from app.models.job_requirement import JobRequirement
from app.models.resume import Resume
from app.models.interview import Interview
from app.models.user import User

def init_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
