"""Configuration management for hrb_emp_lms."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    postgres_db_host: str = os.getenv("POSTGRES_DB_HOST", "localhost")
    postgres_db_port: int = int(os.getenv("POSTGRES_DB_PORT", "5432"))
    postgres_db_name: str = os.getenv("POSTGRES_DB_NAME", "coco")
    postgres_db_user: str = os.getenv("POSTGRES_DB_USER", "postgres")
    postgres_db_password: str = os.getenv("POSTGRES_DB_PASSWORD", "Igates_71")
    
    # Server
    server_port: int = int(os.getenv("SERVER_PORT", "8081"))
    api_key: str = os.getenv("API_KEY", "default-api-key")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def database_url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.postgres_db_user}:{self.postgres_db_password}@{self.postgres_db_host}:{self.postgres_db_port}/{self.postgres_db_name}"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

