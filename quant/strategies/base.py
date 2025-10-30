"""Base classes and enumerations for creating trading strategies.

This module provides the foundational components for building strategies, including
the `Signal` enum for trade actions, the `Position` dataclass for tracking open
trades, and the `Strategy` abstract base class that all strategies must inherit from.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import polars as pl


class Signal(Enum):
    """Enumeration for trading signals."""

    BUY = 1
    SELL = -1
    HOLD = 0


@dataclass
class Position:
    """Represents an open trading position.

    Attributes:
        ticker (str): The ticker symbol of the asset.
        quantity (float): The number of shares or units held.
        entry_price (float): The average price at which the position was entered.
        entry_date (str): The date the position was opened.
        side (str): The side of the trade ('long' or 'short').
    """

    ticker: str
    quantity: float
    entry_price: float
    entry_date: str
    side: str  # 'long' or 'short'

    def pnl(self, current_price: float) -> float:
        """Calculates the unrealized profit or loss for the position."""
        if self.side == "long":
            return (current_price - self.entry_price) * self.quantity
        return (self.entry_price - current_price) * self.quantity

    def pnl_percent(self, current_price: float) -> float:
        """Calculates the unrealized P&L as a percentage."""
        if self.side == "long":
            return ((current_price - self.entry_price) / self.entry_price) * 100
        return ((self.entry_price - current_price) / self.entry_price) * 100


class Strategy(ABC):
    """Abstract base class for all trading strategies.

    This class defines the essential methods that every strategy must implement.
    It provides a consistent interface for the backtesting engine.

    Attributes:
        name (str): The name of the strategy.
        positions (dict): A dictionary to track open positions.
    """

    def __init__(self, name: str):
        """Initializes the strategy with a name."""
        self.name = name
        self.positions: dict[str, Position] = {}

    @abstractmethod
    def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame:
        """Generates trading signals based on the strategy's logic.

        This method must be implemented by all subclasses. It should take a
        DataFrame of market data and return it with a 'signal' column added.

        Args:
            df: A Polars DataFrame with OHLCV data and any required indicators.

        Returns:
            A Polars DataFrame with a 'signal' column (1 for BUY, -1 for SELL, 0 for HOLD).
        """

    @abstractmethod
    def calculate_position_size(
        self,
        df: pl.DataFrame,
        capital: float,
        current_price: float,
    ) -> float:
        """Calculates the size of a position for a new trade.

        This method must be implemented by all subclasses.

        Args:
            df: The DataFrame of market data.
            capital: The available capital for trading.
            current_price: The current price of the asset.

        Returns:
            The number of shares or units to trade.
        """

    def add_position(self, position: Position) -> None:
        """Adds a new open position to the strategy's tracking."""
        self.positions[position.ticker] = position

    def close_position(self, ticker: str) -> Position | None:
        """Closes an open position and returns it."""
        return self.positions.pop(ticker, None)

    def get_position(self, ticker: str) -> Position | None:
        """Retrieves the current position for a given ticker."""
        return self.positions.get(ticker)

    def has_position(self, ticker: str) -> bool:
        """Checks if there is an open position for a given ticker."""
        return ticker in self.positions
