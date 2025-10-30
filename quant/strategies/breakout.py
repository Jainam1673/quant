"""A trading strategy that identifies and trades price breakouts.

This module implements a classic breakout strategy that buys when the price
breaks above a recent resistance level and sells when it breaks below a
support level, with volume confirmation.
"""

import polars as pl

from .base import Signal, Strategy


class BreakoutStrategy(Strategy):
    """Implements a breakout strategy using rolling highs and lows as support/resistance.

    This strategy identifies breakouts by comparing the current price to the
    highest high and lowest low over a specified lookback period.

    Args:
        lookback_period (int): The number of periods to use for identifying
            support and resistance levels.
        volume_multiplier (float): The factor by which the current volume must
            exceed the average volume to confirm a breakout.
        position_size_pct (float): The percentage of capital to allocate to each trade.
    """

    def __init__(
        self,
        lookback_period: int = 20,
        volume_multiplier: float = 1.5,
        position_size_pct: float = 0.1,
    ):
        """Initializes the BreakoutStrategy."""
        super().__init__("Breakout Strategy")
        self.lookback_period = lookback_period
        self.volume_multiplier = volume_multiplier
        self.position_size_pct = position_size_pct

    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generates trading signals based on breakout logic.

        A BUY signal is generated when the price closes above the resistance
        level (the highest high of the lookback period) with high volume.
        A SELL signal is generated when the price closes below the support
        level (the lowest low of the lookback period).

        Args:
            df: A Polars DataFrame with OHLCV data.

        Returns:
            The DataFrame with a 'signal' column added.
        """
        # Calculate support and resistance levels
        df = df.with_columns(
            [
                pl.col("high")
                .rolling_max(window_size=self.lookback_period)
                .shift(1)
                .alias("resistance"),
                pl.col("low")
                .rolling_min(window_size=self.lookback_period)
                .shift(1)
                .alias("support"),
                pl.col("volume").rolling_mean(window_size=self.lookback_period).alias("avg_volume"),
            ]
        )

        # Breakout conditions
        df = df.with_columns(
            [
                # Bullish breakout: close above resistance
                (pl.col("close") > pl.col("resistance")).alias("bullish_breakout"),
                # Bearish breakdown: close below support
                (pl.col("close") < pl.col("support")).alias("bearish_breakdown"),
                # Volume confirmation
                (pl.col("volume") > (pl.col("avg_volume") * self.volume_multiplier)).alias(
                    "high_volume"
                ),
            ]
        )

        # Generate signals
        df = df.with_columns(
            [
                pl.when(
                    pl.col("bullish_breakout") & pl.col("high_volume"),
                )
                .then(Signal.BUY.value)
                .when(
                    pl.col("bearish_breakdown"),
                )
                .then(Signal.SELL.value)
                .otherwise(Signal.HOLD.value)
                .alias("signal"),
            ]
        )

        # Clean up temporary columns
        return df.drop(
            [
                "resistance",
                "support",
                "avg_volume",
                "bullish_breakout",
                "bearish_breakdown",
                "high_volume",
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
