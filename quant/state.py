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
from quant.utils.logger import get_logger

logger = get_logger(__name__)


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
    portfolio_cash: float = 100000.0
    portfolio_position_count: int = 0
    portfolio_total_pnl: float = 0.0
    portfolio_total_pnl_pct: float = 0.0
    portfolio_allocation_data: list[dict] = []
    
    # New position inputs
    new_position_ticker: str = ""
    new_position_quantity: str = ""
    new_position_price: str = ""
    
    # Portfolio optimization
    optimized_weights: list[dict] = []
    
    # Risk analytics state
    portfolio_var_95: float = 0.0
    portfolio_cvar_95: float = 0.0
    portfolio_max_drawdown: float = 0.0
    portfolio_sharpe: float = 0.0
    risk_calculating: bool = False
    
    # VaR calculation inputs
    var_confidence_level: str = "95%"
    var_method: str = "Historical"
    var_time_horizon: str = "1"
    
    # Risk metrics and data
    risk_metrics_data: list[dict] = []
    correlation_matrix_data: list[dict] = []
    drawdown_data: list[dict] = []
    
    # Risk limits
    max_position_size: str = "25"
    max_drawdown_alert: str = "20"
    max_daily_loss: str = "5000"
    min_sharpe_ratio: str = "1.0"
    
    # Dashboard stats
    active_strategies_count: int = 0
    overall_win_rate: float = 0.0
    total_trades_count: int = 0
    
    # Strategy selection
    selected_strategy: str = "Momentum"
    strategy_options: list[str] = ["Momentum", "Mean Reversion", "Breakout"]
    
    # Strategy builder state
    custom_strategy_name: str = ""
    custom_strategy_type: str = "Momentum"
    
    # Indicator toggles
    indicator_sma: bool = False
    indicator_ema: bool = False
    indicator_macd: bool = False
    indicator_adx: bool = False
    indicator_rsi: bool = False
    indicator_stochastic: bool = False
    indicator_roc: bool = False
    indicator_williams: bool = False
    indicator_bollinger: bool = False
    indicator_atr: bool = False
    indicator_keltner: bool = False
    indicator_obv: bool = False
    indicator_vwap: bool = False
    indicator_mfi: bool = False
    
    # Indicator parameters
    sma_period: str = "20"
    ema_period: str = "20"
    rsi_period: str = "14"
    bollinger_period: str = "20"
    bollinger_std: str = "2"
    
    # Trading rules
    entry_conditions: str = ""
    exit_conditions: str = ""
    
    # Position sizing
    position_size_pct: str = "10"
    stop_loss_pct: str = "2"
    take_profit_pct: str = "5"
    max_positions: str = "5"
    
    # Saved strategies
    saved_strategies: list[dict] = []

    def set_ticker(self, new_ticker: str):
        """Explicitly set the ticker value."""
        self.ticker = new_ticker.upper()

    def fetch_data(self):
        """Fetch stock data from yfinance and update the state."""
        if not self.ticker:
            logger.warning("No ticker specified")
            return

        self.is_loading = True
        try:
            # Download data using yfinance
            logger.info(f"Fetching data for {self.ticker}")
            raw_data = yf.download(self.ticker, period="1y")

            if raw_data is None or raw_data.empty:
                self.is_loading = False
                logger.error(f"No data found for ticker: {self.ticker}")
                return

            # Convert to Polars DataFrame for processing
            polars_df = pl.from_pandas(raw_data.reset_index())

            # Convert DataFrame to list of dicts for state storage
            if "Date" in polars_df.columns:
                dict_data = polars_df.with_columns(pl.col("Date").dt.strftime("%Y-%m-%d")).to_dicts()
            else:
                dict_data = polars_df.to_dicts()
                
            self.data = dict_data
            self.chart_data = dict_data
            logger.info(f"Successfully fetched {len(dict_data)} rows for {self.ticker}")

        except Exception as e:
            logger.error(f"Error fetching data for {self.ticker}: {e}", exc_info=True)
        finally:
            self.is_loading = False
    
    def run_backtest(self):
        """Run backtest on current ticker with selected strategy."""
        if not self.ticker:
            logger.warning("No ticker specified for backtest")
            return
        
        self.backtest_running = True
        try:
            # Fetch data using DataManager
            logger.info(f"Running backtest for {self.ticker} with {self.selected_strategy} strategy")
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
            logger.info(f"Backtest completed: {result.num_trades} trades, {result.total_return_pct:.2f}% return")
            
        except Exception as e:
            logger.error(f"Error running backtest: {e}", exc_info=True)
            self.backtest_results = {}
            self.backtest_trades = []
            self.backtest_equity_curve = []
        finally:
            self.backtest_running = False
    
    def set_strategy(self, strategy: str):
        """Set the selected strategy."""
        self.selected_strategy = strategy
    
    # Portfolio management methods
    def set_new_position_ticker(self, ticker: str):
        """Set the new position ticker."""
        self.new_position_ticker = ticker.upper()
    
    def set_new_position_quantity(self, quantity: str):
        """Set the new position quantity."""
        self.new_position_quantity = quantity
    
    def set_new_position_price(self, price: str):
        """Set the new position price."""
        self.new_position_price = price
    
    def add_portfolio_position(self):
        """Add a new position to the portfolio."""
        if not self.new_position_ticker or not self.new_position_quantity or not self.new_position_price:
            return
        
        try:
            qty = float(self.new_position_quantity)
            price = float(self.new_position_price)
            cost = qty * price
            
            # Add to holdings
            self.portfolio_holdings.append({
                "ticker": self.new_position_ticker,
                "quantity": qty,
                "entry_price": price,
                "current_price": price,
                "market_value": cost,
                "pnl": 0.0,
                "pnl_pct": 0.0,
                "weight": 0.0,
            })
            
            self.portfolio_cash -= cost
            self.portfolio_position_count += 1
            
            # Clear inputs
            self.new_position_ticker = ""
            self.new_position_quantity = ""
            self.new_position_price = ""
            
            self._update_portfolio_metrics()
        except Exception as e:
            print(f"Error adding position: {e}")
    
    def _update_portfolio_metrics(self):
        """Update portfolio metrics."""
        total_value = self.portfolio_cash
        for holding in self.portfolio_holdings:
            total_value += holding["market_value"]
        
        self.portfolio_value = total_value
        
        # Update weights
        for holding in self.portfolio_holdings:
            holding["weight"] = (holding["market_value"] / total_value) * 100 if total_value > 0 else 0
        
        # Update allocation data for pie chart
        self.portfolio_allocation_data = [
            {"ticker": h["ticker"], "value": h["market_value"]}
            for h in self.portfolio_holdings
        ]
    
    def optimize_portfolio_sharpe(self):
        """Optimize portfolio for maximum Sharpe ratio."""
        print("Optimizing for maximum Sharpe ratio...")
        # Implementation would use portfolio optimization module
        
    def optimize_portfolio_volatility(self):
        """Optimize portfolio for minimum volatility."""
        print("Optimizing for minimum volatility...")
        
    def optimize_portfolio_risk_parity(self):
        """Optimize portfolio using risk parity."""
        print("Optimizing using risk parity...")
        
    def apply_rebalancing(self):
        """Apply the optimized rebalancing."""
        print("Applying rebalancing...")
    
    # Risk analytics methods
    def set_var_confidence_level(self, level: str):
        """Set VaR confidence level."""
        self.var_confidence_level = level
    
    def set_var_method(self, method: str):
        """Set VaR calculation method."""
        self.var_method = method
    
    def set_var_time_horizon(self, horizon: str):
        """Set VaR time horizon."""
        self.var_time_horizon = horizon
    
    def calculate_portfolio_var(self):
        """Calculate portfolio VaR and risk metrics."""
        self.risk_calculating = True
        try:
            # Implementation would use risk module
            print(f"Calculating VaR using {self.var_method} method...")
            self.portfolio_var_95 = -5000.0
            self.portfolio_cvar_95 = -7500.0
            
            self.risk_metrics_data = [
                {"metric": "VaR (95%)", "value": "$-5,000", "description": "1-day Value at Risk"},
                {"metric": "CVaR (95%)", "value": "$-7,500", "description": "Conditional VaR"},
                {"metric": "Sharpe Ratio", "value": "1.25", "description": "Risk-adjusted return"},
                {"metric": "Sortino Ratio", "value": "1.45", "description": "Downside risk-adjusted"},
                {"metric": "Max Drawdown", "value": "-15.2%", "description": "Peak to trough"},
                {"metric": "Calmar Ratio", "value": "0.82", "description": "Return / Max DD"},
            ]
        except Exception as e:
            print(f"Error calculating VaR: {e}")
        finally:
            self.risk_calculating = False
    
    def calculate_correlations(self):
        """Calculate correlation matrix for portfolio assets."""
        self.risk_calculating = True
        try:
            print("Calculating correlations...")
            # Implementation would calculate actual correlations
        except Exception as e:
            print(f"Error calculating correlations: {e}")
        finally:
            self.risk_calculating = False
    
    def load_portfolio_history(self):
        """Load portfolio history for drawdown analysis."""
        print("Loading portfolio history...")
    
    def set_max_position_size(self, size: str):
        """Set max position size."""
        self.max_position_size = size
    
    def set_max_drawdown_alert(self, alert: str):
        """Set max drawdown alert."""
        self.max_drawdown_alert = alert
    
    def set_max_daily_loss(self, loss: str):
        """Set max daily loss."""
        self.max_daily_loss = loss
    
    def set_min_sharpe_ratio(self, ratio: str):
        """Set min Sharpe ratio."""
        self.min_sharpe_ratio = ratio
    
    def save_risk_limits(self):
        """Save risk limits."""
        print("Saving risk limits...")
    
    # Strategy builder methods
    def set_custom_strategy_name(self, name: str):
        """Set custom strategy name."""
        self.custom_strategy_name = name
    
    def set_custom_strategy_type(self, strategy_type: str):
        """Set custom strategy type."""
        self.custom_strategy_type = strategy_type
    
    def toggle_indicator_sma(self, checked: bool):
        """Toggle SMA indicator."""
        self.indicator_sma = checked
    
    def toggle_indicator_ema(self, checked: bool):
        """Toggle EMA indicator."""
        self.indicator_ema = checked
    
    def toggle_indicator_macd(self, checked: bool):
        """Toggle MACD indicator."""
        self.indicator_macd = checked
    
    def toggle_indicator_adx(self, checked: bool):
        """Toggle ADX indicator."""
        self.indicator_adx = checked
    
    def toggle_indicator_rsi(self, checked: bool):
        """Toggle RSI indicator."""
        self.indicator_rsi = checked
    
    def toggle_indicator_stochastic(self, checked: bool):
        """Toggle Stochastic indicator."""
        self.indicator_stochastic = checked
    
    def toggle_indicator_roc(self, checked: bool):
        """Toggle ROC indicator."""
        self.indicator_roc = checked
    
    def toggle_indicator_williams(self, checked: bool):
        """Toggle Williams %R indicator."""
        self.indicator_williams = checked
    
    def toggle_indicator_bollinger(self, checked: bool):
        """Toggle Bollinger Bands indicator."""
        self.indicator_bollinger = checked
    
    def toggle_indicator_atr(self, checked: bool):
        """Toggle ATR indicator."""
        self.indicator_atr = checked
    
    def toggle_indicator_keltner(self, checked: bool):
        """Toggle Keltner Channel indicator."""
        self.indicator_keltner = checked
    
    def toggle_indicator_obv(self, checked: bool):
        """Toggle OBV indicator."""
        self.indicator_obv = checked
    
    def toggle_indicator_vwap(self, checked: bool):
        """Toggle VWAP indicator."""
        self.indicator_vwap = checked
    
    def toggle_indicator_mfi(self, checked: bool):
        """Toggle MFI indicator."""
        self.indicator_mfi = checked
    
    def set_sma_period(self, period: str):
        """Set SMA period."""
        self.sma_period = period
    
    def set_ema_period(self, period: str):
        """Set EMA period."""
        self.ema_period = period
    
    def set_rsi_period(self, period: str):
        """Set RSI period."""
        self.rsi_period = period
    
    def set_bollinger_period(self, period: str):
        """Set Bollinger Bands period."""
        self.bollinger_period = period
    
    def set_bollinger_std(self, std: str):
        """Set Bollinger Bands standard deviation."""
        self.bollinger_std = std
    
    def set_entry_conditions(self, conditions: str):
        """Set entry conditions."""
        self.entry_conditions = conditions
    
    def set_exit_conditions(self, conditions: str):
        """Set exit conditions."""
        self.exit_conditions = conditions
    
    def set_position_size_pct(self, pct: str):
        """Set position size percentage."""
        self.position_size_pct = pct
    
    def set_stop_loss_pct(self, pct: str):
        """Set stop loss percentage."""
        self.stop_loss_pct = pct
    
    def set_take_profit_pct(self, pct: str):
        """Set take profit percentage."""
        self.take_profit_pct = pct
    
    def set_max_positions(self, max_pos: str):
        """Set maximum positions."""
        self.max_positions = max_pos
    
    def save_custom_strategy(self):
        """Save the custom strategy."""
        if not self.custom_strategy_name:
            return
        
        indicators = []
        if self.indicator_sma:
            indicators.append(f"SMA({self.sma_period})")
        if self.indicator_ema:
            indicators.append(f"EMA({self.ema_period})")
        if self.indicator_rsi:
            indicators.append(f"RSI({self.rsi_period})")
        if self.indicator_macd:
            indicators.append("MACD")
        if self.indicator_bollinger:
            indicators.append(f"BB({self.bollinger_period})")
        
        self.saved_strategies.append({
            "name": self.custom_strategy_name,
            "type": self.custom_strategy_type,
            "indicators": ", ".join(indicators) if indicators else "None",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "actions": "Load | Delete"
        })
        
        print(f"Saved strategy: {self.custom_strategy_name}")
    
    def test_custom_strategy(self):
        """Test the custom strategy."""
        print(f"Testing strategy: {self.custom_strategy_name}")
    
    def reset_strategy_builder(self):
        """Reset the strategy builder."""
        self.custom_strategy_name = ""
        self.indicator_sma = False
        self.indicator_ema = False
        self.indicator_macd = False
        self.indicator_adx = False
        self.indicator_rsi = False
        self.indicator_stochastic = False
        self.indicator_roc = False
        self.indicator_williams = False
        self.indicator_bollinger = False
        self.indicator_atr = False
        self.indicator_keltner = False
        self.indicator_obv = False
        self.indicator_vwap = False
        self.indicator_mfi = False
        self.entry_conditions = ""
        self.exit_conditions = ""
