"""Defines the main layout for the application."""

import reflex as rx
from components.sidebar import sidebar

def main_layout(child: rx.Component) -> rx.Component:
    """The main layout for the application.

    Args:
        child: The child component to render.

    Returns:
        The main layout component.
    """
    return rx.box(
        sidebar(),
        rx.box(
            child,
            padding="2rem",
            margin_left="250px",  # Same as sidebar width
        ),
    )
