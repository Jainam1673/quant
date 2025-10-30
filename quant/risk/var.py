"""Value at Risk (VaR) and Conditional VaR (CVaR) calculations.

This module provides a `VaRCalculator` class with static methods to estimate
potential investment losses over a specific time horizon at a given confidence
level. It includes historical, parametric, and Monte Carlo methods.
"""

from typing import Literal, Dict

import numpy as np
from scipy import stats


class VaRCalculator:
    """Provides methods for calculating Value at Risk (VaR) and Conditional VaR (CVaR)."""

    @staticmethod
    def historical_var(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000,
    ) -> float:
        """Calculates VaR using the historical simulation method.

        This method is non-parametric and relies on the actual historical
        distribution of returns.

        Args:
            returns: A NumPy array of historical returns.
            confidence_level: The confidence level for the VaR calculation.
            portfolio_value: The total value of the portfolio.

        Returns:
            The estimated Value at Risk in dollar terms.
        """
        percentile = (1 - confidence_level) * 100
        var_return = float(np.percentile(returns, percentile))
        return abs(var_return * portfolio_value)

    @staticmethod
    def parametric_var(
        returns: np.ndarray,
        confidence_level: float = 0.95,
        portfolio_value: float = 1000000,
    ) -> float:
        """Calculates VaR using the parametric (variance-covariance) method.

        This method assumes that returns are normally distributed.

        Args:
            returns: A NumPy array of historical returns.
            confidence_level: The confidence level for the VaR calculation.
            portfolio_value: The total value of the portfolio.

        Returns:
            The estimated Value at Risk in dollar terms.
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
        n_simulations: int = 10000,
    ) -> float:
        """Calculates VaR using Monte Carlo simulation.

        This method generates a large number of random return scenarios to
        estimate the potential loss.

        Args:
            returns: A NumPy array of historical returns.
            confidence_level: The confidence level for the VaR calculation.
            portfolio_value: The total value of the portfolio.
            n_simulations: The number of simulations to run.

        Returns:
            The estimated Value at Risk in dollar terms.
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
        portfolio_value: float = 1000000,
    ) -> float:
        """Calculates Conditional VaR (CVaR) using the historical method.

        CVaR, also known as Expected Shortfall, measures the expected loss given
        that the loss is greater than the VaR.

        Args:
            returns: A NumPy array of historical returns.
            confidence_level: The confidence level for the calculation.
            portfolio_value: The total value of the portfolio.

        Returns:
            The estimated Conditional VaR in dollar terms.
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
        portfolio_value: float = 1000000,
    ) -> float:
        """Calculates CVaR using the parametric method.

        Args:
            returns: A NumPy array of historical returns.
            confidence_level: The confidence level for the calculation.
            portfolio_value: The total value of the portfolio.

        Returns:
            The estimated Conditional VaR in dollar terms.
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
        n_simulations: int = 10000,
    ) -> Dict[str, float]:
        """Calculates VaR and CVaR using all available methods.

        Args:
            returns: A NumPy array of historical returns.
            confidence_level: The confidence level.
            portfolio_value: The total value of the portfolio.
            n_simulations: The number of Monte Carlo simulations.

        Returns:
            A dictionary containing the VaR and CVaR values from all methods.
        """
        return {
            "historical_var": VaRCalculator.historical_var(
                returns, confidence_level, portfolio_value
            ),
            "parametric_var": VaRCalculator.parametric_var(
                returns, confidence_level, portfolio_value
            ),
            "monte_carlo_var": VaRCalculator.monte_carlo_var(
                returns, confidence_level, portfolio_value, n_simulations
            ),
            "historical_cvar": VaRCalculator.historical_cvar(
                returns, confidence_level, portfolio_value
            ),
            "parametric_cvar": VaRCalculator.parametric_cvar(
                returns, confidence_level, portfolio_value
            ),
            "confidence_level": confidence_level,
            "portfolio_value": portfolio_value,
        }

    @staticmethod
    def var_time_horizon(
        var_1day: float,
        days: int,
        method: Literal["sqrt", "linear"] = "sqrt",
    ) -> float:
        """Scales a 1-day VaR to a different time horizon.

        Args:
            var_1day: The 1-day Value at Risk.
            days: The number of days in the new time horizon.
            method: The scaling method ('sqrt' for square root of time, or 'linear').

        Returns:
            The scaled VaR for the specified time horizon.
        """
        if method == "sqrt":
            return var_1day * np.sqrt(days)
        # linear
        return var_1day * days

    @staticmethod
    def marginal_var(
        returns_df: np.ndarray,
        weights: np.ndarray,
        confidence_level: float = 0.95,
    ) -> np.ndarray:
        """Calculates the marginal VaR for each asset in a portfolio.

        Marginal VaR measures the change in portfolio VaR that results from
        adding or removing a small amount of a particular asset.

        Args:
            returns_df: An array of returns for multiple assets (n_samples x n_assets).
            weights: The portfolio weights.
            confidence_level: The confidence level.

        Returns:
            A NumPy array of the marginal VaR for each asset.
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
