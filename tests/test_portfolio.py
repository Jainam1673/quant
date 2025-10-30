'''Unit tests for the portfolio and holding classes.'''

import pytest
from quant.portfolio.portfolio import Holding, Portfolio


@pytest.fixture
def sample_portfolio():
    """Sample portfolio for testing."""
    return Portfolio(name="Test Portfolio", initial_capital=100000)


def test_holding_calculation():
    """Tests the calculations within the Holding class."""
    holding = Holding(ticker="AAPL", quantity=10, avg_price=150, current_price=160)
    assert holding.cost_basis == 1500
    assert holding.market_value == 1600
    assert holding.unrealized_pnl == 100
    assert holding.unrealized_pnl_pct == pytest.approx((100 / 1500) * 100)


def test_portfolio_initialization(sample_portfolio):
    """Tests the initialization of the Portfolio class."""
    assert sample_portfolio.name == "Test Portfolio"
    assert sample_portfolio.initial_capital == 100000
    assert sample_portfolio.cash == 100000
    assert sample_portfolio.total_value == 100000


def test_buy_transaction(sample_portfolio):
    """Tests the buy method of the Portfolio class."""
    sample_portfolio.buy(ticker="AAPL", quantity=10, price=150)
    assert sample_portfolio.cash == 100000 - (10 * 150)
    assert "AAPL" in sample_portfolio.holdings
    assert sample_portfolio.holdings["AAPL"].quantity == 10
    assert len(sample_portfolio.transaction_history) == 1


def test_sell_transaction(sample_portfolio):
    """Tests the sell method of the Portfolio class."""
    sample_portfolio.buy(ticker="AAPL", quantity=10, price=150)
    sample_portfolio.sell(ticker="AAPL", quantity=5, price=160)
    assert sample_portfolio.cash == 100000 - (10 * 150) + (5 * 160)
    assert sample_portfolio.holdings["AAPL"].quantity == 5
    assert len(sample_portfolio.transaction_history) == 2


def test_update_prices(sample_portfolio):
    """Tests the update_prices method."""
    sample_portfolio.buy(ticker="AAPL", quantity=10, price=150)
    sample_portfolio.update_prices({"AAPL": 160})
    assert sample_portfolio.holdings["AAPL"].current_price == 160
    assert sample_portfolio.holdings["AAPL"].market_value == 1600


def test_portfolio_summary(sample_portfolio):
    """Tests the summary method."""
    sample_portfolio.buy(ticker="AAPL", quantity=10, price=150)
    sample_portfolio.update_prices({"AAPL": 160})
    summary = sample_portfolio.summary()
    assert summary["total_value"] == 100000 - 1500 + 1600
    assert summary["total_pnl"] == 100
