'''Unit tests for the Value at Risk (VaR) calculator.'''

import pytest
import numpy as np
from quant.risk.var import VaRCalculator


@pytest.fixture
def sample_returns():
    """Sample returns data for testing."""
    np.random.seed(42)
    return np.random.normal(0.001, 0.02, 1000)


def test_historical_var(sample_returns):
    """Tests the historical_var method."""
    var = VaRCalculator.historical_var(sample_returns)
    assert var > 0


def test_parametric_var(sample_returns):
    """Tests the parametric_var method."""
    var = VaRCalculator.parametric_var(sample_returns)
    assert var > 0


def test_monte_carlo_var(sample_returns):
    """Tests the monte_carlo_var method."""
    var = VaRCalculator.monte_carlo_var(sample_returns)
    assert var > 0


def test_historical_cvar(sample_returns):
    """Tests the historical_cvar method."""
    cvar = VaRCalculator.historical_cvar(sample_returns)
    assert cvar > 0


def test_parametric_cvar(sample_returns):
    """Tests the parametric_cvar method."""
    cvar = VaRCalculator.parametric_cvar(sample_returns)
    assert cvar > 0


def test_calculate_all_var(sample_returns):
    """Tests the calculate_all_var method."""
    all_var = VaRCalculator.calculate_all_var(sample_returns)
    assert "historical_var" in all_var
    assert "parametric_var" in all_var
    assert "monte_carlo_var" in all_var
    assert "historical_cvar" in all_var
    assert "parametric_cvar" in all_var
