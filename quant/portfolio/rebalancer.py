"""Portfolio rebalancing logic to align with target allocations.

This module provides the `Rebalancer` class, which contains strategies for
adjusting a portfolio to match a desired set of target weights. This is crucial
for maintaining a portfolio's strategic asset allocation over time.
"""

from quant.utils.logger import get_logger

from .portfolio import Portfolio

logger = get_logger(__name__)


class Rebalancer:
    """Implements portfolio rebalancing strategies.

    This class calculates the necessary trades to align the current portfolio
    with a target allocation and can execute those trades.

    Args:
        portfolio (Portfolio): The portfolio instance to be rebalanced.
    """

    def __init__(self, portfolio: Portfolio):
        """Initializes the Rebalancer with a portfolio."""
        self.portfolio = portfolio

    def calculate_trades(
        self,
        target_weights: dict[str, float],
        current_prices: dict[str, float],
        min_trade_value: float = 100.0,
    ) -> list[tuple[str, str, float]]:
        """Calculates the trades required to meet target weights.

        This method compares the current portfolio allocation to the target
        allocation and generates a list of buy/sell orders to bridge the gap.

        Args:
            target_weights: A dictionary mapping tickers to their target weights (e.g., {"AAPL": 50.0, "GOOG": 50.0}).
            current_prices: A dictionary of current market prices for the assets.
            min_trade_value: The minimum value of a trade to be executed, to avoid tiny, inefficient trades.

        Returns:
            A list of tuples, where each tuple represents a trade order in the
            format (ticker, action, quantity).
        """
        # Update portfolio with current prices
        self.portfolio.update_prices(current_prices)

        total_value = self.portfolio.total_value
        current_allocation = self.portfolio.get_allocation()

        trades = []

        # Calculate required changes
        for ticker, target_weight in target_weights.items():
            current_weight = current_allocation.get(ticker, 0.0)
            weight_diff = target_weight - current_weight

            # Calculate value difference
            value_diff = (weight_diff / 100.0) * total_value

            # Skip if below minimum trade value
            if abs(value_diff) < min_trade_value:
                continue

            # Calculate quantity to trade
            price = current_prices.get(ticker)
            if price is None:
                continue

            quantity = abs(value_diff) / price

            if value_diff > 0:
                # Need to buy
                trades.append((ticker, "BUY", quantity))
            else:
                # Need to sell
                trades.append((ticker, "SELL", quantity))

        # Check for positions to exit (not in target)
        for ticker in current_allocation:
            if ticker not in target_weights:
                holding = self.portfolio.holdings[ticker]
                trades.append((ticker, "SELL", holding.quantity))

        return trades

    def execute_rebalance(
        self,
        target_weights: dict[str, float],
        current_prices: dict[str, float],
        commission: float = 0.0,
        min_trade_value: float = 100.0,
    ) -> list[dict]:
        """Executes the rebalancing trades on the portfolio.

        This method first calculates the required trades and then executes them
        by calling the portfolio's buy/sell methods.

        Args:
            target_weights: The target allocation.
            current_prices: The current market prices.
            commission: The commission cost per trade.
            min_trade_value: The minimum trade value to execute.

        Returns:
            A list of dictionaries, each representing an executed trade.
        """
        trades = self.calculate_trades(target_weights, current_prices, min_trade_value)
        executed = []

        for ticker, action, quantity in trades:
            price = current_prices[ticker]

            try:
                if action == "BUY":
                    self.portfolio.buy(ticker, quantity, price, commission)
                else:  # SELL
                    self.portfolio.sell(ticker, quantity, price, commission)

                executed.append(
                    {
                        "ticker": ticker,
                        "action": action,
                        "quantity": quantity,
                        "price": price,
                        "value": quantity * price,
                    }
                )
            except ValueError as e:
                logger.exception(f"Error executing {action} {quantity} {ticker}: {e}")
                continue

        return executed

    def periodic_rebalance(
        self,
        target_weights: dict[str, float],
        current_prices: dict[str, float],
        threshold_pct: float = 5.0,
    ) -> bool:
        """Checks if a rebalance is needed based on a drift threshold.

        This method is useful for periodic rebalancing strategies, where trades
        are only made if the portfolio has drifted significantly from its target.

        Args:
            target_weights: The target allocation.
            current_prices: The current market prices.
            threshold_pct: The maximum allowed drift (in percent) for any single
                position before a rebalance is triggered.

        Returns:
            True if the portfolio's drift exceeds the threshold, False otherwise.
        """
        self.portfolio.update_prices(current_prices)
        current_allocation = self.portfolio.get_allocation()

        for ticker, target_weight in target_weights.items():
            current_weight = current_allocation.get(ticker, 0.0)
            drift = abs(target_weight - current_weight)

            if drift > threshold_pct:
                return True

        return False

    def threshold_rebalance(
        self,
        target_weights: dict[str, float],
        current_prices: dict[str, float],
        threshold_pct: float = 5.0,
        commission: float = 0.0,
    ) -> list[dict]:
        """Executes a rebalance only if the drift threshold is exceeded.

        Args:
            target_weights: The target allocation.
            current_prices: The current market prices.
            threshold_pct: The drift threshold.
            commission: The commission per trade.

        Returns:
            A list of executed trades, or an empty list if no rebalance was needed.
        """
        if self.periodic_rebalance(target_weights, current_prices, threshold_pct):
            return self.execute_rebalance(target_weights, current_prices, commission)
        return []
