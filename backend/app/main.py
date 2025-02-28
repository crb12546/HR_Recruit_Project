import os
import time
import dotenv
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import get_db, init_db
from .routers import resumes_router, jobs_router, interviews_router, onboardings_router
from app.config.config import get_config, reload_config
from app.config.logging_config import get_logger
from app.middleware.db_session import DBSessionMiddleware

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
    "*",  # 允许所有来源，用于开发和测试
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加数据库会话中间件
app.add_middleware(DBSessionMiddleware)

# 包含API路由
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(interviews_router)
app.include_router(onboardings_router)

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
    try:
        # 尝试执行一个简单的数据库查询来验证数据库连接
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        db_status = "disconnected"
    
    return {
        "status": "healthy", 
        "environment": env,
        "database": db_status,
        "timestamp": time.time()
    }

# 启动事件
@app.on_event("startup")
async def startup_event():
    # 加载环境变量
    env_file = f".env.{env.lower()}"
    if os.path.exists(env_file):
        logger.info(f"从 {env_file} 加载环境变量")
        dotenv.load_dotenv(env_file)
        # 重新加载配置
        reload_config()
    else:
        logger.warning(f"环境变量文件 {env_file} 不存在")
    
    logger.info(f"应用启动 (环境: {env})")
    
    # 初始化数据库
    db_initialized = init_db()
    if db_initialized:
        logger.info("数据库初始化成功")
    else:
        logger.warning("数据库初始化失败，应用可能无法正常工作")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用关闭")
