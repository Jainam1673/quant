"""Portfolio rebalancing logic."""

from typing import Dict, List, Tuple
from .portfolio import Portfolio


class Rebalancer:
    """Portfolio rebalancing strategies."""
    
    def __init__(self, portfolio: Portfolio):
        """Initialize rebalancer.
        
        Args:
            portfolio: Portfolio to rebalance
        """
        self.portfolio = portfolio
    
    def calculate_trades(
        self,
        target_weights: Dict[str, float],
        current_prices: Dict[str, float],
        min_trade_value: float = 100.0
    ) -> List[Tuple[str, str, float]]:
        """Calculate trades needed to reach target weights.
        
        Args:
            target_weights: Target allocation (ticker -> weight %)
            current_prices: Current prices (ticker -> price)
            min_trade_value: Minimum trade value to execute
            
        Returns:
            List of (ticker, action, quantity) tuples
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
        for ticker in current_allocation.keys():
            if ticker not in target_weights:
                holding = self.portfolio.holdings[ticker]
                trades.append((ticker, "SELL", holding.quantity))
        
        return trades
    
    def execute_rebalance(
        self,
        target_weights: Dict[str, float],
        current_prices: Dict[str, float],
        commission: float = 0.0,
        min_trade_value: float = 100.0
    ) -> List[Dict]:
        """Execute rebalancing trades.
        
        Args:
            target_weights: Target allocation
            current_prices: Current prices
            commission: Commission per trade
            min_trade_value: Minimum trade value
            
        Returns:
            List of executed trades
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
                
                executed.append({
                    "ticker": ticker,
                    "action": action,
                    "quantity": quantity,
                    "price": price,
                    "value": quantity * price
                })
            except ValueError as e:
                print(f"Error executing {action} {quantity} {ticker}: {e}")
                continue
        
        return executed
    
    def periodic_rebalance(
        self,
        target_weights: Dict[str, float],
        current_prices: Dict[str, float],
        threshold_pct: float = 5.0
    ) -> bool:
        """Check if rebalancing is needed based on drift threshold.
        
        Args:
            target_weights: Target allocation
            current_prices: Current prices
            threshold_pct: Rebalance if any position drifts more than this %
            
        Returns:
            True if rebalancing is needed
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
        target_weights: Dict[str, float],
        current_prices: Dict[str, float],
        threshold_pct: float = 5.0,
        commission: float = 0.0
    ) -> List[Dict]:
        """Rebalance only if threshold is exceeded.
        
        Args:
            target_weights: Target allocation
            current_prices: Current prices
            threshold_pct: Drift threshold
            commission: Commission per trade
            
        Returns:
            List of executed trades (empty if no rebalancing needed)
        """
        if self.periodic_rebalance(target_weights, current_prices, threshold_pct):
            return self.execute_rebalance(target_weights, current_prices, commission)
        return []
