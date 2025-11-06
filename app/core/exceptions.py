"""
Custom exception classes for the application
"""
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Exception raised when a resource is not found"""
    def __init__(self, entity: str, entity_id: str = None):
        detail = f"{entity} not found"
        if entity_id:
            detail = f"{entity} with id '{entity_id}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class DuplicateException(HTTPException):
    """Exception raised when trying to create a duplicate resource"""
    def __init__(self, field: str, value: str = None):
        detail = f"{field} already exists"
        if value:
            detail = f"{field} '{value}' already exists"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ValidationException(HTTPException):
    """Exception raised for validation errors"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )


class UnauthorizedException(HTTPException):
    """Exception raised for unauthorized access"""
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(HTTPException):
    """Exception raised for forbidden access"""
    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class AIServiceException(Exception):
    """Exception raised when AI service fails"""
    def __init__(self, message: str = "AI service error"):
        self.message = message
        super().__init__(self.message)


class FileUploadException(HTTPException):
    """Exception raised for file upload errors"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File upload error: {message}"
        )