from fastapi import APIRouter

from app.core.security import *
from app.schemas.ai import MechanicSuggestionRequest
from app.services.ai import suggest_mechanics_ai
from app.services.mechanic import mechanic_service

router = APIRouter(tags=["AI"])

@router.post('/suggest-mechanic')
def ai_suggestion(request: MechanicSuggestionRequest, db: Session = Depends(get_db)):
    mechanics = mechanic_service.get_all(db)
    return suggest_mechanics_ai(
        issue_type=request.issue_type,
        description=request.issue_description,
        mechanics=mechanics
    )