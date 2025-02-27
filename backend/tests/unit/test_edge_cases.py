import pytest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.interview import Interview
from app.models.onboarding import Onboarding, OnboardingTask
from app.services.ocr_mock import OCRService as MockOCRService
from app.services.gpt_mock import GPTService as MockGPTService
from app.services.storage_mock import StorageService as MockStorageService

class TestEdgeCases:
    """测试边缘情况处理"""
    
    @pytest.mark.asyncio
    async def test_empty_resume_handling(self):
        """测试空简历处理"""
        ocr_service = MockOCRService()
        
        # 模拟空文件URL
        empty_file_url = "https://test-bucket.oss.aliyuncs.com/empty.pdf"
        
        # 测试OCR服务处理空文件
        with patch.object(ocr_service, '_is_file_empty', return_value=True):
            with pytest.raises(ValueError) as excinfo:
                await ocr_service.extract_text_from_url(empty_file_url)
            assert "空文件" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_invalid_file_type_handling(self):
        """测试无效文件类型处理"""
        ocr_service = MockOCRService()
        
        # 模拟无效文件类型
        invalid_file_url = "https://test-bucket.oss.aliyuncs.com/invalid.xyz"
        
        # 测试OCR服务处理无效文件类型
        with patch.object(ocr_service, '_get_file_type', return_value="xyz"):
            with pytest.raises(ValueError) as excinfo:
                await ocr_service.extract_text_from_url(invalid_file_url)
            assert "不支持的文件类型" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_large_file_handling(self):
        """测试大文件处理"""
        storage_service = MockStorageService()
        
        # 模拟大文件上传
        large_file_content = b"x" * (100 * 1024 * 1024 + 1)  # 100MB + 1B
        
        # 测试存储服务处理大文件
        with patch.object(storage_service, '_get_file_size', return_value=100 * 1024 * 1024 + 1):
            with pytest.raises(ValueError) as excinfo:
                await storage_service.upload_file(large_file_content, "large_file.pdf", "application/pdf")
            assert "文件大小超过限制" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_duplicate_tag_handling(self):
        """测试重复标签处理"""
        gpt_service = MockGPTService()
        
        # 模拟GPT服务返回重复标签
        with patch.object(gpt_service, 'generate_resume_tags', return_value=["Python", "Python", "FastAPI"]):
            tags = await gpt_service.generate_resume_tags("简历内容")
            
            # 验证重复标签被去重
            assert len(tags) == 2
            assert "Python" in tags
            assert "FastAPI" in tags
    
    @pytest.mark.asyncio
    async def test_past_interview_scheduling(self):
        """测试过去时间的面试预约处理"""
        # 创建过去的面试时间
        past_time = datetime.now() - timedelta(days=1)
        
        # 创建面试记录
        interview = Interview(
            resume_id=1,
            job_requirement_id=1,
            interviewer_id=1,
            interview_time=past_time,
            status="scheduled"
        )
        
        # 验证面试时间在过去会导致验证错误
        with pytest.raises(ValueError) as excinfo:
            interview.validate_interview_time()
        assert "面试时间不能在过去" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_onboarding_task_deadline_validation(self):
        """测试入职任务截止日期验证"""
        # 创建入职记录
        onboarding = Onboarding(
            id=1,
            resume_id=1,
            job_requirement_id=1,
            status="pending",
            offer_date=datetime.now(),
            start_date=datetime.now() + timedelta(days=30)
        )
        
        # 创建截止日期在入职日期之后的任务
        task = OnboardingTask(
            onboarding_id=1,
            name="完成入职文档",
            description="填写并签署所有入职文档",
            deadline=onboarding.start_date + timedelta(days=1),
            status="pending"
        )
        
        # 验证截止日期在入职日期之后会导致验证错误
        with pytest.raises(ValueError) as excinfo:
            task.validate_deadline(onboarding.start_date)
        assert "任务截止日期必须在入职日期之前" in str(excinfo.value)
