"""员工服务"""
import logging
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.onboarding import Employee, EmployeeDocument
from app.models.resume import Resume

logger = logging.getLogger(__name__)

class EmployeeService:
    """员工服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_employee(
        self,
        name: str,
        department: str,
        position: str,
        entry_date: datetime,
        resume_id: Optional[int] = None
    ) -> Employee:
        """创建新员工"""
        try:
            # 生成工号
            employee_id = self._generate_employee_id()
            
            employee = Employee(
                name=name,
                employee_id=employee_id,
                department=department,
                position=position,
                entry_date=entry_date,
                resume_id=resume_id
            )
            
            self.db.add(employee)
            self.db.commit()
            self.db.refresh(employee)
            
            return employee
            
        except Exception as e:
            logger.error(f"创建员工失败: {str(e)}")
            self.db.rollback()
            raise
    
    def _generate_employee_id(self) -> str:
        """生成工号"""
        # 格式：年月日 + 4位序号
        date_prefix = datetime.now().strftime("%Y%m")
        
        # 获取当天最大工号
        latest_employee = self.db.query(Employee)\
            .filter(Employee.employee_id.like(f"{date_prefix}%"))\
            .order_by(Employee.employee_id.desc())\
            .first()
            
        if latest_employee:
            sequence = int(latest_employee.employee_id[-4:]) + 1
        else:
            sequence = 1
            
        return f"{date_prefix}{sequence:04d}"
    
    def update_employee_status(
        self,
        employee_id: int,
        status: str
    ) -> Employee:
        """更新员工状态"""
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise ValueError("员工不存在")
            
        employee.status = status
        self.db.commit()
        self.db.refresh(employee)
        return employee
    
    def add_document(
        self,
        employee_id: int,
        document_type: str,
        file_url: str,
        file_name: str,
        note: Optional[str] = None
    ) -> EmployeeDocument:
        """添加员工档案"""
        document = EmployeeDocument(
            employee_id=employee_id,
            document_type=document_type,
            file_url=file_url,
            file_name=file_name,
            note=note
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document
    
    def get_employee_documents(
        self,
        employee_id: int
    ) -> List[EmployeeDocument]:
        """获取员工档案"""
        return self.db.query(EmployeeDocument)\
            .filter(EmployeeDocument.employee_id == employee_id)\
            .all()
