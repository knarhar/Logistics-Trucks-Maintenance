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
    def validate_expertise(cls, value):
        if value is None or value == "":
            raise ValidationException("Expertise cannot be empty", status_code=400)

        if isinstance(value, ExpertiseEnum):
            return value

        try:
            return ExpertiseEnum(value)
        except ValueError:
            allowed = [e.value for e in ExpertiseEnum]
            raise ValidationException(
                f"Invalid expertise value '{value}'. Allowed: {', '.join(allowed)}",
                status_code=400
            )


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
    def validate_expertise(cls, value):
        if value is None or value == "":
            raise ValidationException("Expertise cannot be empty", status_code=400)

        if isinstance(value, ExpertiseEnum):
            return value

        try:
            return ExpertiseEnum(value)
        except ValueError:
            allowed = [e.value for e in ExpertiseEnum]
            raise ValidationException(
                f"Invalid expertise value '{value}'. Allowed: {', '.join(allowed)}",
                status_code=400
            )


class MechanicResponse(UUIDMixin, TimestampMixin, MechanicBase):
    """Mechanic response"""

    class Config:
        from_attributes = True
        json_schema_extra = {
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
