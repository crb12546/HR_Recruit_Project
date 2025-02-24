"""考勤服务"""
import logging
from datetime import datetime, time, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.onboarding import AttendanceRecord, Employee

logger = logging.getLogger(__name__)

class AttendanceService:
    """考勤服务"""
    
    def __init__(self, db: Session):
        self.db = db
        # 配置工作时间
        self.work_start = time(9, 0)  # 上班时间9:00
        self.work_end = time(18, 0)   # 下班时间18:00
    
    def check_in(
        self,
        employee_id: int,
        check_time: Optional[datetime] = None
    ) -> AttendanceRecord:
        """员工上班打卡"""
        if not check_time:
            check_time = datetime.now()
            
        # 判断是否迟到
        status = "正常" if check_time.time() <= self.work_start else "迟到"
        
        record = AttendanceRecord(
            employee_id=employee_id,
            check_in=check_time,
            status=status
        )
        
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def check_out(
        self,
        employee_id: int,
        check_time: Optional[datetime] = None
    ) -> AttendanceRecord:
        """员工下班打卡"""
        if not check_time:
            check_time = datetime.now()
            
        # 获取当天打卡记录
        record = self.db.query(AttendanceRecord)\
            .filter(
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.check_in >= datetime.combine(check_time.date(), time.min),
                AttendanceRecord.check_in < datetime.combine(check_time.date() + timedelta(days=1), time.min)
            )\
            .first()
            
        if not record:
            raise ValueError("未找到上班打卡记录")
            
        # 更新下班打卡时间和状态
        record.check_out = check_time
        if check_time.time() < self.work_end:
            record.status = "早退"
        elif record.status == "正常":
            record.status = "正常"
            
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def get_monthly_attendance(
        self,
        employee_id: int,
        year: int,
        month: int
    ) -> List[AttendanceRecord]:
        """获取月度考勤记录"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
            
        return self.db.query(AttendanceRecord)\
            .filter(
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.check_in >= start_date,
                AttendanceRecord.check_in < end_date
            )\
            .all()
    
    def get_department_attendance(
        self,
        department: str,
        date: datetime
    ) -> List[dict]:
        """获取部门考勤统计"""
        # 获取部门所有员工
        employees = self.db.query(Employee)\
            .filter(Employee.department == department)\
            .all()
            
        attendance_stats = []
        for employee in employees:
            # 获取当天考勤记录
            record = self.db.query(AttendanceRecord)\
                .filter(
                    AttendanceRecord.employee_id == employee.id,
                    AttendanceRecord.check_in >= datetime.combine(date, time.min),
                    AttendanceRecord.check_in < datetime.combine(date + timedelta(days=1), time.min)
                )\
                .first()
                
            attendance_stats.append({
                "employee_id": employee.id,
                "name": employee.name,
                "status": record.status if record else "缺勤",
                "check_in": record.check_in if record else None,
                "check_out": record.check_out if record else None
            })
            
        return attendance_stats
