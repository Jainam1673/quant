"""Volume-based indicators for technical analysis.

This module provides indicators that use trading volume to help assess the
strength of price movements and identify potential trend reversals.
"""

import polars as pl

from .base import IndicatorBase


class OBV(IndicatorBase):
    """Calculates the On-Balance Volume (OBV).

    OBV is a momentum indicator that uses volume flow to predict changes in
    stock price. It relates volume to price change and can be used to confirm
    price trends.
    """

    def __init__(self):
        """Initializes the OBV indicator."""
        super().__init__("OBV")

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the OBV calculation."""
        df = df.with_columns(
            [
                pl.when(pl.col("close") > pl.col("close").shift(1))
                .then(pl.col("volume"))
                .when(pl.col("close") < pl.col("close").shift(1))
                .then(-pl.col("volume"))
                .otherwise(0)
                .alias("obv_change"),
            ]
        )

        df = df.with_columns(
            [
                pl.col("obv_change").cum_sum().alias(self.name),
            ]
        )

        return df.drop(["obv_change"])


class VWAP(IndicatorBase):
    """Calculates the Volume-Weighted Average Price (VWAP).

    VWAP is a trading benchmark that gives the average price a security has
    traded at throughout the day, based on both volume and price.
    """

    def __init__(self):
        """Initializes the VWAP indicator."""
        super().__init__("VWAP")

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the VWAP calculation."""
        # Typical price
        df = df.with_columns(
            [
                ((pl.col("high") + pl.col("low") + pl.col("close")) / 3).alias("typical_price"),
            ]
        )

        # VWAP calculation
        df = df.with_columns(
            [
                (pl.col("typical_price") * pl.col("volume")).alias("tp_volume"),
            ]
        )

        df = df.with_columns(
            [
                (pl.col("tp_volume").cum_sum() / pl.col("volume").cum_sum()).alias(self.name),
            ]
        )

        return df.drop(["typical_price", "tp_volume"])


class MFI(IndicatorBase):
    """Calculates the Money Flow Index (MFI).

    The MFI is a momentum indicator that measures the flow of money into and
    out of a security over a specified period. It is related to RSI but
    incorporates volume.

    Args:
        period (int): The period for the MFI calculation.
    """

    def __init__(self, period: int = 14):
        """Initializes the MFI indicator."""
        super().__init__(f"MFI_{period}")
        self.period = period

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Performs the MFI calculation."""
        # Typical price
        df = df.with_columns(
            [
                ((pl.col("high") + pl.col("low") + pl.col("close")) / 3).alias("typical_price"),
            ]
        )

        # Raw money flow
        df = df.with_columns(
            [
                (pl.col("typical_price") * pl.col("volume")).alias("raw_money_flow"),
            ]
        )

        # Positive and negative money flow
        df = df.with_columns(
            [
                pl.when(pl.col("typical_price") > pl.col("typical_price").shift(1))
                .then(pl.col("raw_money_flow"))
                .otherwise(0)
                .alias("positive_flow"),
                pl.when(pl.col("typical_price") < pl.col("typical_price").shift(1))
                .then(pl.col("raw_money_flow"))
                .otherwise(0)
                .alias("negative_flow"),
            ]
        )

        # Sum over period
        df = df.with_columns(
            [
                pl.col("positive_flow").rolling_sum(window_size=self.period).alias("positive_mf"),
                pl.col("negative_flow").rolling_sum(window_size=self.period).alias("negative_mf"),
            ]
        )

        # Money flow ratio and MFI
        df = df.with_columns(
            [
                (pl.col("positive_mf") / pl.col("negative_mf")).alias("mf_ratio"),
            ]
        )

        df = df.with_columns(
            [
                (100 - (100 / (1 + pl.col("mf_ratio")))).alias(self.name),
            ]
        )

        return df.drop(
            [
                "typical_price",
                "raw_money_flow",
                "positive_flow",
                "negative_flow",
                "positive_mf",
                "negative_mf",
                "mf_ratio",
            ]
        )
