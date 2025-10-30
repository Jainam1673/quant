"""Production-ready error handling and logging utilities."""

import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from functools import wraps


def handle_exceptions(func):
    """Decorator to handle exceptions in production code."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(
                "Exception in %s: %s", 
                func.__name__, 
                str(e), 
                exc_info=True
            )
            raise
    return wrapper


def get_utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def safe_float_conversion(value: Any) -> float:
    """Safely convert value to float."""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        if hasattr(value, 'item'):  # numpy scalar
            return float(value.item())
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return 0.0


def validate_portfolio_data(data: Dict[str, Any]) -> bool:
    """Validate portfolio data structure."""
    required_fields = ['ticker', 'quantity', 'price']
    return all(field in data for field in required_fields)


class ProductionLogger:
    """Production-ready logger with proper formatting."""
    
    @staticmethod
    def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """Set up production logger."""
        logger = logging.getLogger(name)
        
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(level)
        
        return logger