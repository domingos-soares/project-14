"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "Person REST API"
    app_version: str = "1.0.0"
    description: str = "A RESTful API for managing Person objects with full CRUD operations"
    debug: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
