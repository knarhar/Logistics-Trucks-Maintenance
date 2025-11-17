"""
Authentication Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    """Login request schema (for documentation)"""
    username: str | None = Field(None)
    password: str | None = Field(None, description="Password")

    @field_validator("username", "password", mode="before")
    @classmethod
    def not_empty(cls, v, field):
        if v is None or v == "":
            raise ValueError(f"{field.name} must be provided")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "dispatcher",
                "password": "password123"
            }
        }


class LoginResponse(BaseModel):
    """Login response with tokens"""
    access_token: str = Field(..., description="Access token for API requests")
    refresh_token: str = Field(..., description="Refresh token to get new access tokens")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class RefreshRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str = Field(..., description="Refresh token")

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshResponse(BaseModel):
    """Refresh token response with new access token"""
    access_token: str = Field(..., description="New access token")
    token_type: str = Field(default="bearer", description="Token type")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class LogoutResponse(BaseModel):
    """Logout response"""
    success: bool = Field(default=True, description="Logout successful")
    message: str = Field(..., description="Success message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully logged out"
            }
        }
