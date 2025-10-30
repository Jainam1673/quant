"""Modern chart components for financial data visualization.

Professional-grade charts optimized for trading and financial analysis
with consistent theming and excellent UX.
"""

import reflex as rx
from typing import List, Dict, Any, Optional
from .theme import get_theme_color, colors


def price_chart(
    data: List[Dict[str, Any]], height: str = "400px", show_volume: bool = True, **props
) -> rx.Component:
    """Professional price chart with volume for financial data.

    Args:
        data: Chart data with OHLCV format
        height: Chart height
        show_volume: Whether to show volume bars
        **props: Additional chart props
    """
    chart_config = {
        "data": data,
        "margin": {"top": 20, "right": 30, "left": 20, "bottom": 5},
        "theme": "dark",
    }

    # Main price line chart
    price_chart_component = rx.recharts.line_chart(
        rx.recharts.line(
            data_key="close",
            stroke=get_theme_color("primary", "400"),
            stroke_width=2,
            dot=False,
        ),
        rx.recharts.x_axis(
            data_key="date",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.y_axis(
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            stroke=get_theme_color("gray", "700"),
        ),
        rx.recharts.tooltip(
            content_style={
                "background": get_theme_color("gray", "800"),
                "border": f"1px solid {get_theme_color('gray', '600')}",
                "border_radius": "0.5rem",
                "color": "white",
            }
        ),
        data=data,
        width="100%",
        height=height,
        **props,
    )

    return price_chart_component


def candlestick_chart(data: List[Dict[str, Any]], height: str = "400px", **props) -> rx.Component:
    """Professional candlestick chart for OHLC data.

    Args:
        data: OHLC data
        height: Chart height
        **props: Additional chart props
    """
    # Since Reflex doesn't have native candlestick, we'll use a combination chart
    return rx.recharts.composed_chart(
        rx.recharts.bar(
            data_key="volume",
            fill=get_theme_color("gray", "600"),
            opacity=0.6,
        ),
        rx.recharts.line(
            data_key="close",
            stroke=get_theme_color("primary", "400"),
            stroke_width=2,
            dot=False,
        ),
        rx.recharts.x_axis(
            data_key="date",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.y_axis(
            y_axis_id="price",
            orientation="right",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.y_axis(
            y_axis_id="volume",
            orientation="left",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            stroke=get_theme_color("gray", "700"),
        ),
        rx.recharts.tooltip(
            content_style={
                "background": get_theme_color("gray", "800"),
                "border": f"1px solid {get_theme_color('gray', '600')}",
                "border_radius": "0.5rem",
                "color": "white",
            }
        ),
        data=data,
        width="100%",
        height=height,
        **props,
    )


def performance_chart(data: List[Dict[str, Any]], height: str = "300px", **props) -> rx.Component:
    """Performance/equity curve chart for backtesting results.

    Args:
        data: Performance data with cumulative returns
        height: Chart height
        **props: Additional chart props
    """
    return rx.recharts.area_chart(
        rx.recharts.area(
            data_key="cumulative_return",
            stroke=get_theme_color("success", "400"),
            fill=f"url(#gradient-success)",
            stroke_width=2,
        ),
        rx.recharts.x_axis(
            data_key="date",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.y_axis(
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            stroke=get_theme_color("gray", "700"),
        ),
        rx.recharts.tooltip(
            content_style={
                "background": get_theme_color("gray", "800"),
                "border": f"1px solid {get_theme_color('gray', '600')}",
                "border_radius": "0.5rem",
                "color": "white",
            }
        ),
        # Add gradient definition
        rx.html.defs(
            rx.html.svg.linear_gradient(
                rx.html.svg.stop(
                    offset="5%",
                    stop_color=get_theme_color("success", "400"),
                    stop_opacity=0.8,
                ),
                rx.html.svg.stop(
                    offset="95%",
                    stop_color=get_theme_color("success", "400"),
                    stop_opacity=0.1,
                ),
                id="gradient-success",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            )
        ),
        data=data,
        width="100%",
        height=height,
        **props,
    )


def portfolio_allocation_chart(data: List[Dict[str, Any]], **props) -> rx.Component:
    """Portfolio allocation pie chart.

    Args:
        data: Allocation data with name and value
        **props: Additional chart props
    """
    colors_list = [
        get_theme_color("primary", "400"),
        get_theme_color("success", "400"),
        get_theme_color("warning", "400"),
        get_theme_color("error", "400"),
        get_theme_color("gray", "400"),
    ]

    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=data,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            outer_radius=80,
            fill=colors_list[0],
            label=True,
        ),
        rx.recharts.tooltip(
            content_style={
                "background": get_theme_color("gray", "800"),
                "border": f"1px solid {get_theme_color('gray', '600')}",
                "border_radius": "0.5rem",
                "color": "white",
            }
        ),
        rx.recharts.legend(),
        width="100%",
        height="300px",
        **props,
    )


def heatmap_chart(
    data: List[Dict[str, Any]],
    x_key: str = "x",
    y_key: str = "y",
    value_key: str = "value",
    **props,
) -> rx.Component:
    """Correlation heatmap chart.

    Args:
        data: Heatmap data
        x_key: X-axis data key
        y_key: Y-axis data key
        value_key: Value data key for color coding
        **props: Additional chart props
    """
    # Simplified heatmap using scatter plot with size/color mapping
    return rx.recharts.scatter_chart(
        rx.recharts.scatter(
            data=data,
            fill=get_theme_color("primary", "400"),
        ),
        rx.recharts.x_axis(
            data_key=x_key,
            type="category",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.y_axis(
            data_key=y_key,
            type="category",
            stroke=get_theme_color("gray", "500"),
        ),
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            stroke=get_theme_color("gray", "700"),
        ),
        rx.recharts.tooltip(
            content_style={
                "background": get_theme_color("gray", "800"),
                "border": f"1px solid {get_theme_color('gray', '600')}",
                "border_radius": "0.5rem",
                "color": "white",
            }
        ),
        width="100%",
        height="400px",
        **props,
    )


def metric_sparkline(
    data: List[Dict[str, Any]],
    data_key: str = "value",
    color: str = "primary",
    height: str = "60px",
    **props,
) -> rx.Component:
    """Small sparkline chart for metric trends.

    Args:
        data: Time series data
        data_key: Data key for values
        color: Color theme
        height: Chart height
        **props: Additional chart props
    """
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key=data_key,
            stroke=get_theme_color(color, "400"),
            stroke_width=2,
            dot=False,
        ),
        data=data,
        width="100%",
        height=height,
        margin={"top": 5, "right": 5, "left": 5, "bottom": 5},
        **props,
    )
