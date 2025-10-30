"""A mean reversion trading strategy using Bollinger Bands.

This module implements a strategy based on the principle that asset prices tend to
revert to their historical average. It uses Bollinger Bands to identify
statistically overextended prices.
"""

import polars as pl

from .base import Signal, Strategy


class MeanReversionStrategy(Strategy):
    """Implements a mean reversion strategy using Bollinger Bands.

    This strategy generates buy signals when the price touches or crosses below
    the lower Bollinger Band and sell signals when it touches or crosses above
    the upper band.

    Args:
        bb_period (int): The period for the Bollinger Bands' moving average.
        bb_std (float): The number of standard deviations for the bands.
        position_size_pct (float): The percentage of capital to allocate to each trade.
    """

    def __init__(
        self,
        bb_period: int = 20,
        bb_std: float = 2.0,
        position_size_pct: float = 0.1,
    ):
        """Initializes the MeanReversionStrategy."""
        super().__init__("Mean Reversion Strategy")
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.position_size_pct = position_size_pct

    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generates trading signals based on Bollinger Bands.

        A BUY signal is generated when the price is at or below the lower band.
        A SELL signal is generated when the price is at or above the upper band,
        or when it crosses back to the middle band from below (profit taking).

        Args:
            df: A Polars DataFrame with OHLCV data and Bollinger Band columns
                (BB_upper, BB_lower, BB_middle).

        Returns:
            The DataFrame with a 'signal' column added.

        Raises:
            ValueError: If the required Bollinger Band columns are not in the DataFrame.
        """
        # Check for required columns
        required_cols = ["BB_upper", "BB_lower", "BB_middle"]
        for col in required_cols:
            if col not in df.columns:
                msg = f"Required indicator {col} not found. Calculate Bollinger Bands first."
                raise ValueError(msg)

        # Generate signals
        df = df.with_columns(
            [
                # Price position relative to bands
                (pl.col("close") <= pl.col("BB_lower")).alias("at_lower_band"),
                (pl.col("close") >= pl.col("BB_upper")).alias("at_upper_band"),
                (pl.col("close").shift(1) < pl.col("BB_middle")).alias("was_below_middle"),
                (pl.col("close") >= pl.col("BB_middle")).alias("at_or_above_middle"),
            ]
        )

        # Buy at lower band, sell at upper band or middle band (take profit)
        df = df.with_columns(
            [
                pl.when(
                    pl.col("at_lower_band"),
                )
                .then(Signal.BUY.value)
                .when(
                    pl.col("at_upper_band")
                    | (pl.col("was_below_middle") & pl.col("at_or_above_middle")),
                )
                .then(Signal.SELL.value)
                .otherwise(Signal.HOLD.value)
                .alias("signal"),
            ]
        )

        # Clean up temporary columns
        return df.drop(
            [
                "at_lower_band",
                "at_upper_band",
                "was_below_middle",
                "at_or_above_middle",
            ]
        )

    def calculate_position_size(
        self,
        df: pl.DataFrame,
        capital: float,
        current_price: float,
    ) -> float:
        """Calculates position size as a fixed percentage of capital."""
        return (capital * self.position_size_pct) / current_price
