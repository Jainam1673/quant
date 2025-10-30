# Project Structure

This document explains the organization of the Quant Dashboard codebase.

## Directory Layout

```
quant/
├── .github/                 # GitHub-specific files
│   └── ISSUE_TEMPLATE/     # Issue templates for bugs/features
├── assets/                  # Static assets
│   └── favicon.ico         # App favicon
├── components/              # Reusable UI components
│   ├── layout.py           # Main layout wrapper with sidebar
│   └── sidebar.py          # Navigation sidebar component
├── pages/                   # Application pages
│   └── index.py            # Stock overview page (main page)
├── quant/                   # Main application package
│   ├── __init__.py         # Package initialization
│   ├── quant.py            # Application entry point and config
│   ├── state.py            # Application state management
│   ├── components/         # Component package marker
│   └── pages/              # Pages package marker
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── SECURITY.md             # Security policy
├── requirements.txt        # Python dependencies
└── rxconfig.py             # Reflex configuration
```

## Key Files

### `rxconfig.py`
Reflex configuration file that defines:
- App name
- Enabled plugins (Sitemap, TailwindV4)

### `quant/quant.py`
Main application entry point that:
- Creates the Reflex app instance
- Configures the theme (dark mode, colors)
- Registers pages

### `quant/state.py`
Application state management:
- `State` class managing ticker symbol, data, loading state
- `fetch_data()` method to retrieve stock data from yfinance
- Data processing with Polars

### `pages/index.py`
Main stock overview page with:
- Ticker input field
- Fetch data button
- Area chart visualization
- Data table display

### `components/layout.py`
Main layout wrapper that:
- Applies sidebar to all pages
- Handles content spacing

### `components/sidebar.py`
Navigation sidebar with:
- App branding
- Navigation links
- Fixed positioning

## Data Flow

The application follows a clear, reactive data flow from user input to UI updates:

1.  **User Interaction**: A user interacts with a UI element, such as entering a ticker in an input field or clicking a button.
2.  **State Update**: The event triggers a method in the `quant.state.State` class. For example, `State.set_ticker` updates the `ticker` variable.
3.  **Backend Logic**: If the event requires backend processing (e.g., `State.fetch_data`), the state method calls the relevant backend modules.
    - The `DataManager` fetches data, either from the `Database` cache or from the `yfinance` API.
    - The data is processed and transformed into a Polars DataFrame.
4.  **State Synchronization**: The results are stored back in the `State` variables (e.g., `self.data`, `self.chart_data`).
5.  **UI Reactivity**: The Reflex framework automatically detects the state change and re-renders only the affected UI components, ensuring a fast and efficient update.

## Tech Stack Details

-   **[Reflex](https://reflex.dev/)**: A full-stack Python framework that transpiles the frontend to React and uses a FastAPI backend. It enables building interactive web apps purely in Python.
-   **[yfinance](https://github.com/ranaroussi/yfinance)**: The primary source for real-time and historical market data from Yahoo Finance.
-   **[Polars](https://pola.rs/)**: A high-performance, Rust-based DataFrame library used for all data manipulation. It is significantly faster than pandas for many operations.
-   **[DuckDB](https://duckdb.org/)**: An embedded analytical database used for caching and persisting historical data, backtest results, and trades. Its columnar storage is ideal for financial analysis.
-   **[SciPy](https://scipy.org/)**: Used for numerical optimization, particularly in the portfolio optimizer.

## Code Style and Conventions

-   **Type Hinting**: All functions and methods should have clear type hints for all arguments and return values.
-   **Docstrings**: All public modules, classes, and functions should have a docstring explaining their purpose, arguments, and return values.
-   **Formatting**: Code is formatted using `black` with a line length of 100.
-   **Naming**: 
    - Classes: `PascalCase` (e.g., `BacktestEngine`).
    - Functions and variables: `snake_case` (e.g., `fetch_data`).
    - Constants: `UPPER_SNAKE_CASE` (e.g., `INITIAL_CAPITAL`).

## Development Workflow

1. **Install dependencies**: `uv pip install -r requirements.txt`
2. **Initialize Reflex**: `reflex init` (first time only)
3. **Run dev server**: `reflex run`
4. **Make changes**: Files auto-reload
5. **Build for production**: `reflex export`

## Adding New Features

### New Page
1. Create file in `pages/` directory
2. Import `main_layout` decorator
3. Create page component
4. Register in `quant/quant.py`

### New Component
1. Create file in `components/` directory
2. Define component function
3. Import and use in pages

### New State Variable
1. Add property to `State` class in `quant/state.py`
2. Create setter methods if needed
3. Use in page components

## Future Enhancements

Planned features (see README roadmap):
- Technical indicators
- Multiple stock comparison
- DuckDB integration
- Portfolio tracking
- Real-time updates
