"""Mean reversion trading strategy."""

import polars as pl
from .base import Strategy, Signal


class MeanReversionStrategy(Strategy):
    """Mean reversion strategy using Bollinger Bands."""
    
    def __init__(
        self,
        bb_period: int = 20,
        bb_std: float = 2.0,
        position_size_pct: float = 0.1
    ):
        """Initialize mean reversion strategy.
        
        Args:
            bb_period: Bollinger Bands period
            bb_std: Bollinger Bands standard deviation
            position_size_pct: Percentage of capital to use per trade
        """
        super().__init__("Mean Reversion Strategy")
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.position_size_pct = position_size_pct
    
    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generate mean reversion signals using Bollinger Bands.
        
        Buy when:
        - Price touches or goes below lower Bollinger Band
        
        Sell when:
        - Price touches or goes above upper Bollinger Band
        - Price returns to middle band (take profit)
        """
        # Check for required columns
        required_cols = ["BB_upper", "BB_lower", "BB_middle"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Required indicator {col} not found. Calculate Bollinger Bands first.")
        
        # Generate signals
        df = df.with_columns([
            # Price position relative to bands
            (pl.col("close") <= pl.col("BB_lower")).alias("at_lower_band"),
            (pl.col("close") >= pl.col("BB_upper")).alias("at_upper_band"),
            (pl.col("close").shift(1) < pl.col("BB_middle")).alias("was_below_middle"),
            (pl.col("close") >= pl.col("BB_middle")).alias("at_or_above_middle"),
        ])
        
        # Buy at lower band, sell at upper band or middle band (take profit)
        df = df.with_columns([
            pl.when(
                pl.col("at_lower_band")
            ).then(Signal.BUY.value)
            .when(
                pl.col("at_upper_band") | 
                (pl.col("was_below_middle") & pl.col("at_or_above_middle"))
            ).then(Signal.SELL.value)
            .otherwise(Signal.HOLD.value)
            .alias("signal")
        ])
        
        # Clean up temporary columns
        df = df.drop([
            "at_lower_band", "at_upper_band", "was_below_middle", "at_or_above_middle"
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
