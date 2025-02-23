from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(50), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)
    ocr_content = Column(Text)
    parsed_content = Column(Text)
    talent_portrait = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
