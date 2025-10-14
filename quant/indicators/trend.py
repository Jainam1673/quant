"""Trend indicators."""

import polars as pl
from .base import IndicatorBase


class SMA(IndicatorBase):
    """Simple Moving Average."""
    
    def __init__(self, period: int = 20, column: str = "close"):
        """Initialize SMA.
        
        Args:
            period: Number of periods for the moving average
            column: Column to calculate SMA on
        """
        super().__init__(f"SMA_{period}")
        self.period = period
        self.column = column
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate SMA."""
        return df.with_columns(
            pl.col(self.column).rolling_mean(window_size=self.period).alias(self.name)
        )


class EMA(IndicatorBase):
    """Exponential Moving Average."""
    
    def __init__(self, period: int = 20, column: str = "close"):
        """Initialize EMA.
        
        Args:
            period: Number of periods for the moving average
            column: Column to calculate EMA on
        """
        super().__init__(f"EMA_{period}")
        self.period = period
        self.column = column
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate EMA."""
        return df.with_columns(
            pl.col(self.column).ewm_mean(span=self.period).alias(self.name)
        )


class MACD(IndicatorBase):
    """Moving Average Convergence Divergence."""
    
    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
        column: str = "close"
    ):
        """Initialize MACD.
        
        Args:
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line period
            column: Column to calculate MACD on
        """
        super().__init__("MACD")
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.column = column
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate MACD."""
        ema_fast = pl.col(self.column).ewm_mean(span=self.fast_period)
        ema_slow = pl.col(self.column).ewm_mean(span=self.slow_period)
        
        df = df.with_columns([
            (ema_fast - ema_slow).alias("MACD"),
        ])
        
        df = df.with_columns([
            pl.col("MACD").ewm_mean(span=self.signal_period).alias("MACD_signal"),
        ])
        
        df = df.with_columns([
            (pl.col("MACD") - pl.col("MACD_signal")).alias("MACD_histogram")
        ])
        
        return df


class ADX(IndicatorBase):
    """Average Directional Index."""
    
    def __init__(self, period: int = 14):
        """Initialize ADX.
        
        Args:
            period: Period for ADX calculation
        """
        super().__init__(f"ADX_{period}")
        self.period = period
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate ADX."""
        # Calculate True Range
        df = df.with_columns([
            pl.max_horizontal([
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs()
            ]).alias("TR")
        ])
        
        # Calculate +DM and -DM
        df = df.with_columns([
            pl.when(
                (pl.col("high") - pl.col("high").shift(1)) > (pl.col("low").shift(1) - pl.col("low"))
            ).then(
                pl.max_horizontal([pl.col("high") - pl.col("high").shift(1), 0])
            ).otherwise(0).alias("plus_DM"),
            
            pl.when(
                (pl.col("low").shift(1) - pl.col("low")) > (pl.col("high") - pl.col("high").shift(1))
            ).then(
                pl.max_horizontal([pl.col("low").shift(1) - pl.col("low"), 0])
            ).otherwise(0).alias("minus_DM")
        ])
        
        # Calculate smoothed TR, +DM, -DM
        df = df.with_columns([
            pl.col("TR").rolling_mean(window_size=self.period).alias("ATR"),
            pl.col("plus_DM").rolling_mean(window_size=self.period).alias("plus_DM_smooth"),
            pl.col("minus_DM").rolling_mean(window_size=self.period).alias("minus_DM_smooth")
        ])
        
        # Calculate +DI and -DI
        df = df.with_columns([
            (100 * pl.col("plus_DM_smooth") / pl.col("ATR")).alias("plus_DI"),
            (100 * pl.col("minus_DM_smooth") / pl.col("ATR")).alias("minus_DI")
        ])
        
        # Calculate DX and ADX
        df = df.with_columns([
            (100 * (pl.col("plus_DI") - pl.col("minus_DI")).abs() / 
             (pl.col("plus_DI") + pl.col("minus_DI"))).alias("DX")
        ])
        
        df = df.with_columns([
            pl.col("DX").rolling_mean(window_size=self.period).alias(self.name)
        ])
        
        return df
