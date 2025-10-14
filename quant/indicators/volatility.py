"""Volatility indicators."""

import polars as pl
from .base import IndicatorBase


class BollingerBands(IndicatorBase):
    """Bollinger Bands."""
    
    def __init__(self, period: int = 20, std_dev: float = 2.0, column: str = "close"):
        """Initialize Bollinger Bands.
        
        Args:
            period: Period for moving average
            std_dev: Number of standard deviations
            column: Column to calculate on
        """
        super().__init__(f"BB_{period}")
        self.period = period
        self.std_dev = std_dev
        self.column = column
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate Bollinger Bands."""
        df = df.with_columns([
            pl.col(self.column).rolling_mean(window_size=self.period).alias("BB_middle"),
            pl.col(self.column).rolling_std(window_size=self.period).alias("BB_std")
        ])
        
        df = df.with_columns([
            (pl.col("BB_middle") + (self.std_dev * pl.col("BB_std"))).alias("BB_upper"),
            (pl.col("BB_middle") - (self.std_dev * pl.col("BB_std"))).alias("BB_lower")
        ])
        
        # Calculate %B (position within bands)
        df = df.with_columns([
            ((pl.col(self.column) - pl.col("BB_lower")) / 
             (pl.col("BB_upper") - pl.col("BB_lower"))).alias("BB_percent")
        ])
        
        # Calculate bandwidth
        df = df.with_columns([
            ((pl.col("BB_upper") - pl.col("BB_lower")) / pl.col("BB_middle")).alias("BB_width")
        ])
        
        return df.drop(["BB_std"])


class ATR(IndicatorBase):
    """Average True Range."""
    
    def __init__(self, period: int = 14):
        """Initialize ATR.
        
        Args:
            period: Period for ATR calculation
        """
        super().__init__(f"ATR_{period}")
        self.period = period
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate ATR."""
        # Calculate True Range
        df = df.with_columns([
            pl.max_horizontal([
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs()
            ]).alias("TR")
        ])
        
        # Calculate ATR (EMA of TR)
        df = df.with_columns([
            pl.col("TR").ewm_mean(span=self.period).alias(self.name)
        ])
        
        return df.drop(["TR"])


class KeltnerChannel(IndicatorBase):
    """Keltner Channel."""
    
    def __init__(self, ema_period: int = 20, atr_period: int = 10, multiplier: float = 2.0):
        """Initialize Keltner Channel.
        
        Args:
            ema_period: Period for EMA (middle line)
            atr_period: Period for ATR
            multiplier: ATR multiplier for bands
        """
        super().__init__(f"KC_{ema_period}")
        self.ema_period = ema_period
        self.atr_period = atr_period
        self.multiplier = multiplier
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate Keltner Channel."""
        # Calculate middle line (EMA of close)
        df = df.with_columns([
            pl.col("close").ewm_mean(span=self.ema_period).alias("KC_middle")
        ])
        
        # Calculate ATR
        df = df.with_columns([
            pl.max_horizontal([
                pl.col("high") - pl.col("low"),
                (pl.col("high") - pl.col("close").shift(1)).abs(),
                (pl.col("low") - pl.col("close").shift(1)).abs()
            ]).alias("TR")
        ])
        
        df = df.with_columns([
            pl.col("TR").ewm_mean(span=self.atr_period).alias("KC_ATR")
        ])
        
        # Calculate upper and lower bands
        df = df.with_columns([
            (pl.col("KC_middle") + (self.multiplier * pl.col("KC_ATR"))).alias("KC_upper"),
            (pl.col("KC_middle") - (self.multiplier * pl.col("KC_ATR"))).alias("KC_lower")
        ])
        
        return df.drop(["TR", "KC_ATR"])
