"""Portfolio and holding classes for managing multiple positions.

This module defines the `Holding` and `Portfolio` dataclasses, which provide a
structured way to track individual assets and the overall portfolio performance.
"""

from dataclasses import dataclass, field
from datetime import datetime

import polars as pl


@dataclass
class Holding:
    """Represents a single holding within a portfolio.

    This dataclass stores all relevant information about a position in a single
    asset, including its quantity, price, and performance metrics.

    Attributes:
        ticker (str): The stock ticker symbol.
        quantity (float): The number of shares held.
        avg_price (float): The average purchase price of the shares.
        current_price (float): The current market price of the asset.
        market_value (float): The total current value of the holding.
        cost_basis (float): The total cost of acquiring the holding.
        unrealized_pnl (float): The unrealized profit or loss.
        unrealized_pnl_pct (float): The unrealized P&L as a percentage.
        weight (float): The weight of the holding in the portfolio.
    """

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
        """Calculates derived financial metrics after initialization."""
        self.cost_basis = self.quantity * self.avg_price
        self.market_value = self.quantity * self.current_price
        self.unrealized_pnl = self.market_value - self.cost_basis
        if self.cost_basis > 0:
            self.unrealized_pnl_pct = (self.unrealized_pnl / self.cost_basis) * 100


@dataclass
class Portfolio:
    """Manages a collection of holdings and tracks overall performance.

    This class provides methods to buy and sell assets, update prices, and
    calculate summary statistics for the entire portfolio.

    Attributes:
        name (str): The name of the portfolio.
        initial_capital (float): The starting capital.
        cash (float): The current cash balance.
        holdings (Dict[str, Holding]): A dictionary of the current holdings.
        transaction_history (List[Dict]): A log of all transactions.
    """

    name: str
    initial_capital: float
    cash: float = 0.0
    holdings: dict[str, Holding] = field(default_factory=dict)
    transaction_history: list[dict] = field(default_factory=list)

    def __post_init__(self):
        """Initializes cash to be equal to initial capital if not set."""
        if self.cash == 0:
            self.cash = self.initial_capital

    @property
    def total_value(self) -> float:
        """Calculates the total current value of the portfolio (holdings + cash)."""
        holdings_value = sum(h.market_value for h in self.holdings.values())
        return self.cash + holdings_value

    @property
    def invested_value(self) -> float:
        """Calculates the total value of all invested assets (cost basis)."""
        return sum(h.cost_basis for h in self.holdings.values())

    @property
    def total_pnl(self) -> float:
        """Calculates the total unrealized profit and loss for the portfolio."""
        return sum(h.unrealized_pnl for h in self.holdings.values())

    @property
    def total_return_pct(self) -> float:
        """Calculates the total return of the portfolio as a percentage."""
        if self.initial_capital > 0:
            return ((self.total_value - self.initial_capital) / self.initial_capital) * 100
        return 0.0

    def buy(self, ticker: str, quantity: float, price: float, commission: float = 0.0) -> None:
        """Executes a buy transaction and updates the portfolio.

        Args:
            ticker: The ticker symbol of the asset to buy.
            quantity: The number of shares to buy.
            price: The price per share.
            commission: The transaction commission.

        Raises:
            ValueError: If there are insufficient funds to complete the purchase.
        """
        cost = (quantity * price) + commission

        if cost > self.cash:
            msg = f"Insufficient funds. Need ${cost:.2f}, have ${self.cash:.2f}"
            raise ValueError(msg)

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
                current_price=price,
            )

        self.cash -= cost

        # Record transaction
        self.transaction_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "type": "BUY",
                "ticker": ticker,
                "quantity": quantity,
                "price": price,
                "commission": commission,
                "value": cost,
            }
        )

    def sell(self, ticker: str, quantity: float, price: float, commission: float = 0.0) -> None:
        """Executes a sell transaction and updates the portfolio.

        Args:
            ticker: The ticker symbol of the asset to sell.
            quantity: The number of shares to sell.
            price: The price per share.
            commission: The transaction commission.

        Raises:
            ValueError: If the asset is not in the portfolio or if there are
                insufficient shares to sell.
        """
        if ticker not in self.holdings:
            msg = f"No position in {ticker}"
            raise ValueError(msg)

        holding = self.holdings[ticker]
        if quantity > holding.quantity:
            msg = f"Insufficient shares. Have {holding.quantity}, trying to sell {quantity}"
            raise ValueError(msg)

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
        self.transaction_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "type": "SELL",
                "ticker": ticker,
                "quantity": quantity,
                "price": price,
                "commission": commission,
                "value": proceeds,
            }
        )

    def update_prices(self, prices: dict[str, float]) -> None:
        """Updates the current market price for all holdings in the portfolio.

        This method should be called periodically to keep the portfolio's market
        value and P&L metrics up to date.

        Args:
            prices: A dictionary mapping tickers to their current prices.
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
        """Returns the current portfolio holdings as a Polars DataFrame.

        Returns:
            A DataFrame with detailed information about each holding.
        """
        if not self.holdings:
            return pl.DataFrame()

        holdings_data = []
        for holding in self.holdings.values():
            holdings_data.append(
                {
                    "ticker": holding.ticker,
                    "quantity": holding.quantity,
                    "avg_price": holding.avg_price,
                    "current_price": holding.current_price,
                    "market_value": holding.market_value,
                    "cost_basis": holding.cost_basis,
                    "unrealized_pnl": holding.unrealized_pnl,
                    "unrealized_pnl_pct": holding.unrealized_pnl_pct,
                    "weight": holding.weight,
                }
            )

        return pl.DataFrame(holdings_data)

    def get_allocation(self) -> dict[str, float]:
        """Returns the current portfolio allocation as percentages.

        Returns:
            A dictionary mapping tickers to their weight in the portfolio.
        """
        return {ticker: holding.weight for ticker, holding in self.holdings.items()}

    def summary(self) -> dict:
        """Generates a summary of the portfolio's current state.

        Returns:
            A dictionary with key performance indicators for the portfolio.
        """
        return {
            "name": self.name,
            "total_value": self.total_value,
            "cash": self.cash,
            "invested_value": self.invested_value,
            "total_pnl": self.total_pnl,
            "total_return_pct": self.total_return_pct,
            "num_positions": len(self.holdings),
            "cash_weight": (self.cash / self.total_value * 100) if self.total_value > 0 else 0,
        }
