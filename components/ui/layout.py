"""Modern layout components for consistent page structure.

Professional layouts optimized for financial applications with
responsive design and excellent UX.
"""

import reflex as rx
from typing import Optional, List, Dict, Any, Callable
from .theme import get_theme_color, spacing
from .navigation import modern_sidebar, top_navigation


def page_container(
    children: List[rx.Component], max_width: str = "1400px", padding: str = "2rem", **props
) -> rx.Component:
    """Container for page content with consistent spacing and max width.

    Args:
        children: Child components
        max_width: Maximum container width
        padding: Container padding
        **props: Additional styling props
    """
    return rx.container(
        *children,
        max_width=max_width,
        padding=padding,
        margin_x="auto",
        **props,
    )


def section_header(
    title: str,
    subtitle: Optional[str] = None,
    actions: Optional[List[rx.Component]] = None,
    divider: bool = True,
    **props,
) -> rx.Component:
    """Section header with title, subtitle, and optional actions.

    Args:
        title: Section title
        subtitle: Optional subtitle/description
        actions: Optional action components
        divider: Whether to show bottom divider
        **props: Additional styling props
    """
    header_content = rx.hstack(
        rx.vstack(
            rx.text(
                title,
                size="5",
                font_weight="600",
                color="white",
            ),
            rx.cond(
                subtitle,
                rx.text(
                    subtitle,
                    size="3",
                    color=get_theme_color("gray", "400"),
                ),
                rx.fragment(),
            ),
            align="start",
            spacing="1",
        ),
        rx.spacer(),
        
        # Actions section
        rx.cond(
            actions and len(actions) > 0,
            rx.hstack(*actions, spacing="2"),
            rx.fragment(),
        ),
        align="center",
        width="100%",
        **props,
    )

    if divider:
        return rx.vstack(
            header_content,
            rx.divider(
                color_scheme="gray",
                margin_y="1rem",
            ),
            spacing="0",
            width="100%",
        )

    return header_content


def grid_layout(
    children: List[rx.Component],
    columns: int = 3,
    gap: str = "1.5rem",
    responsive: bool = True,
    **props,
) -> rx.Component:
    """Responsive grid layout for cards and components.

    Args:
        children: Child components
        columns: Number of columns (desktop)
        gap: Grid gap
        responsive: Whether to use responsive breakpoints
        **props: Additional styling props
    """
    if responsive:
        # Responsive grid: 1 column on mobile, 2 on tablet, specified on desktop
        grid_template_columns = [
            "1fr",  # Mobile
            "repeat(2, 1fr)",  # Tablet
            f"repeat({columns}, 1fr)",  # Desktop
        ]
    else:
        grid_template_columns = f"repeat({columns}, 1fr)"

    return rx.box(
        *children,
        display="grid",
        grid_template_columns=grid_template_columns,
        gap=gap,
        width="100%",
        **props,
    )


def sidebar_layout(
    sidebar_content: rx.Component, main_content: rx.Component, sidebar_width: str = "280px", **props
) -> rx.Component:
    """Layout with sidebar and main content area.

    Args:
        sidebar_content: Sidebar component
        main_content: Main content component
        sidebar_width: Width of the sidebar
        **props: Additional styling props
    """
    return rx.hstack(
        sidebar_content,
        rx.box(
            main_content,
            flex="1",
            min_height="100vh",
            background=get_theme_color("gray", "950"),
            overflow_x="auto",
        ),
        spacing="0",
        width="100%",
        height="100vh",
        **props,
    )


def dashboard_layout(
    current_path: str = "/",
    nav_items: Optional[List[Dict[str, Any]]] = None,
    page_title: str = "Dashboard",
    page_subtitle: Optional[str] = None,
    page_actions: Optional[List[rx.Component]] = None,
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    user_info: Optional[Dict[str, str]] = None,
) -> Callable[[Callable], rx.Component]:
    """Complete dashboard layout decorator with sidebar and top navigation.

    Args:
        current_path: Current page path
        nav_items: Navigation items for sidebar
        page_title: Page title for top nav
        page_subtitle: Optional page subtitle
        page_actions: Optional page action components
        breadcrumbs: Optional breadcrumb navigation
        user_info: Optional user information
    """
    # Default navigation items
    if nav_items is None:
        nav_items = [
            {
                "label": "Dashboard",
                "href": "/",
                "icon": "🏠",
                "description": "Overview and metrics",
            },
            {
                "label": "Backtesting",
                "href": "/backtest",
                "icon": "📊",
                "description": "Strategy testing",
            },
            {
                "label": "Portfolio",
                "href": "/portfolio",
                "icon": "💼",
                "description": "Portfolio management",
            },
            {"label": "Risk Analysis", "href": "/risk", "icon": "⚠️", "description": "Risk metrics"},
            {
                "label": "Strategy Builder",
                "href": "/strategy",
                "icon": "⚙️",
                "description": "Custom strategies",
            },
        ]

    def decorator(page_function: Callable) -> rx.Component:
        def wrapped_page() -> rx.Component:
            # Get the actual page content
            page_content = page_function()

            # Create sidebar
            sidebar = modern_sidebar(
                nav_items=nav_items,
                current_path=current_path,
                user_info=user_info,
            )

            # Create top navigation
            top_nav = top_navigation(
                title=page_title,
                subtitle=page_subtitle,
                actions=page_actions,
                breadcrumbs=breadcrumbs,
            )

            # Create main content area
            main_content = rx.vstack(
                top_nav,
                rx.box(
                    page_content,
                    padding="2rem",
                    flex="1",
                    overflow_y="auto",
                ),
                spacing="0",
                height="100vh",
                width="100%",
            )

            # Return complete layout
            return sidebar_layout(
                sidebar_content=sidebar,
                main_content=main_content,
            )

        return wrapped_page

    return decorator
