"""考勤记录模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class AttendanceRecord(Base):
    """考勤记录"""
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    check_in = Column(DateTime, nullable=True, comment="上班打卡时间")
    check_out = Column(DateTime, nullable=True, comment="下班打卡时间")
    status = Column(String(20), comment="考勤状态：正常/迟到/早退/缺勤")
    note = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    employee = relationship("Employee", back_populates="attendance_records")
