from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.exceptions import DuplicateException
from app.models.truck import Truck
from app.schemas.truck import TruckCreate, TruckUpdate
from uuid import UUID


class TruckService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10):
        """Get all trucks with pagination."""
        query = select(Truck).where(Truck.is_deleted == False).offset(skip).limit(limit)
        result = db.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_by_id(db: Session, id: UUID):
        """Get truck by id."""
        query = select(Truck).where(Truck.id == id)
        result = db.execute(query)
        return result.scalars().first()

    @staticmethod
    def create(db: Session, data: TruckCreate):
        """Create new truck."""
        truck = db.execute(
            select(Truck).where(Truck.plate_number == data.plate_number)
        ).scalar_one_or_none()

        if truck and truck.is_deleted == False:
            raise DuplicateException('Plate number', truck.plate_number)
        elif truck and truck.is_deleted == True:
            truck.is_deleted = False
        else:
            truck = Truck(**data.model_dump())
            db.add(truck)

        db.commit()
        db.refresh(truck)

    @staticmethod
    def update(db: Session, db_obj: Truck, obj_in: TruckUpdate):
        """Update truck with given data."""
        update_data = obj_in.model_dump(exclude_none=True)
        for key, value in update_data.items():
            if value not in [None, '']:
                setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj


truck_service = TruckService()
