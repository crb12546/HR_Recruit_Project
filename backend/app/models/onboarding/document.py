"""员工档案模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class EmployeeDocument(Base):
    """员工档案"""
    __tablename__ = "employee_documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    document_type = Column(String(50), nullable=False, comment="文档类型")
    file_url = Column(String(255), nullable=False, comment="文件URL")
    file_name = Column(String(100), nullable=False, comment="文件名")
    upload_time = Column(DateTime, default=datetime.utcnow)
    note = Column(Text, comment="备注")
    
    # 关联
    employee = relationship("Employee", back_populates="documents")
