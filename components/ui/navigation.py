"""Modern navigation components for the Quant Trading Platform.

Professional navigation with excellent UX, accessibility, and visual design.
"""

import reflex as rx
from typing import List, Dict, Optional, Any
from .theme import get_theme_color, get_component_style


def nav_item(
    label: str,
    href: str,
    icon: Optional[str] = None,
    active: bool = False,
    badge: Optional[str] = None,
    description: Optional[str] = None,
    **props,
) -> rx.Component:
    """Modern navigation item with hover effects and states.

    Args:
        label: Navigation item label
        href: URL to navigate to
        icon: Optional icon (emoji or icon name)
        active: Whether this item is currently active
        badge: Optional badge text (e.g., "New", "5")
        description: Optional description for tooltip
        **props: Additional styling props
    """
    # Active state styling
    active_styles = (
        {
            "background": f"{get_theme_color('primary', '600')}20",
            "border_left": f"3px solid {get_theme_color('primary', '500')}",
            "color": get_theme_color("primary", "400"),
        }
        if active
        else {}
    )

    # Badge component
    badge_component = None
    if badge:
        badge_component = rx.badge(
            badge,
            size="1",
            color_scheme="blue" if active else "gray",
            radius="full",
        )

    return rx.link(
        rx.hstack(
            # Icon
            rx.cond(
                icon,
                rx.text(
                    icon,
                    font_size="1.25rem",
                    color="inherit",
                ),
                rx.fragment(),
            ),
            # Label and description
            rx.vstack(
                rx.text(
                    label,
                    size="3",
                    font_weight="500",
                    color="inherit",
                ),
                rx.cond(
                    description,
                    rx.text(
                        description,
                        size="1",
                        color=get_theme_color("gray", "500"),
                    ),
                    rx.fragment(),
                ),
                align="start",
                spacing="1",
                flex="1",
            ),
            # Badge
            rx.cond(
                badge_component,
                badge_component,
                rx.fragment(),
            ),
            align="center",
            spacing="3",
            width="100%",
            padding="0.75rem 1rem",
        ),
        href=href,
        width="100%",
        border_radius="0.5rem",
        transition="all 0.2s ease",
        text_decoration="none",
        color=get_theme_color("gray", "300"),
        _hover={
            "background": get_theme_color("gray", "800"),
            "color": "white",
            "text_decoration": "none",
        },
        **active_styles,
        **props,
    )


