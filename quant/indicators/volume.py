"""Volume indicators."""

import polars as pl
from .base import IndicatorBase


class OBV(IndicatorBase):
    """On-Balance Volume."""
    
    def __init__(self):
        """Initialize OBV."""
        super().__init__("OBV")
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate OBV."""
        df = df.with_columns([
            pl.when(pl.col("close") > pl.col("close").shift(1))
            .then(pl.col("volume"))
            .when(pl.col("close") < pl.col("close").shift(1))
            .then(-pl.col("volume"))
            .otherwise(0)
            .alias("obv_change")
        ])
        
        df = df.with_columns([
            pl.col("obv_change").cum_sum().alias(self.name)
        ])
        
        return df.drop(["obv_change"])


class VWAP(IndicatorBase):
    """Volume Weighted Average Price."""
    
    def __init__(self):
        """Initialize VWAP."""
        super().__init__("VWAP")
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate VWAP."""
        # Typical price
        df = df.with_columns([
            ((pl.col("high") + pl.col("low") + pl.col("close")) / 3).alias("typical_price")
        ])
        
        # VWAP calculation
        df = df.with_columns([
            (pl.col("typical_price") * pl.col("volume")).alias("tp_volume")
        ])
        
        df = df.with_columns([
            (pl.col("tp_volume").cum_sum() / pl.col("volume").cum_sum()).alias(self.name)
        ])
        
        return df.drop(["typical_price", "tp_volume"])


class MFI(IndicatorBase):
    """Money Flow Index."""
    
    def __init__(self, period: int = 14):
        """Initialize MFI.
        
        Args:
            period: Period for MFI calculation
        """
        super().__init__(f"MFI_{period}")
        self.period = period
    
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate MFI."""
        # Typical price
        df = df.with_columns([
            ((pl.col("high") + pl.col("low") + pl.col("close")) / 3).alias("typical_price")
        ])
        
        # Raw money flow
        df = df.with_columns([
            (pl.col("typical_price") * pl.col("volume")).alias("raw_money_flow")
        ])
        
        # Positive and negative money flow
        df = df.with_columns([
            pl.when(pl.col("typical_price") > pl.col("typical_price").shift(1))
            .then(pl.col("raw_money_flow"))
            .otherwise(0)
            .alias("positive_flow"),
            
            pl.when(pl.col("typical_price") < pl.col("typical_price").shift(1))
            .then(pl.col("raw_money_flow"))
            .otherwise(0)
            .alias("negative_flow")
        ])
        
        # Sum over period
        df = df.with_columns([
            pl.col("positive_flow").rolling_sum(window_size=self.period).alias("positive_mf"),
            pl.col("negative_flow").rolling_sum(window_size=self.period).alias("negative_mf")
        ])
        
        # Money flow ratio and MFI
        df = df.with_columns([
            (pl.col("positive_mf") / pl.col("negative_mf")).alias("mf_ratio")
        ])
        
        df = df.with_columns([
            (100 - (100 / (1 + pl.col("mf_ratio")))).alias(self.name)
        ])
        
        return df.drop([
            "typical_price", "raw_money_flow", "positive_flow", "negative_flow",
            "positive_mf", "negative_mf", "mf_ratio"
        ])
