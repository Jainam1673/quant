# Quant Trading Platform 📊

A **production-ready, f## Installation

### Prerequisites

- Python 3.13 or higher
- Node.js 16+ (automatically installed by Reflex)stack quantitative trading platform** built with Python. Features comprehensive backtesting, portfolio management, risk analytics, and custom strategy building capabilities.

## 🌟 Key Features

### 📈 **Advanced Backtesting**
- Multi-strategy backtesting engine with realistic position tracking
- Comprehensive performance metrics (Sharpe, Sortino, Calmar ratios)
- Trade-by-trade analysis with P&L tracking
- Equity curve visualization
- Persistent storage of backtest runs

### 💼 **Portfolio Management**
- Real-time portfolio tracking and position management
- Modern Portfolio Theory (MPT) optimization
- Multiple optimization strategies: Maximum Sharpe, Minimum Volatility, Risk Parity
- Interactive allocation charts and rebalancing recommendations
- Portfolio performance analytics

### ⚠️ **Risk Analytics**
- Value at Risk (VaR) and Conditional VaR (CVaR) calculations
- Multiple VaR methods: Historical, Parametric, Monte Carlo
- Correlation matrix analysis
- Drawdown tracking and visualization
- Comprehensive risk metrics dashboard
- Customizable risk limits and alerts

### ⚙️ **Strategy Builder**
- Interactive custom strategy creation
- 15+ technical indicators across 4 categories (Trend, Momentum, Volatility, Volume)
- Visual indicator parameter configuration
- Entry/Exit condition builder
- Position sizing and risk management rules
- Strategy library with save/load functionality

### 📊 **Technical Indicators Library**
- **Trend**: SMA, EMA, MACD, ADX
- **Momentum**: RSI, Stochastic, ROC, Williams %R
- **Volatility**: Bollinger Bands, ATR, Keltner Channel
- **Volume**: OBV, VWAP, MFI
- All indicators with configurable parameters

## 🛠️ Tech Stack

