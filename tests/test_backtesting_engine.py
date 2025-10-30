'''Unit tests for the backtesting engine.'''

import pytest
import polars as pl
from quant.backtesting.engine import BacktestEngine, Trade
from quant.strategies.base import Strategy, Signal


class MockStrategy(Strategy):
    """A mock strategy for testing purposes."""

    def __init__(self, signals):
        super().__init__("Mock Strategy")
        self.signals = signals

    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generates signals from a predefined list."""
        return df.with_columns(pl.Series("signal", self.signals))

    def calculate_position_size(self, df: pl.DataFrame, capital: float, current_price: float) -> float:
        """Calculates a fixed position size."""
        return 10


@pytest.fixture
def sample_data():
    """Sample data for backtesting."""
    return pl.DataFrame({
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        "close": [100.0, 110.0, 120.0, 115.0, 125.0],
    })


def test_backtest_single_trade(sample_data):
    """Tests a simple backtest with a single buy and sell."""
    signals = [Signal.BUY.value, Signal.HOLD.value, Signal.SELL.value, Signal.HOLD.value, Signal.HOLD.value]
    strategy = MockStrategy(signals)
    engine = BacktestEngine(strategy)

    result = engine.run(sample_data, ticker="TEST")

    assert result.num_trades == 1
    assert result.winning_trades == 1
    assert result.losing_trades == 0
    assert result.win_rate == 100.0

    trade = result.trades[0]
    assert trade.entry_price == 100.0
    assert trade.exit_price == 120.0
    assert trade.quantity == 10
    assert trade.pnl == (120.0 - 100.0) * 10 - (100.0 * 10 * 0.001) - (120.0 * 10 * 0.001) # PnL - commission


def test_backtest_hold_position(sample_data):
    """Tests a backtest where a position is held until the end."""
    signals = [Signal.BUY.value, Signal.HOLD.value, Signal.HOLD.value, Signal.HOLD.value, Signal.HOLD.value]
    strategy = MockStrategy(signals)
    engine = BacktestEngine(strategy)

    result = engine.run(sample_data, ticker="TEST")

    assert result.num_trades == 1
    trade = result.trades[0]
    assert trade.exit_price == 125.0  # Should exit at the last price


def test_backtest_with_commission(sample_data):
    """Tests that commission is correctly applied."""
    signals = [Signal.BUY.value, Signal.SELL.value, Signal.HOLD.value, Signal.HOLD.value, Signal.HOLD.value]
    strategy = MockStrategy(signals)
    engine = BacktestEngine(strategy, commission=0.01)  # 1% commission

    result = engine.run(sample_data, ticker="TEST")

    trade = result.trades[0]
    entry_cost = 100.0 * 10
    exit_proceeds = 110.0 * 10
    entry_commission = entry_cost * 0.01
    exit_commission = exit_proceeds * 0.01
    expected_pnl = (exit_proceeds - entry_cost) - (entry_commission + exit_commission)

    assert trade.pnl == pytest.approx(expected_pnl)
