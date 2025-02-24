"""入职管理模块模型"""
from .employee import Employee
from .attendance import AttendanceRecord
from .document import EmployeeDocument

__all__ = ["Employee", "AttendanceRecord", "EmployeeDocument"]
