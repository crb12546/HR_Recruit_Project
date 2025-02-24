"""主应用程序"""
from fastapi import FastAPI
from app.routers import jobs, resumes, interviews
from app.routers.onboarding import router as onboarding_router

app = FastAPI(title="智能招聘系统")

# 注册路由
app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(interviews.router)
app.include_router(onboarding_router)

@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
