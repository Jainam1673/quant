"""Main entry point for the Quant Dashboard application."""

import reflex as rx
from pages import index, backtest, portfolio, risk, strategy

# Create and run the app
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        gray_color="sand",
        radius="large",
    )
)

# Add pages
app.add_page(index.index, route="/", title="Dashboard - Quant Platform")
app.add_page(backtest.backtest, route="/backtest", title="Backtesting - Quant Platform")
app.add_page(portfolio.portfolio, route="/portfolio", title="Portfolio - Quant Platform")
app.add_page(risk.risk, route="/risk", title="Risk Analysis - Quant Platform")
app.add_page(strategy.strategy, route="/strategy", title="Strategy Builder - Quant Platform")