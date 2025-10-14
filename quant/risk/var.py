"""Value at Risk (VaR) and Conditional VaR (CVaR) calculations."""

import numpy as np
from scipy import stats
from typing import Literal


class VaRCalculator:
    """Calculate Value at Risk and Conditional Value at Risk."""
    
    @staticmethod
    def historical_var(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000
    ) -> float:
        """Calculate VaR using historical simulation.
        
        Args:
            returns: Historical returns
            confidence_level: Confidence level (e.g., 0.95 for 95%)
            portfolio_value: Current portfolio value
            
        Returns:
            VaR in dollar terms
        """
        percentile = (1 - confidence_level) * 100
        var_return = np.percentile(returns, percentile)
        return abs(var_return * portfolio_value)
    
    @staticmethod
    def parametric_var(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000
    ) -> float:
        """Calculate VaR using parametric method (assumes normal distribution).
        
        Args:
            returns: Historical returns
            confidence_level: Confidence level
            portfolio_value: Current portfolio value
            
        Returns:
            VaR in dollar terms
        """
        mean = np.mean(returns)
        std = np.std(returns)
        z_score = stats.norm.ppf(1 - confidence_level)
        var_return = mean + (z_score * std)
        return abs(var_return * portfolio_value)
    
    @staticmethod
    def monte_carlo_var(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000,
        n_simulations: int = 10000
    ) -> float:
        """Calculate VaR using Monte Carlo simulation.
        
        Args:
            returns: Historical returns
            confidence_level: Confidence level
            portfolio_value: Current portfolio value
            n_simulations: Number of simulations
            
        Returns:
            VaR in dollar terms
        """
        mean = np.mean(returns)
        std = np.std(returns)
        
        # Simulate returns
        simulated_returns = np.random.normal(mean, std, n_simulations)
        
        percentile = (1 - confidence_level) * 100
        var_return = np.percentile(simulated_returns, percentile)
        return abs(var_return * portfolio_value)
    
    @staticmethod
    def historical_cvar(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000
    ) -> float:
        """Calculate CVaR (Expected Shortfall) using historical method.
        
        Args:
            returns: Historical returns
            confidence_level: Confidence level
            portfolio_value: Current portfolio value
            
        Returns:
            CVaR in dollar terms
        """
        percentile = (1 - confidence_level) * 100
        var_threshold = np.percentile(returns, percentile)
        
        # CVaR is the average of returns below VaR threshold
        tail_returns = returns[returns <= var_threshold]
        if len(tail_returns) == 0:
            return 0.0
        
        cvar_return = np.mean(tail_returns)
        return abs(cvar_return * portfolio_value)
    
    @staticmethod
    def parametric_cvar(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000
    ) -> float:
        """Calculate CVaR using parametric method.
        
        Args:
            returns: Historical returns
            confidence_level: Confidence level
            portfolio_value: Current portfolio value
            
        Returns:
            CVaR in dollar terms
        """
        mean = np.mean(returns)
        std = np.std(returns)
        z_score = stats.norm.ppf(1 - confidence_level)
        
        # Expected shortfall for normal distribution
        cvar_return = mean - (std * stats.norm.pdf(z_score) / (1 - confidence_level))
        return abs(cvar_return * portfolio_value)
    
    @staticmethod
    def calculate_all_var(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000,
        n_simulations: int = 10000
    ) -> dict:
        """Calculate VaR using all methods.
        
        Args:
            returns: Historical returns
            confidence_level: Confidence level
            portfolio_value: Current portfolio value
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            Dictionary with VaR from all methods
        """
        return {
            "historical_var": VaRCalculator.historical_var(returns, confidence_level, portfolio_value),
            "parametric_var": VaRCalculator.parametric_var(returns, confidence_level, portfolio_value),
            "monte_carlo_var": VaRCalculator.monte_carlo_var(returns, confidence_level, portfolio_value, n_simulations),
            "historical_cvar": VaRCalculator.historical_cvar(returns, confidence_level, portfolio_value),
            "parametric_cvar": VaRCalculator.parametric_cvar(returns, confidence_level, portfolio_value),
            "confidence_level": confidence_level,
            "portfolio_value": portfolio_value
        }
    
    @staticmethod
    def var_time_horizon(
        var_1day: float,
        days: int,
        method: Literal["sqrt", "linear"] = "sqrt"
    ) -> float:
        """Scale VaR to different time horizons.
        
        Args:
            var_1day: 1-day VaR
            days: Number of days
            method: Scaling method ('sqrt' or 'linear')
            
        Returns:
            Scaled VaR
        """
        if method == "sqrt":
            return var_1day * np.sqrt(days)
        else:  # linear
            return var_1day * days
    
    @staticmethod
    def marginal_var(
        returns_df: np.ndarray,
        weights: np.ndarray,
        confidence_level: float = 0.95
    ) -> np.ndarray:
        """Calculate marginal VaR for each asset in portfolio.
        
        Args:
            returns_df: Array of returns for multiple assets (n_samples x n_assets)
            weights: Portfolio weights
            confidence_level: Confidence level
            
        Returns:
            Array of marginal VaR for each asset
        """
        # Portfolio returns
        portfolio_returns = np.dot(returns_df, weights)
        
        # Portfolio VaR
        percentile = (1 - confidence_level) * 100
        portfolio_var = np.percentile(portfolio_returns, percentile)
        
        # Marginal VaR for each asset
        marginal_vars = np.zeros(len(weights))
        epsilon = 0.01  # Small weight change
        
        for i in range(len(weights)):
            # Increase weight slightly
            new_weights = weights.copy()
            new_weights[i] += epsilon
            new_weights = new_weights / np.sum(new_weights)  # Renormalize
            
            new_portfolio_returns = np.dot(returns_df, new_weights)
            new_var = np.percentile(new_portfolio_returns, percentile)
            
            # Marginal VaR is the change in VaR per unit change in weight
            marginal_vars[i] = (new_var - portfolio_var) / epsilon
        
        return marginal_vars
