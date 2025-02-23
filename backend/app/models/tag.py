from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

# 简历-标签关联表
resume_tags = Table(
    'resume_tags',
    Base.metadata,
    Column('resume_id', Integer, ForeignKey('resumes.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# 职位-标签关联表
job_tags = Table(
    'job_tags',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('job_requirements.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    """标签模型"""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    category = Column(String(20), nullable=False)  # 技能、经验、教育等
    
    # 关联关系
    resumes = relationship("Resume", secondary=resume_tags, back_populates="tags")
    jobs = relationship("JobRequirement", secondary=job_tags, back_populates="tags")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }
