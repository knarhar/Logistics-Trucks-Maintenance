from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.exceptions import NotFoundException
from app.models.mechanic import Mechanic
from app.schemas.mechanic import MechanicCreate, MechanicUpdate


class MechanicService:
    @staticmethod
    def create(db: Session, data: MechanicCreate):
        new_mechanic = Mechanic(**data.model_dump())
        db.add(new_mechanic)
        db.commit()
        db.refresh(new_mechanic)
        return new_mechanic

    @staticmethod
    def get_all(db: Session, search: str | None = None):
        query = select(Mechanic)
        if search:
            query = query.where(
                (Mechanic.first_name.ilike(f"%{search}%")) |
                (Mechanic.last_name.ilike(f"%{search}%"))
            )
        return db.execute(query).scalars().all()

    @staticmethod
    def update(db: Session, mechanic_id: str, data: MechanicUpdate):
        mechanic = db.get(Mechanic, mechanic_id)
        if not mechanic:
            raise NotFoundException(entity='Mechanic', entity_id=mechanic_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(mechanic, field, value)

        mechanic.updated_at = datetime.now()
        db.commit()
        db.refresh(mechanic)
        return mechanic

    @staticmethod
    def delete(db: Session, mechanic_id: str):
        mechanic = db.get(Mechanic, mechanic_id)
        if not mechanic:
            raise NotFoundException(entity='Mechanic', entity_id=mechanic_id)
        db.delete(mechanic)
        db.commit()


mechanic_service = MechanicService()