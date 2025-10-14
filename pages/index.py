"""The stock overview page."""

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
    """The main page of the app."""
    return rx.vstack(
        rx.heading("Stock Overview", size="8", margin_bottom="1rem"),
        
        # Input and Button
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
                is_loading=State.is_loading,
                size="3",
            ),
            spacing="4",
            align="center",
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
