"""主应用程序入口"""
from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers import resumes, jobs, interviews

app = FastAPI(
    title="智能招聘系统",
    description="基于FastAPI的智能招聘系统后端服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 包含API路由
app.include_router(resumes.router, prefix="/api/v1/resumes", tags=["resumes"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(interviews.router, prefix="/api/v1/interviews", tags=["interviews"])

@app.get("/api/v1/health", tags=["health"])
def health_check():
    """健康检查接口"""
    return {"status": "healthy"}
