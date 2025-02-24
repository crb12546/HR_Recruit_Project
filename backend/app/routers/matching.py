from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.matching import MatchingService

router = APIRouter(prefix="/api/v1/matching", tags=["matching"])

@router.get("/jobs/{resume_id}")
async def get_matching_jobs(
    resume_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    获取与简历匹配的职位列表
    
    Args:
        resume_id: 简历ID
        limit: 返回的最大职位数量
        db: 数据库会话
        
    Returns:
        List[dict]: 匹配的职位列表
    """
    try:
        matching_service = MatchingService(db)
        matches = matching_service.find_matching_jobs(resume_id, limit)
        return matches
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匹配失败: {str(e)}")

@router.get("/resumes/{job_id}")
async def get_matching_resumes(
    job_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    获取与职位匹配的简历列表
    
    Args:
        job_id: 职位ID
        limit: 返回的最大简历数量
        db: 数据库会话
        
    Returns:
        List[dict]: 匹配的简历列表
    """
    try:
        matching_service = MatchingService(db)
        matches = matching_service.find_matching_resumes(job_id, limit)
        return matches
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匹配失败: {str(e)}")
