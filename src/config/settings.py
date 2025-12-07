"""
Configuration Settings
API keys, environment variables, and service endpoints
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Research Genie - AI Service"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8001, env="PORT")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_ORIGINS"
    )
    
    # LLM Configuration
    LLM_PROVIDER: str = Field(default="gemini", env="LLM_PROVIDER")  # gemini or openai
    LLM_API_KEY: str = Field(default="", env="LLM_API_KEY")
    LLM_MODEL: str = Field(default="gemini-2.5-flash", env="LLM_MODEL")  # gemini-2.5-flash or gpt-4
    
    # OpenAI specific (if using OpenAI)
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    # Gemini specific (if using Gemini)
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", env="GEMINI_MODEL")
    
    # Service URLs
    BACKEND_URL: str = Field(default="http://localhost:8000", env="BACKEND_URL")
    SCRAPER_URL: str = Field(default="http://localhost:8002", env="SCRAPER_URL")
    
    # Request settings
    REQUEST_TIMEOUT: float = Field(default=30.0, env="REQUEST_TIMEOUT")
    MAX_PAPERS_TO_ANALYZE: int = Field(default=10, env="MAX_PAPERS_TO_ANALYZE")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/ai_service.log", env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set LLM API key based on provider
        if self.LLM_PROVIDER == "openai" and not self.LLM_API_KEY:
            self.LLM_API_KEY = self.OPENAI_API_KEY
            if not self.LLM_MODEL or self.LLM_MODEL == "gemini-2.5-flash":
                self.LLM_MODEL = self.OPENAI_MODEL
        elif self.LLM_PROVIDER == "gemini" and not self.LLM_API_KEY:
            self.LLM_API_KEY = self.GEMINI_API_KEY
            if not self.LLM_MODEL or self.LLM_MODEL == "gpt-4":
                self.LLM_MODEL = self.GEMINI_MODEL


# Create settings instance
settings = Settings()
