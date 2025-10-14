"""Performance metrics calculation."""

import polars as pl
import numpy as np
from typing import List, Dict, Any


class PerformanceMetrics:
    """Calculate trading performance metrics."""
    
    @staticmethod
    def calculate(equity_curve: pl.DataFrame, trades: List) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics.
        
        Args:
            equity_curve: DataFrame with timestamp and equity columns
            trades: List of Trade objects
            
        Returns:
            Dictionary with performance metrics
        """
        if len(trades) == 0:
            return {
                "num_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "avg_win": 0,
                "avg_loss": 0,
                "largest_win": 0,
                "largest_loss": 0,
                "sharpe_ratio": 0,
                "sortino_ratio": 0,
                "max_drawdown": 0,
                "max_drawdown_pct": 0
            }
        
        # Trade statistics
        pnls = [trade.pnl for trade in trades]
        winning_trades = [p for p in pnls if p > 0]
        losing_trades = [p for p in pnls if p < 0]
        
        num_trades = len(trades)
        num_winning = len(winning_trades)
        num_losing = len(losing_trades)
        win_rate = (num_winning / num_trades * 100) if num_trades > 0 else 0
        
        avg_win = np.mean(winning_trades) if winning_trades else 0
        avg_loss = np.mean(losing_trades) if losing_trades else 0
        largest_win = max(pnls) if pnls else 0
        largest_loss = min(pnls) if pnls else 0
        
        # Returns-based metrics
        equity_values = equity_curve["equity"].to_numpy()
        returns = np.diff(equity_values) / equity_values[:-1]
        
        # Sharpe Ratio (annualized, assuming daily returns)
        if len(returns) > 0 and np.std(returns) > 0:
            sharpe_ratio = np.sqrt(252) * (np.mean(returns) / np.std(returns))
        else:
            sharpe_ratio = 0
        
        # Sortino Ratio (annualized)
        negative_returns = returns[returns < 0]
        if len(negative_returns) > 0:
            downside_std = np.std(negative_returns)
            if downside_std > 0:
                sortino_ratio = np.sqrt(252) * (np.mean(returns) / downside_std)
            else:
                sortino_ratio = 0
        else:
            sortino_ratio = 0
        
        # Maximum Drawdown
        cumulative_max = np.maximum.accumulate(equity_values)
        drawdown = equity_values - cumulative_max
        max_drawdown = np.min(drawdown)
        max_drawdown_pct = (max_drawdown / cumulative_max[np.argmin(drawdown)] * 100) if cumulative_max[np.argmin(drawdown)] > 0 else 0
        
        return {
            "num_trades": num_trades,
            "winning_trades": num_winning,
            "losing_trades": num_losing,
            "win_rate": win_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "largest_win": largest_win,
            "largest_loss": largest_loss,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "max_drawdown": max_drawdown,
            "max_drawdown_pct": abs(max_drawdown_pct)
        }
    
    @staticmethod
    def calculate_rolling_metrics(
        equity_curve: pl.DataFrame,
        window: int = 30
    ) -> pl.DataFrame:
        """Calculate rolling performance metrics.
        
        Args:
            equity_curve: DataFrame with equity values
            window: Rolling window size
            
        Returns:
            DataFrame with rolling metrics
        """
        df = equity_curve.with_columns([
            pl.col("equity").pct_change().alias("returns")
        ])
        
        df = df.with_columns([
            pl.col("returns").rolling_mean(window_size=window).alias("rolling_return"),
            pl.col("returns").rolling_std(window_size=window).alias("rolling_volatility")
        ])
        
        df = df.with_columns([
            (pl.col("rolling_return") / pl.col("rolling_volatility") * np.sqrt(252)).alias("rolling_sharpe")
        ])
        
        return df
