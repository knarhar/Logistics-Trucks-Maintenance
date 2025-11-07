"""
Mechanic model
"""
import enum, uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.db.base import Base


class ExpertiseEnum(str, enum.Enum):
    ENGINE = 'engine'
    TRANSMISSION = 'transmission'
    TIRES = 'tires'
    ELECTRICAL = "electrical"
    SUSPENSION = "suspension"


class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    expertise = Column(Enum(ExpertiseEnum), nullable=False)
    performance_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
