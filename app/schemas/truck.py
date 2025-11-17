"""
    Truck model Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator

from app.core.exceptions import ValidationException
from app.schemas.common import UUIDMixin, TimestampMixin

class TruckBase(BaseModel):
    plate_number: str | None = Field(..., description="Car Plate number")
    model: str | None = Field(..., description="Car Model")
    year: int | None = Field(0, description="Model Year")

    @classmethod
    @field_validator("plate_number", "model", mode="before")
    def validate_not_empty(cls, v, field):
        if v is None or v == "":
            raise ValidationException(f"{field.name} cannot be empty", status_code=400)
        return v



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
