"""Configuration settings for the Investment Report Generator"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, description="OpenAI API Key")
    anthropic_api_key: Optional[str] = Field(None, description="Anthropic API Key")
    
    # Application Settings
    app_name: str = "AI Investment Report Generator"
    app_version: str = "2.0.0"
    debug: bool = Field(False, description="Debug mode")
    
    # API Settings
    api_host: str = Field("0.0.0.0", description="API host")
    api_port: int = Field(8000, description="API port")
    api_reload: bool = Field(True, description="API reload")
    
    # Streamlit Settings
    streamlit_host: str = Field("0.0.0.0", description="Streamlit host")
    streamlit_port: int = Field(8501, description="Streamlit port")
    
    # Model Settings
    default_model: str = Field("openai/gpt-4o-mini", description="Default model")
    max_tokens: int = Field(4000, description="Max tokens")
    temperature: float = Field(0.1, description="Temperature")
    
    # File Management
    reports_dir: Path = Field(Path("reports"), description="Reports directory")
    max_report_age_days: int = Field(30, description="Max report age in days")
    
    # Logging
    log_level: str = Field("INFO", description="Log level")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(self.openai_api_key)
    
    @property
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is configured"""
        return bool(self.anthropic_api_key)
    
    @property
    def has_any_api_key(self) -> bool:
        """Check if any API key is configured"""
        return self.has_openai_key or self.has_anthropic_key


# Global settings instance
settings = Settings()
