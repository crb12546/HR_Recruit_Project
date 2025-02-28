"""入职管理模块单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.onboarding import Onboarding, OnboardingTask
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.services.gpt import GPTService
from app.routers.onboardings import create_onboarding, get_onboarding, get_onboardings, update_onboarding, delete_onboarding

class TestOnboardingManagement:
    """入职管理测试类"""
    
    def test_create_onboarding(self, db: Session, monkeypatch):
        """测试创建入职记录"""
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.generate_onboarding_tasks.return_value = [
            {"title": "完成入职文档", "description": "填写并提交所有入职文档", "deadline": 1},
            {"title": "参加入职培训", "description": "参加公司入职培训", "deadline": 3},
            {"title": "配置开发环境", "description": "安装和配置开发环境", "deadline": 2}
        ]
        
        # 打补丁替换服务
        monkeypatch.setattr("app.routers.onboardings.get_gpt_service", lambda: mock_gpt)
        
        # 创建测试数据
        resume = Resume(candidate_name="张三", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="Python工程师", department="技术部", status="open")
        
        db.add(resume)
        db.add(job)
        db.commit()
        
        # 入职数据
        start_date = datetime.now() + timedelta(days=14)
        onboarding_data = {
            "resume_id": resume.id,
            "job_requirement_id": job.id,
            "department": "技术部",
            "position": "Python高级工程师",
            "salary": "30k",
            "offer_date": datetime.now().isoformat(),
            "start_date": start_date.isoformat(),
            "probation_end_date": (start_date + timedelta(days=90)).isoformat(),
            "status": "pending",
            "notes": "优秀候选人，尽快入职",
            "generate_tasks": True
        }
        
        # 调用创建入职记录函数
        onboarding = create_onboarding(db=db, onboarding_data=onboarding_data)
        
        # 验证结果
        assert onboarding is not None
        assert onboarding.resume_id == resume.id
        assert onboarding.job_requirement_id == job.id
        assert onboarding.department == "技术部"
        assert onboarding.position == "Python高级工程师"
        assert onboarding.salary == "30k"
        assert onboarding.status == "pending"
        
        # 验证任务生成
        assert len(onboarding.tasks) >= 3
        assert any(task.title == "完成入职文档" for task in onboarding.tasks)
        assert any(task.title == "参加入职培训" for task in onboarding.tasks)
        assert any(task.title == "配置开发环境" for task in onboarding.tasks)
        
        # 验证服务调用
        mock_gpt.generate_onboarding_tasks.assert_called_once()
    
    def test_get_onboarding(self, db: Session):
        """测试获取单个入职记录"""
        # 创建测试数据
        resume = Resume(candidate_name="李四", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="前端工程师", department="技术部", status="open")
        
        db.add(resume)
        db.add(job)
        db.commit()
        
        onboarding = Onboarding(
            resume_id=resume.id,
            job_requirement_id=job.id,
            department="技术部",
            position="前端工程师",
            salary="25k",
            offer_date=datetime.now(),
            start_date=datetime.now() + timedelta(days=14),
            probation_end_date=datetime.now() + timedelta(days=104),
            status="pending"
        )
        db.add(onboarding)
        db.commit()
        
        # 添加任务
        task1 = OnboardingTask(
            onboarding_id=onboarding.id,
            title="完成入职文档",
            description="填写并提交所有入职文档",
            deadline=datetime.now() + timedelta(days=15),
            status="pending"
        )
        task2 = OnboardingTask(
            onboarding_id=onboarding.id,
            title="参加入职培训",
            description="参加公司入职培训",
            deadline=datetime.now() + timedelta(days=17),
            status="pending"
        )
        db.add(task1)
        db.add(task2)
        db.commit()
        
        # 获取入职记录
        retrieved_onboarding = get_onboarding(db=db, onboarding_id=onboarding.id)
        
        # 验证结果
        assert retrieved_onboarding is not None
        assert retrieved_onboarding.id == onboarding.id
        assert retrieved_onboarding.resume_id == resume.id
        assert retrieved_onboarding.job_requirement_id == job.id
        assert retrieved_onboarding.position == "前端工程师"
        assert len(retrieved_onboarding.tasks) == 2
        assert any(task.title == "完成入职文档" for task in retrieved_onboarding.tasks)
        assert any(task.title == "参加入职培训" for task in retrieved_onboarding.tasks)
    
    def test_get_onboardings(self, db: Session):
        """测试获取入职记录列表"""
        # 创建测试数据
        resume1 = Resume(candidate_name="王五", file_url="url1", file_type="pdf")
        resume2 = Resume(candidate_name="赵六", file_url="url2", file_type="pdf")
        job1 = JobRequirement(position_name="测试工程师", department="测试部", status="open")
        job2 = JobRequirement(position_name="产品经理", department="产品部", status="open")
        
        db.add(resume1)
        db.add(resume2)
        db.add(job1)
        db.add(job2)
        db.commit()
        
        onboarding1 = Onboarding(
            resume_id=resume1.id,
            job_requirement_id=job1.id,
            department="测试部",
            position="测试工程师",
            status="pending"
        )
        onboarding2 = Onboarding(
            resume_id=resume2.id,
            job_requirement_id=job2.id,
            department="产品部",
            position="产品经理",
            status="in_progress"
        )
        db.add(onboarding1)
        db.add(onboarding2)
        db.commit()
        
        # 获取入职记录列表
        onboardings = get_onboardings(db=db, skip=0, limit=10)
        
        # 验证结果
        assert len(onboardings) >= 2
        assert any(o.position == "测试工程师" for o in onboardings)
        assert any(o.position == "产品经理" for o in onboardings)
    
    def test_update_onboarding(self, db: Session):
        """测试更新入职记录"""
        # 创建测试数据
        resume = Resume(candidate_name="测试更新", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="测试职位", department="测试部", status="open")
        
        db.add(resume)
        db.add(job)
        db.commit()
        
        onboarding = Onboarding(
            resume_id=resume.id,
            job_requirement_id=job.id,
            department="测试部",
            position="测试职位",
            salary="20k",
            status="pending"
        )
        db.add(onboarding)
        db.commit()
        
        # 更新数据
        updated_data = {
            "salary": "25k",
            "status": "in_progress",
            "notes": "已完成入职准备"
        }
        
        # 更新入职记录
        updated_onboarding = update_onboarding(db=db, onboarding_id=onboarding.id, onboarding_data=updated_data)
        
        # 验证结果
        assert updated_onboarding is not None
        assert updated_onboarding.salary == "25k"
        assert updated_onboarding.status == "in_progress"
        assert updated_onboarding.notes == "已完成入职准备"
        assert updated_onboarding.position == "测试职位"  # 未更新的字段保持不变
    
    def test_delete_onboarding(self, db: Session):
        """测试删除入职记录"""
        # 创建测试数据
        resume = Resume(candidate_name="待删除", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="待删除", department="测试部", status="open")
        
        db.add(resume)
        db.add(job)
        db.commit()
        
        onboarding = Onboarding(
            resume_id=resume.id,
            job_requirement_id=job.id,
            department="测试部",
            position="待删除",
            status="pending"
        )
        db.add(onboarding)
        db.commit()
        
        onboarding_id = onboarding.id
        
        # 删除入职记录
        result = delete_onboarding(db=db, onboarding_id=onboarding_id)
        
        # 验证结果
        assert result is True
        
        # 确认已删除
        deleted_onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()
        assert deleted_onboarding is None
    
    def test_onboarding_task_management(self, db: Session):
        """测试入职任务管理"""
        # 创建测试数据
        resume = Resume(candidate_name="任务测试", file_url="url", file_type="pdf")
        job = JobRequirement(position_name="任务测试", department="测试部", status="open")
        
        db.add(resume)
        db.add(job)
        db.commit()
        
        onboarding = Onboarding(
            resume_id=resume.id,
            job_requirement_id=job.id,
            department="测试部",
            position="任务测试",
            status="pending"
        )
        db.add(onboarding)
        db.commit()
        
        # 添加任务
        task = OnboardingTask(
            onboarding_id=onboarding.id,
            title="测试任务",
            description="测试任务描述",
            deadline=datetime.now() + timedelta(days=5),
            status="pending"
        )
        db.add(task)
        db.commit()
        
        # 更新任务
        task.status = "completed"
        db.commit()
        
        # 获取任务
        retrieved_task = db.query(OnboardingTask).filter(OnboardingTask.id == task.id).first()
        
        # 验证结果
        assert retrieved_task is not None
        assert retrieved_task.status == "completed"
        assert retrieved_task.title == "测试任务"
        
        # 验证关联
        retrieved_onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding.id).first()
        assert len(retrieved_onboarding.tasks) == 1
        assert retrieved_onboarding.tasks[0].id == task.id
