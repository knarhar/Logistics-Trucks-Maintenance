from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.schemas.common import ExpertiseEnum


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


class MechanicResponse(MechanicBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True