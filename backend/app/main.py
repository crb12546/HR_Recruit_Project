import os
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import get_db
from .routers import resumes, jobs, interviews, onboardings
from app.config.config import get_config
from app.config.logging_config import get_logger

# 获取日志记录器
logger = get_logger()

# 获取配置
config = get_config()
env = config.ENV

# 创建FastAPI应用
app = FastAPI(
    title="HR招聘系统",
    description="智能招聘平台API",
    version="1.0.0",
    docs_url="/api/docs" if env != "production" else None,
    redoc_url="/api/redoc" if env != "production" else None,
)

# 配置CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://hr-recruitment.example.com",
    "https://test-hr-recruitment.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(resumes.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(interviews.router, prefix="/api/v1")
app.include_router(onboardings.router, prefix="/api/v1")

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP错误: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"服务器错误: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误"},
    )

# 健康检查端点
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    logger.info("健康检查请求")
    return {"status": "healthy", "environment": env}

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info(f"应用启动 (环境: {env})")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用关闭")
