"""
 Incident model Pydantic schemas
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.core.exceptions import ValidationException
from app.schemas.common import IncidentStatusEnum, UUIDMixin, TimestampMixin


class IncidentBase(BaseModel):
    """Base Incident model"""
    truck_id: UUID
    mechanic_id: Optional[UUID] | None
    issue_type: str = Field(..., description="Incident issue type")
    description: Optional[str] = None
    photo_url: Optional[str] = None
    photo_public_id: Optional[str] = None
    status: Optional[IncidentStatusEnum] = IncidentStatusEnum.PLANNED

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None or value == "":
            return None

        allowed = [e for e in IncidentStatusEnum]
        if value not in allowed:
            raise ValidationException(f"Invalid status value '{value}'. Allowed:  {', '.join(allowed)}")

        return value


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

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None or value == "":
            return None

        allowed = [e for e in IncidentStatusEnum]
        if value not in allowed:
            raise ValidationException(f"Invalid status value '{value}'. Allowed:  {', '.join(allowed)}")

        return value


class IncidentResponse(UUIDMixin, TimestampMixin, IncidentBase):
    """Incident response model"""

    class Config:
        form_attributes = True
