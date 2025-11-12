import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.cloudinary import delete_image, upload_image
from app.core.exceptions import NotFoundException

from app.models.incident import Incident
from app.models.truck import Truck

from app.schemas.common import IncidentStatusEnum
from app.schemas.incident import IncidentCreate

from app.services.mechanic import mechanic_service


class IncidentService:
    @staticmethod
    def get_by_id(db: Session, incident_id: uuid.UUID):
        """Get incident by id"""
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            raise NotFoundException(entity="Incident", entity_id=str(incident_id))
        return incident

    @staticmethod
    def create(db: Session, data: IncidentCreate):
        """Create incident with given data"""
        truck = db.query(Truck).filter(
            Truck.id == data.truck_id,
            Truck.is_deleted == False
        ).first()
        if not truck:
            raise NotFoundException(entity='Truck', entity_id=str(data.truck_id))

        mechanic = None
        if data.mechanic_id:
            mechanic = mechanic_service.get_by_id(db, data.mechanic_id)
            mechanic_service.update_performance(db=db, mechanic_id=data.mechanic_id)
            if not mechanic:
                raise NotFoundException(entity='Mechanic', entity_id=str(data.mechanic_id))

        incident = Incident(**data.model_dump())
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident

    @staticmethod
    def update(db: Session, incident_id: uuid.UUID, data: dict):
        """Update incident with given data"""
        incident = IncidentService.get_by_id(db, incident_id)

        old_status = incident.status
        old_mechanic_id = incident.mechanic_id

        if not incident:
            raise NotFoundException(entity="Incident", entity_id=str(incident_id))

        if "photo" in data.keys():
            urls = upload_image(data["photo"])
            data["photo_url"] = urls['url']
            data["photo_public_id"] = urls['public_id']
            data.pop("photo")

        if incident.photo_url and data["photo_url"]:
            try:
                delete_image(str(incident.photo_public_id))
            except Exception:  # don't go down if there's a problem with Cloudinary
                pass

        for key, value in data.items():
            if value not in [None, ""]:
                setattr(incident, key, value)

        db.commit()
        db.refresh(incident)

        if data.get("status"):
            if incident.mechanic_id:
                mechanic_service.update_performance(db, incident.mechanic_id)
            if old_mechanic_id and old_mechanic_id != incident.mechanic_id:
                mechanic_service.update_performance(db, old_mechanic_id)

        return incident

    @staticmethod
    def list(db: Session, status=None, truck_id=None, mechanic_id=None):
        """List all incidents with given status, truck id and mechanic_id"""
        query = db.query(Incident)
        if status:
            query = query.filter(Incident.status == status)
        if truck_id:
            query = query.filter(Incident.truck_id == truck_id)
        if mechanic_id:
            query = query.filter(Incident.mechanic_id == mechanic_id)
        return query.all()

    @staticmethod
    def delete(db: Session, incident_id: uuid.UUID):
        """Delete incident with given id"""
        incident = IncidentService.get_by_id(db, incident_id)
        if not incident:
            raise NotFoundException(entity='Incident', entity_id=str(incident_id))

        if incident.photo_url and incident.photo_public_id:
            try:
                delete_image(str(incident.photo_public_id))
            except Exception:
                pass

        db.delete(incident)
        db.commit()

        if incident.mechanic_id:
            mechanic_service.update_performance(db, incident.mechanic_id)

        return True

    @staticmethod
    def assign(db: Session, incident_id: uuid.UUID, mechanic_id: uuid.UUID):
        """Assign incident with given id"""

        incident = IncidentService.get_by_id(db, incident_id)
        if not incident:
            raise NotFoundException(entity="Incident", entity_id=str(incident_id))

        mechanic = mechanic_service.get_by_id(db, mechanic_id)
        if not mechanic:
            raise NotFoundException(entity="Mechanic", entity_id=str(mechanic_id))
        incident.mechanic_id = mechanic_id

        if incident.status == IncidentStatusEnum.PLANNED:
            incident.status = IncidentStatusEnum.IN_PROGRESS

        incident.updated_at = datetime.now()

        db.commit()
        db.refresh(incident)

        mechanic_service.update_performance(db, mechanic_id)

        return incident


incident_service = IncidentService()
