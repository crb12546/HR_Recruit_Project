"""考勤管理路由"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.onboarding import AttendanceService

router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])

@router.post("/check-in/{employee_id}")
async def check_in(
    employee_id: int,
    check_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """员工上班打卡"""
    service = AttendanceService(db)
    try:
        record = service.check_in(employee_id, check_time)
        return {"message": "打卡成功", "data": record}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/check-out/{employee_id}")
async def check_out(
    employee_id: int,
    check_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """员工下班打卡"""
    service = AttendanceService(db)
    try:
        record = service.check_out(employee_id, check_time)
        return {"message": "打卡成功", "data": record}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/monthly/{employee_id}")
async def get_monthly_attendance(
    employee_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """获取月度考勤记录"""
    service = AttendanceService(db)
    try:
        records = service.get_monthly_attendance(employee_id, year, month)
        return {"message": "获取成功", "data": records}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/department/{department}")
async def get_department_attendance(
    department: str,
    date: datetime,
    db: Session = Depends(get_db)
):
    """获取部门考勤统计"""
    service = AttendanceService(db)
    try:
        stats = service.get_department_attendance(department, date)
        return {"message": "获取成功", "data": stats}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
