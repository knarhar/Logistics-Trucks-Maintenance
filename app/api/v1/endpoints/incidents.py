"""
Incident management endpoints
"""
import uuid
from typing import List

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session

from app.core.cloudinary import upload_image
from app.core.security import get_db, get_current_user
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.incident import *
from app.services.incident import incident_service

router = APIRouter(tags=["Incidents"])


@router.get('/', response_model=List[IncidentResponse])
def get_incidents(
        status: str = None,
        truck_id: str = None,
        mechanic_id: str = None,
        db: Session = Depends(get_db)
):
    return incident_service.list(db, status, truck_id, mechanic_id)


@router.post('/add', response_model=IncidentResponse)
def add_incident(
        truck_id: str = Form(...),
        mechanic_id: str | None = Form(None),
        status: str | None = Form(None),
        issue_type: str = Form("General"),
        description: str = Form(...),
        photo: UploadFile | str | None = File(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    photo_url = None
    photo_public_id = None

    if photo == "" or isinstance(photo, str):
        photo = None
    elif photo not in (None, ""):
        urls = upload_image(photo)
        photo_url = urls['url']
        photo_public_id = urls['public_id']

    if mechanic_id == "":
        mechanic_id = None

    try:
        truck_uuid = uuid.UUID(truck_id)
    except ValueError:
        raise ValidationException("Truck ID not found", status_code=404)

    mechanic_uuid = None
    try:
        if mechanic_id:
            mechanic_uuid = uuid.UUID(mechanic_id)
    except ValueError:
        raise ValidationException("Mechanic ID not found", status_code=404)

    incident_data = IncidentCreate(
        truck_id=truck_uuid,
        mechanic_id=mechanic_uuid,
        status=status,
        issue_type=issue_type,
        photo_url=photo_url,
        photo_public_id=photo_public_id,
        description=description
    )
    return incident_service.create(db, incident_data)


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(
        incident_id: UUID,
        mechanic_id: str | None = Form(None),
        description: str | None = Form(None),
        status: str | None = Form(None),
        photo: UploadFile | str | None = File(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if photo == "" or isinstance(photo, str):
        photo = None

    mechanic_uuid = None
    try:
        if mechanic_id not in [None, ""]:
            mechanic_uuid = uuid.UUID(mechanic_id)
    except ValueError:
        raise ValidationException("Mechanic ID not found", status_code=404)

    update_data = IncidentUpdate(
        mechanic_id=mechanic_uuid,
        description=description,
        status=status
    )

    data = update_data.model_dump(exclude_none=True)

    if photo:
        data["photo"] = photo

    return incident_service.update(db, incident_id, data)


@router.delete("/{incident_id}", response_model=SuccessResponse)
def delete_incident(
        incident_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    incident_service.delete(db, incident_id)

    return SuccessResponse(message="Incident deleted successfully")