def modern_sidebar(
    nav_items: List[Dict[str, Any]],
    current_path: str = "/",
    brand_name: str = "Quant Platform",
    brand_subtitle: str = "Professional Trading Analytics",
    user_info: Optional[Dict[str, str]] = None,
    **props,
) -> rx.Component:
    """Modern sidebar with brand, navigation, and user info.

    Args:
        nav_items: List of navigation item dictionaries
        current_path: Current page path for active state
        brand_name: Application brand name
        brand_subtitle: Brand subtitle/tagline
        user_info: Optional user information dict
        **props: Additional styling props
    """
    # Brand section
    brand_section = rx.vstack(
        rx.hstack(
            rx.box(
                "📊",
                font_size="2rem",
                padding="0.5rem",
                background=f"linear-gradient(135deg, {get_theme_color('primary', '600')}, {get_theme_color('primary', '700')})",
                border_radius="0.75rem",
                box_shadow="0 4px 12px rgba(0,0,0,0.3)",
            ),
            rx.vstack(
                rx.text(
                    brand_name,
                    size="5",
                    font_weight="700",
                    color="white",
                ),
                rx.text(
                    brand_subtitle,
                    size="2",
                    color=get_theme_color("gray", "400"),
                ),
                align="start",
                spacing="1",
            ),
            align="center",
            spacing="3",
        ),
        padding="1.5rem 1rem",
        border_bottom=f"1px solid {get_theme_color('gray', '700')}",
        margin_bottom="1rem",
    )

    # Navigation section
    nav_section = rx.vstack(
        *[
            nav_item(
                label=item["label"],
                href=item["href"],
                icon=item.get("icon"),
                active=current_path == item["href"],
                badge=item.get("badge"),
                description=item.get("description"),
            )
            for item in nav_items
        ],
        spacing="1",
        padding="0 1rem",
        width="100%",
    )

    # User section (if provided)
    user_section = None
    if user_info:
        user_section = rx.vstack(
            rx.divider(color_scheme="gray", margin_y="1rem"),
            rx.hstack(
                rx.avatar(
                    src=user_info.get("avatar"),
                    fallback=user_info.get("name", "U")[0],
                    size="2",
                ),
                rx.vstack(
                    rx.text(
                        user_info.get("name", "User"),
                        size="2",
                        font_weight="500",
                        color="white",
                    ),
                    rx.text(
                        user_info.get("email", ""),
                        size="1",
                        color=get_theme_color("gray", "500"),
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.spacer(),
                align="center",
                spacing="3",
                width="100%",
            ),
            padding="0 1rem 1rem",
            width="100%",
        )

    return rx.box(
        rx.vstack(
            brand_section,
            nav_section,
            rx.spacer(),
            user_section if user_section else rx.fragment(),
            spacing="0",
            height="100vh",
            width="100%",
        ),
        width="280px",
        background=get_theme_color("gray", "900"),
        border_right=f"1px solid {get_theme_color('gray', '700')}",
        flex_shrink="0",
        **props,
    )


def top_navigation(
    title: str,
    subtitle: Optional[str] = None,
    actions: Optional[List[rx.Component]] = None,
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    search_enabled: bool = True,
    **props,
) -> rx.Component:
    """Modern top navigation bar with title, breadcrumbs, and actions.

    Args:
        title: Page title
        subtitle: Optional page subtitle
        actions: Optional action components (buttons, etc.)
        breadcrumbs: Optional breadcrumb navigation
        search_enabled: Whether to show search bar
        **props: Additional styling props
    """
    # Breadcrumbs component
    breadcrumb_component = None
    if breadcrumbs:
        breadcrumb_items = []
        for i, crumb in enumerate(breadcrumbs):
            if i > 0:
                breadcrumb_items.append(
                    rx.text(
                        "/",
                        color=get_theme_color("gray", "500"),
                        font_size="0.875rem",
                    )
                )

            is_last = i == len(breadcrumbs) - 1
            breadcrumb_items.append(
                rx.link(
                    crumb["label"],
                    href=crumb.get("href", "#"),
                    color=get_theme_color("gray", "400") if not is_last else "white",
                    font_size="0.875rem",
                    font_weight="500" if is_last else "400",
                    text_decoration="none",
                    _hover={"color": "white"} if not is_last else {},
                )
            )

        breadcrumb_component = rx.hstack(
            *breadcrumb_items,
            spacing="2",
            align="center",
        )

    # Search component
    search_component = None
    if search_enabled:
        search_component = rx.hstack(
            rx.text("🔍", font_size="1rem", color=get_theme_color("gray", "500")),
            rx.input(
                placeholder="Search...",
                border="none",
                background="transparent",
                color=get_theme_color("gray", "300"),
                font_size="0.875rem",
                flex="1",
                _focus={"outline": "none"},
                _placeholder={"color": get_theme_color("gray", "500")},
            ),
            background=get_theme_color("gray", "800"),
            border=f"1px solid {get_theme_color('gray', '600')}",
            border_radius="0.5rem",
            padding="0.5rem 0.75rem",
            width="300px",
            align="center",
            spacing="2",
            _focus_within={
                "border_color": get_theme_color("primary", "500"),
                "box_shadow": f"0 0 0 2px {get_theme_color('primary', '500')}20",
            },
        )

    return rx.hstack(
        # Title section
        rx.vstack(
            rx.cond(
                breadcrumb_component,
                breadcrumb_component,
                rx.fragment(),
            ),
            rx.text(
                title,
                size="6",
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
        # Search and actions
        rx.hstack(
            search_component if search_component else rx.fragment(),
            rx.cond(
                actions,
                rx.hstack(*actions, spacing="2"),
                rx.fragment(),
            ),
            align="center",
            spacing="4",
        ),
        align="center",
        padding="1.5rem 2rem",
        background=get_theme_color("gray", "900"),
        border_bottom=f"1px solid {get_theme_color('gray', '700')}",
        width="100%",
        **props,
    )
