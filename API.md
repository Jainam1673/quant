# API Documentation

## Overview

This document provides comprehensive documentation for the Quant Trading Platform's internal APIs and modules.

## Core Modules

### Data Management

#### `quant.data.database.Database`

DuckDB database wrapper for persistent storage.

**Methods:**

```python
def __init__(self, db_path: str = "data/quant.duckdb")
```
Initialize database connection and create schema.

```python
def insert_ohlcv(self, df: pl.DataFrame)
```
Insert OHLCV data into database.
- **Parameters**: `df` - Polars DataFrame with columns: ticker, timestamp, open, high, low, close, volume

```python
def get_ohlcv(self, ticker: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pl.DataFrame
```
Retrieve OHLCV data for a ticker.
- **Parameters**:
  - `ticker`: Stock ticker symbol
  - `start_date`: Start date (YYYY-MM-DD format)
  - `end_date`: End date (YYYY-MM-DD format)
- **Returns**: Polars DataFrame with OHLCV data

```python
def get_multiple_tickers(self, tickers: list[str], start_date: Optional[str] = None, end_date: Optional[str] = None) -> pl.DataFrame
```
Retrieve OHLCV data for multiple tickers.

```python
def save_backtest_run(self, run_data: dict)
```
Save backtest run results.

```python
def get_backtest_runs(self, limit: int = 100) -> pl.DataFrame
```
Get recent backtest runs.

#### `quant.data.data_manager.DataManager`

Manages data fetching, caching, and storage.

**Methods:**

```python
def __init__(self, db: Optional[Database] = None)
```
Initialize data manager with optional database instance.

```python
def fetch_and_store(self, ticker: str, period: str = "1y", interval: str = "1d", force_update: bool = False) -> pl.DataFrame
```
Fetch data from yfinance and store in database.
- **Parameters**:
  - `ticker`: Stock ticker symbol
  - `period`: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
  - `interval`: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
  - `force_update`: Force fetching new data even if cached
- **Returns**: Polars DataFrame with OHLCV data
- **Raises**: `ValueError` if ticker is invalid or no data is found

```python
def fetch_multiple(self, tickers: list[str], period: str = "1y", interval: str = "1d") -> pl.DataFrame
```
Fetch data for multiple tickers.

```python
def get_latest_price(self, ticker: str) -> float
```
Get the most recent close price for a ticker.

---

### Technical Indicators

#### `quant.indicators.base.IndicatorBase`

Abstract base class for all technical indicators.

**Methods:**

```python
def __init__(self, name: str)
```
Initialize indicator with a name.

```python
@abstractmethod
def calculate(self, df: pl.DataFrame) -> pl.DataFrame
```
Calculate indicator values. Must be implemented by subclasses.

```python
def __call__(self, df: pl.DataFrame) -> pl.DataFrame
```
Allow calling indicator as a function.

#### Trend Indicators

**`SMA(period: int = 20, column: str = "close")`**
- Simple Moving Average
- Adds column: `SMA_{period}`

**`EMA(period: int = 20, column: str = "close")`**
- Exponential Moving Average
- Adds column: `EMA_{period}`

**`MACD(fast: int = 12, slow: int = 26, signal: int = 9)`**
- Moving Average Convergence Divergence
- Adds columns: `MACD`, `MACD_signal`, `MACD_hist`

**`ADX(period: int = 14)`**
- Average Directional Index
- Adds columns: `ADX`, `+DI`, `-DI`

#### Momentum Indicators

**`RSI(period: int = 14, column: str = "close")`**
- Relative Strength Index
- Adds column: `RSI_{period}`
- Values range from 0 to 100

**`Stochastic(k_period: int = 14, d_period: int = 3)`**
- Stochastic Oscillator
- Adds columns: `stoch_k`, `stoch_d`

**`ROC(period: int = 12)`**
- Rate of Change
- Adds column: `ROC_{period}`

**`Williams_R(period: int = 14)`**
- Williams %R
- Adds column: `Williams_R`

#### Volatility Indicators

**`BollingerBands(period: int = 20, std_dev: float = 2.0)`**
- Bollinger Bands
- Adds columns: `BB_upper`, `BB_middle`, `BB_lower`

**`ATR(period: int = 14)`**
- Average True Range
- Adds column: `ATR`

**`KeltnerChannel(period: int = 20, multiplier: float = 2.0)`**
- Keltner Channel
- Adds columns: `KC_upper`, `KC_middle`, `KC_lower`

#### Volume Indicators

**`OBV()`**
- On-Balance Volume
- Adds column: `OBV`

**`VWAP()`**
- Volume Weighted Average Price
- Adds column: `VWAP`

**`MFI(period: int = 14)`**
- Money Flow Index
- Adds column: `MFI`

---

### Trading Strategies

#### `quant.strategies.base.Strategy`

Abstract base class for trading strategies.

**Classes:**

```python
class Signal(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0
```

