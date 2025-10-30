"""Configuration management for the Quant platform.

This module defines a `Config` class that centralizes all application
configuration. It loads settings from environment variables with sensible
defaults, making the application easily configurable for different environments
(development, testing, production).
"""

import os
from pathlib import Path


class Config:
    """Manages application configuration by loading from environment variables.

    Attributes:
        BASE_DIR (Path): The root directory of the application.
        DATA_DIR (Path): Directory for storing data files (e.g., DuckDB database).
        LOGS_DIR (Path): Directory for storing log files.
        APP_NAME (str): The name of the application.
        APP_ENV (str): The application environment (e.g., 'development', 'production').
        DEBUG (bool): Whether the application is in debug mode.
        DATABASE_PATH (str): The full path to the DuckDB database file.
        DEFAULT_INITIAL_CAPITAL (float): The default starting capital for backtests.
        DEFAULT_COMMISSION (float): The default trade commission rate.
        DEFAULT_VAR_CONFIDENCE (float): The default confidence level for VaR calculations.
        DEFAULT_POSITION_SIZE (float): The default percentage of capital to allocate to a position.
        MAX_POSITION_SIZE: float = float(os.getenv("MAX_POSITION_SIZE", "0.25"))
        LOG_LEVEL (str): The logging level for the application.
        LOG_FILE (str): The path to the main log file.
    """

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
    def ensure_directories(cls) -> None:
        """Ensures that the necessary data and logs directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

    @classmethod
    def is_production(cls) -> bool:
        """Checks if the application is running in a production environment."""
        return cls.APP_ENV.lower() == "production"

    @classmethod
    def is_development(cls) -> bool:
        """Checks if the application is running in a development environment."""
        return cls.APP_ENV.lower() == "development"


# Initialize directories on import
Config.ensure_directories()

# Create config instance
config = Config()
