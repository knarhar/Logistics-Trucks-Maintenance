"""
    Mechanic model Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator

from app.core.exceptions import ValidationException
from app.schemas.common import ExpertiseEnum, UUIDMixin, TimestampMixin


class MechanicBase(BaseModel):
    """Base Mechanic model"""
    first_name: str
    last_name: str
    expertise: ExpertiseEnum
    performance_score: int = Field(default=0, ge=0, le=100)

    @field_validator("expertise", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None or value == "":
            return None

        allowed = [e for e in ExpertiseEnum]
        if value not in allowed:
            raise ValidationException(f"Invalid status '{value}'. Allowed:  {', '.join(allowed)}")

        return value


class MechanicCreate(MechanicBase):
    """Create Mechanic model"""
    pass


class MechanicUpdate(BaseModel):
    """Update Mechanic model"""
    first_name: str | None = None
    last_name: str | None = None
    expertise: ExpertiseEnum | None = None
    performance_score: int | None = Field(default=None, ge=0, le=100)

    @field_validator("expertise", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None or value == "":
            return None

        allowed = [e for e in ExpertiseEnum]
        if value not in allowed:
            raise ValidationException(f"Invalid status '{value}'. Allowed:  {', '.join(allowed)}")

        return value


class MechanicResponse(UUIDMixin, TimestampMixin, MechanicBase):
    """Mechanic response"""
    class Config:
        from_attributes = True
        json_scheme_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "expertise": "engine",
                "performance_score": 0,
                "id": "3fa85f64...",
                "created_at": "2025-11-14T10:20:42.625Z",
                "updated_at": "2025-11-14T10:20:42.625Z"
            }
        }
