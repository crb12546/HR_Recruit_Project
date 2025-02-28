"""简历与职位匹配服务模块"""
from typing import Dict, List, Any, Optional, Set
from sqlalchemy.orm import Session

from ..models.resume import Resume
from ..models.job_requirement import JobRequirement
from ..models.tag import Tag
from .service_factory import get_gpt_service

def match_resume_to_job(db: Session, resume_id: int, job_id: int) -> Dict[str, Any]:
    """匹配简历与职位"""
    # 获取简历和职位
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
    
    if not resume or not job:
        return {
            "score": 0,
            "analysis": "简历或职位不存在",
            "matching_points": [],
            "missing_points": []
        }
    
    # 获取GPT服务
    gpt_service = get_gpt_service()
    
    # 基于标签的匹配
    resume_tags = set(tag.name for tag in resume.tags)
    job_tags = set(tag.name for tag in job.tags)
    
    common_tags = resume_tags.intersection(job_tags)
    missing_tags = job_tags - resume_tags
    
    # 计算标签匹配度
    tag_match_score = len(common_tags) / len(job_tags) * 100 if job_tags else 0
    
    # 使用GPT进行深度匹配分析
    try:
        # 尝试使用关键字参数
        match_result = gpt_service.match_job_requirements(
            resume_content=resume.ocr_content,
            job_requirements=job.requirements,
            talent_portrait=resume.talent_portrait
        )
    except TypeError:
        # 如果失败，尝试使用位置参数
        match_result = gpt_service.match_job_requirements(
            resume.ocr_content,
            job.requirements
        )
    
    # 合并结果
    result = {
        "score": match_result.get("score", tag_match_score),
        "analysis": match_result.get("analysis", "基于标签匹配分析"),
        "matching_points": match_result.get("matching_points", list(common_tags)),
        "missing_points": match_result.get("missing_points", list(missing_tags))
    }
    
    return result

def find_matching_jobs(db: Session, resume_id: int, min_score: float = 60.0) -> List[Dict[str, Any]]:
    """查找匹配的职位"""
    # 获取简历
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        return []
    
    # 获取所有开放的职位
    jobs = db.query(JobRequirement).filter(JobRequirement.status == "open").all()
    
    # 匹配结果
    matches = []
    
    for job in jobs:
        match_result = match_resume_to_job(db, resume_id, job.id)
        if match_result["score"] >= min_score:
            matches.append({
                "job_id": job.id,
                "position_name": job.position_name,
                "department": job.department,
                "match_score": match_result["score"],
                "analysis": match_result["analysis"],
                "matching_points": match_result["matching_points"],
                "missing_points": match_result["missing_points"]
            })
    
    # 按匹配度排序
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    
    return matches

def find_matching_resumes(db: Session, job_id: int, min_score: float = 60.0) -> List[Dict[str, Any]]:
    """查找匹配的简历"""
    # 获取职位
    job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
    if not job:
        return []
    
    # 获取所有简历
    resumes = db.query(Resume).all()
    
    # 匹配结果
    matches = []
    
    for resume in resumes:
        match_result = match_resume_to_job(db, resume.id, job_id)
        if match_result["score"] >= min_score:
            matches.append({
                "resume_id": resume.id,
                "candidate_name": resume.candidate_name,
                "match_score": match_result["score"],
                "analysis": match_result["analysis"],
                "matching_points": match_result["matching_points"],
                "missing_points": match_result["missing_points"]
            })
    
    # 按匹配度排序
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    
    return matches
