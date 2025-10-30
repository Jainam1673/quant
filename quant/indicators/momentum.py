"""Momentum indicators for technical analysis.

This module contains a collection of widely used momentum indicators, which are
designed to measure the speed and strength of price movements.
"""

import polars as pl

from .base import IndicatorBase


class RSI(IndicatorBase):
    """Calculates the Relative Strength Index (RSI).

    RSI is a momentum oscillator that measures the speed and change of price
    movements. It oscillates between 0 and 100 and is typically used to
    identify overbought or oversold conditions.

    Args:
        period (int): The number of periods for the RSI calculation.
        column (str): The name of the column to use for the calculation (e.g., "close").
    """

    def __init__(self, period: int = 14, column: str = "close"):
        """Initializes the RSI indicator."""
        super().__init__(f"RSI_{period}")
        self.period = period
        self.column = column

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the RSI calculation."""
        # Calculate price changes
        df = df.with_columns(
            [
                (pl.col(self.column) - pl.col(self.column).shift(1)).alias("change"),
            ]
        )

        # Separate gains and losses
        df = df.with_columns(
            [
                pl.when(pl.col("change") > 0).then(pl.col("change")).otherwise(0).alias("gain"),
                pl.when(pl.col("change") < 0)
                .then(pl.col("change").abs())
                .otherwise(0)
                .alias("loss"),
            ]
        )

        # Calculate average gain and loss
        df = df.with_columns(
            [
                pl.col("gain").rolling_mean(window_size=self.period).alias("avg_gain"),
                pl.col("loss").rolling_mean(window_size=self.period).alias("avg_loss"),
            ]
        )

        # Calculate RS and RSI
        df = df.with_columns(
            [
                (pl.col("avg_gain") / pl.col("avg_loss")).alias("RS"),
            ]
        )

        df = df.with_columns(
            [
                (100 - (100 / (1 + pl.col("RS")))).alias(self.name),
            ]
        )

        return df.drop(["change", "gain", "loss", "avg_gain", "avg_loss", "RS"])


class Stochastic(IndicatorBase):
    """Calculates the Stochastic Oscillator.

    The Stochastic Oscillator is a momentum indicator that compares a particular
    closing price of a security to a range of its prices over a certain period
    of time. It is used to generate overbought and oversold trading signals.

    Args:
        k_period (int): The lookback period for the %K line.
        d_period (int): The smoothing period for the %D line (SMA of %K).
    """

    def __init__(self, k_period: int = 14, d_period: int = 3):
        """Initializes the Stochastic Oscillator indicator."""
        super().__init__("Stochastic")
        self.k_period = k_period
        self.d_period = d_period

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the Stochastic calculation."""
        # Calculate %K
        df = df.with_columns(
            [
                pl.col("low").rolling_min(window_size=self.k_period).alias("lowest_low"),
                pl.col("high").rolling_max(window_size=self.k_period).alias("highest_high"),
            ]
        )

        df = df.with_columns(
            [
                (
                    100
                    * (pl.col("close") - pl.col("lowest_low"))
                    / (pl.col("highest_high") - pl.col("lowest_low"))
                ).alias("stoch_k"),
            ]
        )

        # Calculate %D (SMA of %K)
        df = df.with_columns(
            [
                pl.col("stoch_k").rolling_mean(window_size=self.d_period).alias("stoch_d"),
            ]
        )

        return df.drop(["lowest_low", "highest_high"])


class ROC(IndicatorBase):
    """Calculates the Rate of Change (ROC).

    The ROC indicator measures the percentage change in price between the current
    price and the price a certain number of periods ago.

    Args:
        period (int): The number of periods to look back.
        column (str): The column to use for the calculation.
    """

    def __init__(self, period: int = 12, column: str = "close"):
        """Initializes the ROC indicator."""
        super().__init__(f"ROC_{period}")
        self.period = period
        self.column = column

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the ROC calculation."""
        return df.with_columns(
            [
                (
                    100
                    * (pl.col(self.column) - pl.col(self.column).shift(self.period))
                    / pl.col(self.column).shift(self.period)
                ).alias(self.name),
            ]
        )


class Williams_R(IndicatorBase):
    """Calculates the Williams %R.

    Williams %R is a momentum indicator that is the inverse of the Stochastic
    Oscillator. It reflects the level of the close relative to the highest high
    for the lookback period.

    Args:
        period (int): The lookback period.
    """

    def __init__(self, period: int = 14):
        """Initializes the Williams %R indicator."""
        super().__init__(f"Williams_R_{period}")
        self.period = period

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the Williams %R calculation."""
        df = df.with_columns(
            [
                pl.col("high").rolling_max(window_size=self.period).alias("highest_high"),
                pl.col("low").rolling_min(window_size=self.period).alias("lowest_low"),
            ]
        )

        df = df.with_columns(
            [
                (
                    -100
                    * (pl.col("highest_high") - pl.col("close"))
                    / (pl.col("highest_high") - pl.col("lowest_low"))
                ).alias(self.name),
            ]
        )

        return df.drop(["highest_high", "lowest_low"])
