"""Resume model"""
from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel
from .associations import resume_tags, job_resume_matches

class Resume(BaseModel):
    """Resume model for storing candidate resumes"""
    __tablename__ = "resumes"
    
    candidate_name = Column(String(50), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)
    ocr_content = Column(Text)
    parsed_content = Column(Text)
    talent_portrait = Column(Text)
    
    # Relationships
    tags = relationship("Tag", secondary=resume_tags, back_populates="resumes")
    matched_jobs = relationship("JobRequirement", secondary=job_resume_matches, back_populates="matched_resumes")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            **super().to_dict(),
            "candidate_name": self.candidate_name,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "ocr_content": self.ocr_content,
            "parsed_content": self.parsed_content,
            "talent_portrait": self.talent_portrait,
            "tags": [tag.to_dict() for tag in self.tags] if self.tags else []
        }
