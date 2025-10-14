"""Test configuration and fixtures."""

import pytest


@pytest.fixture
def sample_ohlcv_data():
    """Provide sample OHLCV data for testing."""
    import polars as pl
    
    return pl.DataFrame({
        "ticker": ["AAPL"] * 10,
        "timestamp": [f"2024-01-{i:02d}" for i in range(1, 11)],
        "open": [150.0 + i for i in range(10)],
        "high": [155.0 + i for i in range(10)],
        "low": [149.0 + i for i in range(10)],
        "close": [154.0 + i for i in range(10)],
        "volume": [1000000 + i * 10000 for i in range(10)],
    })
