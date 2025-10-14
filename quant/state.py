"""The shared application state for the Quant Dashboard."""

import reflex as rx
import yfinance as yf
import polars as pl
from datetime import datetime
from typing import List, Dict

from quant.data.data_manager import DataManager
from quant.data.database import Database
from quant.indicators import (
    SMA, EMA, RSI, MACD, BollingerBands, ATR
)
from quant.strategies import (
    MomentumStrategy, MeanReversionStrategy, BreakoutStrategy
)
from quant.backtesting import BacktestEngine
from quant.portfolio import Portfolio


class State(rx.State):
    """The application state."""
    
    # Current ticker and data
    ticker: str = "AAPL"
    data: list[dict] = []
    table_columns: list[rx.Component] = []
    chart_data: list[dict] = []
    is_loading: bool = False
    
    # Backtest state
    backtest_running: bool = False
    backtest_results: dict = {}
    backtest_trades: list[dict] = []
    backtest_equity_curve: list[dict] = []
    
    # Portfolio state
    portfolio_name: str = "My Portfolio"
    portfolio_value: float = 100000.0
    portfolio_holdings: list[dict] = []
    
    # Strategy selection
    selected_strategy: str = "Momentum"
    strategy_options: list[str] = ["Momentum", "Mean Reversion", "Breakout"]

    def set_ticker(self, new_ticker: str):
        """Explicitly set the ticker value."""
        self.ticker = new_ticker.upper()

    def fetch_data(self):
        """Fetch stock data from yfinance and update the state."""
        if not self.ticker:
            return

        self.is_loading = True
        try:
            # Download data using yfinance
            raw_data = yf.download(self.ticker, period="1y")

            if raw_data.empty:
                self.is_loading = False
                print(f"No data found for ticker: {self.ticker}")
                return

            # Convert to Polars DataFrame for processing
            polars_df = pl.from_pandas(raw_data.reset_index())

            # Create column definitions for the data table
            self.table_columns = [
                rx.data_table.column(
                    header=col,
                    accessor_key=str(col),
                )
                for col in polars_df.columns
            ]
            
            # Convert DataFrame to list of dicts for state storage
            dict_data = polars_df.with_columns(pl.col("Date").dt.strftime("%Y-%m-%d")).to_dicts()
            self.data = dict_data
            self.chart_data = dict_data

        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
        finally:
            self.is_loading = False
    
    def run_backtest(self):
        """Run backtest on current ticker with selected strategy."""
        if not self.ticker or not self.data:
            return
        
        self.backtest_running = True
        try:
            # Fetch data using DataManager
            db = Database()
            data_manager = DataManager(db)
            df = data_manager.fetch_and_store(self.ticker, period="1y")
            
            # Add indicators
            df = SMA(20)(df)
            df = SMA(50)(df)
            df = SMA(200)(df)
            df = EMA(20)(df)
            df = RSI(14)(df)
            df = MACD()(df)
            df = BollingerBands()(df)
            df = ATR()(df)
            
            # Select strategy
            if self.selected_strategy == "Momentum":
                strategy = MomentumStrategy()
            elif self.selected_strategy == "Mean Reversion":
                strategy = MeanReversionStrategy()
            else:
                strategy = BreakoutStrategy()
            
            # Run backtest
            engine = BacktestEngine(strategy, initial_capital=100000, db=db)
            result = engine.run(df, self.ticker)
            
            # Store results
            self.backtest_results = {
                "strategy_name": result.strategy_name,
                "initial_capital": result.initial_capital,
                "final_value": result.final_value,
                "total_return": result.total_return,
                "total_return_pct": result.total_return_pct,
                "num_trades": result.num_trades,
                "win_rate": result.win_rate,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown_pct
            }
            
            # Store trades
            self.backtest_trades = [
                {
                    "ticker": t.ticker,
                    "entry_date": t.entry_date,
                    "exit_date": t.exit_date,
                    "entry_price": t.entry_price,
                    "exit_price": t.exit_price,
                    "quantity": t.quantity,
                    "pnl": t.pnl,
                    "pnl_pct": t.pnl_percent
                }
                for t in result.trades
            ]
            
            # Store equity curve
            self.backtest_equity_curve = result.equity_curve.to_dicts()
            
        except Exception as e:
            print(f"Error running backtest: {e}")
        finally:
            self.backtest_running = False
    
    def set_strategy(self, strategy: str):
        """Set the selected strategy."""
        self.selected_strategy = strategy
