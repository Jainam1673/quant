"""Modern form components with excellent UX and validation.

Professional form controls optimized for financial data input
with consistent styling and validation.
"""

import reflex as rx
from typing import Optional, List, Dict, Any, Callable
from .theme import get_component_style, get_theme_color


def form_input(
    label: str,
    placeholder: Optional[str] = None,
    value: str = "",
    on_change: Optional[Callable] = None,
    error: Optional[str] = None,
    help_text: Optional[str] = None,
    required: bool = False,
    disabled: bool = False,
    input_type: str = "text",
    **props,
) -> rx.Component:
    """Modern form input with label, validation, and help text.

    Args:
        label: Input label
        placeholder: Placeholder text
        value: Input value
        on_change: Change handler
        error: Error message
        help_text: Help/description text
        required: Whether input is required
        disabled: Whether input is disabled
        input_type: Input type (text, number, email, etc.)
        **props: Additional input props
    """
    # Label with required indicator
    label_element = rx.text(
        label,
        rx.cond(
            required,
            rx.text(" *", color=get_theme_color("error", "400")),
            rx.fragment(),
        ),
        size="2",
        font_weight="500",
        color=get_theme_color("gray", "300"),
        margin_bottom="0.5rem",
    )

    # Input with error state styling
    input_styles = get_component_style("input").copy()
    if error:
        input_styles.update(
            {
                "border_color": get_theme_color("error", "500"),
                "_focus": {
                    "outline": "none",
                    "border_color": get_theme_color("error", "500"),
                    "box_shadow": f"0 0 0 2px {get_theme_color('error', '500')}40",
                },
            }
        )

    input_element = rx.input(
        placeholder=placeholder or f"Enter {label.lower()}",
        value=value,
        on_change=on_change,
        disabled=disabled,
        type=input_type,
        **{**input_styles, **props},
    )

    # Error message
    error_element = None
    if error:
        error_element = rx.text(
            error,
            size="1",
            color=get_theme_color("error", "400"),
            margin_top="0.25rem",
        )

    # Help text
    help_element = None
    if help_text:
        help_element = rx.text(
            help_text,
            size="1",
            color=get_theme_color("gray", "500"),
            margin_top="0.25rem",
        )

    return rx.vstack(
        label_element,
        input_element,
        error_element or rx.fragment(),
        help_element or rx.fragment(),
        align="start",
        spacing="0",
        width="100%",
    )


def form_select(
    label: str,
    options: List[Dict[str, str]],
    value: str = "",
    on_change: Optional[Callable] = None,
    placeholder: str = "Select an option",
    error: Optional[str] = None,
    help_text: Optional[str] = None,
    required: bool = False,
    disabled: bool = False,
    **props,
) -> rx.Component:
    """Modern select dropdown with label and validation.

    Args:
        label: Select label
        options: List of option dicts with 'value' and 'label' keys
        value: Selected value
        on_change: Change handler
        placeholder: Placeholder text
        error: Error message
        help_text: Help text
        required: Whether select is required
        disabled: Whether select is disabled
        **props: Additional select props
    """
    # Label with required indicator
    label_element = rx.text(
        label,
        rx.cond(
            required,
            rx.text(" *", color=get_theme_color("error", "400")),
            rx.fragment(),
        ),
        size="2",
        font_weight="500",
        color=get_theme_color("gray", "300"),
        margin_bottom="0.5rem",
    )

    # Select with error state styling
    select_styles = {
        "background": get_theme_color("gray", "800"),
        "border": f"1px solid {get_theme_color('gray', '600')}",
        "border_radius": "0.375rem",
        "padding": "0.5rem 1rem",
        "color": get_theme_color("gray", "100"),
        "font_size": "1rem",
        "_focus": {
            "outline": "none",
            "border_color": get_theme_color("primary", "500"),
            "box_shadow": f"0 0 0 2px {get_theme_color('primary', '500')}40",
        },
    }

    if error:
        select_styles.update(
            {
                "border_color": get_theme_color("error", "500"),
                "_focus": {
                    "outline": "none",
                    "border_color": get_theme_color("error", "500"),
                    "box_shadow": f"0 0 0 2px {get_theme_color('error', '500')}40",
                },
            }
        )

    select_element = rx.select(
        options,
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        disabled=disabled,
        **{**select_styles, **props},
    )

    # Error message
    error_element = None
    if error:
        error_element = rx.text(
            error,
            size="1",
            color=get_theme_color("error", "400"),
            margin_top="0.25rem",
        )

    # Help text
    help_element = None
    if help_text:
        help_element = rx.text(
            help_text,
            size="1",
            color=get_theme_color("gray", "500"),
            margin_top="0.25rem",
        )

    return rx.vstack(
        label_element,
        select_element,
        error_element or rx.fragment(),
        help_element or rx.fragment(),
        align="start",
        spacing="0",
        width="100%",
    )


