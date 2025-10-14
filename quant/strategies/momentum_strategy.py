"""Momentum-based trading strategy."""

import polars as pl
from .base import Strategy, Signal


class MomentumStrategy(Strategy):
    """Momentum strategy using RSI and moving averages."""
    
    def __init__(
        self,
        rsi_period: int = 14,
        rsi_oversold: float = 30,
        rsi_overbought: float = 70,
        fast_ma: int = 50,
        slow_ma: int = 200,
        position_size_pct: float = 0.1
    ):
        """Initialize momentum strategy.
        
        Args:
            rsi_period: Period for RSI calculation
            rsi_oversold: RSI level considered oversold
            rsi_overbought: RSI level considered overbought
            fast_ma: Fast moving average period
            slow_ma: Slow moving average period
            position_size_pct: Percentage of capital to use per trade
        """
        super().__init__("Momentum Strategy")
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.position_size_pct = position_size_pct
    
    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generate momentum-based trading signals.
        
        Buy when:
        - RSI crosses above oversold level
        - Fast MA is above slow MA (uptrend)
        
        Sell when:
        - RSI crosses above overbought level
        - Fast MA crosses below slow MA
        """
        # Ensure required indicators are present
        required_cols = [f"RSI_{self.rsi_period}", f"SMA_{self.fast_ma}", f"SMA_{self.slow_ma}"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Required indicator {col} not found. Calculate indicators first.")
        
        rsi_col = f"RSI_{self.rsi_period}"
        fast_ma_col = f"SMA_{self.fast_ma}"
        slow_ma_col = f"SMA_{self.slow_ma}"
        
        # Generate signals
        df = df.with_columns([
            # Trend filter: fast MA above slow MA
            (pl.col(fast_ma_col) > pl.col(slow_ma_col)).alias("uptrend"),
            
            # RSI conditions
            (pl.col(rsi_col) < self.rsi_oversold).alias("rsi_oversold"),
            (pl.col(rsi_col) > self.rsi_overbought).alias("rsi_overbought"),
            
            # RSI crosses
            ((pl.col(rsi_col) > self.rsi_oversold) & 
             (pl.col(rsi_col).shift(1) <= self.rsi_oversold)).alias("rsi_cross_above_oversold"),
            
            ((pl.col(rsi_col) > self.rsi_overbought) & 
             (pl.col(rsi_col).shift(1) <= self.rsi_overbought)).alias("rsi_cross_above_overbought"),
            
            # MA cross
            ((pl.col(fast_ma_col) < pl.col(slow_ma_col)) & 
             (pl.col(fast_ma_col).shift(1) >= pl.col(slow_ma_col).shift(1))).alias("ma_bearish_cross")
        ])
        
        # Buy signal: RSI crosses above oversold AND in uptrend
        # Sell signal: RSI crosses above overbought OR bearish MA cross
        df = df.with_columns([
            pl.when(
                pl.col("rsi_cross_above_oversold") & pl.col("uptrend")
            ).then(Signal.BUY.value)
            .when(
                pl.col("rsi_cross_above_overbought") | pl.col("ma_bearish_cross")
            ).then(Signal.SELL.value)
            .otherwise(Signal.HOLD.value)
            .alias("signal")
        ])
        
        # Clean up temporary columns
        df = df.drop([
            "uptrend", "rsi_oversold", "rsi_overbought",
            "rsi_cross_above_oversold", "rsi_cross_above_overbought", "ma_bearish_cross"
        ])
        
        return df
    
    def calculate_position_size(
        self,
        df: pl.DataFrame,
        capital: float,
        current_price: float
    ) -> float:
        """Calculate position size based on fixed percentage of capital."""
        return (capital * self.position_size_pct) / current_price
