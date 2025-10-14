# Development Setup Guide

Quick start guide for developers who want to contribute to or run Quant Dashboard locally.

## Prerequisites

- **Python 3.11+** (Python 3.11, 3.12, or 3.13)
- **Git** for version control
- **uv** (recommended) or pip for package management

## Step-by-Step Setup

### 1. Install Python

Check your Python version:
```bash
python --version
# or
python3 --version
```

If you need to install Python 3.11+:
- **Ubuntu/Debian**: `sudo apt install python3.11`
- **macOS**: `brew install python@3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### 2. Install uv (Recommended)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 3. Clone the Repository

```bash
git clone https://github.com/yourusername/quant.git
cd quant
```

### 4. Set Up Virtual Environment

**Using uv (Recommended):**
```bash
# Create and activate virtual environment
uv venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

**Using pip:**
```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Initialize Reflex

First time setup:
```bash
reflex init
```

This will:
- Create `.web/` directory for frontend build
- Create `.states/` directory for state management
- Download and set up Node.js dependencies

### 6. Run the Development Server

```bash
reflex run
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### 7. Verify Everything Works

1. Open http://localhost:3000 in your browser
2. Enter a stock ticker (e.g., "AAPL")
3. Click "Fetch Data"
4. You should see a chart and data table

## Common Issues

### Port Already in Use

If port 3000 or 8000 is already in use:
```bash
# Find and kill the process
# Linux/macOS
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module Not Found Errors

Make sure you're in the virtual environment:
```bash
# Check if virtual environment is activated
which python  # Should show path to .venv/bin/python

# If not activated, activate it
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Reflex Command Not Found

Install Reflex directly:
```bash
uv pip install reflex
# or
pip install reflex
```

### yfinance Data Issues

If you get errors fetching stock data:
- Check your internet connection
- Try a different ticker symbol
- Yahoo Finance might be rate-limiting - wait a few minutes

## Development Workflow

### Making Changes

1. **Backend changes** (Python files):
   - Edit files in `quant/`, `pages/`, or `components/`
   - Reflex will auto-reload

2. **Frontend changes** (components):
   - Edit component files
   - Changes are hot-reloaded automatically

3. **State changes**:
   - Edit `quant/state.py`
   - Add new state variables or methods
   - Use in components

### Testing Changes

```bash
# Run in development mode
reflex run

# Check for Python errors in terminal
# Check for frontend errors in browser console (F12)
```

### Building for Production

```bash
# Export static frontend
reflex export --frontend-only

# Or run in production mode
reflex run --env prod
```

## Project Structure Overview

```
quant/
├── .venv/              # Virtual environment (git ignored)
├── .web/               # Frontend build (git ignored)
├── .states/            # State storage (git ignored)
├── assets/             # Static files
├── components/         # UI components
├── pages/              # App pages
├── quant/              # Main package
│   ├── quant.py       # App entry point
│   └── state.py       # State management
├── requirements.txt    # Dependencies
└── rxconfig.py        # Reflex config
```

## Useful Commands

```bash
# Start dev server
reflex run

# Initialize/reinitialize project
reflex init

# Export for deployment
reflex export

# Check Reflex version
reflex --version

# Install new package
uv pip install <package>
# or
pip install <package>

# Update requirements.txt
uv pip freeze > requirements.txt
# or
pip freeze > requirements.txt
```

## IDE Setup

### VS Code (Recommended)

1. Install Python extension
2. Select Python interpreter from `.venv/`
3. Enable formatters: Black, isort
4. Install Pylance for type checking

### PyCharm

1. Open project folder
2. File → Settings → Project → Python Interpreter
3. Add interpreter from `.venv/`
4. Enable Python optimizations

## Environment Variables

Create `.env` file for secrets (never commit this):
```bash
# Example .env
# API_KEY=your_api_key_here
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
```

## Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for code structure
- Review [README.md](README.md) for feature roadmap
- Join discussions in GitHub Issues

## Getting Help

- Check [Reflex Documentation](https://reflex.dev/docs)
- Open an issue on GitHub
- Read existing issues and discussions

Happy coding! 🚀
