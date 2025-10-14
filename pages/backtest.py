"""Backtesting page for strategy testing."""

import reflex as rx
from quant.state import State
from components.layout import main_layout


@main_layout
def backtest() -> rx.Component:
    """The backtesting page."""
    return rx.vstack(
        rx.heading("Strategy Backtesting", size="8", margin_bottom="1rem"),
        
        # Strategy selection and controls
        rx.card(
            rx.vstack(
                rx.heading("Backtest Configuration", size="6"),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Ticker Symbol", weight="bold"),
                        rx.input(
                            placeholder="Enter ticker (e.g., AAPL)",
                            value=State.ticker,
                            on_change=State.set_ticker,
                            size="3",
                            width="200px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text("Strategy", weight="bold"),
                        rx.select(
                            State.strategy_options,
                            value=State.selected_strategy,
                            on_change=State.set_strategy,
                            size="3",
                            width="200px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text(" ", weight="bold"),  # Spacing
                        rx.button(
                            "Run Backtest",
                            on_click=State.run_backtest,
                            loading=State.backtest_running,
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
        
        # Results section
        rx.cond(
            State.backtest_results,
            rx.vstack(
                # Performance metrics cards
                rx.heading("Performance Metrics", size="6", margin_bottom="1rem"),
                
                rx.grid(
                    # Total Return card
                    rx.card(
                        rx.vstack(
                            rx.text("Total Return", size="2", color="gray"),
                            rx.heading(
                                rx.text.span(State.backtest_results["total_return_pct"], " %"),
                                size="7",
                                color=rx.cond(
                                    State.backtest_results["total_return_pct"] >= 0,
                                    "green",
                                    "red"
                                )
                            ),
                            rx.text(
                                f"${State.backtest_results['total_return']:.2f}",
                                size="2"
                            ),
                            align="start",
                            spacing="1",
                        )
                    ),
                    
                    # Sharpe Ratio card
                    rx.card(
                        rx.vstack(
                            rx.text("Sharpe Ratio", size="2", color="gray"),
                            rx.heading(
                                State.backtest_results["sharpe_ratio"],
                                size="7"
                            ),
                            rx.text("Risk-adjusted return", size="2"),
                            align="start",
                            spacing="1",
                        )
                    ),
                    
                    # Max Drawdown card
                    rx.card(
                        rx.vstack(
                            rx.text("Max Drawdown", size="2", color="gray"),
                            rx.heading(
                                rx.text.span(State.backtest_results["max_drawdown"], " %"),
                                size="7",
                                color="red"
                            ),
                            rx.text("Largest peak-to-trough", size="2"),
                            align="start",
                            spacing="1",
                        )
                    ),
                    
                    # Win Rate card
                    rx.card(
                        rx.vstack(
                            rx.text("Win Rate", size="2", color="gray"),
                            rx.heading(
                                rx.text.span(State.backtest_results["win_rate"], " %"),
                                size="7"
                            ),
                            rx.text(
                                rx.text.span(State.backtest_results["num_trades"], " trades"),
                                size="2"
                            ),
                            align="start",
                            spacing="1",
                        )
                    ),
                    
                    columns="4",
                    spacing="4",
                    width="100%",
                ),
                
                rx.divider(margin_y="1rem"),
                
                # Equity curve chart
                rx.heading("Equity Curve", size="6", margin_bottom="1rem"),
                rx.recharts.area_chart(
                    rx.recharts.area(
                        data_key="equity",
                        type="monotone",
                        stroke="#3366FF",
                        fill="#3366FF80"
                    ),
                    rx.recharts.x_axis(data_key="timestamp"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    data=State.backtest_equity_curve,
                    height=400,
                    width="100%",
                ),
                
                rx.divider(margin_y="1rem"),
                
                # Trades table
                rx.heading("Trade History", size="6", margin_bottom="1rem"),
                rx.cond(
                    State.backtest_trades,
                    rx.data_table(
                        data=State.backtest_trades,
                        pagination=True,
                        search=True,
                        sort=True,
                        width="100%",
                    ),
                    rx.text("No trades executed", color="gray"),
                ),
                
                spacing="4",
                width="100%",
            ),
            rx.center(
                rx.text(
                    "Configure and run a backtest to see results",
                    color="gray",
                    size="4"
                ),
                padding="4rem",
            ),
        ),
        
        width="100%",
        spacing="4",
    )
