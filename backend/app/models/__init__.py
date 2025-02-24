"""Models package"""
# Import Base and BaseModel from database.py
from ..database import Base
from .base import BaseModel

# Import models in dependency order
from .tag import Tag  # No dependencies
from .user import User  # No dependencies
from .resume import Resume  # Depends on Tag
from .job_requirement import JobRequirement  # No model dependencies
from .interview import Interview  # Depends on Resume, JobRequirement, User
from .associations import resume_tags  # Association tables

__all__ = ['Base', 'BaseModel', 'Tag', 'User', 'Resume', 'JobRequirement', 'Interview']
