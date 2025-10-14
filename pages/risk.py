"""Risk analytics and management page."""

import reflex as rx
from quant.state import State
from components.layout import main_layout


@main_layout
def risk() -> rx.Component:
    """The risk analytics page."""
    return rx.vstack(
        rx.heading("Risk Analytics", size="8", margin_bottom="1rem"),
        
        # Risk overview cards
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Portfolio VaR (95%)", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_var_95,
                        size="7",
                        color="red"
                    ),
                    rx.text("1-day Value at Risk", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("CVaR (95%)", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_cvar_95,
                        size="7",
                        color="red"
                    ),
                    rx.text("Conditional VaR", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Max Drawdown", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_max_drawdown,
                        size="7",
                        color="orange"
                    ),
                    rx.text("Peak to trough decline", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Sharpe Ratio", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_sharpe,
                        size="7",
                        color="blue"
                    ),
                    rx.text("Risk-adjusted return", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            columns="4",
            spacing="4",
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # VaR calculation controls
        rx.card(
            rx.vstack(
                rx.heading("Calculate Risk Metrics", size="6"),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Confidence Level", weight="bold"),
                        rx.select(
                            ["90%", "95%", "99%"],
                            value=State.var_confidence_level,
                            on_change=State.set_var_confidence_level,
                            size="3",
                            width="150px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text("Method", weight="bold"),
                        rx.select(
                            ["Historical", "Parametric", "Monte Carlo"],
                            value=State.var_method,
                            on_change=State.set_var_method,
                            size="3",
                            width="200px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text("Time Horizon (days)", weight="bold"),
                        rx.input(
                            placeholder="1",
                            value=State.var_time_horizon,
                            on_change=State.set_var_time_horizon,
                            type="number",
                            size="3",
                            width="150px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text(" ", weight="bold"),  # Spacing
                        rx.button(
                            "Calculate VaR",
                            on_click=State.calculate_portfolio_var,
                            loading=State.risk_calculating,
                            size="3",
                        ),
                        align="start",
                    ),
                    
                    spacing="4",
                    align="center",
                ),
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Risk metrics table
        rx.heading("Detailed Risk Metrics", size="6", margin_bottom="1rem"),
        rx.cond(
            State.risk_metrics_data,
            rx.data_table(
                data=State.risk_metrics_data,
                columns=[
                    {"title": "Metric", "field": "metric"},
                    {"title": "Value", "field": "value"},
                    {"title": "Description", "field": "description"},
                ],
                width="100%",
            ),
            rx.center(
                rx.text(
                    "Calculate risk metrics to see detailed analysis",
                    color="gray",
                    size="4"
                ),
                padding="2rem",
            ),
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Correlation matrix
        rx.heading("Asset Correlation Matrix", size="6", margin_bottom="1rem"),
        rx.card(
            rx.vstack(
                rx.button(
                    "Calculate Correlations",
                    on_click=State.calculate_correlations,
                    loading=State.risk_calculating,
                    size="3",
                    margin_bottom="1rem",
                ),
                
                rx.cond(
                    State.correlation_matrix_data,
                    rx.vstack(
                        rx.text(
                            "Correlation coefficients between portfolio assets (1-year daily returns)",
                            color="gray",
                            size="2",
                            margin_bottom="1rem"
                        ),
                        rx.data_table(
                            data=State.correlation_matrix_data,
                            columns=[
                                {"title": "Asset", "field": "asset"},
                                {"title": "Correlation", "field": "correlation"},
                            ],
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.text(
                        "Click above to calculate correlation matrix",
                        color="gray",
                        size="3"
                    ),
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Drawdown chart
        rx.heading("Drawdown Analysis", size="6", margin_bottom="1rem"),
        rx.cond(
            State.drawdown_data,
            rx.vstack(
                rx.recharts.area_chart(
                    rx.recharts.area(
                        data_key="drawdown",
                        type="monotone",
                        stroke="#FF6B6B",
                        fill="#FF6B6B80"
                    ),
                    rx.recharts.x_axis(data_key="date"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    data=State.drawdown_data,
                    height=400,
                    width="100%",
                ),
                
                rx.text(
                    "Drawdown represents the decline from a historical peak in portfolio value",
                    color="gray",
                    size="2",
                    margin_top="1rem"
                ),
                
                spacing="3",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.text(
                        "Run a backtest or load portfolio history to see drawdown analysis",
                        color="gray",
                        size="4"
                    ),
                    rx.button(
                        "Load Portfolio History",
                        on_click=State.load_portfolio_history,
                        size="3",
                        margin_top="1rem",
                    ),
                    align="center",
                ),
                padding="4rem",
            ),
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Risk limits and alerts
        rx.card(
            rx.vstack(
                rx.heading("Risk Limits & Alerts", size="6"),
                rx.text(
                    "Set risk limits to monitor portfolio exposure",
                    color="gray",
                    margin_bottom="1rem"
                ),
                
                rx.grid(
                    rx.vstack(
                        rx.text("Max Position Size (%)", weight="bold"),
                        rx.input(
                            placeholder="25",
                            value=State.max_position_size,
                            on_change=State.set_max_position_size,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.text("Max Drawdown Alert (%)", weight="bold"),
                        rx.input(
                            placeholder="20",
                            value=State.max_drawdown_alert,
                            on_change=State.set_max_drawdown_alert,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.text("Max Daily Loss ($)", weight="bold"),
                        rx.input(
                            placeholder="5000",
                            value=State.max_daily_loss,
                            on_change=State.set_max_daily_loss,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.text("Min Sharpe Ratio", weight="bold"),
                        rx.input(
                            placeholder="1.0",
                            value=State.min_sharpe_ratio,
                            on_change=State.set_min_sharpe_ratio,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    columns="4",
                    spacing="4",
                    width="100%",
                ),
                
                rx.button(
                    "Save Risk Limits",
                    on_click=State.save_risk_limits,
                    size="3",
                    margin_top="1rem",
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        
        width="100%",
        spacing="4",
    )
