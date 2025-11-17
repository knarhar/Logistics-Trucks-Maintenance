"""
Incident model
"""
import uuid
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey

from app.db.base import Base
from app.schemas.common import IncidentStatusEnum


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    truck_id = Column(UUID, ForeignKey("trucks.id"))
    mechanic_id = Column(UUID, ForeignKey("mechanics.id"), nullable=True)
    status = Column(Enum(IncidentStatusEnum))
    issue_type = Column(String, nullable=False)
    description = Column(String)
    photo_url = Column(String, nullable=True)
    photo_public_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    truck = relationship('Truck', backref='incidents')
    mechanic = relationship('Mechanic', backref='mechanics')

    def __repr__(self):
        return f"<Incident {self.issue_type} ({self.status})>"
