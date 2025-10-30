"""Modern card components for displaying metrics, charts, and data.

Professional-grade cards optimized for financial data visualization
with consistent styling and excellent UX.
"""

import reflex as rx
from typing import Optional, Union, List, Dict, Any
from .theme import get_component_style, get_theme_color


def metric_card(
    title: str,
    value: Union[str, int, float],
    change: Optional[Union[str, float]] = None,
    change_type: str = "neutral",  # "positive", "negative", "neutral"
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    loading: bool = False,
    **props,
) -> rx.Component:
    """Modern metric card component for KPIs and statistics.

    Args:
        title: The metric title/label
        value: The main metric value
        change: Optional change indicator (e.g., "+5.2%" or -3.1)
        change_type: Type of change for color coding
        subtitle: Optional subtitle/description
        icon: Optional icon (emoji or lucide icon name)
        loading: Show loading state
        **props: Additional styling props
    """
    # Determine change color
    change_colors = {
        "positive": get_theme_color("success", "400"),
        "negative": get_theme_color("error", "400"),
        "neutral": get_theme_color("gray", "400"),
    }

    change_color = change_colors.get(change_type, change_colors["neutral"])

    # Change indicator with appropriate styling
    change_element = None
    if change is not None:
        change_prefix = (
            "↗" if change_type == "positive" else "↘" if change_type == "negative" else ""
        )
        change_element = rx.text(
            f"{change_prefix} {change}",
            size="2",
            color=change_color,
            font_weight="600",
        )

    return rx.card(
        rx.vstack(
            # Header with icon and title
            rx.hstack(
                rx.cond(
                    icon,
                    rx.text(icon, font_size="1.5rem"),
                    rx.fragment(),
                ),
                rx.vstack(
                    rx.text(
                        title,
                        size="2",
                        color=get_theme_color("gray", "400"),
                        font_weight="500",
                    ),
                    rx.cond(
                        subtitle,
                        rx.text(
                            subtitle,
                            size="1",
                            color=get_theme_color("gray", "500"),
                        ),
                        rx.fragment(),
                    ),
                    align="start",
                    spacing="1",
                ),
                justify="between" if icon else "start",
                align="center",
                width="100%",
            ),
            # Main value
            rx.cond(
                loading,
                rx.skeleton(height="2.5rem", width="60%"),
                rx.text(
                    str(value),
                    size="8",
                    font_weight="700",
                    color="white",
                ),
            ),
            # Change indicator
            rx.cond(
                change_element,
                change_element,
                rx.fragment(),
            ),
            align="start",
            spacing="3",
            width="100%",
        ),
        **{**get_component_style("card"), **props},
    )


def chart_card(
    title: str,
    chart_component: rx.Component,
    subtitle: Optional[str] = None,
    actions: Optional[List[rx.Component]] = None,
    loading: bool = False,
    **props,
) -> rx.Component:
    """Card wrapper for charts with consistent styling.

    Args:
        title: Chart title
        chart_component: The chart component to display
        subtitle: Optional subtitle
        actions: Optional action buttons/components
        loading: Show loading state
        **props: Additional styling props
    """
    header = rx.hstack(
        rx.vstack(
            rx.text(
                title,
                size="4",
                font_weight="600",
                color="white",
            ),
            rx.cond(
                subtitle,
                rx.text(
                    subtitle,
                    size="2",
                    color=get_theme_color("gray", "400"),
                ),
                rx.fragment(),
            ),
            align="start",
            spacing="1",
        ),
        rx.cond(
            actions,
            rx.hstack(*actions, spacing="2"),
            rx.fragment(),
        ),
        justify="between",
        align="center",
        width="100%",
        margin_bottom="4",
    )

    chart_content = rx.cond(
        loading,
        rx.skeleton(height="300px", width="100%"),
        chart_component,
    )

    return rx.card(
        rx.vstack(
            header,
            chart_content,
            spacing="0",
            width="100%",
        ),
        **{**get_component_style("card"), **props},
    )
