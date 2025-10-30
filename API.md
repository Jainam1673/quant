# API Documentation

## Overview

This document provides comprehensive documentation for the Quant Trading Platform's internal APIs and modules.

## Core Modules

### Data Management

The data management layer is responsible for fetching, storing, and retrieving all market data.

#### `quant.data.database.Database`

A high-performance wrapper for DuckDB, designed for efficient storage and querying of financial time-series data.

**Key Methods:**

- `__init__(self, db_path: str)`: Initializes the connection to the database file and creates the necessary tables if they don't exist.
- `insert_ohlcv(self, df: pl.DataFrame)`: Inserts or replaces OHLCV data. This method is idempotent, preventing duplicate entries for the same ticker and timestamp.
- `get_ohlcv(self, ticker: str, start_date: Optional[str], end_date: Optional[str]) -> pl.DataFrame`: Retrieves OHLCV data for a single ticker within an optional date range.
- `get_multiple_tickers(self, tickers: list[str], ...) -> pl.DataFrame`: Efficiently retrieves data for a list of tickers.
- `save_backtest_run(self, run_data: dict)`: Persists the summary results of a backtest run to the `backtest_runs` table.

#### `quant.data.data_manager.DataManager`

This class acts as a smart cache and data source, abstracting away the complexities of data fetching and storage.

**Key Methods:**

- `fetch_and_store(self, ticker: str, ...)`: The primary method for acquiring data. It first checks the local DuckDB cache for recent data. If the data is stale or not present, it fetches it from yfinance, standardizes the format, and stores it in the database before returning a Polars DataFrame.
- `fetch_multiple(self, tickers: list[str], ...)`: A convenience method for fetching data for multiple tickers in a single call.
- `get_latest_price(self, ticker: str) -> float`: Quickly retrieves the most recent closing price for a given ticker, useful for real-time portfolio valuation.

---

### Technical Indicators

The `quant.indicators` module provides a library of over 15 common technical indicators, built for performance using Polars.

#### `quant.indicators.base.IndicatorBase`

This is an abstract base class that all indicators inherit from. It standardizes the API for calculating indicators.

- `calculate(self, df: pl.DataFrame) -> pl.DataFrame`: The core method that takes a DataFrame and returns it with the indicator column(s) added.
- `__call__(self, df: pl.DataFrame)`: Allows the indicator to be called like a function for a more fluent API (e.g., `SMA(20)(df)`).

#### Trend Indicators

- **`SMA(period: int, column: str)`**: Calculates the Simple Moving Average. Adds a column named `SMA_{period}`.
- **`EMA(period: int, column: str)`**: Calculates the Exponential Moving Average. Adds a column named `EMA_{period}`.
- **`MACD(fast: int, slow: int, signal: int)`**: Calculates the Moving Average Convergence Divergence. Adds `MACD`, `MACD_signal`, and `MACD_hist` columns.
- **`ADX(period: int)`**: Calculates the Average Directional Index. Adds `ADX`, `+DI`, and `-DI` columns to gauge trend strength.

#### Momentum Indicators

- **`RSI(period: int, column: str)`**: Calculates the Relative Strength Index. Adds an `RSI_{period}` column with values from 0 to 100.
- **`Stochastic(k_period: int, d_period: int)`**: Calculates the Stochastic Oscillator. Adds `stoch_k` and `stoch_d` columns.
- **`ROC(period: int)`**: Calculates the Rate of Change. Adds an `ROC_{period}` column.
- **`Williams_R(period: int)`**: Calculates Williams %R. Adds a `Williams_R` column.

#### Volatility Indicators

- **`BollingerBands(period: int, std_dev: float)`**: Calculates Bollinger Bands. Adds `BB_upper`, `BB_middle`, and `BB_lower` columns.
- **`ATR(period: int)`**: Calculates the Average True Range, a key measure of market volatility. Adds an `ATR` column.
- **`KeltnerChannel(period: int, multiplier: float)`**: Calculates Keltner Channels. Adds `KC_upper`, `KC_middle`, and `KC_lower` columns.

#### Volume Indicators

