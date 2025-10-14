"""Unit tests for database module."""

import pytest
import polars as pl
from pathlib import Path
import tempfile
import os

from quant.data.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.duckdb")
        db = Database(db_path)
        yield db
        db.close()


def test_database_initialization(temp_db):
    """Test database initializes correctly."""
    assert temp_db.conn is not None
    assert Path(temp_db.db_path).exists()


def test_insert_and_retrieve_ohlcv(temp_db):
    """Test inserting and retrieving OHLCV data."""
    # Create sample data
    data = pl.DataFrame({
        "ticker": ["AAPL"] * 3,
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "open": [150.0, 151.0, 152.0],
        "high": [155.0, 156.0, 157.0],
        "low": [149.0, 150.0, 151.0],
        "close": [154.0, 155.0, 156.0],
        "volume": [1000000, 1100000, 1200000],
    })
    
    # Insert data
    temp_db.insert_ohlcv(data)
    
    # Retrieve data
    result = temp_db.get_ohlcv("AAPL")
    
    assert not result.is_empty()
    assert len(result) == 3
    assert result["ticker"][0] == "AAPL"


def test_get_ohlcv_with_date_filter(temp_db):
    """Test retrieving OHLCV data with date filters."""
    # Create sample data
    data = pl.DataFrame({
        "ticker": ["AAPL"] * 5,
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        "open": [150.0, 151.0, 152.0, 153.0, 154.0],
        "high": [155.0, 156.0, 157.0, 158.0, 159.0],
        "low": [149.0, 150.0, 151.0, 152.0, 153.0],
        "close": [154.0, 155.0, 156.0, 157.0, 158.0],
        "volume": [1000000, 1100000, 1200000, 1300000, 1400000],
    })
    
    temp_db.insert_ohlcv(data)
    
    # Test date filtering
    result = temp_db.get_ohlcv("AAPL", start_date="2024-01-02", end_date="2024-01-04")
    
    assert len(result) == 3


def test_get_multiple_tickers(temp_db):
    """Test retrieving data for multiple tickers."""
    # Create sample data for multiple tickers
    data = pl.DataFrame({
        "ticker": ["AAPL", "AAPL", "GOOGL", "GOOGL"],
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02"],
        "open": [150.0, 151.0, 2800.0, 2850.0],
        "high": [155.0, 156.0, 2900.0, 2950.0],
        "low": [149.0, 150.0, 2750.0, 2800.0],
        "close": [154.0, 155.0, 2880.0, 2930.0],
        "volume": [1000000, 1100000, 500000, 550000],
    })
    
    temp_db.insert_ohlcv(data)
    
    # Retrieve multiple tickers
    result = temp_db.get_multiple_tickers(["AAPL", "GOOGL"])
    
    assert len(result) == 4
    assert "AAPL" in result["ticker"].to_list()
    assert "GOOGL" in result["ticker"].to_list()


def test_save_and_retrieve_backtest_run(temp_db):
    """Test saving and retrieving backtest runs."""
    run_data = {
        "run_id": "test_run_1",
        "strategy_name": "TestStrategy",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "initial_capital": 100000.0,
        "final_value": 120000.0,
        "total_return": 20000.0,
        "sharpe_ratio": 1.5,
        "max_drawdown": -0.15
    }
    
    temp_db.save_backtest_run(run_data)
    
    # Retrieve runs
    runs = temp_db.get_backtest_runs()
    
    assert not runs.is_empty()
    assert runs["run_id"][0] == "test_run_1"
    assert runs["strategy_name"][0] == "TestStrategy"
