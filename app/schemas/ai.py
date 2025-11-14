"""
AI response schemas
"""
from pydantic import BaseModel

class MechanicSuggestionRequest(BaseModel):
    issue_type: str
    issue_description: str

    class Config:
        json_schema_extra = {
            "example": {
                "issue_type": "engine",
                "issue_description": "The truck makes a loud knocking sound when accelerating"
            }
        }
