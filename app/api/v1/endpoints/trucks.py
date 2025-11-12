"""
Truck management endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.core.security import get_db, get_current_user
from app.models.user import User
from app.schemas.common import *
from app.schemas.truck import *
from app.services.truck import truck_service

router = APIRouter(tags=["Trucks"])

@router.post("/add", response_model=SuccessResponse)
def create_truck(
    truck_in: TruckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    truck_service.create(db, truck_in)
    return SuccessResponse(message="Truck Created Successfully")


@router.get("/", response_model=PaginatedResponse[TruckResponse])
def get_trucks(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    trucks = truck_service.get_all(db, skip=skip, limit=limit)
    return PaginatedResponse(items=trucks, total=len(trucks), skip=skip, limit=limit)


@router.patch("/{truck_id}", response_model=TruckResponse)
def update_truck(
    truck_id: UUID,
    truck_in: TruckUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    truck = truck_service.get_by_id(db, truck_id)
    return truck_service.update(db, truck, truck_in)


@router.delete("/{truck_id}", response_model=SuccessResponse)
def delete_truck(
    truck_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    truck = truck_service.get_by_id(db, truck_id)
    if not truck:
        raise NotFoundException(entity='Truck', entity_id=str(truck_id))
    truck.soft_delete(db)
    return SuccessResponse(message="Truck deleted successfully")