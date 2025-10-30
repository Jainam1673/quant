"""A library of functions for calculating financial risk and performance metrics.

This module provides a `RiskMetrics` class with a suite of static methods for
calculating common metrics such as Sharpe ratio, Sortino ratio, max drawdown,
and more. These are essential for evaluating the performance of trading
strategies and portfolios.
"""

import numpy as np
import polars as pl
from scipy import stats


class RiskMetrics:
    """Provides a collection of static methods for risk and performance calculation."""

    @staticmethod
    def calculate_returns(prices: np.ndarray) -> np.ndarray:
        """Calculates the percentage change between consecutive prices.

        Args:
            prices: A NumPy array of prices.

        Returns:
            A NumPy array of returns.
        """
        return np.diff(prices) / prices[:-1]

    @staticmethod
    def volatility(returns: np.ndarray, annualize: bool = True) -> float:
        """Calculates the volatility (standard deviation) of returns.

        Args:
            returns: A NumPy array of returns.
            annualize: If True, annualizes the volatility (assumes daily returns).

        Returns:
            The calculated volatility.
        """
        vol = np.std(returns)
        return vol * np.sqrt(252) if annualize else vol

    @staticmethod
    def downside_deviation(
        returns: np.ndarray, target: float = 0.0, annualize: bool = True
    ) -> float:
        """Calculates the downside deviation, used in the Sortino ratio.

        This measures the volatility of returns that fall below a specified target.

        Args:
            returns: A NumPy array of returns.
            target: The target return, typically the risk-free rate.
            annualize: If True, annualizes the deviation.

        Returns:
            The downside deviation.
        """
        downside_returns = returns[returns < target]
        if len(downside_returns) == 0:
            return 0.0

        downside_dev = np.std(downside_returns)
        return downside_dev * np.sqrt(252) if annualize else downside_dev

    @staticmethod
    def sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
        """Calculates the Sharpe ratio.

        The Sharpe ratio measures the performance of an investment compared to a
        risk-free asset, after adjusting for its risk.

        Args:
            returns: A NumPy array of returns.
            risk_free_rate: The annualized risk-free rate.

        Returns:
            The annualized Sharpe ratio.
        """
        mean_return = np.mean(returns) * 252  # Annualize
        vol = np.std(returns) * np.sqrt(252)  # Annualize

        if vol == 0:
            return 0.0

        return (mean_return - risk_free_rate) / vol

    @staticmethod
    def sortino_ratio(
        returns: np.ndarray, target: float = 0.0, risk_free_rate: float = 0.0
    ) -> float:
        """Calculates the Sortino ratio.

        The Sortino ratio is a variation of the Sharpe ratio that only penalizes
        for downside volatility.

        Args:
            returns: A NumPy array of returns.
            target: The target return for calculating downside deviation.
            risk_free_rate: The annualized risk-free rate.

        Returns:
            The annualized Sortino ratio.
        """
        mean_return = np.mean(returns) * 252
        downside_dev = RiskMetrics.downside_deviation(returns, target, annualize=True)

        if downside_dev == 0:
            return 0.0

        return (mean_return - risk_free_rate) / downside_dev

    @staticmethod
    def max_drawdown(prices: np.ndarray) -> dict[str, float]:
        """Calculates the maximum drawdown from an equity curve.

        The maximum drawdown is the largest peak-to-trough decline in the value
        of a portfolio.

        Args:
            prices: A NumPy array of prices or equity values.

        Returns:
            A dictionary containing the max drawdown amount, percentage, and peak/trough info.
        """
        cumulative_max = np.maximum.accumulate(prices)
        drawdown = prices - cumulative_max
        max_dd = np.min(drawdown)
        max_dd_idx = np.argmin(drawdown)
        peak_idx = np.argmax(cumulative_max[: max_dd_idx + 1])

        max_dd_pct = (
            (max_dd / cumulative_max[max_dd_idx]) * 100 if cumulative_max[max_dd_idx] > 0 else 0
        )

        return {
            "max_drawdown": abs(max_dd),
            "max_drawdown_pct": abs(max_dd_pct),
            "peak_value": prices[peak_idx],
            "trough_value": prices[max_dd_idx],
            "peak_idx": int(peak_idx),
            "trough_idx": int(max_dd_idx),
        }

    @staticmethod
    def calmar_ratio(returns: np.ndarray, prices: np.ndarray) -> float:
        """Calculates the Calmar ratio.

        The Calmar ratio is the ratio of the annualized return to the maximum drawdown.

        Args:
            returns: A NumPy array of returns.
            prices: A NumPy array of prices for the max drawdown calculation.

        Returns:
            The Calmar ratio.
        """
        annual_return = np.mean(returns) * 252
        max_dd = RiskMetrics.max_drawdown(prices)["max_drawdown_pct"]

        if max_dd == 0:
            return 0.0

        return annual_return / max_dd

    @staticmethod
    def skewness(returns: np.ndarray) -> float:
        """Calculates the skewness of the returns distribution."""
        return stats.skew(returns)

    @staticmethod
    def kurtosis(returns: np.ndarray) -> float:
        """Calculates the kurtosis of the returns distribution."""
        return stats.kurtosis(returns)

    @staticmethod
    def correlation_matrix(returns_df: pl.DataFrame) -> np.ndarray:
        """Calculates the correlation matrix for a DataFrame of asset returns."""
        returns_array = returns_df.to_numpy()
        return np.corrcoef(returns_array.T)

    @staticmethod
    def beta(asset_returns: np.ndarray, market_returns: np.ndarray) -> float:
        """Calculates the beta of an asset relative to a benchmark.

        Beta measures the volatility of an asset in relation to the overall market.

        Args:
            asset_returns: The returns of the asset.
            market_returns: The returns of the market or benchmark.

        Returns:
            The beta value.
        """
        covariance = np.cov(asset_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)

        if market_variance == 0:
            return 0.0

        return covariance / market_variance

    @staticmethod
    def alpha(
        asset_returns: np.ndarray, market_returns: np.ndarray, risk_free_rate: float = 0.0
    ) -> float:
        """Calculates Jensen's alpha.

        Alpha represents the excess return of an investment relative to the return
        of a benchmark index.

        Args:
            asset_returns: The returns of the asset.
            market_returns: The returns of the benchmark.
            risk_free_rate: The annualized risk-free rate.

        Returns:
            The alpha value.
        """
        beta = RiskMetrics.beta(asset_returns, market_returns)
        asset_return = np.mean(asset_returns) * 252
        market_return = np.mean(market_returns) * 252

        return asset_return - (risk_free_rate + beta * (market_return - risk_free_rate))

    @staticmethod
    def information_ratio(asset_returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
        """Calculates the information ratio.

        This ratio measures a portfolio manager's ability to generate excess
        returns relative to a benchmark, but also attempts to identify the
        consistency of the portfolio manager.

        Args:
            asset_returns: The returns of the asset.
            benchmark_returns: The returns of the benchmark.

        Returns:
            The information ratio.
        """
        excess_returns = asset_returns - benchmark_returns
        tracking_error = np.std(excess_returns) * np.sqrt(252)

        if tracking_error == 0:
            return 0.0

        return (np.mean(excess_returns) * 252) / tracking_error

    @staticmethod
    def tail_ratio(returns: np.ndarray, percentile: float = 5.0) -> float:
        """Calculates the tail ratio.

        This ratio compares the value of the 95th percentile of returns to the
        absolute value of the 5th percentile of returns, providing a measure of
        the asymmetry of the return distribution.

        Args:
            returns: A NumPy array of returns.
            percentile: The percentile to use for the tails (e.g., 5.0 for 5th and 95th).

        Returns:
            The tail ratio.
        """
        upper_tail = np.percentile(returns, 100 - percentile)
        lower_tail = np.percentile(returns, percentile)

        if lower_tail >= 0:
            return 0.0

        return abs(upper_tail / lower_tail)

    @staticmethod
    def comprehensive_report(returns: np.ndarray, prices: np.ndarray) -> dict:
        """Generates a comprehensive report of all key risk and performance metrics.

        Args:
            returns: A NumPy array of returns.
            prices: A NumPy array of prices for drawdown calculation.

        Returns:
            A dictionary containing a wide range of calculated metrics.
        """
        return {
            "volatility": RiskMetrics.volatility(returns),
            "downside_deviation": RiskMetrics.downside_deviation(returns),
            "sharpe_ratio": RiskMetrics.sharpe_ratio(returns),
            "sortino_ratio": RiskMetrics.sortino_ratio(returns),
            "max_drawdown": RiskMetrics.max_drawdown(prices)["max_drawdown_pct"],
            "calmar_ratio": RiskMetrics.calmar_ratio(returns, prices),
            "skewness": RiskMetrics.skewness(returns),
            "kurtosis": RiskMetrics.kurtosis(returns),
            "tail_ratio": RiskMetrics.tail_ratio(returns),
            "mean_return": np.mean(returns) * 252,
            "median_return": np.median(returns) * 252,
        }