- **`OBV()`**: Calculates On-Balance Volume. Adds an `OBV` column.
- **`VWAP()`**: Calculates the Volume-Weighted Average Price. Adds a `VWAP` column.
- **`MFI(period: int)`**: Calculates the Money Flow Index. Adds an `MFI` column.

---

### Trading Strategies

The `quant.strategies` module contains the framework for creating and backtesting trading strategies.

#### `quant.strategies.base.Strategy`

An abstract base class that defines the interface for all trading strategies.

- `generate_signals(self, df: pl.DataFrame) -> pl.DataFrame`: The core method where the strategy's logic resides. It must return a DataFrame with a `signal` column containing `1` for BUY, `-1` for SELL, and `0` for HOLD.
- `calculate_position_size(...)`: A method to determine the size of a position based on available capital and risk parameters.

#### Built-in Strategies

- **`MomentumStrategy()`**: A strategy that aims to capitalize on the continuation of existing trends. It uses a combination of RSI to identify entry points in an established trend (defined by a moving average crossover).
- **`MeanReversionStrategy()`**: This strategy is based on the principle that prices tend to revert to their historical mean. It uses Bollinger Bands to identify overbought and oversold conditions, buying near the lower band and selling near the upper band.
- **`BreakoutStrategy()`**: This strategy looks for strong price movements that "break out" of a defined support or resistance level, often confirmed by a surge in volume. It aims to capture the start of a new trend.

---

### Backtesting

The `quant.backtesting` module provides the tools to simulate trading strategies on historical data and evaluate their performance.

#### `quant.backtesting.engine.BacktestEngine`

This is the core of the backtesting framework. It takes a strategy and historical data, simulates trades, and generates a detailed performance report.

- `__init__(self, strategy: Strategy, ...)`: Initializes the engine with a strategy object, initial capital, and commission settings.
- `run(self, df: pl.DataFrame, ticker: str) -> BacktestResult`: Executes the backtest. It iterates through the historical data, processes signals generated by the strategy, simulates trades, and tracks the portfolio's equity over time.

#### `quant.backtesting.metrics.BacktestResult`

This dataclass is a container for all the results of a backtest run. It provides a comprehensive overview of the strategy's performance.

**Key Attributes:**

- `total_return_pct`: The total return of the strategy as a percentage.
- `sharpe_ratio`: The risk-adjusted return.
- `max_drawdown_pct`: The largest peak-to-trough decline in portfolio value.
- `win_rate`: The percentage of trades that were profitable.
- `trades`: A list of all trades executed during the backtest.
- `equity_curve`: A Polars DataFrame showing the portfolio's value over time.

---

### Portfolio Management

The `quant.portfolio` module provides tools for managing a collection of assets, optimizing allocations, and rebalancing.

#### `quant.portfolio.portfolio.Portfolio`

This class is used to track a multi-asset portfolio. It manages holdings, cash, and transaction history.

- `buy(self, ticker: str, ...)` and `sell(self, ticker: str, ...)`: Methods to execute trades and update the portfolio's state.
- `update_prices(self, prices: Dict[str, float])`: Updates the current market value of all holdings.
- `total_value`, `total_pnl`, `total_return_pct`: Properties to get real-time performance metrics.

#### `quant.portfolio.optimizer.PortfolioOptimizer`

This class implements Modern Portfolio Theory (MPT) to find optimal asset allocations.

- `maximize_sharpe()`: Finds the portfolio allocation with the highest risk-adjusted return.
- `minimize_volatility()`: Finds the portfolio with the lowest expected volatility.
- `efficient_frontier()`: Calculates the set of optimal portfolios that offer the highest expected return for a given level of risk.

#### `quant.portfolio.rebalancer.Rebalancer`

This class provides logic for rebalancing a portfolio to match target allocations.

- `calculate_trades(self, target_weights: Dict, ...)`: Determines the trades needed to move the current portfolio to the desired target weights.
- `execute_rebalance(self, ...)`: Executes the trades to rebalance the portfolio.

---

### Risk Management

The `quant.risk` module provides a suite of tools for measuring and managing portfolio and strategy risk.

#### `quant.risk.metrics.RiskMetrics`

This class provides a collection of static methods for calculating common risk and performance metrics.

