"""入职管理模型"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Onboarding(Base):
    __tablename__ = "onboardings"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_requirement_id = Column(Integer, ForeignKey("job_requirements.id"), nullable=False)
    # 入职状态: pending(待入职), in_progress(入职中), completed(已入职), cancelled(已取消)
    status = Column(String(20), nullable=False, default="pending")
    offer_date = Column(DateTime, nullable=False)
    start_date = Column(DateTime, nullable=True)
    probation_end_date = Column(DateTime, nullable=True)
    department = Column(String(50), nullable=True)
    position = Column(String(100), nullable=True)
    salary = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与简历和职位的关系
    resume = relationship("Resume", backref="onboardings")
    job_requirement = relationship("JobRequirement", backref="onboardings")
    
    def to_dict(self):
        """将Onboarding对象转换为字典"""
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "job_requirement_id": self.job_requirement_id,
            "status": self.status,
            "offer_date": self.offer_date.isoformat() if self.offer_date else None,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "probation_end_date": self.probation_end_date.isoformat() if self.probation_end_date else None,
            "department": self.department,
            "position": self.position,
            "salary": self.salary,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    onboarding_id = Column(Integer, ForeignKey("onboardings.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    # 任务状态: pending(待完成), in_progress(进行中), completed(已完成), cancelled(已取消)
    status = Column(String(20), nullable=False, default="pending")
    deadline = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与入职记录的关系
    onboarding = relationship("Onboarding", backref="tasks")
    
    def to_dict(self):
        """将OnboardingTask对象转换为字典"""
        return {
            "id": self.id,
            "onboarding_id": self.onboarding_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
