'''Unit tests for the backtesting performance metrics.'''

import pytest
import polars as pl
import numpy as np
from quant.backtesting.metrics import PerformanceMetrics
from quant.backtesting.engine import Trade


@pytest.fixture
def sample_equity_curve():
    """Sample equity curve for testing."""
    return pl.DataFrame({
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        "equity": [100000.0, 101000.0, 100500.0, 101500.0, 102000.0],
    })


@pytest.fixture
def sample_trades():
    """Sample trades for testing."""
    return [
        Trade("1", "TEST", "2024-01-01", "2024-01-02", 100, 101, 10, "long", 100, 1, 1),
        Trade("2", "TEST", "2024-01-03", "2024-01-04", 100.5, 101.5, 10, "long", 100, 1, 1),
        Trade("3", "TEST", "2024-01-04", "2024-01-05", 101.5, 102, 10, "long", 50, 0.5, 1),
    ]


def test_calculate_no_trades():
    """Tests the calculate method with no trades."""
    metrics = PerformanceMetrics.calculate(pl.DataFrame(), [])
    assert metrics["num_trades"] == 0
    assert metrics["sharpe_ratio"] == 0


def test_calculate_with_trades(sample_equity_curve, sample_trades):
    """Tests the calculate method with sample trades."""
    metrics = PerformanceMetrics.calculate(sample_equity_curve, sample_trades)
    assert metrics["num_trades"] == 3
    assert metrics["winning_trades"] == 3
    assert metrics["losing_trades"] == 0
    assert metrics["win_rate"] == 100.0
    assert metrics["sharpe_ratio"] > 0


def test_calculate_rolling_metrics(sample_equity_curve):
    """Tests the calculate_rolling_metrics method."""
    rolling_metrics = PerformanceMetrics.calculate_rolling_metrics(sample_equity_curve, window=2)
    assert "rolling_sharpe" in rolling_metrics.columns
    assert rolling_metrics["rolling_sharpe"].is_null().sum() == 2
