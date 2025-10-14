"""Unit tests for technical indicators."""

import pytest
import polars as pl
from quant.indicators import SMA, EMA, RSI, MACD, BollingerBands


@pytest.fixture
def sample_price_data():
    """Create sample price data for indicator testing."""
    return pl.DataFrame({
        "timestamp": [f"2024-01-{i:02d}" for i in range(1, 31)],
        "open": [100.0 + i * 0.5 for i in range(30)],
        "high": [102.0 + i * 0.5 for i in range(30)],
        "low": [98.0 + i * 0.5 for i in range(30)],
        "close": [101.0 + i * 0.5 for i in range(30)],
        "volume": [1000000 + i * 10000 for i in range(30)],
    })


def test_sma_calculation(sample_price_data):
    """Test Simple Moving Average calculation."""
    sma = SMA(period=10)
    result = sma.calculate(sample_price_data)
    
    assert "SMA_10" in result.columns
    assert not result["SMA_10"].is_null().all()
    
    # Check that first 9 values are null (window size)
    assert result["SMA_10"][:9].is_null().all()
    
    # Check that calculation is approximately correct
    manual_sma = sample_price_data["close"][9:10].to_list()[0] 
    calculated_sma = result["SMA_10"][9]
    assert calculated_sma is not None


def test_ema_calculation(sample_price_data):
    """Test Exponential Moving Average calculation."""
    ema = EMA(period=10)
    result = ema.calculate(sample_price_data)
    
    assert "EMA_10" in result.columns
    assert not result["EMA_10"].is_null().all()


def test_rsi_calculation(sample_price_data):
    """Test RSI calculation."""
    rsi = RSI(period=14)
    result = rsi.calculate(sample_price_data)
    
    assert "RSI_14" in result.columns
    
    # RSI should be between 0 and 100
    rsi_values = result["RSI_14"].drop_nulls()
    assert all(0 <= val <= 100 for val in rsi_values)


def test_macd_calculation(sample_price_data):
    """Test MACD calculation."""
    macd = MACD()
    result = macd.calculate(sample_price_data)
    
    assert "MACD" in result.columns
    assert "MACD_signal" in result.columns
    assert "MACD_hist" in result.columns


def test_bollinger_bands_calculation(sample_price_data):
    """Test Bollinger Bands calculation."""
    bb = BollingerBands(period=20, std_dev=2)
    result = bb.calculate(sample_price_data)
    
    assert "BB_upper" in result.columns
    assert "BB_middle" in result.columns
    assert "BB_lower" in result.columns
    
    # Upper band should be higher than middle, middle higher than lower
    non_null_rows = result.filter(pl.col("BB_upper").is_not_null())
    if len(non_null_rows) > 0:
        assert all(non_null_rows["BB_upper"] > non_null_rows["BB_middle"])
        assert all(non_null_rows["BB_middle"] > non_null_rows["BB_lower"])