def form_checkbox(
    label: str,
    checked: bool = False,
    on_change: Optional[Callable] = None,
    description: Optional[str] = None,
    disabled: bool = False,
    **props,
) -> rx.Component:
    """Modern checkbox with label and description.

    Args:
        label: Checkbox label
        checked: Whether checkbox is checked
        on_change: Change handler
        description: Optional description
        disabled: Whether checkbox is disabled
        **props: Additional checkbox props
    """
    return rx.hstack(
        rx.checkbox(
            checked=checked, on_change=on_change, disabled=disabled, color_scheme="blue", **props
        ),
        rx.vstack(
            rx.text(
                label,
                size="2",
                font_weight="500",
                color=get_theme_color("gray", "300"),
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
        ),
        align="start",
        spacing="3",
    )


def form_range_slider(
    label: str,
    min_value: float = 0,
    max_value: float = 100,
    value: float = 50,
    step: float = 1,
    on_change: Optional[Callable] = None,
    show_value: bool = True,
    **props,
) -> rx.Component:
    """Modern range slider with label and value display.

    Args:
        label: Slider label
        min_value: Minimum value
        max_value: Maximum value
        value: Current value
        step: Step size
        on_change: Change handler
        show_value: Whether to show current value
        **props: Additional slider props
    """
    return rx.vstack(
        rx.hstack(
            rx.text(
                label,
                size="2",
                font_weight="500",
                color=get_theme_color("gray", "300"),
            ),
            rx.spacer(),
            rx.cond(
                show_value,
                rx.badge(
                    str(value),
                    color_scheme="blue",
                    variant="soft",
                ),
                rx.fragment(),
            ),
            width="100%",
            align="center",
        ),
        rx.slider(
            min=min_value,
            max=max_value,
            step=step,
            value=value,
            on_change=on_change,
            color_scheme="blue",
            **props,
        ),
        align="start",
        spacing="2",
        width="100%",
    )


def form_button(
    text: str,
    variant: str = "primary",  # "primary", "secondary", "danger"
    size: str = "md",  # "sm", "md", "lg"
    loading: bool = False,
    disabled: bool = False,
    icon: Optional[str] = None,
    on_click: Optional[Callable] = None,
    **props,
) -> rx.Component:
    """Modern button with variants and states.

    Args:
        text: Button text
        variant: Button variant
        size: Button size
        loading: Loading state
        disabled: Disabled state
        icon: Optional icon
        on_click: Click handler
        **props: Additional button props
    """
    # Size configurations
    size_configs = {
        "sm": {"size": "1", "padding": "0.375rem 0.75rem"},
        "md": {"size": "2", "padding": "0.5rem 1rem"},
        "lg": {"size": "3", "padding": "0.75rem 1.5rem"},
    }

    size_config = size_configs.get(size, size_configs["md"])

    # Variant styles
    variant_styles = {
        "primary": get_component_style("button_primary"),
        "secondary": get_component_style("button_secondary"),
        "danger": {
            "background": get_theme_color("error", "600"),
            "color": "white",
            "_hover": {"background": get_theme_color("error", "700")},
        },
    }

    button_styles = variant_styles.get(variant, variant_styles["primary"])
    button_styles.update(size_config)

    # Button content with optional icon and loading
    content = []

    if loading:
        content.append(rx.spinner(size="1"))
    elif icon:
        content.append(rx.text(icon))

    content.append(rx.text(text, font_weight="500"))

    return rx.button(
        rx.hstack(*content, spacing="2", align="center"),
        on_click=on_click,
        disabled=disabled or loading,
        **{**button_styles, **props},
    )
