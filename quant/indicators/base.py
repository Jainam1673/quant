"""Base class for all technical indicators.

This module defines the `IndicatorBase` abstract class, which provides a
standard interface for all technical indicators in the library. By inheriting
from this class, new indicators can be seamlessly integrated into the platform.
"""

from abc import ABC, abstractmethod

import polars as pl


class IndicatorBase(ABC):
    """Abstract base class for all technical indicators.

    This class defines the common structure for indicators, ensuring they can be
    applied to a Polars DataFrame in a consistent way.

    Attributes:
        name (str): The name of the indicator, used as the column name in the DataFrame.
    """

    def __init__(self, name: str):
        """Initializes the indicator with a name.

        Args:
            name: The name of the indicator (e.g., "SMA_20").
        """
        self.name = name

    @abstractmethod
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculates the indicator values.

        This is an abstract method that must be implemented by all subclasses.
        It should take a DataFrame with OHLCV data and return a new DataFrame
        with the indicator's column(s) added.

        Args:
            df: The input DataFrame with market data.

        Returns:
            A DataFrame with the calculated indicator values.
        """

    def __call__(self, df: pl.DataFrame) -> pl.DataFrame:
        """Allows the indicator to be called as a function for a fluent API.

        This enables a more readable syntax, like `SMA(20)(df)`.

        Args:
            df: The input DataFrame.

        Returns:
            The DataFrame with the indicator calculated.
        """
        return self.calculate(df)
