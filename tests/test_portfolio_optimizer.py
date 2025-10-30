'''Unit tests for the portfolio optimizer.'''

import pytest
import polars as pl
import numpy as np
from quant.portfolio.optimizer import PortfolioOptimizer


@pytest.fixture
def sample_returns_df():
    """Sample returns data for testing."""
    return pl.DataFrame({
        "AAPL": np.random.normal(0.001, 0.02, 252),
        "GOOG": np.random.normal(0.001, 0.02, 252),
    })


def test_optimizer_initialization(sample_returns_df):
    """Tests the initialization of the PortfolioOptimizer."""
    optimizer = PortfolioOptimizer(sample_returns_df)
    assert optimizer.n_assets == 2
    assert optimizer.mean_returns.shape == (2,)
    assert optimizer.cov_matrix.shape == (2, 2)


def test_portfolio_stats(sample_returns_df):
    """Tests the portfolio_stats method."""
    optimizer = PortfolioOptimizer(sample_returns_df)
    weights = np.array([0.5, 0.5])
    ret, vol, sharpe = optimizer.portfolio_stats(weights)
    assert isinstance(ret, float)
    assert isinstance(vol, float)
    assert isinstance(sharpe, float)


def test_minimize_volatility(sample_returns_df):
    """Tests the minimize_volatility method."""
    optimizer = PortfolioOptimizer(sample_returns_df)
    result = optimizer.minimize_volatility()
    assert result["success"]
    assert len(result["weights"]) == 2
    assert np.isclose(sum(result["weights"].values()), 1.0)


def test_maximize_sharpe(sample_returns_df):
    """Tests the maximize_sharpe method."""
    optimizer = PortfolioOptimizer(sample_returns_df)
    result = optimizer.maximize_sharpe()
    assert result["success"]
    assert len(result["weights"]) == 2
    assert np.isclose(sum(result["weights"].values()), 1.0)


def test_efficient_frontier(sample_returns_df):
    """Tests the efficient_frontier method."""
    optimizer = PortfolioOptimizer(sample_returns_df)
    frontier = optimizer.efficient_frontier(n_points=10)
    assert isinstance(frontier, pl.DataFrame)
    assert len(frontier) > 0
    assert "return" in frontier.columns
    assert "volatility" in frontier.columns
    assert "sharpe_ratio" in frontier.columns
