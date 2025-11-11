import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.cloudinary import delete_image, upload_image
from app.core.exceptions import NotFoundException, ValidationException
from app.models.incident import Incident
from app.models.mechanic import Mechanic
from app.models.truck import Truck
from app.schemas.common import IncidentStatusEnum
from app.schemas.incident import IncidentCreate
from app.services.mechanic import mechanic_service


class IncidentService:
    @staticmethod
    def create(db: Session, data: IncidentCreate):
        truck = db.query(Truck).filter(Truck.id == data.truck_id).first()
        if not truck:
            raise NotFoundException(entity='Truck', entity_id=str(data.truck_id))

        mechanic = None
        if data.mechanic_id:
            mechanic = db.query(Mechanic).filter(Mechanic.id == data.mechanic_id).first()
            if not mechanic:
                raise NotFoundException(entity='Mechanic', entity_id=str(data.mechanic_id))


        incident = Incident(**data.model_dump())
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident

    @staticmethod
    def update(db: Session, incident_id: uuid.UUID, data: dict):
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            raise NotFoundException(entity="Incident", entity_id=str(incident_id))

        if "photo" in data.keys():
            urls = upload_image(data["photo"])

            data["photo_url"] = urls['url']
            data["photo_public_id"] = urls['public_id']

            data.pop("photo")

        if incident.photo_url and data["photo_url"]:
            delete_image(str(incident.photo_public_id))

        if data["status"] == IncidentStatusEnum.FINISHED and incident.mechanic_id:
            mechanic_service.update_performance(db, incident.mechanic_id)

        for key, value in data.items():
            if value not in [None, ""]:
                setattr(incident, key, value)

        db.commit()
        db.refresh(incident)
        return incident

    @staticmethod
    def list(db: Session, status=None, truck_id=None, mechanic_id=None):
        query = db.query(Incident)
        if status:
            query = query.filter(Incident.status == status)
        if truck_id:
            query = query.filter(Incident.truck_id == truck_id)
        if mechanic_id:
            query = query.filter(Incident.mechanic_id == mechanic_id)
        return query.all()

    @staticmethod
    def delete(db: Session, incident_id: str):
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            raise NotFoundException(entity='Incident', entity_id=incident_id)

        if incident.photo_url and incident.photo_public_id:
            delete_image(str(incident.photo_public_id))

        db.delete(incident)
        db.commit()
        return True

    @staticmethod
    def assign(db: Session, incident_id: str, mechanic_id: str):
        try:
            incident_uuid = uuid.UUID(incident_id)
            mechanic_uuid = uuid.UUID(mechanic_id)
        except ValueError:
            raise ValidationException(message="Invalid UUID format for incident_id or mechanic_id")

        incident = db.query(Incident).filter(Incident.id == incident_uuid).first()
        if not incident:
            raise NotFoundException(entity="Incident", entity_id=incident_id)

        mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_uuid).first()
        if not mechanic:
            raise NotFoundException(entity="Mechanic", entity_id=mechanic_id)

        incident.mechanic_id = mechanic_id
        incident.status = IncidentStatusEnum.IN_PROGRESS
        incident.updated_at = datetime.now()

        mechanic_service.update_performance(db, mechanic_id)

        db.commit()
        db.refresh(incident)
        return incident

incident_service = IncidentService()
