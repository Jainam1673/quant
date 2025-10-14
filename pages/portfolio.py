"""Portfolio management and tracking page."""

import reflex as rx
from quant.state import State
from components.layout import main_layout


@main_layout
def portfolio() -> rx.Component:
    """The portfolio management page."""
    return rx.vstack(
        rx.heading("Portfolio Dashboard", size="8", margin_bottom="1rem"),
        
        # Portfolio overview cards
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Total Value", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_value,
                        size="7",
                        color="blue"
                    ),
                    rx.text("Current portfolio value", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Total Positions", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_position_count,
                        size="7"
                    ),
                    rx.text("Active holdings", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Total P&L", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_total_pnl,
                        size="7",
                    ),
                    rx.text(
                        State.portfolio_total_pnl_pct,
                        size="2"
                    ),
                    align="start",
                    spacing="1",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Cash Available", size="2", color="gray"),
                    rx.heading(
                        State.portfolio_cash,
                        size="7",
                        color="green"
                    ),
                    rx.text("Uninvested capital", size="2"),
                    align="start",
                    spacing="1",
                )
            ),
            
            columns="4",
            spacing="4",
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Add position section
        rx.card(
            rx.vstack(
                rx.heading("Add New Position", size="6"),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Ticker", weight="bold"),
                        rx.input(
                            placeholder="e.g., AAPL",
                            value=State.new_position_ticker,
                            on_change=State.set_new_position_ticker,
                            size="3",
                            width="150px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text("Quantity", weight="bold"),
                        rx.input(
                            placeholder="100",
                            value=State.new_position_quantity,
                            on_change=State.set_new_position_quantity,
                            type="number",
                            size="3",
                            width="150px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text("Entry Price", weight="bold"),
                        rx.input(
                            placeholder="150.00",
                            value=State.new_position_price,
                            on_change=State.set_new_position_price,
                            type="number",
                            size="3",
                            width="150px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text(" ", weight="bold"),  # Spacing
                        rx.button(
                            "Add Position",
                            on_click=State.add_portfolio_position,
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
        
        # Holdings table
        rx.heading("Current Holdings", size="6", margin_bottom="1rem"),
        rx.cond(
            State.portfolio_holdings,
            rx.vstack(
                rx.data_table(
                    data=State.portfolio_holdings,
                    columns=[
                        {"title": "Ticker", "field": "ticker"},
                        {"title": "Quantity", "field": "quantity"},
                        {"title": "Entry Price", "field": "entry_price"},
                        {"title": "Current Price", "field": "current_price"},
                        {"title": "Market Value", "field": "market_value"},
                        {"title": "P&L", "field": "pnl"},
                        {"title": "P&L %", "field": "pnl_pct"},
                        {"title": "Weight", "field": "weight"},
                    ],
                    pagination=True,
                    search=True,
                    sort=True,
                    width="100%",
                ),
                
                rx.divider(margin_y="1rem"),
                
                # Portfolio allocation chart
                rx.heading("Portfolio Allocation", size="6", margin_bottom="1rem"),
                rx.recharts.pie_chart(
                    rx.recharts.pie(
                        data=State.portfolio_allocation_data,
                        data_key="value",
                        name_key="ticker",
                        cx="50%",
                        cy="50%",
                        label=True,
                        fill="#8884d8"
                    ),
                    rx.recharts.tooltip(),
                    rx.recharts.legend(),
                    width="100%",
                    height=400,
                ),
                
                spacing="4",
                width="100%",
            ),
            rx.center(
                rx.text(
                    "No positions in portfolio. Add a position above to get started.",
                    color="gray",
                    size="4"
                ),
                padding="4rem",
            ),
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Portfolio optimization section
        rx.card(
            rx.vstack(
                rx.heading("Portfolio Optimization", size="6"),
                rx.text(
                    "Optimize your portfolio allocation using Modern Portfolio Theory",
                    color="gray",
                    margin_bottom="1rem"
                ),
                
                rx.hstack(
                    rx.button(
                        "Maximize Sharpe Ratio",
                        on_click=State.optimize_portfolio_sharpe,
                        size="3",
                        variant="solid",
                    ),
                    rx.button(
                        "Minimize Volatility",
                        on_click=State.optimize_portfolio_volatility,
                        size="3",
                        variant="soft",
                    ),
                    rx.button(
                        "Risk Parity",
                        on_click=State.optimize_portfolio_risk_parity,
                        size="3",
                        variant="soft",
                    ),
                    spacing="3",
                ),
                
                rx.cond(
                    State.optimized_weights,
                    rx.vstack(
                        rx.divider(margin_y="1rem"),
                        rx.heading("Optimized Allocation", size="5"),
                        rx.data_table(
                            data=State.optimized_weights,
                            columns=[
                                {"title": "Ticker", "field": "ticker"},
                                {"title": "Current Weight", "field": "current_weight"},
                                {"title": "Target Weight", "field": "target_weight"},
                                {"title": "Difference", "field": "difference"},
                            ],
                            width="100%",
                        ),
                        rx.button(
                            "Apply Rebalancing",
                            on_click=State.apply_rebalancing,
                            size="3",
                            color_scheme="green",
                            margin_top="1rem",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        
        width="100%",
        spacing="4",
    )
