"""
API路由模块
"""
from .resumes import router as resumes_router
from .jobs import router as jobs_router
from .interviews import router as interviews_router
from .onboardings import router as onboardings_router

# 导出路由器
__all__ = ["resumes_router", "jobs_router", "interviews_router", "onboardings_router"]
