"""
Configuration Management
"""

import os
from typing import Optional
from pydantic import BaseModel

class Config(BaseModel):
    """Application configuration"""
    
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    MODEL_NAME: str = "anthropic/claude-3.5-sonnet"
    MAX_TOKENS: int = 2500
    TEMPERATURE: float = 0.7
    APP_TITLE: str = "AI Design Intelligence"
    APP_ICON: str = "🤖"
    
    class Config:
        env_file = ".env"

config = Config()

def set_api_key(api_key: str):
    """Set the API key dynamically"""
    config.OPENROUTER_API_KEY = api_key
    os.environ["OPENROUTER_API_KEY"] = api_key

def get_api_key() -> Optional[str]:
    """Get the configured API key"""
    return config.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
