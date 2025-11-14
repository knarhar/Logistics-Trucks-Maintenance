from pydantic import BaseModel, Field

from app.schemas.common import ExpertiseEnum, UUIDMixin, TimestampMixin


class MechanicBase(BaseModel):
    first_name: str
    last_name: str
    expertise: ExpertiseEnum
    performance_score: int = Field(default=0, ge=0, le=100)


class MechanicCreate(MechanicBase):
    pass


class MechanicUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    expertise: ExpertiseEnum | None = None
    performance_score: int | None = Field(default=None, ge=0, le=100)


class MechanicResponse(UUIDMixin, TimestampMixin, MechanicBase):
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
