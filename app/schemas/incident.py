from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.common import IncidentStatusEnum


class IncidentBase(BaseModel):
    truck_id: UUID
    mechanic_id: Optional[UUID] | None
    issue_type: str = Field(..., example="engine")
    description: Optional[str] = None
    photo_url: Optional[str] = None
    photo_public_id: Optional[str] = None
    status: IncidentStatusEnum = IncidentStatusEnum.PLANNED


class IncidentCreate(IncidentBase):
    pass


class IncidentResponse(IncidentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        form_attribute = True
