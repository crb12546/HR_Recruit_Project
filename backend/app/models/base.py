"""Base model for SQLAlchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

# Import Base from database.py to ensure single instance
from app.database import Base

class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
