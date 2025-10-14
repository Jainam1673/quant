"""Portfolio class for managing multiple positions."""

import polars as pl
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class Holding:
    """Represents a holding in the portfolio."""
    ticker: str
    quantity: float
    avg_price: float
    current_price: float
    market_value: float = 0.0
    cost_basis: float = 0.0
    unrealized_pnl: float = 0.0
    unrealized_pnl_pct: float = 0.0
    weight: float = 0.0
    
    def __post_init__(self):
        """Calculate derived values."""
        self.cost_basis = self.quantity * self.avg_price
        self.market_value = self.quantity * self.current_price
        self.unrealized_pnl = self.market_value - self.cost_basis
        if self.cost_basis > 0:
            self.unrealized_pnl_pct = (self.unrealized_pnl / self.cost_basis) * 100


@dataclass
class Portfolio:
    """Portfolio manager for tracking multiple positions."""
    
    name: str
    initial_capital: float
    cash: float = 0.0
    holdings: Dict[str, Holding] = field(default_factory=dict)
    transaction_history: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize cash if not set."""
        if self.cash == 0:
            self.cash = self.initial_capital
    
    @property
    def total_value(self) -> float:
        """Calculate total portfolio value."""
        holdings_value = sum(h.market_value for h in self.holdings.values())
        return self.cash + holdings_value
    
    @property
    def invested_value(self) -> float:
        """Calculate total invested value."""
        return sum(h.cost_basis for h in self.holdings.values())
    
    @property
    def total_pnl(self) -> float:
        """Calculate total unrealized P&L."""
        return sum(h.unrealized_pnl for h in self.holdings.values())
    
    @property
    def total_return_pct(self) -> float:
        """Calculate total return percentage."""
        if self.initial_capital > 0:
            return ((self.total_value - self.initial_capital) / self.initial_capital) * 100
        return 0.0
    
    def buy(self, ticker: str, quantity: float, price: float, commission: float = 0.0):
        """Buy shares of a ticker.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to buy
            price: Price per share
            commission: Transaction commission
        """
        cost = (quantity * price) + commission
        
        if cost > self.cash:
            raise ValueError(f"Insufficient funds. Need ${cost:.2f}, have ${self.cash:.2f}")
        
        # Update or create holding
        if ticker in self.holdings:
            holding = self.holdings[ticker]
            total_cost = holding.cost_basis + cost
            total_quantity = holding.quantity + quantity
            holding.quantity = total_quantity
            holding.avg_price = total_cost / total_quantity
            holding.cost_basis = total_cost
        else:
            self.holdings[ticker] = Holding(
                ticker=ticker,
                quantity=quantity,
                avg_price=price,
                current_price=price
            )
        
        self.cash -= cost
        
        # Record transaction
        self.transaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "BUY",
            "ticker": ticker,
            "quantity": quantity,
            "price": price,
            "commission": commission,
            "value": cost
        })
    
    def sell(self, ticker: str, quantity: float, price: float, commission: float = 0.0):
        """Sell shares of a ticker.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to sell
            price: Price per share
            commission: Transaction commission
        """
        if ticker not in self.holdings:
            raise ValueError(f"No position in {ticker}")
        
        holding = self.holdings[ticker]
        if quantity > holding.quantity:
            raise ValueError(f"Insufficient shares. Have {holding.quantity}, trying to sell {quantity}")
        
        proceeds = (quantity * price) - commission
        
        # Update holding
        if quantity == holding.quantity:
            # Closing entire position
            del self.holdings[ticker]
        else:
            holding.quantity -= quantity
            holding.cost_basis = holding.quantity * holding.avg_price
        
        self.cash += proceeds
        
        # Record transaction
        self.transaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "SELL",
            "ticker": ticker,
            "quantity": quantity,
            "price": price,
            "commission": commission,
            "value": proceeds
        })
    
    def update_prices(self, prices: Dict[str, float]):
        """Update current prices for all holdings.
        
        Args:
            prices: Dictionary mapping ticker to current price
        """
        total_value = self.cash
        
        for ticker, holding in self.holdings.items():
            if ticker in prices:
                holding.current_price = prices[ticker]
                holding.market_value = holding.quantity * holding.current_price
                holding.unrealized_pnl = holding.market_value - holding.cost_basis
                if holding.cost_basis > 0:
                    holding.unrealized_pnl_pct = (holding.unrealized_pnl / holding.cost_basis) * 100
            total_value += holding.market_value
        
        # Update weights
        if total_value > 0:
            for holding in self.holdings.values():
                holding.weight = (holding.market_value / total_value) * 100
    
    def get_holdings_df(self) -> pl.DataFrame:
        """Get holdings as a DataFrame.
        
        Returns:
            Polars DataFrame with holding information
        """
        if not self.holdings:
            return pl.DataFrame()
        
        holdings_data = []
        for holding in self.holdings.values():
            holdings_data.append({
                "ticker": holding.ticker,
                "quantity": holding.quantity,
                "avg_price": holding.avg_price,
                "current_price": holding.current_price,
                "market_value": holding.market_value,
                "cost_basis": holding.cost_basis,
                "unrealized_pnl": holding.unrealized_pnl,
                "unrealized_pnl_pct": holding.unrealized_pnl_pct,
                "weight": holding.weight
            })
        
        return pl.DataFrame(holdings_data)
    
    def get_allocation(self) -> Dict[str, float]:
        """Get portfolio allocation as percentages.
        
        Returns:
            Dictionary mapping ticker to weight percentage
        """
        return {ticker: holding.weight for ticker, holding in self.holdings.items()}
    
    def summary(self) -> Dict:
        """Get portfolio summary statistics.
        
        Returns:
            Dictionary with portfolio summary
        """
        return {
            "name": self.name,
            "total_value": self.total_value,
            "cash": self.cash,
            "invested_value": self.invested_value,
            "total_pnl": self.total_pnl,
            "total_return_pct": self.total_return_pct,
            "num_positions": len(self.holdings),
            "cash_weight": (self.cash / self.total_value * 100) if self.total_value > 0 else 0
        }
