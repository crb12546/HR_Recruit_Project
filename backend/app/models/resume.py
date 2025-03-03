from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base
from .tag import resume_tag

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
    
    # 与标签的多对多关系
    tags = relationship("Tag", secondary=resume_tag, back_populates="resumes")
    
    def to_dict(self):
        return {
            "id": self.id,
            "candidate_name": self.candidate_name,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "ocr_content": self.ocr_content,
            "parsed_content": self.parsed_content,
            "talent_portrait": self.talent_portrait,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
