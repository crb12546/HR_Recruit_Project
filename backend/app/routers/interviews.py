"""面试管理路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.interview import Interview

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.get("/")
def list_interviews(db: Session = Depends(get_db)):
    """获取面试列表"""
    interviews = db.query(Interview).all()
    return [interview.to_dict() for interview in interviews]

@router.get("/{interview_id}")
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    """获取面试详情"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    return interview.to_dict()
