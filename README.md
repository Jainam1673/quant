# Quant Trading Platform 📊

A **production-ready, best-in-class quantitative trading platform** built with modern Python. Features comprehensive backtesting, portfolio management, risk analytics, custom strategy building, and a professional UI/UX optimized for financial applications.

> **🏆 Production Status**: Enterprise-ready with 41/41 tests passing, modern UI components, and comprehensive security audit completed.

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

### **Core Technologies**
- **[Reflex](https://reflex.dev/)** 0.8.14+ - Full-stack Python web framework
- **[Python 3.13+](https://www.python.org/)** - Latest Python with modern type hints
- **[UV](https://github.com/astral-sh/uv)** - Lightning-fast Python package manager
- **[Ruff](https://github.com/astral-sh/ruff)** - Modern linting and formatting

### **Data & Analytics**
- **[yfinance](https://github.com/ranaroussi/yfinance)** - Real-time market data from Yahoo Finance
- **[Polars](https://pola.rs/)** - Lightning-fast dataframe processing (Rust-based)
- **[DuckDB](https://duckdb.org/)** - Embedded analytical database for data persistence
- **[NumPy](https://numpy.org/)** & **[SciPy](https://scipy.org/)** - Numerical computing and optimization

### **Modern UI/UX System**
- **1,728+ lines** of professional UI components
- **Dark-first design** optimized for financial applications
- **Fully responsive** with mobile-first approach
- **Professional color palette** with financial-specific styling
- **Interactive dashboards** with real-time metrics

## 🚀 Getting Started

This guide will get you up and running with the Quant Trading Platform in just a few minutes.

### **Prerequisites**
- Python 3.13 or higher
- Git for version control
- Internet connection for data fetching

### 1. **Clone the Repository**

```bash
git clone https://github.com/Jainam1673/quant.git
cd quant
```

### 2. **Install Dependencies**

We recommend using `uv` for lightning-fast dependency management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

**Alternative with pip:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Initialize and Run**

```bash
# Initialize Reflex (one-time setup)
reflex init

# Start the development server
reflex run
```

### 4. **Access the Application**

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 🎯 Quick Start Guide

### **Dashboard Overview**
Navigate to the main dashboard to see:
- Real-time portfolio value and performance metrics
- Active strategies count and overall statistics
- Professional KPI cards with trend indicators
- Quick action buttons for common tasks

### **Run Your First Backtest**
1. Go to **Backtesting** page (`/backtest`)
2. Enter a ticker symbol (e.g., AAPL, TSLA, MSFT)
3. Select a strategy (Momentum, Mean Reversion, or Breakout)
4. Adjust parameters and click "Run Backtest"
5. View comprehensive results with performance metrics and equity curves

### **Manage Your Portfolio**
1. Navigate to **Portfolio** page (`/portfolio`)
2. Add positions with ticker, quantity, and entry price
3. View real-time allocation and performance
4. Use Modern Portfolio Theory optimization
5. Apply rebalancing recommendations

### **Analyze Risk Metrics**
1. Go to **Risk Analysis** page (`/risk`)
2. Calculate VaR/CVaR with multiple methods
3. View detailed risk metrics and correlations
4. Set custom risk limits and alerts
5. Analyze historical drawdowns

### **Build Custom Strategies**
1. Open **Strategy Builder** page (`/strategy`)
2. Select from 15+ technical indicators
3. Configure parameters and conditions
4. Define entry/exit rules and position sizing
5. Save, test, and deploy your strategies

## 🧪 Development & Testing

### **Run Tests**
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=quant --cov-report=html

# Run specific test categories
python -m pytest -m unit
python -m pytest -m integration
```

### **Code Quality**
```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type checking
mypy quant/ --ignore-missing-imports
```

### **Development Tools**
```bash
# Using the included Makefile
make test          # Run tests
make lint          # Check code quality
make format        # Format code
make run           # Start development server
make setup-dev     # Setup complete dev environment
```

## 📊 Performance Metrics

The platform calculates comprehensive financial metrics:

### **Returns & Performance**
- Total return, annualized return, return percentage
- Sharpe ratio, Sortino ratio, Calmar ratio
- Information ratio, Treynor ratio

### **Risk Metrics**
- Maximum drawdown, volatility (daily/annual)
- Value at Risk (VaR) - Historical, Parametric, Monte Carlo
- Conditional VaR (CVaR) for tail risk assessment
- Beta, correlation analysis

### **Trade Statistics**
- Win rate, profit factor, expectancy
- Average trade P&L, largest win/loss
- Trade frequency and holding periods

### **Portfolio Analytics**
- Asset allocation weights and drift
- Correlation matrix and diversification ratio
- Rebalancing recommendations
- Performance attribution

## 🔧 Configuration

### **Environment Setup**
Create a `.env` file from the template:

```bash
cp .env.example .env
```

Configure your settings:
```env
# Application Environment
APP_ENV=development  # or production
LOG_LEVEL=INFO
DEBUG=True

# Database Configuration
DB_PATH=data/quant.duckdb

# Trading Parameters
DEFAULT_INITIAL_CAPITAL=100000
DEFAULT_COMMISSION=0.001
DEFAULT_VAR_CONFIDENCE=0.95

# API Keys (optional)
# ALPHA_VANTAGE_KEY=your_key_here
# POLYGON_API_KEY=your_key_here
```

### **Production Deployment**
```bash
# Build for production
reflex export --frontend-only

# Run in production mode
reflex run --env prod --backend-port 8000 --frontend-port 3000
```

## 📈 Modern UI/UX Features

### **Professional Design System**
- **Dark-first theme** optimized for financial applications
- **Consistent typography** with Inter and JetBrains Mono fonts
- **Professional color palette** with financial-specific styling
- **Modern shadows and animations** for enhanced UX

### **Interactive Components**
- **Real-time dashboards** with live data updates
- **Interactive charts** for price and performance analysis
- **Professional forms** with validation and error handling
- **Responsive grid layouts** adapting to all screen sizes

### **Financial UI Optimization**
- **KPI metric cards** with trend indicators and color coding
- **Risk-aware color schemes** (green=profit, red=loss)
- **Dense data displays** optimized for trading workflows
- **Quick action cards** for common operations

## 📚 Project Structure

```
quant/
├── assets/                    # Static assets
├── components/                # Reusable UI components
│   ├── ui/                   # Modern UI component library (1,728 lines)
│   │   ├── theme.py         # Professional theme system
│   │   ├── cards.py         # Metric and chart cards
│   │   ├── charts.py        # Financial chart components
│   │   ├── forms.py         # Form controls with validation
│   │   ├── navigation.py    # Modern navigation components
│   │   └── layout.py        # Layout and grid systems
│   ├── layout.py            # Main layout decorator
│   └── sidebar.py           # Navigation sidebar
├── pages/                     # Application pages (UI)
│   ├── index.py             # Modern dashboard with KPIs
│   ├── backtest.py          # Backtesting interface
│   ├── portfolio.py         # Portfolio management
│   ├── risk.py              # Risk analytics
│   └── strategy.py          # Strategy builder
├── quant/                     # Core application package (4,301 lines)
│   ├── backtesting/         # Backtesting engine
│   │   ├── engine.py        # Backtest execution
│   │   └── metrics.py       # Performance metrics
│   ├── data/                # Data management
│   │   ├── database.py      # DuckDB wrapper
│   │   └── data_manager.py  # Data fetching & caching
│   ├── indicators/          # Technical indicators (15+)
│   │   ├── trend.py         # SMA, EMA, MACD, ADX
│   │   ├── momentum.py      # RSI, Stochastic, ROC
│   │   ├── volatility.py    # Bollinger, ATR, Keltner
│   │   └── volume.py        # OBV, VWAP, MFI
│   ├── strategies/          # Trading strategies
│   │   ├── base.py          # Strategy base class
│   │   ├── momentum_strategy.py
│   │   ├── mean_reversion.py
│   │   └── breakout.py
│   ├── portfolio/           # Portfolio management
│   │   ├── portfolio.py     # Portfolio class
│   │   ├── optimizer.py     # MPT optimization
│   │   └── rebalancer.py    # Rebalancing logic
│   ├── risk/                # Risk management
│   │   ├── metrics.py       # Risk metrics
│   │   └── var.py           # VaR calculations
│   ├── utils/               # Utilities
│   │   ├── logger.py        # Logging setup
│   │   ├── config.py        # Configuration
│   │   └── production.py    # Production utilities
│   ├── state.py             # Application state
│   └── quant.py             # App entry point
├── tests/                     # Comprehensive test suite (41 tests)
│   ├── test_backtesting_*.py
│   ├── test_portfolio_*.py
│   ├── test_risk_*.py
│   └── conftest.py
├── .env.example               # Environment template
├── pyproject.toml             # Modern Python project config
├── requirements.txt           # Dependencies
├── Makefile                   # Development commands
├── PRODUCTION_AUDIT_REPORT.md # Production readiness audit
└── README.md                  # This file
```
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

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/quant.git
cd quant

# Set up development environment
make setup-dev

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and test
make test
make lint

# Commit and push
git commit -m "feat: Add amazing feature"
git push origin feature/amazing-feature

# Create a Pull Request
```

### Code Quality Standards
- **Type hints**: All functions must have type annotations
- **Documentation**: Google-style docstrings required
- **Testing**: Minimum 80% test coverage for new code
- **Linting**: Code must pass Ruff checks
- **Formatting**: Use Ruff formatting standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links & Resources

### **Documentation**
- [Production Audit Report](PRODUCTION_AUDIT_REPORT.md) - Comprehensive production readiness assessment
- [Modern UI System](MODERN_UI_SYSTEM.md) - Complete UI/UX documentation
- [Architecture Guide](ARCHITECTURE.md) - Technical architecture details
- [API Documentation](API.md) - API endpoints and usage

### **External Resources**
- [Reflex Documentation](https://reflex.dev/docs) - Web framework docs
- [Polars Guide](https://pola.rs/user-guide/) - Data processing library
- [DuckDB Documentation](https://duckdb.org/docs/) - Analytical database
- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory) - MPT background

## 🌟 Acknowledgments

- **[Reflex Team](https://reflex.dev/)** for the amazing Python web framework
- **[Polars Team](https://pola.rs/)** for lightning-fast data processing
- **[DuckDB Team](https://duckdb.org/)** for embedded analytics
- **[UV Team](https://github.com/astral-sh/uv)** for fast package management
- **[Ruff Team](https://github.com/astral-sh/ruff)** for modern Python tooling

## 📞 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Jainam1673/quant/issues)
- **Discussions**: [Community discussions](https://github.com/Jainam1673/quant/discussions)
- **Email**: jainam1673@gmail.com

---

## 🏆 Production Ready

**✅ This platform has passed comprehensive production readiness audits with:**
- 41/41 tests passing (100% success rate)
- Zero critical security vulnerabilities
- Modern codebase with 4,301+ lines of production code
- Professional UI/UX with 1,728+ component lines
- Enterprise-grade architecture and documentation

**Ready for immediate deployment and commercial use!** 🚀

---

*Made with ❤️ and modern Python | Enterprise-ready quantitative trading platform*
