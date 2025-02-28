"""面试管理集成测试"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview
from app.models.user import User
from app.services.gpt import GPTService
from app.services.notification import NotificationService
from app.routers.interviews import create_interview, update_interview, get_interviews_by_resume

class TestInterviewManagement:
    """面试管理集成测试类"""
    
    @pytest.fixture
    def mock_services(self, monkeypatch):
        """模拟服务"""
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.generate_interview_questions.return_value = [
            "问题1：请描述您的工作经验？",
            "问题2：您如何处理工作中的压力？",
            "问题3：您为什么选择应聘我们公司？"
        ]
        mock_gpt.analyze_interview_feedback.return_value = {
            "strengths": ["技术能力强", "沟通能力好"],
            "weaknesses": ["项目经验不足"],
            "recommendation": "建议录用",
            "fit_score": 85
        }
        
        # 模拟通知服务
        mock_notification = MagicMock()
        mock_notification.send_interview_invitation.return_value = True
        mock_notification.send_interview_feedback.return_value = True
        
        # 打补丁替换服务
        monkeypatch.setattr("app.routers.interviews.get_gpt_service", lambda: mock_gpt)
        monkeypatch.setattr("app.services.notification.get_notification_service", lambda: mock_notification)
        
        return {"gpt": mock_gpt, "notification": mock_notification}
    
    def test_interview_scheduling_and_feedback(self, db: Session, mock_services):
        """测试面试安排和反馈流程"""
        # 创建测试数据
        resume = Resume(candidate_name="张三", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="Python工程师", department="技术部", status="open")
        interviewer1 = User(username="tech_interviewer", email="tech@example.com", role="interviewer")
        interviewer2 = User(username="hr_interviewer", email="hr@example.com", role="hr")
        
        db.add(resume)
        db.add(job)
        db.add(interviewer1)
        db.add(interviewer2)
        db.commit()
        
        # 安排技术面试
        tech_interview_time = datetime.now() + timedelta(days=1)
        tech_interview_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "interviewer_id": interviewer1.id,
            "interview_time": tech_interview_time.isoformat(),
            "interview_type": "技术面试",
            "status": "scheduled",
            "send_notification": True
        }
        
        tech_interview = create_interview(db=db, interview_data=tech_interview_data)
        assert tech_interview is not None
        assert tech_interview.status == "scheduled"
        assert tech_interview.interview_type == "技术面试"
        
        # 验证通知发送
        mock_services["notification"].send_interview_invitation.assert_called_once()
        
        # 更新技术面试结果
        tech_feedback_data = {
            "status": "completed",
            "feedback": "技术能力强，项目经验丰富，推荐进入HR面试",
            "evaluation_score": 90,
            "send_notification": True
        }
        
        updated_tech_interview = update_interview(db=db, interview_id=tech_interview.id, interview_data=tech_feedback_data)
        assert updated_tech_interview is not None
        assert updated_tech_interview.status == "completed"
        assert updated_tech_interview.evaluation_score == 90
        
        # 验证反馈通知发送
        mock_services["notification"].send_interview_feedback.assert_called_once()
        
        # 安排HR面试
        hr_interview_time = datetime.now() + timedelta(days=2)
        hr_interview_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "interviewer_id": interviewer2.id,
            "interview_time": hr_interview_time.isoformat(),
            "interview_type": "HR面试",
            "status": "scheduled",
            "send_notification": True
        }
        
        hr_interview = create_interview(db=db, interview_data=hr_interview_data)
        assert hr_interview is not None
        assert hr_interview.status == "scheduled"
        assert hr_interview.interview_type == "HR面试"
        
        # 验证通知发送
        assert mock_services["notification"].send_interview_invitation.call_count == 2
        
        # 更新HR面试结果
        hr_feedback_data = {
            "status": "completed",
            "feedback": "沟通能力好，团队意识强，薪资期望合理",
            "evaluation_score": 85,
            "send_notification": True
        }
        
        updated_hr_interview = update_interview(db=db, interview_id=hr_interview.id, interview_data=hr_feedback_data)
        assert updated_hr_interview is not None
        assert updated_hr_interview.status == "completed"
        assert updated_hr_interview.evaluation_score == 85
        
        # 验证反馈通知发送
        assert mock_services["notification"].send_interview_feedback.call_count == 2
        
        # 获取候选人的所有面试记录
        interviews = get_interviews_by_resume(db=db, resume_id=resume.id)
        
        # 验证结果
        assert len(interviews) == 2
        assert any(i.interview_type == "技术面试" for i in interviews)
        assert any(i.interview_type == "HR面试" for i in interviews)
        assert all(i.status == "completed" for i in interviews)
        
        # 验证GPT服务调用
        assert mock_services["gpt"].generate_interview_questions.call_count >= 1
        assert mock_services["gpt"].analyze_interview_feedback.call_count >= 1
