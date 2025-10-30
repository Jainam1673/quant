"""Portfolio optimization using Modern Portfolio Theory (MPT).

This module provides the `PortfolioOptimizer` class, which uses mean-variance
optimization to find optimal portfolio allocations based on historical returns.
It can be used to construct portfolios that maximize the Sharpe ratio, minimize
volatility, or achieve a specific target return.
"""

import numpy as np
import polars as pl
from scipy.optimize import minimize


class PortfolioOptimizer:
    """Implements mean-variance portfolio optimization.

    This optimizer calculates the efficient frontier and finds optimal portfolios
    based on different risk/return objectives.

    Args:
        returns_df (pl.DataFrame): A DataFrame where each column represents the
            returns of a single asset.
    """

    def __init__(self, returns_df: pl.DataFrame):
        """Initializes the optimizer with historical returns."""
        self.returns_df = returns_df
        self.tickers = [col for col in returns_df.columns if col != "timestamp"]
        self.n_assets = len(self.tickers)

        # Calculate mean returns and covariance matrix
        self.mean_returns = self._calculate_mean_returns()
        self.cov_matrix = self._calculate_covariance()

    def _calculate_mean_returns(self) -> np.ndarray:
        """Calculates the annualized mean returns for each asset."""
        returns_data = self.returns_df.select(self.tickers).to_numpy()
        mean_returns = np.mean(returns_data, axis=0)
        return mean_returns * 252  # Annualize (assuming daily returns)

    def _calculate_covariance(self) -> np.ndarray:
        """Calculates the annualized covariance matrix of asset returns."""
        returns_data = self.returns_df.select(self.tickers).to_numpy()
        cov = np.cov(returns_data.T)
        return cov * 252  # Annualize

    def portfolio_stats(self, weights: np.ndarray) -> tuple[float, float, float]:
        """Calculates the expected return, volatility, and Sharpe ratio for a given portfolio.

        Args:
            weights: An array of asset weights.

        Returns:
            A tuple containing the portfolio's expected return, volatility, and Sharpe ratio.
        """
        portfolio_return = np.sum(self.mean_returns * weights)
        portfolio_variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)

        # Sharpe ratio (assuming risk-free rate of 0)
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0

        return portfolio_return, portfolio_volatility, sharpe_ratio

    def minimize_volatility(self, target_return: float | None = None) -> dict:
        """Finds the portfolio with the minimum volatility.

        If a target return is provided, it finds the minimum volatility portfolio
        that achieves at least that level of return.

        Args:
            target_return: The desired level of return.

        Returns:
            A dictionary containing the optimal weights and portfolio statistics.
        """
        # Initial guess: equal weights
        initial_weights = np.ones(self.n_assets) / self.n_assets

        # Constraints
        constraints = [
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},  # Weights sum to 1
        ]

        if target_return is not None:
            constraints.append(
                {
                    "type": "eq",
                    "fun": lambda x: np.sum(self.mean_returns * x) - target_return,
                }
            )

        # Bounds: weights between 0 and 1
        bounds = tuple((0, 1) for _ in range(self.n_assets))

        # Optimize
        result = minimize(
            lambda w: np.sqrt(np.dot(w.T, np.dot(self.cov_matrix, w))),
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.portfolio_stats(optimal_weights)

            return {
                "weights": dict(zip(self.tickers, optimal_weights, strict=False)),
                "return": ret,
                "volatility": vol,
                "sharpe_ratio": sharpe,
                "success": True,
            }
        return {"success": False, "message": result.message}

    def maximize_sharpe(self) -> dict:
        """Finds the portfolio that maximizes the Sharpe ratio.

        This is often considered the "optimal" portfolio as it provides the best
        return for a given level of risk.

        Returns:
            A dictionary containing the optimal weights and portfolio statistics.
        """
        # Initial guess
        initial_weights = np.ones(self.n_assets) / self.n_assets

        # Constraints
        constraints = [
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},
        ]

        # Bounds
        bounds = tuple((0, 1) for _ in range(self.n_assets))

        # Optimize (minimize negative Sharpe ratio)
        def negative_sharpe(weights):
            _ret, _vol, sharpe = self.portfolio_stats(weights)
            return -sharpe

        result = minimize(
            negative_sharpe,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.portfolio_stats(optimal_weights)

            return {
                "weights": dict(zip(self.tickers, optimal_weights, strict=False)),
                "return": ret,
                "volatility": vol,
                "sharpe_ratio": sharpe,
                "success": True,
            }
        return {"success": False, "message": result.message}

    def efficient_frontier(self, n_points: int = 100) -> pl.DataFrame:
        """Calculates the efficient frontier.

        The efficient frontier is the set of optimal portfolios that offer the
        highest expected return for a defined level of risk or the lowest risk
        for a given level of expected return.

        Args:
            n_points: The number of points to calculate on the frontier.

        Returns:
            A DataFrame with the returns, volatilities, and Sharpe ratios for
            each portfolio on the frontier.
        """
        min_ret = np.min(self.mean_returns)
        max_ret = np.max(self.mean_returns)
        target_returns = np.linspace(min_ret, max_ret, n_points)

        frontier_data = []

        for target_ret in target_returns:
            result = self.minimize_volatility(target_return=target_ret)
            if result.get("success"):
                frontier_data.append(
                    {
                        "return": result["return"],
                        "volatility": result["volatility"],
                        "sharpe_ratio": result["sharpe_ratio"],
                    }
                )

        return pl.DataFrame(frontier_data)

    def equal_weight(self) -> dict:
        """Calculates the statistics for an equal-weight portfolio.

        Returns:
            A dictionary with equal weights and portfolio statistics.
        """
        weights = np.ones(self.n_assets) / self.n_assets
        ret, vol, sharpe = self.portfolio_stats(weights)

        return {
            "weights": dict(zip(self.tickers, weights, strict=False)),
            "return": ret,
            "volatility": vol,
            "sharpe_ratio": sharpe,
        }

    def risk_parity(self) -> dict:
        """Calculates the risk parity portfolio.

        A risk parity portfolio is one where each asset contributes equally to
        the total portfolio risk.

        Returns:
            A dictionary with risk parity weights and portfolio statistics.
        """
        # Initial guess
        initial_weights = np.ones(self.n_assets) / self.n_assets

        def risk_contributions(weights):
            """Calculate risk contributions of each asset."""
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            marginal_contrib = np.dot(self.cov_matrix, weights)
            return weights * marginal_contrib / portfolio_vol

        def risk_parity_objective(weights):
            """Minimize variance of risk contributions."""
            contrib = risk_contributions(weights)
            target_contrib = np.ones(self.n_assets) / self.n_assets
            return np.sum((contrib - target_contrib) ** 2)

        # Constraints
        constraints = [
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},
        ]

        # Bounds
        bounds = tuple((0, 1) for _ in range(self.n_assets))

        result = minimize(
            risk_parity_objective,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.portfolio_stats(optimal_weights)

            return {
                "weights": dict(zip(self.tickers, optimal_weights, strict=False)),
                "return": ret,
                "volatility": vol,
                "sharpe_ratio": sharpe,
                "success": True,
            }
        return {"success": False, "message": result.message}
