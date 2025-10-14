# Contributing to Quant Dashboard

Thank you for your interest in contributing to Quant Dashboard! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Enhancements

We welcome feature requests! Please create an issue with:
- A clear description of the feature
- Why this feature would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/quant.git
   cd quant
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   
   # Initialize Reflex
   reflex init
   ```

4. **Make Your Changes**
   - Write clear, readable code
   - Follow Python PEP 8 style guidelines
   - Add comments for complex logic
   - Update documentation if needed

5. **Test Your Changes**
   ```bash
   # Run the development server
   reflex run
   
   # Test your changes thoroughly
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```
   
   Use clear commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Refactor:` for code refactoring
   - `Docs:` for documentation changes

7. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub with a clear description.

## 📝 Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable names

Example:
```python
def fetch_stock_data(ticker: str, period: str = "1y") -> pl.DataFrame:
    """Fetch historical stock data for a given ticker.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL')
        period: The time period to fetch (default: '1y')
        
    Returns:
        A Polars DataFrame with stock data
    """
    # Implementation
    pass
```

## 🏗️ Project Structure

```
quant/
├── components/       # Reusable UI components
├── pages/           # Application pages
├── quant/           # Main application package
│   ├── state.py    # State management
│   └── quant.py    # App entry point
└── assets/          # Static assets
```

## 🧪 Testing

- Test all new features manually
- Ensure the app runs without errors
- Check for console warnings/errors
- Test on different screen sizes (responsive design)

## 📋 Areas for Contribution

### High Priority
- Technical indicators (RSI, MACD, Moving Averages)
- DuckDB integration for data persistence
- Multiple stock comparison charts
- Error handling improvements

### Medium Priority
- Export functionality (CSV, Excel)
- Watchlist feature
- Portfolio tracking
- More chart types

### Documentation
- Improve README
- Add inline code comments
- Create tutorial content
- API documentation

## 💡 Development Tips

1. **Hot Reload**: Reflex supports hot reload in development mode
2. **State Management**: Use Reflex's state management for reactive updates
3. **Components**: Create reusable components for common UI patterns
4. **Performance**: Consider data size when working with large datasets

## 🐛 Debugging

- Check browser console for frontend errors
- Check terminal for backend errors
- Use `print()` or logging for debugging state changes
- Review Reflex documentation for framework-specific issues

## 📧 Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in GitHub Discussions
- Reach out to maintainers

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others when possible
- Follow best practices

## 🙏 Thank You!

Every contribution, no matter how small, helps make Quant Dashboard better. We appreciate your time and effort!
