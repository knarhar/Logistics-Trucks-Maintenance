"""
Common Pydantic schemas used across the application
"""
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional
from datetime import datetime
from uuid import UUID

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

    class Config:
        from_attributes = True


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key"""
    id: UUID

    class Config:
        from_attributes = True


class StatusEnum:
    """Common status enumerations"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class IncidentStatusEnum:
    """Incident status enumerations"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    ON_HOLD = "on_hold"


class IssueTypeEnum:
    """Issue type enumerations"""
    ENGINE = "engine"
    TRANSMISSION = "transmission"
    BRAKES = "brakes"
    ELECTRICAL = "electrical"
    TIRES = "tires"
    BODY = "body"
    OTHER = "other"


class SpecializationEnum:
    """Mechanic specialization enumerations"""
    ENGINE = "engine"
    TRANSMISSION = "transmission"
    BRAKES = "brakes"
    ELECTRICAL = "electrical"
    TIRES = "tires"
    GENERAL = "general"


class PriorityEnum:
    """Priority level enumerations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"