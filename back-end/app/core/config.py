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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
