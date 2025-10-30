"""A momentum-based trading strategy using RSI and moving averages.

This module implements a trend-following momentum strategy that enters trades
based on RSI signals when the overall trend is favorable, as determined by
moving averages.
"""

import polars as pl

from .base import Signal, Strategy


class MomentumStrategy(Strategy):
    """Implements a momentum strategy using RSI and SMA indicators.

    This strategy aims to enter trades in the direction of the prevailing trend.
    It uses a long-term moving average to identify the trend and RSI to time entries.

    Args:
        rsi_period (int): The period for the RSI calculation.
        rsi_oversold (float): The RSI level considered to be oversold.
        rsi_overbought (float): The RSI level considered to be overbought.
        fast_ma (int): The period for the fast moving average.
        slow_ma (int): The period for the slow moving average, used for trend direction.
        position_size_pct (float): The percentage of capital to allocate to each trade.
    """

    def __init__(
        self,
        rsi_period: int = 14,
        rsi_oversold: float = 30,
        rsi_overbought: float = 70,
        fast_ma: int = 50,
        slow_ma: int = 200,
        position_size_pct: float = 0.1,
    ):
        """Initializes the MomentumStrategy."""
        super().__init__("Momentum Strategy")
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.position_size_pct = position_size_pct

    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generates trading signals based on momentum indicators.

        A BUY signal is generated when the RSI crosses above the oversold level
        while the fast moving average is above the slow moving average (indicating
        an uptrend).
        A SELL signal is generated if the RSI crosses above the overbought level
        or if the fast MA crosses below the slow MA (a potential trend reversal).

        Args:
            df: A Polars DataFrame with OHLCV data and the required SMA and RSI
                indicator columns.

        Returns:
            The DataFrame with a 'signal' column added.

        Raises:
            ValueError: If the required indicator columns are not in the DataFrame.
        """
        # Ensure required indicators are present
        required_cols = [f"RSI_{self.rsi_period}", f"SMA_{self.fast_ma}", f"SMA_{self.slow_ma}"]
        for col in required_cols:
            if col not in df.columns:
                msg = f"Required indicator {col} not found. Calculate indicators first."
                raise ValueError(msg)

        rsi_col = f"RSI_{self.rsi_period}"
        fast_ma_col = f"SMA_{self.fast_ma}"
        slow_ma_col = f"SMA_{self.slow_ma}"

        # Generate signals
        df = df.with_columns(
            [
                # Trend filter: fast MA above slow MA
                (pl.col(fast_ma_col) > pl.col(slow_ma_col)).alias("uptrend"),
                # RSI conditions
                (pl.col(rsi_col) < self.rsi_oversold).alias("rsi_oversold"),
                (pl.col(rsi_col) > self.rsi_overbought).alias("rsi_overbought"),
                # RSI crosses
                (
                    (pl.col(rsi_col) > self.rsi_oversold)
                    & (pl.col(rsi_col).shift(1) <= self.rsi_oversold)
                ).alias("rsi_cross_above_oversold"),
                (
                    (pl.col(rsi_col) > self.rsi_overbought)
                    & (pl.col(rsi_col).shift(1) <= self.rsi_overbought)
                ).alias("rsi_cross_above_overbought"),
                # MA cross
                (
                    (pl.col(fast_ma_col) < pl.col(slow_ma_col))
                    & (pl.col(fast_ma_col).shift(1) >= pl.col(slow_ma_col).shift(1))
                ).alias("ma_bearish_cross"),
            ]
        )

        # Buy signal: RSI crosses above oversold AND in uptrend
        # Sell signal: RSI crosses above overbought OR bearish MA cross
        df = df.with_columns(
            [
                pl.when(
                    pl.col("rsi_cross_above_oversold") & pl.col("uptrend"),
                )
                .then(Signal.BUY.value)
                .when(
                    pl.col("rsi_cross_above_overbought") | pl.col("ma_bearish_cross"),
                )
                .then(Signal.SELL.value)
                .otherwise(Signal.HOLD.value)
                .alias("signal"),
            ]
        )

        # Clean up temporary columns
        return df.drop(
            [
                "uptrend",
                "rsi_oversold",
                "rsi_overbought",
                "rsi_cross_above_oversold",
                "rsi_cross_above_overbought",
                "ma_bearish_cross",
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
