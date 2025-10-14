"""Momentum indicators."""

import polars as pl
from .base import IndicatorBase


class RSI(IndicatorBase):
    """Relative Strength Index."""
    
    def __init__(self, period: int = 14, column: str = "close"):
        """Initialize RSI.
        
        Args:
            period: Number of periods for RSI calculation
            column: Column to calculate RSI on
        """
        super().__init__(f"RSI_{period}")
        self.period = period
        self.column = column
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate RSI."""
        # Calculate price changes
        df = df.with_columns([
            (pl.col(self.column) - pl.col(self.column).shift(1)).alias("change")
        ])
        
        # Separate gains and losses
        df = df.with_columns([
            pl.when(pl.col("change") > 0).then(pl.col("change")).otherwise(0).alias("gain"),
            pl.when(pl.col("change") < 0).then(pl.col("change").abs()).otherwise(0).alias("loss")
        ])
        
        # Calculate average gain and loss
        df = df.with_columns([
            pl.col("gain").rolling_mean(window_size=self.period).alias("avg_gain"),
            pl.col("loss").rolling_mean(window_size=self.period).alias("avg_loss")
        ])
        
        # Calculate RS and RSI
        df = df.with_columns([
            (pl.col("avg_gain") / pl.col("avg_loss")).alias("RS")
        ])
        
        df = df.with_columns([
            (100 - (100 / (1 + pl.col("RS")))).alias(self.name)
        ])
        
        return df.drop(["change", "gain", "loss", "avg_gain", "avg_loss", "RS"])


class Stochastic(IndicatorBase):
    """Stochastic Oscillator."""
    
    def __init__(self, k_period: int = 14, d_period: int = 3):
        """Initialize Stochastic.
        
        Args:
            k_period: %K period
            d_period: %D period (SMA of %K)
        """
        super().__init__("Stochastic")
        self.k_period = k_period
        self.d_period = d_period
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate Stochastic."""
        # Calculate %K
        df = df.with_columns([
            pl.col("low").rolling_min(window_size=self.k_period).alias("lowest_low"),
            pl.col("high").rolling_max(window_size=self.k_period).alias("highest_high")
        ])
        
        df = df.with_columns([
            (100 * (pl.col("close") - pl.col("lowest_low")) / 
             (pl.col("highest_high") - pl.col("lowest_low"))).alias("stoch_k")
        ])
        
        # Calculate %D (SMA of %K)
        df = df.with_columns([
            pl.col("stoch_k").rolling_mean(window_size=self.d_period).alias("stoch_d")
        ])
        
        return df.drop(["lowest_low", "highest_high"])


class ROC(IndicatorBase):
    """Rate of Change."""
    
    def __init__(self, period: int = 12, column: str = "close"):
        """Initialize ROC.
        
        Args:
            period: Number of periods to look back
            column: Column to calculate ROC on
        """
        super().__init__(f"ROC_{period}")
        self.period = period
        self.column = column
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate ROC."""
        return df.with_columns([
            (100 * (pl.col(self.column) - pl.col(self.column).shift(self.period)) / 
             pl.col(self.column).shift(self.period)).alias(self.name)
        ])


class Williams_R(IndicatorBase):
    """Williams %R."""
    
    def __init__(self, period: int = 14):
        """Initialize Williams %R.
        
        Args:
            period: Lookback period
        """
        super().__init__(f"Williams_R_{period}")
        self.period = period
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate Williams %R."""
        df = df.with_columns([
            pl.col("high").rolling_max(window_size=self.period).alias("highest_high"),
            pl.col("low").rolling_min(window_size=self.period).alias("lowest_low")
        ])
        
        df = df.with_columns([
            (-100 * (pl.col("highest_high") - pl.col("close")) / 
             (pl.col("highest_high") - pl.col("lowest_low"))).alias(self.name)
        ])
        
        return df.drop(["highest_high", "lowest_low"])
