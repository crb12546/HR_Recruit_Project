from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Enum
from datetime import datetime
from . import Base

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_requirement_id = Column(Integer, ForeignKey("job_requirements.id"), nullable=False)
    interviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_time = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="scheduled")
    feedback = Column(Text)
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
