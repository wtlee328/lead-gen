"""
Configuration management for Lead Generation API
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Lead Generation AI Service"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    PORT: int = 7860  # HuggingFace Spaces requirement
    LOG_LEVEL: str = "INFO"
    
    # Security
    JWT_SECRET_KEY: str = "default-jwt-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = [
        "*",
        "https://www.prospec.io",
        "https://prospec.io",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Supabase
    SUPABASE_URL: str = "https://example.supabase.co"  # Default placeholder
    SUPABASE_SERVICE_ROLE_KEY: str = "placeholder-service-role-key"  # For server-side operations
    SUPABASE_JWT_SECRET: str = "placeholder-jwt-secret"        # For JWT verification
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # Apify (Required for n8n workflow replication)
    APIFY_API_TOKEN: Optional[str] = None
    
    # Lead Enrichment Services
    APOLLO_API_KEY: Optional[str] = None
    HUNTER_API_KEY: Optional[str] = None
    CLEARBIT_API_KEY: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour in seconds
    
    # Processing
    MAX_LEADS_PER_REQUEST: int = 50
    REQUEST_TIMEOUT: int = 300  # 5 minutes
    
    # Database
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()

# Validate critical settings
def validate_settings():
    """Validate critical configuration"""
    required_settings = [
        "JWT_SECRET_KEY",
        "SUPABASE_URL", 
        "SUPABASE_SERVICE_ROLE_KEY",
        "SUPABASE_JWT_SECRET"
    ]
    
    missing = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing.append(setting)
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    # Warn about missing optional but important settings
    if not settings.APIFY_API_TOKEN:
        print("WARNING: APIFY_API_TOKEN not set - Apify crawler will not work")
    
    if not settings.OPENAI_API_KEY and not settings.ANTHROPIC_API_KEY:
        print("WARNING: No AI service API keys set - will use fallback URL generation")

# Don't validate on import for HuggingFace Spaces compatibility
# validate_settings()