from typing import List, Dict
from sqlalchemy.orm import Session
from .gpt import GPTService
from ..models.resume import Resume
from ..models.job_requirement import JobRequirement

class MatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.gpt = GPTService()

    def find_matching_resumes(self, job_id: int, limit: int = 10) -> List[Dict]:
        """
        查找与职位要求匹配的简历
        
        Args:
            job_id: 职位ID
            limit: 返回的最大简历数量
            
        Returns:
            List[Dict]: 匹配的简历列表，包含匹配分数
        """
        job = self.db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise ValueError("职位不存在")
            
        # 获取所有简历
        resumes = self.db.query(Resume).all()
        matches = []
        
        for resume in resumes:
            try:
                # 计算匹配分数
                match_score = self.gpt.calculate_match_score(
                    resume.to_dict(),
                    job.to_dict()
                )
                
                matches.append({
                    "resume": resume.to_dict(),
                    "match_score": match_score
                })
            except Exception as e:
                print(f"计算简历 {resume.id} 的匹配分数失败: {str(e)}")
                continue
        
        # 按总分排序
        matches.sort(key=lambda x: x["match_score"]["total_score"], reverse=True)
        return matches[:limit]

    def find_matching_jobs(self, resume_id: int, limit: int = 10) -> List[Dict]:
        """
        查找与简历匹配的职位
        
        Args:
            resume_id: 简历ID
            limit: 返回的最大职位数量
            
        Returns:
            List[Dict]: 匹配的职位列表，包含匹配分数
        """
        resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise ValueError("简历不存在")
            
        # 获取所有活跃的职位
        jobs = self.db.query(JobRequirement).filter(
            JobRequirement.status == 'active'
        ).all()
        
        matches = []
        for job in jobs:
            try:
                # 计算匹配分数
                match_score = self.gpt.calculate_match_score(
                    resume.to_dict(),
                    job.to_dict()
                )
                
                matches.append({
                    "job": job.to_dict(),
                    "match_score": match_score
                })
            except Exception as e:
                print(f"计算职位 {job.id} 的匹配分数失败: {str(e)}")
                continue
        
        # 按总分排序
        matches.sort(key=lambda x: x["match_score"]["total_score"], reverse=True)
        return matches[:limit]
