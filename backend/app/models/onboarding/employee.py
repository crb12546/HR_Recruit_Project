"""员工模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base

class Employee(Base):
    """员工信息"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="姓名")
    employee_id = Column(String(20), unique=True, nullable=False, comment="工号")
    department = Column(String(50), nullable=False, comment="部门")
    position = Column(String(50), nullable=False, comment="职位")
    status = Column(Enum("在职", "离职", "试用期"), default="试用期", comment="状态")
    entry_date = Column(DateTime, nullable=False, comment="入职日期")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    resume = relationship("Resume", back_populates="employee")
    attendance_records = relationship("AttendanceRecord", back_populates="employee")
    documents = relationship("EmployeeDocument", back_populates="employee")
