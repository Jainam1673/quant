# Quant Dashboard 📊

A modern, interactive stock market dashboard built with Python, featuring real-time stock data visualization and analysis capabilities.

## 🚀 Features

- **Real-time Stock Data**: Fetch and display historical stock data for any ticker symbol
- **Interactive Charts**: Beautiful area charts with customizable themes
- **Data Tables**: Comprehensive tabular view of stock metrics
- **Dark Mode UI**: Modern, eye-friendly dark theme interface
- **Responsive Design**: Sidebar navigation with clean layout

## 🛠️ Tech Stack

- **[Reflex](https://reflex.dev/)**: Full-stack Python web framework
- **[yfinance](https://github.com/ranaroussi/yfinance)**: Market data from Yahoo Finance
- **[Polars](https://pola.rs/)**: Fast dataframe library for data processing
- **[DuckDB](https://duckdb.org/)**: Embedded analytical database (ready for integration)
- **[uv](https://github.com/astral-sh/uv)**: Ultra-fast Python package installer

## 📋 Prerequisites

- Python 3.11 or higher
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
├── assets/              # Static assets (favicon, images)
├── components/          # Reusable UI components
│   ├── layout.py       # Main layout wrapper
│   └── sidebar.py      # Navigation sidebar
├── pages/              # Application pages
│   └── index.py        # Stock overview page
├── quant/              # Main application package
│   ├── __init__.py
│   ├── quant.py        # Application entry point
│   ├── state.py        # State management
│   ├── components/     # Package components
│   └── pages/          # Package pages
├── requirements.txt    # Python dependencies
├── rxconfig.py        # Reflex configuration
└── README.md          # This file
```

## 🎨 Features in Detail

### Stock Data Fetching
- Enter any valid stock ticker (e.g., AAPL, GOOGL, MSFT)
- Fetches 1 year of historical data
- Automatic data processing with Polars

### Interactive Visualization
- Area chart showing closing prices over time
- Responsive and interactive tooltips
- Customizable chart themes

### Data Table
- Displays all available metrics (Open, High, Low, Close, Volume)
- Scrollable table for large datasets
- Clean, readable formatting

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
