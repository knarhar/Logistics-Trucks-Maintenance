from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import IncidentStatusEnum, UUIDMixin, TimestampMixin


class IncidentBase(BaseModel):
    """Base Incident model"""
    truck_id: UUID
    mechanic_id: Optional[UUID] | None
    issue_type: str = Field(..., description="Incident issue type")
    description: Optional[str] = None
    photo_url: Optional[str] = None
    photo_public_id: Optional[str] = None
    status: IncidentStatusEnum = IncidentStatusEnum.PLANNED


class IncidentCreate(IncidentBase):
    """Incident create model"""
    pass


class IncidentUpdate(BaseModel):
    """Incident update model"""
    mechanic_id: Optional[UUID] = None
    description: Optional[str] = None
    status: Optional[IncidentStatusEnum] = None
    photo_url: Optional[str] = None
    photo_public_id: Optional[str] = None


class IncidentResponse(UUIDMixin, TimestampMixin, IncidentBase):
    """Incident response model"""

    class Config:
        form_attributes = True