- `sharpe_ratio(...)`, `sortino_ratio(...)`, `calmar_ratio(...)`: Calculate various risk-adjusted return metrics.
- `max_drawdown(...)`: Calculates the largest peak-to-trough decline in an equity curve.
- `beta(...)`, `alpha(...)`: Measure a strategy's performance relative to a benchmark.

#### `quant.risk.var.VaRCalculator`

This class is dedicated to calculating Value at Risk (VaR) and Conditional Value at Risk (CVaR), key measures of downside risk.

- `historical_var(...)`: Calculates VaR based on the direct historical distribution of returns.
- `parametric_var(...)`: A parametric approach that assumes returns are normally distributed.
- `monte_carlo_var(...)`: A simulation-based approach to estimate VaR.
- `historical_cvar(...)`, `parametric_cvar(...)`: Calculate Conditional VaR (or Expected Shortfall), which measures the expected loss given that the VaR has been exceeded.

---

## State Management

### `quant.state.State`

Reflex application state managing all UI interactions.

**Key State Variables:**

- `ticker: str` - Current ticker symbol
- `data: list[dict]` - Stock data
- `is_loading: bool` - Loading state
- `backtest_running: bool` - Backtest execution state
- `backtest_results: dict` - Backtest metrics
- `backtest_trades: list[dict]` - Trade history
- `portfolio_holdings: list[dict]` - Current positions
- `portfolio_value: float` - Total portfolio value

**Key Methods:**

```python
def fetch_data(self)
```
Fetch stock data for current ticker.

```python
def run_backtest(self)
```
Execute backtest with selected strategy.

```python
def add_portfolio_position(self)
```
Add new position to portfolio.

---

## Utility Modules

### `quant.utils.logger`

Logging configuration.

```python
def get_logger(name: str) -> logging.Logger
```
Get a configured logger instance.

### `quant.config`

Application configuration from environment variables.

```python
class Config:
    APP_ENV: str
    LOG_LEVEL: str
    DB_PATH: str
    # ... other config variables
```

---

## Error Handling

All modules implement comprehensive error handling:

- **ValueError**: Invalid input parameters
- **TypeError**: Type mismatches
- **Database Errors**: Connection and query failures
- **API Errors**: Data fetching failures

Errors are logged with full context and stack traces when LOG_LEVEL=DEBUG.

---

## Usage Examples

### Fetch and Store Data

```python
from quant.data import DataManager, Database

db = Database()
dm = DataManager(db)
df = dm.fetch_and_store("AAPL", period="1y")
```

### Calculate Indicators

```python
from quant.indicators import SMA, RSI, BollingerBands

df = SMA(20)(df)
df = RSI(14)(df)
df = BollingerBands(20, 2)(df)
```

### Run Backtest

```python
from quant.strategies import MomentumStrategy
from quant.backtesting import BacktestEngine

strategy = MomentumStrategy()
engine = BacktestEngine(strategy, initial_capital=100000)
result = engine.run(df, "AAPL")

print(f"Return: {result.total_return_pct:.2f}%")
print(f"Sharpe: {result.sharpe_ratio:.2f}")
print(f"Trades: {result.num_trades}")
```

### Calculate Risk Metrics

```python
from quant.risk import RiskMetrics, VaRCalculator

returns = df["close"].pct_change()
sharpe = RiskMetrics.sharpe_ratio(returns)
var_95 = VaRCalculator.historical_var(returns, 0.95)
cvar_95 = VaRCalculator.conditional_var(returns, 0.95)
```

---

## Performance Considerations

- **Data Caching**: Data is cached in DuckDB to minimize API calls
- **Lazy Loading**: UI components load data on demand
- **Polars**: High-performance dataframe operations
- **DuckDB**: Fast analytical queries with columnar storage
- **Async Support**: Ready for async operations (currently synchronous)

---

## Security Notes

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Validate all user inputs before processing
- Sanitize data before database insertion (parameterized queries used)
- Log security events at appropriate levels

---

## Version Compatibility

- Python 3.13+
- Reflex 0.8.14+
- Polars 1.15.0+
- DuckDB 1.1.3+
- NumPy 1.24.0+
- SciPy 1.11.0+
