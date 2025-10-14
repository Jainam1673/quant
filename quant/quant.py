"""Main entry point for the Quant Dashboard application."""

import reflex as rx
from pages import index, backtest

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
app.add_page(index.index, route="/")
app.add_page(backtest.backtest, route="/backtest")