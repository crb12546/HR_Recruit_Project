from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .routers import resumes, jobs, interviews

app = FastAPI(title="HR Recruitment System")

# Include API routers
app.include_router(resumes.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(interviews.router, prefix="/api/v1")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "healthy"}
