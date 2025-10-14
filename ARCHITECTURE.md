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

1. User enters ticker symbol in input field
2. `State.set_ticker()` updates state
3. User clicks "Fetch Data" button
4. `State.fetch_data()` is called:
   - Downloads data from yfinance
   - Processes data with Polars
   - Updates state with chart and table data
5. UI reactively updates to show:
   - Area chart with closing prices
   - Data table with all metrics

## Tech Stack Details

- **Reflex**: Full-stack Python framework for web apps
  - Frontend: Compiled to React
  - Backend: Python FastAPI
  - State management: Reactive state system
  
- **yfinance**: Yahoo Finance API for stock data
  - Free market data
  - Historical price data
  - Company information

- **Polars**: Fast DataFrame library
  - Rust-based performance
  - Better than pandas for large datasets
  - Type-safe operations

- **DuckDB**: Embedded analytical database
  - Currently in requirements but not yet integrated
  - Future use for data caching/storage

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
