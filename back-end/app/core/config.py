from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
import json
import os


def _parse_allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            return [origin.strip() for origin in raw.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
    ]


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/artiverse")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production-123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration (comma-separated or JSON array via ALLOWED_ORIGINS env)
    ALLOWED_ORIGINS: list = Field(default_factory=_parse_allowed_origins)
    
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
