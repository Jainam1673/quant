"""Configuration management for the Quant platform."""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "quant")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", str(DATA_DIR / "quant.duckdb"))
    
    # Backtesting defaults
    DEFAULT_INITIAL_CAPITAL: float = float(os.getenv("DEFAULT_INITIAL_CAPITAL", "100000"))
    DEFAULT_COMMISSION: float = float(os.getenv("DEFAULT_COMMISSION", "0.001"))
    
    # Risk management defaults
    DEFAULT_VAR_CONFIDENCE: float = float(os.getenv("DEFAULT_VAR_CONFIDENCE", "0.95"))
    DEFAULT_POSITION_SIZE: float = float(os.getenv("DEFAULT_POSITION_SIZE", "0.1"))
    MAX_POSITION_SIZE: float = float(os.getenv("MAX_POSITION_SIZE", "0.25"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", str(LOGS_DIR / "quant.log"))
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production."""
        return cls.APP_ENV.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development."""
        return cls.APP_ENV.lower() == "development"


# Initialize directories on import
Config.ensure_directories()

# Create config instance
config = Config()
