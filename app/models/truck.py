"""
Truck model
"""
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.db.base import Base
import uuid

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plate_number = Column(String(20), unique=True, nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def soft_delete(self, db: Session):
        """Mark truck as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()
        db.commit()