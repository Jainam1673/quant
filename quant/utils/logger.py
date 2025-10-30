"""Logging configuration for the Quant platform.

This module provides a standardized way to set up and use logging across the
application. It ensures that log messages are consistently formatted and can be
directed to both the console and log files.
"""

import logging
import sys
from pathlib import Path

from quant.config import config


def setup_logger(
    name: str,
    level: str | None = None,
    log_file: str | None = None,
) -> logging.Logger:
    """Configures and returns a logger instance.

    This function sets up a logger with both a console handler and an optional
    file handler. The console handler has a simple format, while the file
    handler has a more detailed format.

    Args:
        name: The name of the logger.
        level: The logging level (e.g., 'INFO', 'DEBUG'). If not provided,
            it defaults to the `LOG_LEVEL` from the application config.
        log_file: The path to the log file. If not provided, it defaults to
            the `LOG_FILE` from the application config.

    Returns:
        A configured `logging.Logger` instance.
    """
    logger = logging.getLogger(name)

    # Set level
    log_level = level or config.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file or config.LOG_FILE:
        log_path = Path(log_file or config.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    return logger


# Create a default logger for general use
logger = setup_logger("quant")


def get_logger(name: str) -> logging.Logger:
    """A convenience function to get a logger for a specific module.

    This is a wrapper around `setup_logger` that is intended to be called from
    different modules to get a logger with a consistent configuration.

    Args:
        name: The name for the logger, typically `__name__`.

    Returns:
        A configured `logging.Logger` instance.
    """
    return setup_logger(name)
