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
    issue_type: str = Field("General", description="Incident issue type")
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

    @field_validator("issue_type", mode="before")
    @classmethod
    def validate_issue_type(cls, value):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValidationException(
                "issue_type is required and cannot be empty",
                status_code=400
            )
        return value.strip() if isinstance(value, str) else value

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value):
        # Convert empty strings to None
        if value is not None and isinstance(value, str) and value.strip() == "":
            return None
        return value.strip() if isinstance(value, str) and value else value


class IncidentCreate(IncidentBase):
    """Incident create model"""
    pass


class IncidentUpdate(BaseModel):
    """Incident update model"""
    mechanic_id: Optional[UUID] = None
    issue_type: Optional[str] = Field(None, min_length=1, description="Incident issue type")
    description: Optional[str] = None
    status: Optional[IncidentStatusEnum] = None
    photo_url: Optional[str] = None
    photo_public_id: Optional[str] = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None:
            return None

        if value == "":
            raise ValidationException(
                "status cannot be empty string",
                status_code=400
            )

        if isinstance(value, IncidentStatusEnum):
            return value

        try:
            return IncidentStatusEnum(value)
        except ValueError:
            allowed = [e.value for e in IncidentStatusEnum]
            raise ValidationException(
                f"Invalid status value '{value}'. Allowed: {', '.join(allowed)}",
                status_code=400
            )

    @field_validator("issue_type", mode="before")
    @classmethod
    def validate_issue_type(cls, value):
        # Allow None for updates (field not being updated)
        if value is None:
            return None

        if isinstance(value, str) and value.strip() == "":
            raise ValidationException(
                "issue_type cannot be empty string",
                status_code=400
            )
        return value.strip() if isinstance(value, str) else value

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value):
        if value is not None and isinstance(value, str) and value.strip() == "":
            return None
        return value.strip() if isinstance(value, str) and value else value


class IncidentResponse(UUIDMixin, TimestampMixin, IncidentBase):
    """Incident response model"""

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "truck_id": "7fa85f64-5717-4562-b3fc-2c963f66afa7",
                "mechanic_id": "8fa85f64-5717-4562-b3fc-2c963f66afa8",
                "issue_type": "Engine failure",
                "description": "Engine overheating during long haul",
                "photo_url": "https://example.com/photos/incident123.jpg",
                "photo_public_id": "incidents/incident123",
                "status": "planned",
                "created_at": "2025-11-14T10:20:42.625Z",
                "updated_at": "2025-11-14T10:20:42.625Z"
            }
        }
    }
