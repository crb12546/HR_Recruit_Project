"""简历匹配服务"""
from dataclasses import dataclass
from typing import List, Dict
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.services.gpt import GPTService

@dataclass
class MatchResult:
    """匹配结果"""
    score: float  # 0-100的匹配度分数
    details: Dict[str, float]  # 各维度的匹配分数
    recommendations: List[str]  # 改进建议

class MatchingService:
    """简历匹配服务"""
    
    def __init__(self):
        self.gpt_service = GPTService()
    
    def calculate_match(
        self,
        resume: Resume,
        job_requirement: JobRequirement
    ) -> MatchResult:
        """计算简历与职位需求的匹配度"""
        # 准备匹配数据
        resume_data = {
            "content": resume.ocr_content,
            "tags": [tag.name for tag in resume.tags],
            "talent_portrait": resume.talent_portrait
        }
        
        job_data = {
            "title": job_requirement.position_name,
            "responsibilities": job_requirement.responsibilities,
            "requirements": job_requirement.requirements,
            "department": job_requirement.department
        }
        
        # 使用GPT-4进行匹配分析
        match_analysis = self.gpt_service.analyze_resume_match(
            resume_data=resume_data,
            job_data=job_data
        )
        
        # 解析匹配结果
        score = match_analysis.get("overall_score", 0)
        details = match_analysis.get("dimension_scores", {})
        recommendations = match_analysis.get("recommendations", [])
        
        return MatchResult(
            score=score,
            details=details,
            recommendations=recommendations
        )
    
    def rank_resumes(
        self,
        resumes: List[Resume],
        job_requirement: JobRequirement
    ) -> List[Dict]:
        """对多份简历进行排序"""
        matches = []
        for resume in resumes:
            match_result = self.calculate_match(resume, job_requirement)
            matches.append({
                "resume": resume,
                "score": match_result.score,
                "details": match_result.details,
                "recommendations": match_result.recommendations
            })
        
        # 按匹配度降序排序
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches
