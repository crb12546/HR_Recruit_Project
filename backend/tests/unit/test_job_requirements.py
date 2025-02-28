"""职位需求管理模块单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.models.job_requirement import JobRequirement
from app.models.tag import Tag
from app.services.gpt import GPTService
from app.routers.jobs import create_job_requirement, get_job_requirement, get_job_requirements, update_job_requirement, delete_job_requirement

class TestJobRequirementManagement:
    """职位需求管理测试类"""
    
    def test_create_job_requirement(self, db: Session, monkeypatch):
        """测试创建职位需求"""
        # 模拟GPT服务
        mock_gpt = MagicMock()
        mock_gpt.generate_interview_questions.return_value = [
            "问题1：请描述您的工作经验？",
            "问题2：您如何处理工作中的压力？"
        ]
        
        # 打补丁替换服务
        monkeypatch.setattr("app.routers.jobs.get_gpt_service", lambda: mock_gpt)
        
        # 创建测试数据
        job_data = {
            "position_name": "Python高级工程师",
            "department": "技术部",
            "job_description": "负责后端系统开发和维护",
            "requirements": "5年以上Python开发经验，熟悉FastAPI框架",
            "salary_range": "25k-35k",
            "status": "open"
        }
        
        # 调用创建职位需求函数
        job = create_job_requirement(db=db, job_data=job_data)
        
        # 验证结果
        assert job is not None
        assert job.position_name == "Python高级工程师"
        assert job.department == "技术部"
        assert job.job_description == "负责后端系统开发和维护"
        assert job.requirements == "5年以上Python开发经验，熟悉FastAPI框架"
        assert job.salary_range == "25k-35k"
        assert job.status == "open"
        assert len(job.interview_questions) >= 2
        assert "问题1" in job.interview_questions
        
        # 验证服务调用
        mock_gpt.generate_interview_questions.assert_called_once()
    
    def test_get_job_requirement(self, db: Session):
        """测试获取单个职位需求"""
        # 创建测试数据
        job = JobRequirement(
            position_name="前端开发工程师",
            department="技术部",
            job_description="负责前端开发",
            requirements="熟悉Vue.js",
            salary_range="20k-30k",
            status="open",
            interview_questions="问题1：请描述您的Vue.js经验？\n问题2：您如何优化前端性能？"
        )
        db.add(job)
        db.commit()
        
        # 获取职位需求
        retrieved_job = get_job_requirement(db=db, job_id=job.id)
        
        # 验证结果
        assert retrieved_job is not None
        assert retrieved_job.id == job.id
        assert retrieved_job.position_name == "前端开发工程师"
        assert retrieved_job.department == "技术部"
        assert "Vue.js" in retrieved_job.interview_questions
    
    def test_get_job_requirements(self, db: Session):
        """测试获取职位需求列表"""
        # 创建测试数据
        job1 = JobRequirement(position_name="产品经理", department="产品部", status="open")
        job2 = JobRequirement(position_name="UI设计师", department="设计部", status="open")
        db.add(job1)
        db.add(job2)
        db.commit()
        
        # 获取职位需求列表
        jobs = get_job_requirements(db=db, skip=0, limit=10)
        
        # 验证结果
        assert len(jobs) >= 2
        assert any(j.position_name == "产品经理" for j in jobs)
        assert any(j.position_name == "UI设计师" for j in jobs)
    
    def test_update_job_requirement(self, db: Session):
        """测试更新职位需求"""
        # 创建测试数据
        job = JobRequirement(
            position_name="测试工程师",
            department="测试部",
            job_description="负责系统测试",
            requirements="熟悉自动化测试",
            salary_range="15k-25k",
            status="open"
        )
        db.add(job)
        db.commit()
        
        # 更新数据
        updated_data = {
            "position_name": "高级测试工程师",
            "salary_range": "20k-30k",
            "status": "closed"
        }
        
        # 更新职位需求
        updated_job = update_job_requirement(db=db, job_id=job.id, job_data=updated_data)
        
        # 验证结果
        assert updated_job is not None
        assert updated_job.position_name == "高级测试工程师"
        assert updated_job.salary_range == "20k-30k"
        assert updated_job.status == "closed"
        assert updated_job.department == "测试部"  # 未更新的字段保持不变
    
    def test_delete_job_requirement(self, db: Session):
        """测试删除职位需求"""
        # 创建测试数据
        job = JobRequirement(position_name="待删除职位", department="测试部", status="open")
        db.add(job)
        db.commit()
        
        job_id = job.id
        
        # 删除职位需求
        result = delete_job_requirement(db=db, job_id=job_id)
        
        # 验证结果
        assert result is True
        
        # 确认已删除
        deleted_job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        assert deleted_job is None
    
    def test_job_tag_relationship(self, db: Session):
        """测试职位与标签的关联关系"""
        # 创建测试数据
        job = JobRequirement(position_name="测试标签关联", department="技术部", status="open")
        tag1 = Tag(name="Python")
        tag2 = Tag(name="FastAPI")
        
        # 建立关联
        job.tags.append(tag1)
        job.tags.append(tag2)
        
        db.add(job)
        db.add(tag1)
        db.add(tag2)
        db.commit()
        
        # 获取职位及其标签
        retrieved_job = db.query(JobRequirement).filter(JobRequirement.id == job.id).first()
        
        # 验证结果
        assert retrieved_job is not None
        assert len(retrieved_job.tags) == 2
        assert any(tag.name == "Python" for tag in retrieved_job.tags)
        assert any(tag.name == "FastAPI" for tag in retrieved_job.tags)
