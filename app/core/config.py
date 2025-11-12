import dataclasses
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Logistics Trucks Maintenance API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DISPATCHER_USERNAME: str
    DISPATCHER_PASSWORD: str
    DISPATCHER_EMAIL: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_FOLDER: str = "logistics_incidents"

    # AI
    GROQ_API_KEY: str
    AI_MODEL: str
    AI_MAX_RETRIES: int = 3
    AI_RETRY_DELAY: int = 2

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # File upload
    ALLOWED_IMAGE_TYPES: list = dataclasses.field(default_factory=lambda: ["image/jpg", "image/jpeg", "image/png"])
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True


settings = Settings()
