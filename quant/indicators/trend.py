"""Trend-following indicators for technical analysis.

This module provides a set of indicators designed to identify the direction and
strength of market trends.
"""

import polars as pl

from .base import IndicatorBase


class SMA(IndicatorBase):
    """Calculates the Simple Moving Average (SMA).

    The SMA is the unweighted mean of the previous n data points. It is a
    common tool to identify the trend direction.

    Args:
        period (int): The number of periods for the moving average.
        column (str): The name of the column to use for the calculation.
    """

    def __init__(self, period: int = 20, column: str = "close"):
        """Initializes the SMA indicator."""
        super().__init__(f"SMA_{period}")
        self.period = period
        self.column = column

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the SMA calculation."""
        return df.with_columns(
            pl.col(self.column).rolling_mean(window_size=self.period).alias(self.name),
        )


class EMA(IndicatorBase):
    """Calculates the Exponential Moving Average (EMA).

    The EMA gives more weight to recent prices, making it more responsive to new
    information than a simple moving average.

    Args:
        period (int): The number of periods for the moving average.
        column (str): The name of the column to use for the calculation.
    """

    def __init__(self, period: int = 20, column: str = "close"):
        """Initializes the EMA indicator."""
        super().__init__(f"EMA_{period}")
        self.period = period
        self.column = column

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the EMA calculation."""
        return df.with_columns(
            pl.col(self.column).ewm_mean(span=self.period).alias(self.name),
        )


class MACD(IndicatorBase):
    """Calculates the Moving Average Convergence Divergence (MACD).

    MACD is a trend-following momentum indicator that shows the relationship
    between two exponential moving averages of a security’s price.

    Args:
        fast_period (int): The period for the fast EMA.
        slow_period (int): The period for the slow EMA.
        signal_period (int): The period for the signal line EMA.
        column (str): The column to use for the calculation.
    """

    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
        column: str = "close",
    ):
        """Initializes the MACD indicator."""
        super().__init__("MACD")
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.column = column

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the MACD calculation."""
        ema_fast = pl.col(self.column).ewm_mean(span=self.fast_period)
        ema_slow = pl.col(self.column).ewm_mean(span=self.slow_period)

        df = df.with_columns(
            [
                (ema_fast - ema_slow).alias("MACD"),
            ]
        )

        df = df.with_columns(
            [
                pl.col("MACD").ewm_mean(span=self.signal_period).alias("MACD_signal"),
            ]
        )

        histogram = pl.col("MACD") - pl.col("MACD_signal")
        return df.with_columns(
            [
                histogram.alias("MACD_hist"),
                histogram.alias("MACD_histogram"),
            ]
        )


class ADX(IndicatorBase):
    """Calculates the Average Directional Index (ADX).

    ADX is used to quantify trend strength. It is composed of the ADX line
    itself, as well as the +DI (Positive Directional Indicator) and -DI
    (Negative Directional Indicator) lines.

    Args:
        period (int): The period for the ADX calculation.
    """

    def __init__(self, period: int = 14):
        """Initializes the ADX indicator."""
        super().__init__(f"ADX_{period}")
        self.period = period

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the ADX calculation."""
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

        # Calculate +DM and -DM
        df = df.with_columns(
            [
                pl.when(
                    (pl.col("high") - pl.col("high").shift(1))
                    > (pl.col("low").shift(1) - pl.col("low")),
                )
                .then(
                    pl.max_horizontal([pl.col("high") - pl.col("high").shift(1), 0]),
                )
                .otherwise(0)
                .alias("plus_DM"),
                pl.when(
                    (pl.col("low").shift(1) - pl.col("low"))
                    > (pl.col("high") - pl.col("high").shift(1)),
                )
                .then(
                    pl.max_horizontal([pl.col("low").shift(1) - pl.col("low"), 0]),
                )
                .otherwise(0)
                .alias("minus_DM"),
            ]
        )

        # Calculate smoothed TR, +DM, -DM
        df = df.with_columns(
            [
                pl.col("TR").rolling_mean(window_size=self.period).alias("ATR"),
                pl.col("plus_DM").rolling_mean(window_size=self.period).alias("plus_DM_smooth"),
                pl.col("minus_DM").rolling_mean(window_size=self.period).alias("minus_DM_smooth"),
            ]
        )

        # Calculate +DI and -DI
        df = df.with_columns(
            [
                (100 * pl.col("plus_DM_smooth") / pl.col("ATR")).alias("plus_DI"),
                (100 * pl.col("minus_DM_smooth") / pl.col("ATR")).alias("minus_DI"),
            ]
        )

        # Calculate DX and ADX
        df = df.with_columns(
            [
                (
                    100
                    * (pl.col("plus_DI") - pl.col("minus_DI")).abs()
                    / (pl.col("plus_DI") + pl.col("minus_DI"))
                ).alias("DX"),
            ]
        )

        return df.with_columns(
            [
                pl.col("DX").rolling_mean(window_size=self.period).alias(self.name),
            ]
        )
