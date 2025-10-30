'''Defines the main layout structure for all pages in the application.

This module provides a decorator that wraps page components to ensure a
consistent layout, including the navigation sidebar.
'''

import reflex as rx
from functools import wraps
from components.sidebar import sidebar


def main_layout(page_function):
    """A decorator to wrap a page component in the main application layout.

    This decorator adds the sidebar to the left of the page content and applies
    consistent padding and margins to ensure a uniform look and feel across
    all pages.

    Args:
        page_function: The function that returns the page's `rx.Component`.

    Returns:
        A new function that returns the page component wrapped in the layout.
    """
    @wraps(page_function)
    def wrapper(*args, **kwargs) -> rx.Component:
        # Call the original page function to get its content
        page_content = page_function(*args, **kwargs)
        
        # Wrap the content in the main layout structure
        return rx.box(
            sidebar(),
            rx.box(
                page_content,
                padding="2rem",
                margin_left="250px",  # This must match the sidebar width
            ),
        )
    
    return wrapper
