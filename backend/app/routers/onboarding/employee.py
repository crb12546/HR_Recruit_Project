"""员工管理路由"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.onboarding import EmployeeService
from app.services.storage import StorageService

router = APIRouter(prefix="/api/v1/employees", tags=["employees"])

@router.post("/")
async def create_employee(
    name: str,
    department: str,
    position: str,
    entry_date: datetime,
    resume_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """创建新员工"""
    service = EmployeeService(db)
    try:
        employee = service.create_employee(
            name=name,
            department=department,
            position=position,
            entry_date=entry_date,
            resume_id=resume_id
        )
        return {"message": "创建成功", "data": employee}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{employee_id}/status")
async def update_status(
    employee_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """更新员工状态"""
    service = EmployeeService(db)
    try:
        employee = service.update_employee_status(employee_id, status)
        return {"message": "更新成功", "data": employee}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{employee_id}/documents")
async def upload_document(
    employee_id: int,
    document_type: str,
    file: UploadFile = File(...),
    note: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """上传员工档案"""
    employee_service = EmployeeService(db)
    storage_service = StorageService()
    
    try:
        # 上传文件
        content = await file.read()
        file_url = storage_service.upload_file(content, file.filename)
        
        # 保存档案记录
        document = employee_service.add_document(
            employee_id=employee_id,
            document_type=document_type,
            file_url=file_url,
            file_name=file.filename,
            note=note
        )
        return {"message": "上传成功", "data": document}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{employee_id}/documents")
async def get_documents(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """获取员工档案"""
    service = EmployeeService(db)
    try:
        documents = service.get_employee_documents(employee_id)
        return {"message": "获取成功", "data": documents}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
