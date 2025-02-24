"""面试服务"""
import logging
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.interview import Interview
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.user import User
from app.services.gpt import GPTService

logger = logging.getLogger(__name__)

class InterviewService:
    """面试服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.gpt = GPTService()
    
    def schedule_interview(
        self,
        resume_id: int,
        job_id: int,
        interviewer_id: int,
        scheduled_time: datetime
    ) -> Interview:
        """安排面试"""
        # 验证数据存在
        resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
        job = self.db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        interviewer = self.db.query(User).filter(User.id == interviewer_id).first()
        
        if not all([resume, job, interviewer]):
            raise ValueError("简历、职位或面试官不存在")
            
        # 创建面试记录
        interview = Interview(
            resume_id=resume_id,
            job_id=job_id,
            interviewer_id=interviewer_id,
            status="已安排",
            scheduled_time=scheduled_time
        )
        
        # 生成面试问题
        interview.questions = self.generate_interview_questions(resume, job)
        
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        
        return interview
    
    def generate_interview_questions(
        self,
        resume: Resume,
        job: JobRequirement
    ) -> List[Dict[str, str]]:
        """生成面试问题"""
        prompt = f"""
        请根据以下信息生成面试问题：
        
        候选人信息：
        {resume.ocr_content}
        
        职位要求：
        {job.requirements}
        
        要求：
        1. 生成5-8个针对性问题
        2. 包含技术问题和软实力问题
        3. 问题应该有梯度，由浅入深
        4. 返回JSON格式，每个问题包含：
           - question: 问题内容
           - type: 问题类型（技术/软实力）
           - purpose: 考察目的
        """
        
        try:
            questions = self.gpt.generate_interview_questions(prompt)
            return questions
        except Exception as e:
            logger.error(f"生成面试问题失败: {str(e)}")
            return []
    
    def start_interview(self, interview_id: int) -> Interview:
        """开始面试"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise ValueError("面试不存在")
            
        interview.status = "进行中"
        interview.actual_start_time = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(interview)
        return interview
    
    def end_interview(
        self,
        interview_id: int,
        feedback: str,
        score: int
    ) -> Interview:
        """结束面试"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise ValueError("面试不存在")
            
        interview.status = "已完成"
        interview.actual_end_time = datetime.utcnow()
        interview.feedback = feedback
        interview.score = score
        
        self.db.commit()
        self.db.refresh(interview)
        return interview
    
    def cancel_interview(self, interview_id: int, reason: str) -> Interview:
        """取消面试"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise ValueError("面试不存在")
            
        interview.status = "已取消"
        interview.feedback = f"取消原因: {reason}"
        
        self.db.commit()
        self.db.refresh(interview)
        return interview
    
    def get_interviewer_schedule(
        self,
        interviewer_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[Interview]:
        """获取面试官的面试安排"""
        return self.db.query(Interview).filter(
            Interview.interviewer_id == interviewer_id,
            Interview.scheduled_time >= start_date,
            Interview.scheduled_time <= end_date
        ).all()
