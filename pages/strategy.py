'''The strategy builder page for creating custom trading strategies.

This module provides a user interface for building, configuring, and saving
custom trading strategies without writing any code. Users can combine various
technical indicators, define entry and exit rules, and set risk management
parameters.
'''

import reflex as rx
from quant.state import State
from components.layout import main_layout


@main_layout
def strategy() -> rx.Component:
    """Renders the strategy builder page.

    The page is composed of several sections:
    - Strategy Configuration: Name and base type of the strategy.
    - Technical Indicators: A grid of cards to select and configure indicators.
    - Trading Rules: Text areas for defining entry and exit conditions.
    - Position Sizing & Risk: Inputs for setting risk management parameters.
    - Actions: Buttons to save, test, or reset the strategy.
    - Saved Strategies: A table displaying all saved custom strategies.

    Returns:
        A Reflex component representing the strategy builder page.
    """
    return rx.vstack(
        rx.heading("Strategy Builder", size="8", margin_bottom="1rem"),
        rx.text(
            "Create custom trading strategies by combining technical indicators and defining entry/exit rules",
            size="4",
            color="gray",
            margin_bottom="2rem"
        ),
        
        # Strategy configuration
        rx.card(
            rx.vstack(
                rx.heading("Strategy Configuration", size="6"),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Strategy Name", weight="bold"),
                        rx.input(
                            placeholder="My Custom Strategy",
                            value=State.custom_strategy_name,
                            on_change=State.set_custom_strategy_name,
                            size="3",
                            width="300px",
                        ),
                        align="start",
                    ),
                    
                    rx.vstack(
                        rx.text("Base Strategy Type", weight="bold"),
                        rx.select(
                            ["Momentum", "Mean Reversion", "Breakout", "Custom"],
                            value=State.custom_strategy_type,
                            on_change=State.set_custom_strategy_type,
                            size="3",
                            width="200px",
                        ),
                        align="start",
                    ),
                    
                    spacing="4",
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Indicator selection
        rx.heading("Technical Indicators", size="6", margin_bottom="1rem"),
        
        rx.grid(
            # Trend Indicators
            rx.card(
                rx.vstack(
                    rx.heading("Trend Indicators", size="5", margin_bottom="1rem"),
                    
                    rx.checkbox(
                        "SMA (Simple Moving Average)",
                        checked=State.indicator_sma,
                        on_change=State.toggle_indicator_sma,
                        size="3",
                    ),
                    rx.cond(
                        State.indicator_sma,
                        rx.hstack(
                            rx.text("Period:", size="2"),
                            rx.input(
                                value=State.sma_period,
                                on_change=State.set_sma_period,
                                type="number",
                                size="2",
                                width="80px",
                            ),
                            spacing="2",
                            margin_left="1.5rem",
                        ),
                        rx.fragment(),
                    ),
                    
                    rx.checkbox(
                        "EMA (Exponential Moving Average)",
                        checked=State.indicator_ema,
                        on_change=State.toggle_indicator_ema,
                        size="3",
                    ),
                    rx.cond(
                        State.indicator_ema,
                        rx.hstack(
                            rx.text("Period:", size="2"),
                            rx.input(
                                value=State.ema_period,
                                on_change=State.set_ema_period,
                                type="number",
                                size="2",
                                width="80px",
                            ),
                            spacing="2",
                            margin_left="1.5rem",
                        ),
                        rx.fragment(),
                    ),
                    
                    rx.checkbox(
                        "MACD",
                        checked=State.indicator_macd,
                        on_change=State.toggle_indicator_macd,
                        size="3",
                    ),
                    
                    rx.checkbox(
                        "ADX (Average Directional Index)",
                        checked=State.indicator_adx,
                        on_change=State.toggle_indicator_adx,
                        size="3",
                    ),
                    
                    align="start",
                    spacing="3",
                    width="100%",
                )
            ),
            
            # Momentum Indicators
            rx.card(
                rx.vstack(
                    rx.heading("Momentum Indicators", size="5", margin_bottom="1rem"),
                    
                    rx.checkbox(
                        "RSI (Relative Strength Index)",
                        checked=State.indicator_rsi,
                        on_change=State.toggle_indicator_rsi,
                        size="3",
                    ),
                    rx.cond(
                        State.indicator_rsi,
                        rx.hstack(
                            rx.text("Period:", size="2"),
                            rx.input(
                                value=State.rsi_period,
                                on_change=State.set_rsi_period,
                                type="number",
                                size="2",
                                width="80px",
                            ),
                            spacing="2",
                            margin_left="1.5rem",
                        ),
                        rx.fragment(),
                    ),
                    
                    rx.checkbox(
                        "Stochastic Oscillator",
                        checked=State.indicator_stochastic,
                        on_change=State.toggle_indicator_stochastic,
                        size="3",
                    ),
                    
                    rx.checkbox(
                        "ROC (Rate of Change)",
                        checked=State.indicator_roc,
                        on_change=State.toggle_indicator_roc,
                        size="3",
                    ),
                    
                    rx.checkbox(
                        "Williams %R",
                        checked=State.indicator_williams,
                        on_change=State.toggle_indicator_williams,
                        size="3",
                    ),
                    
                    align="start",
                    spacing="3",
                    width="100%",
                )
            ),
            
            # Volatility Indicators
            rx.card(
                rx.vstack(
                    rx.heading("Volatility Indicators", size="5", margin_bottom="1rem"),
                    
                    rx.checkbox(
                        "Bollinger Bands",
                        checked=State.indicator_bollinger,
                        on_change=State.toggle_indicator_bollinger,
                        size="3",
                    ),
                    rx.cond(
                        State.indicator_bollinger,
                        rx.vstack(
                            rx.hstack(
                                rx.text("Period:", size="2"),
                                rx.input(
                                    value=State.bollinger_period,
                                    on_change=State.set_bollinger_period,
                                    type="number",
                                    size="2",
                                    width="80px",
                                ),
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.text("Std Dev:", size="2"),
                                rx.input(
                                    value=State.bollinger_std,
                                    on_change=State.set_bollinger_std,
                                    type="number",
                                    size="2",
                                    width="80px",
                                ),
                                spacing="2",
                            ),
                            spacing="2",
                            margin_left="1.5rem",
                        ),
                        rx.fragment(),
                    ),
                    
                    rx.checkbox(
                        "ATR (Average True Range)",
                        checked=State.indicator_atr,
                        on_change=State.toggle_indicator_atr,
                        size="3",
                    ),
                    
                    rx.checkbox(
                        "Keltner Channel",
                        checked=State.indicator_keltner,
                        on_change=State.toggle_indicator_keltner,
                        size="3",
                    ),
                    
                    align="start",
                    spacing="3",
                    width="100%",
                )
            ),
            
            # Volume Indicators
            rx.card(
                rx.vstack(
                    rx.heading("Volume Indicators", size="5", margin_bottom="1rem"),
                    
                    rx.checkbox(
                        "OBV (On-Balance Volume)",
                        checked=State.indicator_obv,
                        on_change=State.toggle_indicator_obv,
                        size="3",
                    ),
                    
                    rx.checkbox(
                        "VWAP (Volume Weighted Avg Price)",
                        checked=State.indicator_vwap,
                        on_change=State.toggle_indicator_vwap,
                        size="3",
                    ),
                    
                    rx.checkbox(
                        "MFI (Money Flow Index)",
                        checked=State.indicator_mfi,
                        on_change=State.toggle_indicator_mfi,
                        size="3",
                    ),
                    
                    align="start",
                    spacing="3",
                    width="100%",
                )
            ),
            
            columns="4",
            spacing="4",
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Entry and Exit Rules
        rx.heading("Trading Rules", size="6", margin_bottom="1rem"),
        
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.heading("Entry Conditions", size="5", margin_bottom="1rem"),
                    
                    rx.text_area(
                        placeholder="Define entry conditions (e.g., RSI < 30 AND price > SMA_50)",
                        value=State.entry_conditions,
                        on_change=State.set_entry_conditions,
                        size="3",
                        height="150px",
                        width="100%",
                    ),
                    
                    rx.text(
                        "Use indicator names and logical operators (AND, OR)",
                        size="2",
                        color="gray"
                    ),
                    
                    spacing="2",
                    width="100%",
                )
            ),
            
            rx.card(
                rx.vstack(
                    rx.heading("Exit Conditions", size="5", margin_bottom="1rem"),
                    
                    rx.text_area(
                        placeholder="Define exit conditions (e.g., RSI > 70 OR profit > 5%)",
                        value=State.exit_conditions,
                        on_change=State.set_exit_conditions,
                        size="3",
                        height="150px",
                        width="100%",
                    ),
                    
                    rx.text(
                        "Define profit targets, stop losses, and exit signals",
                        size="2",
                        color="gray"
                    ),
                    
                    spacing="2",
                    width="100%",
                )
            ),
            
            columns="2",
            spacing="4",
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Position sizing and risk management
        rx.card(
            rx.vstack(
                rx.heading("Position Sizing & Risk Management", size="6"),
                
                rx.grid(
                    rx.vstack(
                        rx.text("Position Size (%)", weight="bold"),
                        rx.input(
                            placeholder="10",
                            value=State.position_size_pct,
                            on_change=State.set_position_size_pct,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.text("Stop Loss (%)", weight="bold"),
                        rx.input(
                            placeholder="2",
                            value=State.stop_loss_pct,
                            on_change=State.set_stop_loss_pct,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.text("Take Profit (%)", weight="bold"),
                        rx.input(
                            placeholder="5",
                            value=State.take_profit_pct,
                            on_change=State.set_take_profit_pct,
                            type="number",
                            size="3",
                        ),
                        align="start",
                        width="100%",
                    ),
                    
                    rx.vstack(
                        rx.text("Max Positions", weight="bold"),
                        rx.input(
                            placeholder="5",
                            value=State.max_positions,
                            on_change=State.set_max_positions,
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
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        
        rx.divider(margin_y="1rem"),
        
        # Action buttons
        rx.hstack(
            rx.button(
                "Save Strategy",
                on_click=State.save_custom_strategy,
                size="4",
                variant="solid",
            ),
            rx.button(
                "Test Strategy",
                on_click=State.test_custom_strategy,
                size="4",
                variant="soft",
            ),
            rx.button(
                "Reset",
                on_click=State.reset_strategy_builder,
                size="4",
                variant="outline",
            ),
            spacing="3",
            width="100%",
            justify="center",
            margin_top="1rem",
        ),
        
        # Saved strategies
        rx.divider(margin_y="1rem"),
        
        rx.heading("Saved Strategies", size="6", margin_bottom="1rem"),
        rx.cond(
            State.saved_strategies,
            rx.data_table(
                data=State.saved_strategies,
                columns=[
                    {"title": "Name", "field": "name"},
                    {"title": "Type", "field": "type"},
                    {"title": "Indicators", "field": "indicators"},
                    {"title": "Created", "field": "created_at"},
                    {"title": "Actions", "field": "actions"},
                ],
                pagination=True,
                search=True,
                width="100%",
            ),
            rx.center(
                rx.text(
                    "No saved strategies. Create and save your first strategy above.",
                    color="gray",
                    size="4"
                ),
                padding="2rem",
            ),
        ),
        
        width="100%",
        spacing="4",
    )