- **[Reflex](https://reflex.dev/)** 0.8.14+ - Full-stack Python web framework
- **[yfinance](https://github.com/ranaroussi/yfinance)** - Real-time market data from Yahoo Finance
- **[Polars](https://pola.rs/)** - Lightning-fast dataframe processing (Rust-based)
- **[DuckDB](https://duckdb.org/)** - Embedded analytical database for data persistence
- **[NumPy](https://numpy.org/)** & **[SciPy](https://scipy.org/)** - Numerical computing and optimization
- **[Python 3.13+](https://www.python.org/)** - Modern Python with type hints

## 📋 Prerequisites

- Python 3.13 or higher
- uv (recommended) or pip

## 🔧 Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/quant.git
cd quant

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/quant.git
cd quant

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Development Mode

```bash
# Initialize Reflex (first time only)
reflex init

# Run the development server
reflex run
```

The application will be available at `http://localhost:3000`

### Production Deployment

```bash
# Build for production
reflex export --frontend-only

# Or deploy with backend
reflex run --env prod
```

## 📚 Project Structure

```
quant/
├── assets/              # Static assets
├── components/          # Reusable UI components
│   ├── layout.py       # Main layout decorator
│   └── sidebar.py      # Navigation sidebar
├── pages/              # Application pages (UI)
│   ├── index.py        # Dashboard/Home
│   ├── backtest.py     # Backtesting interface
│   ├── portfolio.py    # Portfolio management
│   ├── risk.py         # Risk analytics
│   └── strategy.py     # Strategy builder
├── quant/              # Core application package
│   ├── backtesting/    # Backtesting engine
│   │   ├── engine.py   # Backtest execution
│   │   └── metrics.py  # Performance metrics
│   ├── data/           # Data management
│   │   ├── database.py    # DuckDB wrapper
│   │   └── data_manager.py # Data fetching & caching
│   ├── indicators/     # Technical indicators
│   │   ├── trend.py    # SMA, EMA, MACD, ADX
│   │   ├── momentum.py # RSI, Stochastic, ROC
│   │   ├── volatility.py # Bollinger, ATR, Keltner
│   │   └── volume.py   # OBV, VWAP, MFI
│   ├── strategies/     # Trading strategies
│   │   ├── base.py     # Strategy base class
│   │   ├── momentum_strategy.py
│   │   ├── mean_reversion.py
│   │   └── breakout.py
│   ├── portfolio/      # Portfolio management
│   │   ├── portfolio.py # Portfolio class
│   │   ├── optimizer.py # MPT optimization
│   │   └── rebalancer.py # Rebalancing logic
│   ├── risk/           # Risk management
│   │   ├── metrics.py  # Risk metrics
│   │   └── var.py      # VaR calculations
│   ├── utils/          # Utilities
│   │   ├── logger.py   # Logging setup
│   │   └── config.py   # Configuration
│   ├── state.py        # Application state
│   └── quant.py        # App entry point
├── tests/              # Unit tests
│   ├── test_database.py
│   ├── test_indicators.py
│   └── conftest.py
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
├── rxconfig.py         # Reflex configuration
└── README.md           # This file
```

## � Quick Start Guide

### 1. **Dashboard Overview**
Navigate to the home page to see:
- Portfolio value and active strategies count
- Overall win rate and total trades
- Quick action cards to navigate features

### 2. **Run a Backtest**
1. Go to **Backtesting** page
2. Enter a ticker symbol (e.g., AAPL)
3. Select a strategy (Momentum, Mean Reversion, or Breakout)
4. Click "Run Backtest"
5. View performance metrics, equity curve, and trade history

### 3. **Manage Portfolio**
1. Go to **Portfolio** page
2. Add positions with ticker, quantity, and entry price
3. View current holdings and allocation
4. Optimize allocation using MPT methods
5. Apply rebalancing recommendations

### 4. **Analyze Risk**
1. Go to **Risk Analysis** page
2. Calculate VaR/CVaR with different methods
3. View detailed risk metrics
4. Analyze correlation matrix
5. Set risk limits and alerts

### 5. **Build Custom Strategy**
1. Go to **Strategy Builder** page
2. Name your strategy
3. Select technical indicators
4. Configure indicator parameters
5. Define entry/exit conditions
6. Set position sizing and risk rules
7. Save and test your strategy

## 🧪 Testing

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=quant --cov-report=html

# Run specific test file
pytest tests/test_database.py

# Run tests by marker
pytest -m unit
pytest -m "not slow"
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Application
APP_ENV=development
LOG_LEVEL=INFO

# Database
DB_PATH=data/quant.duckdb

# API Keys (if needed)
# ALPHA_VANTAGE_KEY=your_key_here
```

## 📊 Performance Metrics

The platform calculates comprehensive metrics:

- **Returns**: Total return, annualized return, return percentage
- **Risk-Adjusted**: Sharpe ratio, Sortino ratio, Calmar ratio
- **Risk**: Max drawdown, volatility, VaR, CVaR
- **Trade Statistics**: Win rate, profit factor, average trade P&L
- **Portfolio**: Weights, correlation, diversification ratio

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap

- [ ] Technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Multiple stock comparison
- [ ] DuckDB integration for historical data storage
- [ ] Portfolio tracking
- [ ] Export data to CSV/Excel
- [ ] Real-time price updates
- [ ] Watchlist functionality

## 🐛 Known Issues

- None at the moment! Please report any issues you find.

## 📧 Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/yourusername/quant](https://github.com/yourusername/quant)

## 🙏 Acknowledgments

- [Reflex](https://reflex.dev/) for the amazing Python web framework
- [yfinance](https://github.com/ranaroussi/yfinance) for free market data
- [Polars](https://pola.rs/) for fast data processing
- All contributors and users of this project

---

Made with ❤️ and Python
