"""职位需求模型"""
from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
from .associations import job_resume_matches

class JobRequirement(BaseModel):
    """职位需求模型"""
    __tablename__ = "job_requirements"
    
    position_name = Column(String(100), nullable=False)
    department = Column(String(50))
    responsibilities = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    salary_range = Column(String(50))
    location = Column(String(100))
    tags = Column(JSON, nullable=True, default=list)
    
    # 关联简历
    matched_resumes = relationship("Resume", secondary=job_resume_matches, back_populates="matched_jobs")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            **super().to_dict(),
            "position_name": self.position_name,
            "department": self.department,
            "responsibilities": self.responsibilities,
            "requirements": self.requirements,
            "salary_range": self.salary_range,
            "location": self.location,
            "tags": self.tags or []
        }
