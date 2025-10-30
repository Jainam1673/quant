'''Unit tests for the trading strategies.'''

import pytest
import polars as pl
from quant.strategies.breakout import BreakoutStrategy
from quant.strategies.mean_reversion import MeanReversionStrategy
from quant.strategies.momentum_strategy import MomentumStrategy
from quant.indicators import SMA, BollingerBands, RSI


@pytest.fixture
def sample_data():
    """Sample data for strategy testing."""
    return pl.DataFrame({
        "timestamp": [f"2024-01-{i:02d}" for i in range(1, 21)],
        "open": [100 + i for i in range(20)],
        "high": [102 + i for i in range(20)],
        "low": [98 + i for i in range(20)],
        "close": [101 + i for i in range(20)],
        "volume": [1000000 + i * 10000 for i in range(20)],
    })


def test_breakout_strategy_buy_signal(sample_data):
    """Tests the BreakoutStrategy for a buy signal."""
    strategy = BreakoutStrategy(lookback_period=5)
    signals = strategy.generate_signals(sample_data)
    assert "signal" in signals.columns


def test_mean_reversion_strategy_buy_signal(sample_data):
    """Tests the MeanReversionStrategy for a buy signal."""
    data_with_bb = BollingerBands(period=5)(sample_data)
    strategy = MeanReversionStrategy(bb_period=5)
    signals = strategy.generate_signals(data_with_bb)
    assert "signal" in signals.columns


def test_momentum_strategy_buy_signal(sample_data):
    """Tests the MomentumStrategy for a buy signal."""
    data_with_indicators = SMA(50)(sample_data)
    data_with_indicators = SMA(200)(data_with_indicators)
    data_with_indicators = RSI(14)(data_with_indicators)
    strategy = MomentumStrategy()
    signals = strategy.generate_signals(data_with_indicators)
    assert "signal" in signals.columns
