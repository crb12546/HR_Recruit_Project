from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from . import Base

class JobRequirement(Base):
    __tablename__ = "job_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(100), nullable=False)
    department = Column(String(50))
    responsibilities = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    salary_range = Column(String(50))
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
