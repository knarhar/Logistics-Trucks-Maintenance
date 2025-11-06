from pydantic import BaseModel, Field
from app.schemas.common import UUIDMixin, TimestampMixin

class TruckBase(BaseModel):
    plate_number: str = Field(..., example="34AB123")
    model: str = Field(..., example="Volvo FH16")
    year: int = Field(..., ge=1900, le=2100, example=2020)


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
