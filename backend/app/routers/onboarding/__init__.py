"""入职管理路由模块"""
from fastapi import APIRouter
from .employee import router as employee_router
from .attendance import router as attendance_router

router = APIRouter(prefix="/api/v1/onboarding")

router.include_router(employee_router)
router.include_router(attendance_router)

__all__ = ["router"]
