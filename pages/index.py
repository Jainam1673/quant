"""The main dashboard page."""

import reflex as rx
from quant.state import State

# Theming for the charts
chart_theme = {
    "grid": {"stroke": "#4A4A4A"},
    "text": {"fill": "#FFFFFF"},
}


from components.layout import main_layout


@main_layout
def index() -> rx.Component:
    """The main dashboard page."""
    return rx.vstack(
        # Welcome section
        rx.hstack(
            rx.vstack(
                rx.heading("Quantitative Trading Platform", size="9", weight="bold"),
                rx.text(
                    "Advanced analytics and backtesting for systematic trading strategies",
                    size="4",
                    color="gray",
                ),
                align="start",
                spacing="2",
            ),
            width="100%",
            margin_bottom="2rem",
        ),
        
        # Quick stats overview
        rx.heading("Market Overview", size="6", margin_bottom="1rem"),
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Active Strategies", size="2", color="gray"),
                    rx.heading(State.active_strategies_count, size="7", color="blue"),
                    rx.text("Running backtests", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Portfolio Value", size="2", color="gray"),
                    rx.heading(State.portfolio_value, size="7", color="green"),
                    rx.text("Total assets", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Win Rate", size="2", color="gray"),
                    rx.heading(State.overall_win_rate, size="7", color="purple"),
                    rx.text("Across all strategies", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Total Trades", size="2", color="gray"),
                    rx.heading(State.total_trades_count, size="7"),
                    rx.text("Historical executions", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            columns="4",
            spacing="4",
            width="100%",
            margin_bottom="2rem",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Quick actions
        rx.heading("Quick Actions", size="6", margin_bottom="1rem"),
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.icon("trending-up", size=48, color="blue"),
                    rx.heading("Backtest Strategy", size="5", margin_top="1rem"),
                    rx.text(
                        "Test your trading strategies against historical data",
                        size="2",
                        color="gray",
                        text_align="center",
                    ),
                    rx.button(
                        "Go to Backtesting",
                        on_click=rx.redirect("/backtest"),
                        size="3",
                        margin_top="1rem",
                    ),
                    align="center",
                    spacing="2",
                    padding="1rem",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.icon("pie-chart", size=48, color="green"),
                    rx.heading("Portfolio", size="5", margin_top="1rem"),
                    rx.text(
                        "Manage positions and optimize portfolio allocation",
                        size="2",
                        color="gray",
                        text_align="center",
                    ),
                    rx.button(
                        "View Portfolio",
                        on_click=rx.redirect("/portfolio"),
                        size="3",
                        margin_top="1rem",
                    ),
                    align="center",
                    spacing="2",
                    padding="1rem",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.icon("triangle-alert", size=48, color="red"),
                    rx.heading("Risk Analysis", size="5", margin_top="1rem"),
                    rx.text(
                        "Analyze VaR, correlations, and risk metrics",
                        size="2",
                        color="gray",
                        text_align="center",
                    ),
                    rx.button(
                        "Analyze Risk",
                        on_click=rx.redirect("/risk"),
                        size="3",
                        margin_top="1rem",
                    ),
                    align="center",
                    spacing="2",
                    padding="1rem",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.icon("sliders-horizontal", size=48, color="purple"),
                    rx.heading("Strategy Builder", size="5", margin_top="1rem"),
                    rx.text(
                        "Create custom strategies with technical indicators",
                        size="2",
                        color="gray",
                        text_align="center",
                    ),
                    rx.button(
                        "Build Strategy",
                        on_click=rx.redirect("/strategy"),
                        size="3",
                        margin_top="1rem",
                    ),
                    align="center",
                    spacing="2",
                    padding="1rem",
                )
            ),
            
            columns="4",
            spacing="4",
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Stock lookup section
        rx.heading("Stock Data Lookup", size="6", margin_bottom="1rem"),
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Enter a stock ticker (e.g., AAPL)",
                        value=State.ticker,
                        on_change=State.set_ticker,
                        size="3",
                        width="300px",
                    ),
                    rx.button(
                        "Fetch Data",
                        on_click=State.fetch_data,
                        loading=State.is_loading,
                        size="3",
                    ),
                    spacing="4",
                    align="center",
                ),
                width="100%",
            ),
            width="100%",
        ),
        
        rx.divider(margin_top="1rem", margin_bottom="1rem"),

        # Conditional rendering for chart and table
        rx.cond(
            State.is_loading,
            rx.center(rx.text("Loading...")),
            rx.vstack(
                # Chart
                rx.recharts.area_chart(
                    rx.recharts.area(
                        data_key="Close", type="monotone", stroke="#3366FF", fill="#3366FF80"
                    ),
                    rx.recharts.x_axis(data_key="Date"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.cartesian_grid(**chart_theme["grid"]),
                    data=State.chart_data,
                    height=400,
                    width="100%",
                ),
                # Data Table
                rx.data_table(
                    columns=State.table_columns,
                    data=State.data,
                    font_size="10px",
                    width="100%",
                    height=300,
                    overflow="auto",
                ),
                spacing="4",
                width="100%",
            ),
        ),
        width="100%",
        spacing="4",
    )