```python
@dataclass
class Position:
    ticker: str
    quantity: float
    entry_price: float
    entry_date: str
    side: str  # 'long' or 'short'
    
    def pnl(self, current_price: float) -> float
    def pnl_percent(self, current_price: float) -> float
```

**Methods:**

```python
def __init__(self, name: str)
```
Initialize strategy with a name.

```python
@abstractmethod
def generate_signals(self, df: pl.DataFrame) -> pl.DataFrame
```
Generate trading signals. Must return DataFrame with 'signal' column (1=BUY, -1=SELL, 0=HOLD).

```python
@abstractmethod
def calculate_position_size(self, df: pl.DataFrame, capital: float, current_price: float) -> float
```
Calculate position size for a trade.

#### Built-in Strategies

**`MomentumStrategy()`**
- Uses RSI and MA crossovers
- Buys on RSI < 30 and fast MA > slow MA
- Sells on RSI > 70

**`MeanReversionStrategy()`**
- Uses Bollinger Bands
- Buys when price touches lower band
- Sells when price touches upper band

**`BreakoutStrategy()`**
- Uses support/resistance levels
- Buys on breakout above resistance with volume confirmation
- Sells on breakdown below support

---

### Backtesting

#### `quant.backtesting.engine.BacktestEngine`

Main backtesting engine.

**Methods:**

```python
def __init__(self, strategy: Strategy, initial_capital: float = 100000, commission: float = 0.001, db: Optional[Database] = None)
```
Initialize backtest engine.
- **Parameters**:
  - `strategy`: Trading strategy instance
  - `initial_capital`: Starting capital
  - `commission`: Commission per trade (default 0.1%)
  - `db`: Database instance for storing results

```python
def run(self, df: pl.DataFrame, ticker: str) -> BacktestResult
```
Run backtest on historical data.
- **Returns**: `BacktestResult` object with metrics and trades

#### `quant.backtesting.metrics.BacktestResult`

Results from a backtest run.

**Attributes:**
- `strategy_name: str`
- `initial_capital: float`
- `final_value: float`
- `total_return: float`
- `total_return_pct: float`
- `num_trades: int`
- `win_rate: float`
- `sharpe_ratio: float`
- `max_drawdown: float`
- `max_drawdown_pct: float`
- `trades: list[Trade]`
- `equity_curve: pl.DataFrame`

---

### Portfolio Management

#### `quant.portfolio.portfolio.Portfolio`

Portfolio management class.

**Methods:**

```python
def __init__(self, name: str, initial_capital: float)
```
Initialize portfolio.

```python
def add_position(self, ticker: str, quantity: float, price: float)
```
Add a new position to portfolio.

```python
def get_positions(self) -> list[dict]
```
Get all current positions.

```python
def get_value(self) -> float
```
Get total portfolio value.

#### `quant.portfolio.optimizer.PortfolioOptimizer`

Portfolio optimization using Modern Portfolio Theory.

**Methods:**

```python
def maximize_sharpe(self, returns: pl.DataFrame, risk_free_rate: float = 0.02) -> dict
```
Optimize for maximum Sharpe ratio.

```python
def minimize_volatility(self, returns: pl.DataFrame) -> dict
```
Optimize for minimum volatility.

```python
def risk_parity(self, returns: pl.DataFrame) -> dict
```
Optimize using risk parity approach.

---

### Risk Management

#### `quant.risk.metrics.RiskMetrics`

Calculate comprehensive risk metrics.

**Static Methods:**

```python
@staticmethod
def sharpe_ratio(returns: pl.Series, risk_free_rate: float = 0.02) -> float
```
Calculate Sharpe ratio.

```python
@staticmethod
def sortino_ratio(returns: pl.Series, risk_free_rate: float = 0.02) -> float
```
Calculate Sortino ratio (downside deviation).

```python
@staticmethod
def calmar_ratio(returns: pl.Series) -> float
```
Calculate Calmar ratio (return / max drawdown).

```python
@staticmethod
def max_drawdown(equity_curve: pl.Series) -> tuple[float, float]
```
Calculate maximum drawdown.
- **Returns**: (max_drawdown_amount, max_drawdown_pct)

#### `quant.risk.var.VaRCalculator`

Value at Risk calculations.

**Methods:**

```python
@staticmethod
def historical_var(returns: pl.Series, confidence_level: float = 0.95) -> float
```
Calculate VaR using historical method.

```python
@staticmethod
def parametric_var(returns: pl.Series, confidence_level: float = 0.95) -> float
```
Calculate VaR using parametric (variance-covariance) method.

```python
@staticmethod
def monte_carlo_var(returns: pl.Series, num_simulations: int = 10000, confidence_level: float = 0.95) -> float
```
Calculate VaR using Monte Carlo simulation.

```python
@staticmethod
def conditional_var(returns: pl.Series, confidence_level: float = 0.95) -> float
```
Calculate Conditional VaR (CVaR/Expected Shortfall).

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
