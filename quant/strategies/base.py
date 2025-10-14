"""Base strategy class and signal definitions."""

import polars as pl
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Signal(Enum):
    """Trading signals."""
    BUY = 1
    SELL = -1
    HOLD = 0


@dataclass
class Position:
    """Represents a trading position."""
    ticker: str
    quantity: float
    entry_price: float
    entry_date: str
    side: str  # 'long' or 'short'
    
    def pnl(self, current_price: float) -> float:
        """Calculate unrealized P&L."""
        if self.side == 'long':
            return (current_price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - current_price) * self.quantity
    
    def pnl_percent(self, current_price: float) -> float:
        """Calculate unrealized P&L percentage."""
        if self.side == 'long':
            return ((current_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - current_price) / self.entry_price) * 100


class Strategy(ABC):
    """Base class for trading strategies."""
    
    def __init__(self, name: str):
        """Initialize strategy.
        
        Args:
            name: Strategy name
        """
        self.name = name
        self.positions: dict[str, Position] = {}
    
    @abstractmethod
    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generate trading signals.
        
        Args:
            df: DataFrame with OHLCV data and indicators
            
        Returns:
            DataFrame with 'signal' column added (1=BUY, -1=SELL, 0=HOLD)
        """
        pass
    
    @abstractmethod
    def calculate_position_size(
        self,
        df: pl.DataFrame,
        capital: float,
        current_price: float
    ) -> float:
        """Calculate position size for a trade.
        
        Args:
            df: DataFrame with market data
            capital: Available capital
            current_price: Current price of the asset
            
        Returns:
            Number of shares/units to trade
        """
        pass
    
    def add_position(self, position: Position):
        """Add a new position."""
        self.positions[position.ticker] = position
    
    def close_position(self, ticker: str) -> Optional[Position]:
        """Close a position."""
        return self.positions.pop(ticker, None)
    
    def get_position(self, ticker: str) -> Optional[Position]:
        """Get current position for a ticker."""
        return self.positions.get(ticker)
    
    def has_position(self, ticker: str) -> bool:
        """Check if there's an open position."""
        return ticker in self.positions
