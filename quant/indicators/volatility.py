"""Volatility indicators for technical analysis.

This module provides indicators that measure the rate and magnitude of price
movements, helping traders to assess market volatility.
"""

import polars as pl

from .base import IndicatorBase


class BollingerBands(IndicatorBase):
    """Calculates Bollinger Bands.

    Bollinger Bands consist of a middle band (an SMA) and two outer bands that
    are a set number of standard deviations away from the middle band. They are
    used to measure volatility and identify overbought/oversold conditions.

    Args:
        period (int): The period for the moving average.
        std_dev (float): The number of standard deviations for the outer bands.
        column (str): The column to use for the calculation.
    """

    def __init__(self, period: int = 20, std_dev: float = 2.0, column: str = "close"):
        """Initializes the BollingerBands indicator."""
        super().__init__(f"BB_{period}")
        self.period = period
        self.std_dev = std_dev
        self.column = column

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the Bollinger Bands calculation."""
        df = df.with_columns(
            [
                pl.col(self.column).rolling_mean(window_size=self.period).alias("BB_middle"),
                pl.col(self.column).rolling_std(window_size=self.period).alias("BB_std"),
            ]
        )

        df = df.with_columns(
            [
                (pl.col("BB_middle") + (self.std_dev * pl.col("BB_std"))).alias("BB_upper"),
                (pl.col("BB_middle") - (self.std_dev * pl.col("BB_std"))).alias("BB_lower"),
            ]
        )

        # Calculate %B (position within bands)
        df = df.with_columns(
            [
                (
                    (pl.col(self.column) - pl.col("BB_lower"))
                    / (pl.col("BB_upper") - pl.col("BB_lower"))
                ).alias("BB_percent"),
            ]
        )

        # Calculate bandwidth
        df = df.with_columns(
            [
                ((pl.col("BB_upper") - pl.col("BB_lower")) / pl.col("BB_middle")).alias("BB_width"),
            ]
        )

        return df.drop(["BB_std"])


class ATR(IndicatorBase):
    """Calculates the Average True Range (ATR).

    ATR is a technical analysis volatility indicator that was originally
    developed by J. Welles Wilder, Jr. for commodities. The indicator does not
    provide an indication of price trend, but rather the degree of price
    volatility.

    Args:
        period (int): The period for the ATR calculation.
    """

    def __init__(self, period: int = 14):
        """Initializes the ATR indicator."""
        super().__init__(f"ATR_{period}")
        self.period = period

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the ATR calculation."""
        # Calculate True Range
        df = df.with_columns(
            [
                pl.max_horizontal(
                    [
                        pl.col("high") - pl.col("low"),
                        (pl.col("high") - pl.col("close").shift(1)).abs(),
                        (pl.col("low") - pl.col("close").shift(1)).abs(),
                    ]
                ).alias("TR"),
            ]
        )

        # Calculate ATR (EMA of TR)
        df = df.with_columns(
            [
                pl.col("TR").ewm_mean(span=self.period).alias(self.name),
            ]
        )

        return df.drop(["TR"])


class KeltnerChannel(IndicatorBase):
    """Calculates Keltner Channels.

    Keltner Channels are volatility-based bands that are placed on either side
    of an asset's price and can aid in determining the direction of a trend.

    Args:
        ema_period (int): The period for the EMA (middle line).
        atr_period (int): The period for the ATR calculation.
        multiplier (float): The multiplier for the ATR to set the channel width.
    """

    def __init__(self, ema_period: int = 20, atr_period: int = 10, multiplier: float = 2.0):
        """Initializes the KeltnerChannel indicator."""
        super().__init__(f"KC_{ema_period}")
        self.ema_period = ema_period
        self.atr_period = atr_period
        self.multiplier = multiplier

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the Keltner Channel calculation."""
        # Calculate middle line (EMA of close)
        df = df.with_columns(
            [
                pl.col("close").ewm_mean(span=self.ema_period).alias("KC_middle"),
            ]
        )

        # Calculate ATR
        df = df.with_columns(
            [
                pl.max_horizontal(
                    [
                        pl.col("high") - pl.col("low"),
                        (pl.col("high") - pl.col("close").shift(1)).abs(),
                        (pl.col("low") - pl.col("close").shift(1)).abs(),
                    ]
                ).alias("TR"),
            ]
        )

        df = df.with_columns(
            [
                pl.col("TR").ewm_mean(span=self.atr_period).alias("KC_ATR"),
            ]
        )

        # Calculate upper and lower bands
        df = df.with_columns(
            [
                (pl.col("KC_middle") + (self.multiplier * pl.col("KC_ATR"))).alias("KC_upper"),
                (pl.col("KC_middle") - (self.multiplier * pl.col("KC_ATR"))).alias("KC_lower"),
            ]
        )

        return df.drop(["TR", "KC_ATR"])
