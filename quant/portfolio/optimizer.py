"""Portfolio optimization using modern portfolio theory."""

import numpy as np
import polars as pl
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional


class PortfolioOptimizer:
    """Portfolio optimizer using mean-variance optimization."""
    
    def __init__(self, returns_df: pl.DataFrame):
        """Initialize optimizer with historical returns.
        
        Args:
            returns_df: DataFrame with columns as tickers and returns as values
        """
        self.returns_df = returns_df
        self.tickers = [col for col in returns_df.columns if col != "timestamp"]
        self.n_assets = len(self.tickers)
        
        # Calculate mean returns and covariance matrix
        self.mean_returns = self._calculate_mean_returns()
        self.cov_matrix = self._calculate_covariance()
    
    def _calculate_mean_returns(self) -> np.ndarray:
        """Calculate annualized mean returns."""
        returns_data = self.returns_df.select(self.tickers).to_numpy()
        mean_returns = np.mean(returns_data, axis=0)
        return mean_returns * 252  # Annualize (assuming daily returns)
    
    def _calculate_covariance(self) -> np.ndarray:
        """Calculate annualized covariance matrix."""
        returns_data = self.returns_df.select(self.tickers).to_numpy()
        cov = np.cov(returns_data.T)
        return cov * 252  # Annualize
    
    def portfolio_stats(self, weights: np.ndarray) -> Tuple[float, float, float]:
        """Calculate portfolio statistics.
        
        Args:
            weights: Asset weights
            
        Returns:
            Tuple of (return, volatility, sharpe_ratio)
        """
        portfolio_return = np.sum(self.mean_returns * weights)
        portfolio_variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Sharpe ratio (assuming risk-free rate of 0)
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def minimize_volatility(self, target_return: Optional[float] = None) -> Dict:
        """Find minimum volatility portfolio.
        
        Args:
            target_return: Optional target return constraint
            
        Returns:
            Dictionary with optimal weights and statistics
        """
        # Initial guess: equal weights
        initial_weights = np.ones(self.n_assets) / self.n_assets
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]
        
        if target_return is not None:
            constraints.append({
                'type': 'eq',
                'fun': lambda x: np.sum(self.mean_returns * x) - target_return
            })
        
        # Bounds: weights between 0 and 1
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        # Optimize
        result = minimize(
            lambda w: np.sqrt(np.dot(w.T, np.dot(self.cov_matrix, w))),
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.portfolio_stats(optimal_weights)
            
            return {
                "weights": {ticker: weight for ticker, weight in zip(self.tickers, optimal_weights)},
                "return": ret,
                "volatility": vol,
                "sharpe_ratio": sharpe,
                "success": True
            }
        else:
            return {"success": False, "message": result.message}
    
    def maximize_sharpe(self) -> Dict:
        """Find maximum Sharpe ratio portfolio.
        
        Returns:
            Dictionary with optimal weights and statistics
        """
        # Initial guess
        initial_weights = np.ones(self.n_assets) / self.n_assets
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]
        
        # Bounds
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        # Optimize (minimize negative Sharpe ratio)
        def negative_sharpe(weights):
            ret, vol, sharpe = self.portfolio_stats(weights)
            return -sharpe
        
        result = minimize(
            negative_sharpe,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.portfolio_stats(optimal_weights)
            
            return {
                "weights": {ticker: weight for ticker, weight in zip(self.tickers, optimal_weights)},
                "return": ret,
                "volatility": vol,
                "sharpe_ratio": sharpe,
                "success": True
            }
        else:
            return {"success": False, "message": result.message}
    
    def efficient_frontier(self, n_points: int = 100) -> pl.DataFrame:
        """Calculate the efficient frontier.
        
        Args:
            n_points: Number of points on the frontier
            
        Returns:
            DataFrame with returns, volatilities, and Sharpe ratios
        """
        min_ret = np.min(self.mean_returns)
        max_ret = np.max(self.mean_returns)
        target_returns = np.linspace(min_ret, max_ret, n_points)
        
        frontier_data = []
        
        for target_ret in target_returns:
            result = self.minimize_volatility(target_return=target_ret)
            if result.get("success"):
                frontier_data.append({
                    "return": result["return"],
                    "volatility": result["volatility"],
                    "sharpe_ratio": result["sharpe_ratio"]
                })
        
        return pl.DataFrame(frontier_data)
    
    def equal_weight(self) -> Dict:
        """Calculate equal-weight portfolio statistics.
        
        Returns:
            Dictionary with equal weights and statistics
        """
        weights = np.ones(self.n_assets) / self.n_assets
        ret, vol, sharpe = self.portfolio_stats(weights)
        
        return {
            "weights": {ticker: weight for ticker, weight in zip(self.tickers, weights)},
            "return": ret,
            "volatility": vol,
            "sharpe_ratio": sharpe
        }
    
    def risk_parity(self) -> Dict:
        """Calculate risk parity portfolio (equal risk contribution).
        
        Returns:
            Dictionary with risk parity weights and statistics
        """
        # Initial guess
        initial_weights = np.ones(self.n_assets) / self.n_assets
        
        def risk_contributions(weights):
            """Calculate risk contributions of each asset."""
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            marginal_contrib = np.dot(self.cov_matrix, weights)
            contrib = weights * marginal_contrib / portfolio_vol
            return contrib
        
        def risk_parity_objective(weights):
            """Minimize variance of risk contributions."""
            contrib = risk_contributions(weights)
            target_contrib = np.ones(self.n_assets) / self.n_assets
            return np.sum((contrib - target_contrib) ** 2)
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]
        
        # Bounds
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        result = minimize(
            risk_parity_objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.portfolio_stats(optimal_weights)
            
            return {
                "weights": {ticker: weight for ticker, weight in zip(self.tickers, optimal_weights)},
                "return": ret,
                "volatility": vol,
                "sharpe_ratio": sharpe,
                "success": True
            }
        else:
            return {"success": False, "message": result.message}
