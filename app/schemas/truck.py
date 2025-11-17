"""
    Truck model Pydantic schemas
"""
from pydantic import BaseModel, Field
from app.schemas.common import UUIDMixin, TimestampMixin

class TruckBase(BaseModel):
    plate_number: str = Field(..., description="Car Plate number")
    model: str = Field(..., description="Car Model")
    year: int = Field(..., ge=1900, le=2100, description="Model Year")


class TruckCreate(TruckBase):
    pass


class TruckUpdate(BaseModel):
    plate_number: str | None = None
    model: str | None = None
    year: int | None = None


class TruckResponse(UUIDMixin, TimestampMixin, TruckBase):
    is_deleted: bool

    class Config:
        from_attributes = True
