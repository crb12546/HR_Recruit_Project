from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from . import Base

# 定义简历标签关联表
resume_tag = Table(
    "resume_tag",
    Base.metadata,
    Column("resume_id", Integer, ForeignKey("resumes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    
    # 与简历的多对多关系
    resumes = relationship("Resume", secondary=resume_tag, back_populates="tags")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
