from sqlalchemy.orm import declarative_base, registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

# Import all models to ensure they're registered with Base
from .job_requirement import JobRequirement
from .resume import Resume
from .interview import Interview
from .user import User

__all__ = ['Base', 'JobRequirement', 'Resume', 'Interview', 'User']
