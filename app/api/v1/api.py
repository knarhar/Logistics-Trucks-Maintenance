from fastapi import APIRouter
from app.api.v1.endpoints import auth, trucks, mechanics, incidents

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(trucks.router, prefix="/trucks")
api_router.include_router(mechanics.router, prefix="/mechanics")
api_router.include_router(incidents.router, prefix="/incidents")
