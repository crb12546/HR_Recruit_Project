"""
模型包初始化
"""
# 导入基类
from app.database import Base

# 导入所有模型以确保它们在创建表时被注册
from .job_requirement import JobRequirement
from .resume import Resume
from .interview import Interview
from .user import User
from .tag import Tag
from .onboarding import Onboarding, OnboardingTask

__all__ = ['Base', 'JobRequirement', 'Resume', 'Interview', 'User', 'Tag', 'Onboarding', 'OnboardingTask']
