from pydantic import BaseModel


class MechanicSuggestionRequest(BaseModel):
    issue_type: str
    issue_description: str