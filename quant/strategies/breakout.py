"""Breakout trading strategy."""

import polars as pl
from .base import Strategy, Signal


class BreakoutStrategy(Strategy):
    """Breakout strategy using support/resistance levels and volume."""
    
    def __init__(
        self,
        lookback_period: int = 20,
        volume_multiplier: float = 1.5,
        position_size_pct: float = 0.1
    ):
        """Initialize breakout strategy.
        
        Args:
            lookback_period: Period for identifying support/resistance levels
            volume_multiplier: Volume must be this many times the average
            position_size_pct: Percentage of capital to use per trade
        """
        super().__init__("Breakout Strategy")
        self.lookback_period = lookback_period
        self.volume_multiplier = volume_multiplier
        self.position_size_pct = position_size_pct
    
    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generate breakout signals.
        
        Buy when:
        - Price breaks above resistance (recent high)
        - Volume is above average
        
        Sell when:
        - Price breaks below support (recent low)
        - OR price drops below entry by stop loss %
        """
        # Calculate support and resistance levels
        df = df.with_columns([
            pl.col("high").rolling_max(window_size=self.lookback_period).shift(1).alias("resistance"),
            pl.col("low").rolling_min(window_size=self.lookback_period).shift(1).alias("support"),
            pl.col("volume").rolling_mean(window_size=self.lookback_period).alias("avg_volume")
        ])
        
        # Breakout conditions
        df = df.with_columns([
            # Bullish breakout: close above resistance
            (pl.col("close") > pl.col("resistance")).alias("bullish_breakout"),
            
            # Bearish breakdown: close below support
            (pl.col("close") < pl.col("support")).alias("bearish_breakdown"),
            
            # Volume confirmation
            (pl.col("volume") > (pl.col("avg_volume") * self.volume_multiplier)).alias("high_volume")
        ])
        
        # Generate signals
        df = df.with_columns([
            pl.when(
                pl.col("bullish_breakout") & pl.col("high_volume")
            ).then(Signal.BUY.value)
            .when(
                pl.col("bearish_breakdown")
            ).then(Signal.SELL.value)
            .otherwise(Signal.HOLD.value)
            .alias("signal")
        ])
        
        # Clean up temporary columns
        df = df.drop([
            "resistance", "support", "avg_volume",
            "bullish_breakout", "bearish_breakdown", "high_volume"
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
