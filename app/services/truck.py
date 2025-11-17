from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.exceptions import DuplicateException, NotFoundException, ValidationException
from app.models.truck import Truck
from app.schemas.truck import TruckCreate, TruckUpdate


class TruckService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10):
        """Get all trucks with pagination."""
        trucks = (
            db.execute(
                select(Truck)
                .where(Truck.is_deleted == False)
                .offset(skip)
                .limit(limit))
            .scalars()
            .all()
        )
        return trucks

    @staticmethod
    def get_by_id(db: Session, id: UUID):
        """Get truck by id."""
        truck = (
            db.execute(
                select(Truck)
                .where(Truck.id == id)
            )
            .scalars()
            .first()
        )

        if not truck:
            raise NotFoundException(entity='Truck', entity_id=str(id))

        return truck

    @staticmethod
    def create(db: Session, data: TruckCreate):
        """Create new truck."""
        if data.plate_number in [None, ""] or data.model in [None, ""] or data.year is None or data.year < 1900:
            raise ValidationException(message='Missing or invalid values', status_code=400)

        truck = db.execute(
            select(Truck)
            .where(Truck.plate_number == data.plate_number)
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
    def update(db: Session, truck_id: UUID, obj_in: TruckUpdate):
        """Update truck with given data."""
        truck = TruckService.get_by_id(db, truck_id)

        update_data = obj_in.model_dump()

        if update_data['year'] and update_data['year'] < 1900:
            update_data['year'] = 1900

        if update_data['plate_number']:
            dub_truck = db.execute(
                select(Truck)
                .filter(Truck.plate_number == update_data['plate_number'], Truck.id != truck_id)).scalar_one_or_none()
            if dub_truck:
                raise DuplicateException('Plate number', update_data['plate_number'])

        for key, value in update_data.items():
            if value not in [None, '']:
                setattr(truck, key, value)

        db.commit()
        db.refresh(truck)
        return truck


truck_service = TruckService()
