"""面试管理模块单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.interview import Interview
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.user import User
from app.services.gpt import GPTService
from app.routers.interviews import create_interview, get_interview, get_interviews, update_interview, delete_interview

class TestInterviewManagement:
    """面试管理测试类"""
    
    def test_create_interview(self, db: Session):
        """测试创建面试"""
        # 创建测试数据
        resume = Resume(candidate_name="张三", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="Python工程师", department="技术部", status="open")
        interviewer = User(username="interviewer", email="test@example.com", role="interviewer")
        
        db.add(resume)
        db.add(job)
        db.add(interviewer)
        db.commit()
        
        # 面试数据
        interview_time = datetime.now() + timedelta(days=1)
        interview_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "interviewer_id": interviewer.id,
            "interview_time": interview_time.isoformat(),
            "interview_type": "技术面试",
            "status": "scheduled"
        }
        
        # 调用创建面试函数
        interview = create_interview(db=db, interview_data=interview_data)
        
        # 验证结果
        assert interview is not None
        assert interview.resume_id == resume.id
        assert interview.job_requirement_id == job.id
        assert interview.interviewer_id == interviewer.id
        assert interview.interview_type == "技术面试"
        assert interview.status == "scheduled"
    
    def test_get_interview(self, db: Session):
        """测试获取单个面试"""
        # 创建测试数据
        resume = Resume(candidate_name="李四", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="前端工程师", department="技术部", status="open")
        interviewer = User(username="interviewer2", email="test2@example.com", role="interviewer")
        
        db.add(resume)
        db.add(job)
        db.add(interviewer)
        db.commit()
        
        interview = Interview(
            resume_id=resume.id,
            job_requirement_id=job.id,
            interviewer_id=interviewer.id,
            interview_time=datetime.now() + timedelta(days=2),
            interview_type="HR面试",
            status="scheduled"
        )
        db.add(interview)
        db.commit()
        
        # 获取面试
        retrieved_interview = get_interview(db=db, interview_id=interview.id)
        
        # 验证结果
        assert retrieved_interview is not None
        assert retrieved_interview.id == interview.id
        assert retrieved_interview.resume_id == resume.id
        assert retrieved_interview.job_requirement_id == job.id
        assert retrieved_interview.interview_type == "HR面试"
    
    def test_get_interviews(self, db: Session):
        """测试获取面试列表"""
        # 创建测试数据
        resume = Resume(candidate_name="王五", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="测试工程师", department="测试部", status="open")
        interviewer = User(username="interviewer3", email="test3@example.com", role="interviewer")
        
        db.add(resume)
        db.add(job)
        db.add(interviewer)
        db.commit()
        
        interview1 = Interview(
            resume_id=resume.id,
            job_requirement_id=job.id,
            interviewer_id=interviewer.id,
            interview_time=datetime.now() + timedelta(days=3),
            interview_type="技术面试",
            status="scheduled"
        )
        interview2 = Interview(
            resume_id=resume.id,
            job_requirement_id=job.id,
            interviewer_id=interviewer.id,
            interview_time=datetime.now() + timedelta(days=4),
            interview_type="HR面试",
            status="scheduled"
        )
        db.add(interview1)
        db.add(interview2)
        db.commit()
        
        # 获取面试列表
        interviews = get_interviews(db=db, skip=0, limit=10)
        
        # 验证结果
        assert len(interviews) >= 2
        assert any(i.interview_type == "技术面试" for i in interviews)
        assert any(i.interview_type == "HR面试" for i in interviews)
    
    def test_update_interview(self, db: Session):
        """测试更新面试"""
        # 创建测试数据
        resume = Resume(candidate_name="赵六", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="产品经理", department="产品部", status="open")
        interviewer = User(username="interviewer4", email="test4@example.com", role="interviewer")
        
        db.add(resume)
        db.add(job)
        db.add(interviewer)
        db.commit()
        
        interview = Interview(
            resume_id=resume.id,
            job_requirement_id=job.id,
            interviewer_id=interviewer.id,
            interview_time=datetime.now() + timedelta(days=5),
            interview_type="产品面试",
            status="scheduled"
        )
        db.add(interview)
        db.commit()
        
        # 更新数据
        new_time = datetime.now() + timedelta(days=6)
        updated_data = {
            "interview_time": new_time.isoformat(),
            "status": "completed",
            "feedback": "面试表现良好，推荐录用",
            "evaluation_score": 85
        }
        
        # 更新面试
        updated_interview = update_interview(db=db, interview_id=interview.id, interview_data=updated_data)
        
        # 验证结果
        assert updated_interview is not None
        assert updated_interview.status == "completed"
        assert updated_interview.feedback == "面试表现良好，推荐录用"
        assert updated_interview.evaluation_score == 85
        assert updated_interview.interview_type == "产品面试"  # 未更新的字段保持不变
    
    def test_delete_interview(self, db: Session):
        """测试删除面试"""
        # 创建测试数据
        resume = Resume(candidate_name="待删除", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="待删除", department="测试部", status="open")
        interviewer = User(username="interviewer5", email="test5@example.com", role="interviewer")
        
        db.add(resume)
        db.add(job)
        db.add(interviewer)
        db.commit()
        
        interview = Interview(
            resume_id=resume.id,
            job_requirement_id=job.id,
            interviewer_id=interviewer.id,
            interview_time=datetime.now() + timedelta(days=7),
            interview_type="待删除",
            status="scheduled"
        )
        db.add(interview)
        db.commit()
        
        interview_id = interview.id
        
        # 删除面试
        result = delete_interview(db=db, interview_id=interview_id)
        
        # 验证结果
        assert result is True
        
        # 确认已删除
        deleted_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        assert deleted_interview is None
