"""Comprehensive risk metrics calculation."""

import numpy as np
import polars as pl
from typing import Dict, Optional
from scipy import stats


class RiskMetrics:
    """Calculate various risk metrics for portfolios and strategies."""
    
    @staticmethod
    def calculate_returns(prices: np.ndarray) -> np.ndarray:
        """Calculate returns from price series.
        
        Args:
            prices: Array of prices
            
        Returns:
            Array of returns
        """
        return np.diff(prices) / prices[:-1]
    
    @staticmethod
    def volatility(returns: np.ndarray, annualize: bool = True) -> float:
        """Calculate volatility (standard deviation of returns).
        
        Args:
            returns: Array of returns
            annualize: Whether to annualize (assume daily returns)
            
        Returns:
            Volatility
        """
        vol = np.std(returns)
        return vol * np.sqrt(252) if annualize else vol
    
    @staticmethod
    def downside_deviation(returns: np.ndarray, target: float = 0.0, annualize: bool = True) -> float:
        """Calculate downside deviation.
        
        Args:
            returns: Array of returns
            target: Target return (default 0)
            annualize: Whether to annualize
            
        Returns:
            Downside deviation
        """
        downside_returns = returns[returns < target]
        if len(downside_returns) == 0:
            return 0.0
        
        downside_dev = np.std(downside_returns)
        return downside_dev * np.sqrt(252) if annualize else downside_dev
    
    @staticmethod
    def sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
        """Calculate Sharpe ratio.
        
        Args:
            returns: Array of returns
            risk_free_rate: Risk-free rate (annualized)
            
        Returns:
            Sharpe ratio
        """
        mean_return = np.mean(returns) * 252  # Annualize
        vol = np.std(returns) * np.sqrt(252)  # Annualize
        
        if vol == 0:
            return 0.0
        
        return (mean_return - risk_free_rate) / vol
    
    @staticmethod
    def sortino_ratio(returns: np.ndarray, target: float = 0.0, risk_free_rate: float = 0.0) -> float:
        """Calculate Sortino ratio.
        
        Args:
            returns: Array of returns
            target: Target return
            risk_free_rate: Risk-free rate (annualized)
            
        Returns:
            Sortino ratio
        """
        mean_return = np.mean(returns) * 252
        downside_dev = RiskMetrics.downside_deviation(returns, target, annualize=True)
        
        if downside_dev == 0:
            return 0.0
        
        return (mean_return - risk_free_rate) / downside_dev
    
    @staticmethod
    def max_drawdown(prices: np.ndarray) -> Dict[str, float]:
        """Calculate maximum drawdown.
        
        Args:
            prices: Array of prices or equity curve
            
        Returns:
            Dictionary with max_drawdown, max_drawdown_pct, peak, trough
        """
        cumulative_max = np.maximum.accumulate(prices)
        drawdown = prices - cumulative_max
        max_dd = np.min(drawdown)
        max_dd_idx = np.argmin(drawdown)
        peak_idx = np.argmax(cumulative_max[:max_dd_idx + 1])
        
        max_dd_pct = (max_dd / cumulative_max[max_dd_idx]) * 100 if cumulative_max[max_dd_idx] > 0 else 0
        
        return {
            "max_drawdown": abs(max_dd),
            "max_drawdown_pct": abs(max_dd_pct),
            "peak_value": prices[peak_idx],
            "trough_value": prices[max_dd_idx],
            "peak_idx": int(peak_idx),
            "trough_idx": int(max_dd_idx)
        }
    
    @staticmethod
    def calmar_ratio(returns: np.ndarray, prices: np.ndarray) -> float:
        """Calculate Calmar ratio (return / max drawdown).
        
        Args:
            returns: Array of returns
            prices: Array of prices for drawdown calculation
            
        Returns:
            Calmar ratio
        """
        annual_return = np.mean(returns) * 252
        max_dd = RiskMetrics.max_drawdown(prices)["max_drawdown_pct"]
        
        if max_dd == 0:
            return 0.0
        
        return annual_return / max_dd
    
    @staticmethod
    def skewness(returns: np.ndarray) -> float:
        """Calculate skewness of returns.
        
        Args:
            returns: Array of returns
            
        Returns:
            Skewness
        """
        return stats.skew(returns)
    
    @staticmethod
    def kurtosis(returns: np.ndarray) -> float:
        """Calculate kurtosis of returns.
        
        Args:
            returns: Array of returns
            
        Returns:
            Kurtosis
        """
        return stats.kurtosis(returns)
    
    @staticmethod
    def correlation_matrix(returns_df: pl.DataFrame) -> np.ndarray:
        """Calculate correlation matrix for multiple assets.
        
        Args:
            returns_df: DataFrame with returns for multiple assets
            
        Returns:
            Correlation matrix
        """
        returns_array = returns_df.to_numpy()
        return np.corrcoef(returns_array.T)
    
    @staticmethod
    def beta(asset_returns: np.ndarray, market_returns: np.ndarray) -> float:
        """Calculate beta relative to market.
        
        Args:
            asset_returns: Asset returns
            market_returns: Market/benchmark returns
            
        Returns:
            Beta
        """
        covariance = np.cov(asset_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        
        if market_variance == 0:
            return 0.0
        
        return covariance / market_variance
    
    @staticmethod
    def alpha(asset_returns: np.ndarray, market_returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
        """Calculate Jensen's alpha.
        
        Args:
            asset_returns: Asset returns
            market_returns: Market/benchmark returns
            risk_free_rate: Risk-free rate
            
        Returns:
            Alpha
        """
        beta = RiskMetrics.beta(asset_returns, market_returns)
        asset_return = np.mean(asset_returns) * 252
        market_return = np.mean(market_returns) * 252
        
        return asset_return - (risk_free_rate + beta * (market_return - risk_free_rate))
    
    @staticmethod
    def information_ratio(asset_returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
        """Calculate information ratio.
        
        Args:
            asset_returns: Asset returns
            benchmark_returns: Benchmark returns
            
        Returns:
            Information ratio
        """
        excess_returns = asset_returns - benchmark_returns
        tracking_error = np.std(excess_returns) * np.sqrt(252)
        
        if tracking_error == 0:
            return 0.0
        
        return (np.mean(excess_returns) * 252) / tracking_error
    
    @staticmethod
    def tail_ratio(returns: np.ndarray, percentile: float = 5.0) -> float:
        """Calculate tail ratio (95th percentile / 5th percentile).
        
        Args:
            returns: Array of returns
            percentile: Percentile for tails
            
        Returns:
            Tail ratio
        """
        upper_tail = np.percentile(returns, 100 - percentile)
        lower_tail = np.percentile(returns, percentile)
        
        if lower_tail >= 0:
            return 0.0
        
        return abs(upper_tail / lower_tail)
    
    @staticmethod
    def comprehensive_report(returns: np.ndarray, prices: np.ndarray) -> Dict:
        """Generate comprehensive risk metrics report.
        
        Args:
            returns: Array of returns
            prices: Array of prices
            
        Returns:
            Dictionary with all risk metrics
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
            "median_return": np.median(returns) * 252
        }
