"""
Common Pydantic schemas used across the application
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, List
from datetime import datetime
from uuid import UUID
import enum

# Generic type for paginated responses
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    skip: int
    limit: int

    class Config:
        from_attributes = True


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Generic error response"""
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Error message here"
            }
        }


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    created_at: datetime
    updated_at: datetime


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key"""
    id: UUID


class IncidentStatusEnum(str, enum.Enum):
    """Incident status enumerations"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    ON_HOLD = "on_hold"


class ExpertiseEnum(str, enum.Enum):
    """Mechanic expertise enumerations"""
    ENGINE = "engine"
    TRANSMISSION = "transmission"
    TIRES = "tires"
    ELECTRICAL = "electrical"
    SUSPENSION = "suspension"
