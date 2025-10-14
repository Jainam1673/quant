"""Defines the main layout for the application."""

import reflex as rx
from functools import wraps
from components.sidebar import sidebar


def main_layout(page_function):
    """Decorator for applying the main layout to a page.

    Args:
        page_function: The page function to wrap.

    Returns:
        Wrapped page function with layout applied.
    """
    @wraps(page_function)
    def wrapper(*args, **kwargs) -> rx.Component:
        # Call the page function to get its content
        page_content = page_function(*args, **kwargs)
        
        # Wrap it in the layout
        return rx.box(
            sidebar(),
            rx.box(
                page_content,
                padding="2rem",
                margin_left="250px",  # Same as sidebar width
            ),
        )
    
    return wrapper
