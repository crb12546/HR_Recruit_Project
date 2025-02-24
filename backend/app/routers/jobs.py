"""职位需求路由"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel
from app.database import get_db
from app.models.job_requirement import JobRequirement
from app.services.gpt import GPTService

class JobCreate(BaseModel):
    position_name: str
    department: str | None = None
    responsibilities: str
    requirements: str
    salary_range: str | None = None
    location: str | None = None

router = APIRouter()

@router.get("/", response_model=List[dict])
def list_jobs(db: Session = Depends(get_db)):
    """获取职位列表"""
    jobs = db.query(JobRequirement).all()
    return [job.to_dict() for job in jobs]

@router.get("/{job_id}", response_model=dict)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """获取职位详情"""
    job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    return job.to_dict()

@router.post("/", response_model=dict, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    """创建新职位"""
    # 使用GPT服务提取标签
    gpt = GPTService()
    tags = gpt.extract_job_tags(
        f"{job_data.position_name}\n{job_data.responsibilities}\n{job_data.requirements}"
    )
    
    # 创建职位记录
    job = JobRequirement(
        position_name=job_data.position_name,
        department=job_data.department,
        responsibilities=job_data.responsibilities,
        requirements=job_data.requirements,
        salary_range=job_data.salary_range,
        location=job_data.location,
        tags=tags
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    return job.to_dict()

@router.get("/{job_id}/matches", response_model=dict)
def get_job_matches(job_id: int, db: Session = Depends(get_db)):
    """获取职位匹配的简历"""
    job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    
    # 根据标签匹配简历
    matched_resumes = []
    for resume in job.matched_resumes:
        matched_resumes.append(resume.to_dict())
    
    return {"matches": matched_resumes}
