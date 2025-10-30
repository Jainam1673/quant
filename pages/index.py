"""The main dashboard page for the Quant Trading Platform.

Modern, professional dashboard with advanced UI/UX components and
comprehensive financial data visualization.
"""

import reflex as rx
from quant.state import State
from components.ui import (
    dashboard_layout, 
    metric_card, 
    chart_card,
    section_header,
    grid_layout,
    performance_chart,
    form_button,
    get_theme_color
)


@dashboard_layout(
    current_path="/",
    page_title="Dashboard",
    page_subtitle="Quantitative Trading Platform Overview",
    page_actions=[
        form_button("New Strategy", icon="⚡", variant="primary"),
        form_button("Export Data", icon="📊", variant="secondary"),
    ]
)
def index() -> rx.Component:
    """Modern dashboard with professional financial UI/UX.
    
    Features:
    - Real-time KPI metrics with trend indicators
    - Interactive performance charts
    - Modern card-based layout
    - Professional color scheme and typography
    - Responsive grid system
    """
    return rx.vstack(
        # KPI Metrics Section
        section_header(
            title="Key Performance Indicators",
            subtitle="Real-time portfolio and strategy metrics",
        ),
        
        grid_layout([
            metric_card(
                title="Portfolio Value",
                value="$1,247,892",
                change="+12.4%",
                change_type="positive",
                icon="💰",
            ),
            metric_card(
                title="Total Return",
                value="24.7%",
                change="+2.3%",
                change_type="positive", 
                icon="📈",
            ),
            metric_card(
                title="Sharpe Ratio",
                value="1.84",
                change="+0.12",
                change_type="positive",
                icon="⚡",
            ),
            metric_card(
                title="Max Drawdown",
                value="8.2%",
                change="-1.1%",
                change_type="positive",
                icon="📉",
            ),
            metric_card(
                title="Active Strategies",
                value="5",
                change="+1",
                change_type="positive",
                icon="⚙️",
            ),
            metric_card(
                title="Win Rate",
                value="68.4%",
                change="+3.2%",
                change_type="positive",
                icon="🎯",
            ),
        ], columns=3),
        
        # Charts Section
        section_header(
            title="Performance Analytics",
            subtitle="Visual analysis of portfolio and strategy performance",
        ),
        
        rx.hstack(
            # Performance Chart
            chart_card(
                title="Portfolio Performance",
                subtitle="Cumulative returns over time",
                chart_component=rx.box(
                    rx.text(
                        "📊 Interactive Performance Chart",
                        color=get_theme_color("gray", "400"),
                        text_align="center",
                        padding="4rem",
                        font_size="1.2rem",
                    ),
                    background=get_theme_color("gray", "800"),
                    border_radius="0.5rem",
                    height="300px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                actions=[
                    form_button("1D", size="sm", variant="secondary"),
                    form_button("1W", size="sm", variant="secondary"),
                    form_button("1M", size="sm", variant="primary"),
                    form_button("1Y", size="sm", variant="secondary"),
                ],
                width="70%",
            ),
            
            # Quick Stats
            rx.vstack(
                rx.card(
                    rx.vstack(
                        rx.text(
                            "Recent Trades",
                            size="4",
                            font_weight="600",
                            color="white",
                            margin_bottom="3",
                        ),
                        
                        # Trade items
                        rx.vstack(
                            rx.hstack(
                                rx.text("AAPL", font_weight="600", color="white"),
                                rx.spacer(),
                                rx.text("+$2,450", color=get_theme_color("success", "400"), font_weight="600"),
                                width="100%",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("TSLA", font_weight="600", color="white"),
                                rx.spacer(),
                                rx.text("-$890", color=get_theme_color("error", "400"), font_weight="600"),
                                width="100%",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("MSFT", font_weight="600", color="white"),
                                rx.spacer(),
                                rx.text("+$1,230", color=get_theme_color("success", "400"), font_weight="600"),
                                width="100%",
                                align="center",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        
                        align="start",
                        spacing="0",
                        width="100%",
                    ),
                    background=get_theme_color("gray", "900"),
                    border=f"1px solid {get_theme_color('gray', '700')}",
                    padding="1.5rem",
                ),
                
                rx.card(
                    rx.vstack(
                        rx.text(
                            "Market Status",
                            size="4",
                            font_weight="600",
                            color="white",
                            margin_bottom="3",
                        ),
                        
                        rx.hstack(
                            rx.box(
                                width="0.5rem",
                                height="0.5rem",
                                background=get_theme_color("success", "400"),
                                border_radius="50%",
                            ),
                            rx.text("Market Open", color=get_theme_color("success", "400")),
                            align="center",
                            spacing="2",
                        ),
                        
                        rx.text(
                            "Next close: 4:00 PM EST",
                            size="2",
                            color=get_theme_color("gray", "400"),
                        ),
                        
                        align="start",
                        spacing="2",
                        width="100%",
                    ),
                    background=get_theme_color("gray", "900"),
                    border=f"1px solid {get_theme_color('gray', '700')}",
                    padding="1.5rem",
                ),
                
                spacing="4",
                width="30%",
            ),
            
            spacing="4",
            width="100%",
            align="stretch",
        ),
        
        # Quick Actions Section
        section_header(
            title="Quick Actions",
            subtitle="Frequently used tools and shortcuts",
        ),
        
        grid_layout([
            rx.card(
                rx.vstack(
                    rx.text("🔬", font_size="3rem"),
                    rx.text(
                        "Run Backtest",
                        size="4",
                        font_weight="600",
                        color="white",
                    ),
                    rx.text(
                        "Test strategies on historical data",
                        size="2",
                        color=get_theme_color("gray", "400"),
                        text_align="center",
                    ),
                    form_button("Start Backtest", variant="primary", size="md"),
                    align="center",
                    spacing="3",
                ),
                background=get_theme_color("gray", "900"),
                border=f"1px solid {get_theme_color('gray', '700')}",
                padding="2rem",
                text_align="center",
                _hover={
                    "border_color": get_theme_color("primary", "500"),
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 8px 25px rgba(0,0,0,0.3)",
                },
                transition="all 0.3s ease",
                cursor="pointer",
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("💼", font_size="3rem"),
                    rx.text(
                        "Optimize Portfolio",
                        size="4",
                        font_weight="600",
                        color="white",
                    ),
                    rx.text(
                        "Modern Portfolio Theory optimization",
                        size="2",
                        color=get_theme_color("gray", "400"),
                        text_align="center",
                    ),
                    form_button("Optimize", variant="primary", size="md"),
                    align="center",
                    spacing="3",
                ),
                background=get_theme_color("gray", "900"),
                border=f"1px solid {get_theme_color('gray', '700')}",
                padding="2rem",
                text_align="center",
                _hover={
                    "border_color": get_theme_color("primary", "500"),
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 8px 25px rgba(0,0,0,0.3)",
                },
                transition="all 0.3s ease",
                cursor="pointer",
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("📊", font_size="3rem"),
                    rx.text(
                        "Risk Analysis",
                        size="4",
                        font_weight="600",
                        color="white",
                    ),
                    rx.text(
                        "VaR, CVaR, and risk metrics",
                        size="2",
                        color=get_theme_color("gray", "400"),
                        text_align="center",
                    ),
                    form_button("Analyze Risk", variant="primary", size="md"),
                    align="center",
                    spacing="3",
                ),
                background=get_theme_color("gray", "900"),
                border=f"1px solid {get_theme_color('gray', '700')}",
                padding="2rem",
                text_align="center",
                _hover={
                    "border_color": get_theme_color("primary", "500"),
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 8px 25px rgba(0,0,0,0.3)",
                },
                transition="all 0.3s ease",
                cursor="pointer",
            ),
        ], columns=3),
        
        spacing="6",
        width="100%",
        max_width="1400px",
    )
