"""Backtesting engine for strategy evaluation."""

import polars as pl
import uuid
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

from quant.strategies.base import Strategy, Signal, Position
from quant.data.database import Database
from .metrics import PerformanceMetrics


@dataclass
class Trade:
    """Represents a completed trade."""
    trade_id: str
    ticker: str
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    quantity: float
    side: str
    pnl: float
    pnl_percent: float
    commission: float


@dataclass
class BacktestResult:
    """Results of a backtest run."""
    run_id: str
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_value: float
    total_return: float
    total_return_pct: float
    num_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    max_drawdown_pct: float
    trades: list[Trade]
    equity_curve: pl.DataFrame


class BacktestEngine:
    """Engine for backtesting trading strategies."""
    
    def __init__(
        self,
        strategy: Strategy,
        initial_capital: float = 100000,
        commission: float = 0.001,  # 0.1% per trade
        db: Optional[Database] = None
    ):
        """Initialize backtest engine.
        
        Args:
            strategy: Trading strategy to backtest
            initial_capital: Starting capital
            commission: Commission per trade (as decimal)
            db: Database for storing results
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.db = db
        
        self.cash = initial_capital
        self.portfolio_value = initial_capital
        self.trades: list[Trade] = []
        self.equity_history = []
    
    def run(
        self,
        data: pl.DataFrame,
        ticker: str = "UNKNOWN"
    ) -> BacktestResult:
        """Run backtest on historical data.
        
        Args:
            data: DataFrame with OHLCV data and indicators
            ticker: Ticker symbol
            
        Returns:
            BacktestResult with performance metrics
        """
        # Reset state
        self.cash = self.initial_capital
        self.portfolio_value = self.initial_capital
        self.trades = []
        self.equity_history = []
        self.strategy.positions = {}
        
        # Generate signals
        data_with_signals = self.strategy.generate_signals(data)
        
        # Iterate through each bar
        for i in range(len(data_with_signals)):
            row = data_with_signals.row(i, named=True)
            timestamp = str(row.get("timestamp", ""))
            signal = row.get("signal", 0)
            close_price = row["close"]
            
            # Update portfolio value
            current_position = self.strategy.get_position(ticker)
            if current_position:
                self.portfolio_value = self.cash + (current_position.quantity * close_price)
            else:
                self.portfolio_value = self.cash
            
            # Record equity
            self.equity_history.append({
                "timestamp": timestamp,
                "equity": self.portfolio_value,
                "cash": self.cash,
                "signal": signal
            })
            
            # Process signals
            if signal == Signal.BUY.value and not self.strategy.has_position(ticker):
                # Enter long position
                position_size = self.strategy.calculate_position_size(
                    data_with_signals, self.cash, close_price
                )
                
                if position_size > 0:
                    cost = position_size * close_price
                    commission_cost = cost * self.commission
                    total_cost = cost + commission_cost
                    
                    if total_cost <= self.cash:
                        # Open position
                        self.cash -= total_cost
                        position = Position(
                            ticker=ticker,
                            quantity=position_size,
                            entry_price=close_price,
                            entry_date=timestamp,
                            side="long"
                        )
                        self.strategy.add_position(position)
            
            elif signal == Signal.SELL.value and self.strategy.has_position(ticker):
                # Exit position
                position = self.strategy.close_position(ticker)
                if position:
                    proceeds = position.quantity * close_price
                    commission_cost = proceeds * self.commission
                    net_proceeds = proceeds - commission_cost
                    
                    self.cash += net_proceeds
                    
                    # Record trade
                    pnl = position.pnl(close_price) - (commission_cost + position.quantity * position.entry_price * self.commission)
                    pnl_pct = position.pnl_percent(close_price)
                    
                    trade = Trade(
                        trade_id=str(uuid.uuid4()),
                        ticker=ticker,
                        entry_date=position.entry_date,
                        exit_date=timestamp,
                        entry_price=position.entry_price,
                        exit_price=close_price,
                        quantity=position.quantity,
                        side=position.side,
                        pnl=pnl,
                        pnl_percent=pnl_pct,
                        commission=commission_cost + position.quantity * position.entry_price * self.commission
                    )
                    self.trades.append(trade)
        
        # Close any remaining positions at final price
        if self.strategy.has_position(ticker):
            final_row = data_with_signals.row(-1, named=True)
            final_price = final_row["close"]
            final_timestamp = str(final_row.get("timestamp", ""))
            
            position = self.strategy.close_position(ticker)
            if position:
                proceeds = position.quantity * final_price
                commission_cost = proceeds * self.commission
                net_proceeds = proceeds - commission_cost
                self.cash += net_proceeds
                
                pnl = position.pnl(final_price) - (commission_cost + position.quantity * position.entry_price * self.commission)
                pnl_pct = position.pnl_percent(final_price)
                
                trade = Trade(
                    trade_id=str(uuid.uuid4()),
                    ticker=ticker,
                    entry_date=position.entry_date,
                    exit_date=final_timestamp,
                    entry_price=position.entry_price,
                    exit_price=final_price,
                    quantity=position.quantity,
                    side=position.side,
                    pnl=pnl,
                    pnl_percent=pnl_pct,
                    commission=commission_cost + position.quantity * position.entry_price * self.commission
                )
                self.trades.append(trade)
        
        # Final portfolio value
        self.portfolio_value = self.cash
        
        # Calculate metrics
        equity_df = pl.DataFrame(self.equity_history)
        metrics = PerformanceMetrics.calculate(equity_df, self.trades)
        
        # Create result
        result = BacktestResult(
            run_id=str(uuid.uuid4()),
            strategy_name=self.strategy.name,
            start_date=str(data_with_signals["timestamp"][0]),
            end_date=str(data_with_signals["timestamp"][-1]),
            initial_capital=self.initial_capital,
            final_value=self.portfolio_value,
            total_return=self.portfolio_value - self.initial_capital,
            total_return_pct=((self.portfolio_value - self.initial_capital) / self.initial_capital) * 100,
            num_trades=metrics["num_trades"],
            winning_trades=metrics["winning_trades"],
            losing_trades=metrics["losing_trades"],
            win_rate=metrics["win_rate"],
            avg_win=metrics["avg_win"],
            avg_loss=metrics["avg_loss"],
            largest_win=metrics["largest_win"],
            largest_loss=metrics["largest_loss"],
            sharpe_ratio=metrics["sharpe_ratio"],
            sortino_ratio=metrics["sortino_ratio"],
            max_drawdown=metrics["max_drawdown"],
            max_drawdown_pct=metrics["max_drawdown_pct"],
            trades=self.trades,
            equity_curve=equity_df
        )
        
        # Save to database if available
        if self.db:
            self._save_to_database(result)
        
        return result
    
    def _save_to_database(self, result: BacktestResult):
        """Save backtest results to database."""
        # Save run
        run_data = {
            "run_id": result.run_id,
            "strategy_name": result.strategy_name,
            "start_date": result.start_date,
            "end_date": result.end_date,
            "initial_capital": result.initial_capital,
            "final_value": result.final_value,
            "total_return": result.total_return_pct,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown_pct
        }
        self.db.save_backtest_run(run_data)
        
        # Save trades
        if result.trades:
            trades_data = []
            for trade in result.trades:
                trade_dict = asdict(trade)
                trade_dict["run_id"] = result.run_id
                trades_data.append(trade_dict)
            
            trades_df = pl.DataFrame(trades_data)
            self.db.save_trades(trades_df)
