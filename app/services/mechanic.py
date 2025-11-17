import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from app.core.exceptions import NotFoundException, ValidationException
from app.models.incident import Incident
from app.models.mechanic import Mechanic
from app.schemas.common import IncidentStatusEnum
from app.schemas.mechanic import MechanicCreate, MechanicUpdate


class MechanicService:
    @staticmethod
    def create(db: Session, data: MechanicCreate):
        """Create a mechanic by given data"""
        if data.first_name in [None, ""] or data.last_name in [None, ""]:
            raise ValidationException("Invalid mechanic credentials.", status.HTTP_400_BAD_REQUEST)

        new_mechanic = Mechanic(**data.model_dump())
        db.add(new_mechanic)
        db.commit()
        db.refresh(new_mechanic)
        return new_mechanic

    @staticmethod
    def get_all(db: Session, search: str | None = None):
        """Get all mechanics with search"""
        query = select(Mechanic)
        if search:
            query = query.where(
                (Mechanic.first_name.ilike(f"%{search}%")) |
                (Mechanic.last_name.ilike(f"%{search}%"))
            )
        return db.execute(query).scalars().all()

    @staticmethod
    def get_by_id(db: Session, mechanic_id: uuid.UUID):
        """Get mechanic by given id."""
        mechanic =  db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
        if not mechanic_id:
            raise NotFoundException(entity="Mechanic", entity_id=str(mechanic_id))
        return mechanic

    @staticmethod
    def update(db: Session, mechanic_id: uuid.UUID, data: MechanicUpdate):
        """Update mechanic by given data"""
        mechanic = MechanicService.get_by_id(db, mechanic_id)
        if not mechanic:
            raise NotFoundException(entity='Mechanic', entity_id=str(mechanic_id))

        for field, value in data.model_dump(exclude_unset=True).items():
            if value not in (None, ''):
                setattr(mechanic, field, value)

        mechanic.updated_at = datetime.now()
        db.commit()
        db.refresh(mechanic)

        return mechanic

    @staticmethod
    def delete(db: Session, mechanic_id: uuid.UUID):
        """Delete mechanic by given id"""
        mechanic = MechanicService.get_by_id(db, mechanic_id)
        if not mechanic:
            raise NotFoundException(entity='Mechanic', entity_id=str(mechanic_id))

        db.delete(mechanic)
        db.commit()

    @staticmethod
    def update_performance(db: Session, mechanic_id: uuid.UUID):
        """Update mechanic performance score"""
        mechanic = MechanicService.get_by_id(db, mechanic_id)
        if not mechanic:
            return

        total_incidents = db.query(Incident).filter(Incident.mechanic_id == mechanic_id).count()
        finished_incidents = (
            db.query(Incident)
            .filter(Incident.mechanic_id == mechanic_id, Incident.status == IncidentStatusEnum.FINISHED)
            .count()
        )

        performance_score = (finished_incidents / total_incidents * 100) if total_incidents > 0 else 0.0
        mechanic.performance_score = round(performance_score, 2)

        db.commit()
        db.refresh(mechanic)

mechanic_service = MechanicService()

