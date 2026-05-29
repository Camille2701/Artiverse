from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/artiverse")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production-123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",      # Frontend dev (Nuxt)
        "http://localhost:8080",      # Alternative
        "http://localhost:5173",      # Vite dev server
    ]
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Artiverse"

    # Image storage: "local" (served from /uploads) or "s3"
    STORAGE_BACKEND: str = os.getenv("STORAGE_BACKEND", "local")

    # S3 / S3-compatible storage (only used when STORAGE_BACKEND == "s3")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME: Optional[str] = os.getenv("S3_BUCKET_NAME")
    # Custom endpoint for S3-compatible providers (MinIO, DigitalOcean Spaces, ...)
    S3_ENDPOINT_URL: Optional[str] = os.getenv("S3_ENDPOINT_URL")
    # Public base URL (CDN or bucket website) used to build returned image URLs
    S3_PUBLIC_URL: Optional[str] = os.getenv("S3_PUBLIC_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
