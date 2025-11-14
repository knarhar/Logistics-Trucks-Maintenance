"""
Mechanic management endpoints
"""
import uuid

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.core.security import get_db, get_current_user
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.mechanic import *
from app.services.mechanic import mechanic_service

router = APIRouter(tags=["Mechanics"])

@router.get("/", response_model=list[MechanicResponse])
def get_mechanics(
        db: Session = Depends(get_db),
        search: str | None = Query(default=None)
):
    return mechanic_service.get_all(db, search)


@router.post("/add", response_model=MechanicResponse)
def add_mechanic(
        data: MechanicCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return mechanic_service.create(db, data)


@router.patch("/{mechanic_id}", response_model=MechanicResponse)
def update_mechanic(
        mechanic_id: uuid.UUID,
        data: MechanicUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return mechanic_service.update(db, mechanic_id, data)


@router.delete("/{mechanic_id}", response_model=SuccessResponse)
def delete_mechanic(
        mechanic_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    mechanic_service.delete(db, mechanic_id)
