'''Unit tests for the risk metrics calculator.'''

import pytest
import numpy as np
import polars as pl
from quant.risk.metrics import RiskMetrics


@pytest.fixture
def sample_prices():
    """Sample price data for testing."""
    return np.array([100, 110, 105, 115, 120, 110, 100, 95, 105, 110])


@pytest.fixture
def sample_returns(sample_prices):
    """Sample returns data for testing."""
    return RiskMetrics.calculate_returns(sample_prices)


def test_calculate_returns(sample_prices):
    """Tests the calculate_returns method."""
    returns = RiskMetrics.calculate_returns(sample_prices)
    assert len(returns) == len(sample_prices) - 1
    assert np.isclose(returns[0], 0.1)


def test_volatility(sample_returns):
    """Tests the volatility method."""
    volatility = RiskMetrics.volatility(sample_returns, annualize=False)
    assert volatility > 0


def test_sharpe_ratio(sample_returns):
    """Tests the sharpe_ratio method."""
    sharpe = RiskMetrics.sharpe_ratio(sample_returns)
    assert isinstance(sharpe, float)


def test_max_drawdown(sample_prices):
    """Tests the max_drawdown method."""
    drawdown = RiskMetrics.max_drawdown(sample_prices)
    assert drawdown["max_drawdown"] > 0
    assert drawdown["max_drawdown_pct"] > 0


def test_comprehensive_report(sample_returns, sample_prices):
    """Tests the comprehensive_report method."""
    report = RiskMetrics.comprehensive_report(sample_returns, sample_prices)
    assert "sharpe_ratio" in report
    assert "max_drawdown" in report
    assert "volatility" in report
