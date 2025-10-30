"""Main entry point for the Quant Dashboard application."""

import reflex as rx

from components.ui.theme import theme_config
from pages import backtest, index, portfolio, risk, strategy

# Create and run the app with modern theme
app = rx.App(theme=theme_config)

# Add pages
app.add_page(index.index, route="/", title="Dashboard - Quant Platform")
app.add_page(backtest.backtest, route="/backtest", title="Backtesting - Quant Platform")
app.add_page(portfolio.portfolio, route="/portfolio", title="Portfolio - Quant Platform")
app.add_page(risk.risk, route="/risk", title="Risk Analysis - Quant Platform")
app.add_page(strategy.strategy, route="/strategy", title="Strategy Builder - Quant Platform")
