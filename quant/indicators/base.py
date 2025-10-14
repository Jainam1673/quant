"""Base class for technical indicators."""

import polars as pl
from abc import ABC, abstractmethod


class IndicatorBase(ABC):
    """Base class for all technical indicators."""
    
    def __init__(self, name: str):
        """Initialize indicator.
        
        Args:
            name: Name of the indicator
        """
        self.name = name
    
    @abstractmethod
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate indicator values.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with indicator columns added
        """
        pass
    
    def __call__(self, df: pl.DataFrame) -> pl.DataFrame:
        """Allow calling indicator as a function."""
        return self.calculate(df)
