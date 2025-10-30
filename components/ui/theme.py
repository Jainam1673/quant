"""Modern theme configuration for the Quant Trading Platform.

Defines a professional, dark-first theme optimized for financial data visualization
with excellent accessibility and visual hierarchy.
"""

import reflex as rx
from typing import Dict, Any

# Color palette optimized for financial data
colors = {
    # Primary brand colors
    "primary": {
        "50": "#f0f9ff",
        "100": "#e0f2fe",
        "200": "#bae6fd",
        "300": "#7dd3fc",
        "400": "#38bdf8",
        "500": "#0ea5e9",  # Main brand color
        "600": "#0284c7",
        "700": "#0369a1",
        "800": "#075985",
        "900": "#0c4a6e",
    },
    # Success/Profit colors
    "success": {
        "50": "#f0fdf4",
        "100": "#dcfce7",
        "200": "#bbf7d0",
        "300": "#86efac",
        "400": "#4ade80",
        "500": "#22c55e",  # Main success
        "600": "#16a34a",
        "700": "#15803d",
        "800": "#166534",
        "900": "#14532d",
    },
    # Error/Loss colors
    "error": {
        "50": "#fef2f2",
        "100": "#fee2e2",
        "200": "#fecaca",
        "300": "#fca5a5",
        "400": "#f87171",
        "500": "#ef4444",  # Main error
        "600": "#dc2626",
        "700": "#b91c1c",
        "800": "#991b1b",
        "900": "#7f1d1d",
    },
    # Warning colors
    "warning": {
        "50": "#fffbeb",
        "100": "#fef3c7",
        "200": "#fde68a",
        "300": "#fcd34d",
        "400": "#fbbf24",
        "500": "#f59e0b",  # Main warning
        "600": "#d97706",
        "700": "#b45309",
        "800": "#92400e",
        "900": "#78350f",
    },
    # Neutral grays (dark theme optimized)
    "gray": {
        "50": "#fafafa",
        "100": "#f4f4f5",
        "200": "#e4e4e7",
        "300": "#d4d4d8",
        "400": "#a1a1aa",
        "500": "#71717a",
        "600": "#52525b",
        "700": "#3f3f46",
        "800": "#27272a",
        "900": "#18181b",
        "950": "#09090b",
    },
}

# Spacing system
spacing = {
    "xs": "0.25rem",  # 4px
    "sm": "0.5rem",  # 8px
    "md": "1rem",  # 16px
    "lg": "1.5rem",  # 24px
    "xl": "2rem",  # 32px
    "2xl": "3rem",  # 48px
    "3xl": "4rem",  # 64px
    "4xl": "6rem",  # 96px
}

# Typography scale
typography = {
    "font_family": {
        "sans": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
        "mono": "JetBrains Mono, Fira Code, Monaco, Consolas, monospace",
    },
    "font_size": {
        "xs": "0.75rem",  # 12px
        "sm": "0.875rem",  # 14px
        "base": "1rem",  # 16px
        "lg": "1.125rem",  # 18px
        "xl": "1.25rem",  # 20px
        "2xl": "1.5rem",  # 24px
        "3xl": "1.875rem",  # 30px
        "4xl": "2.25rem",  # 36px
        "5xl": "3rem",  # 48px
    },
    "line_height": {
        "tight": "1.25",
        "normal": "1.5",
        "relaxed": "1.75",
    },
}

# Shadows and effects
shadows = {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
    "glow": "0 0 20px rgb(14 165 233 / 0.5)",
}

# Border radius
radius = {
    "sm": "0.25rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "full": "9999px",
}

# Animation configuration
animations = {
    "duration": {
        "fast": "150ms",
        "normal": "300ms",
        "slow": "500ms",
    },
    "easing": {
        "ease_in": "cubic-bezier(0.4, 0, 1, 1)",
        "ease_out": "cubic-bezier(0, 0, 0.2, 1)",
        "ease_in_out": "cubic-bezier(0.4, 0, 0.2, 1)",
    },
}

# Reflex theme configuration
theme_config = rx.theme(
    appearance="dark",
    has_background=True,
    radius="large",
    accent_color="blue",
    gray_color="slate",
    panel_background="solid",
    scaling="100%",
)

# Component default styles
component_styles = {
    "card": {
        "background": colors["gray"]["900"],
        "border": f"1px solid {colors['gray']['700']}",
        "border_radius": radius["lg"],
        "box_shadow": shadows["md"],
        "padding": spacing["lg"],
    },
    "button_primary": {
        "background": colors["primary"]["600"],
        "color": "white",
        "border": "none",
        "border_radius": radius["md"],
        "padding": f"{spacing['sm']} {spacing['md']}",
        "font_weight": "600",
        "transition": f"all {animations['duration']['normal']} {animations['easing']['ease_out']}",
        "_hover": {
            "background": colors["primary"]["700"],
            "transform": "translateY(-1px)",
            "box_shadow": shadows["lg"],
        },
    },
    "button_secondary": {
        "background": "transparent",
        "color": colors["gray"]["300"],
        "border": f"1px solid {colors['gray']['600']}",
        "border_radius": radius["md"],
        "padding": f"{spacing['sm']} {spacing['md']}",
        "font_weight": "500",
        "transition": f"all {animations['duration']['normal']} {animations['easing']['ease_out']}",
        "_hover": {
            "background": colors["gray"]["800"],
            "border_color": colors["gray"]["500"],
        },
    },
    "input": {
        "background": colors["gray"]["800"],
        "border": f"1px solid {colors['gray']['600']}",
        "border_radius": radius["md"],
        "padding": f"{spacing['sm']} {spacing['md']}",
        "color": colors["gray"]["100"],
        "font_size": typography["font_size"]["base"],
        "_focus": {
            "outline": "none",
            "border_color": colors["primary"]["500"],
            "box_shadow": f"0 0 0 2px {colors['primary']['500']}40",
        },
        "_placeholder": {
            "color": colors["gray"]["500"],
        },
    },
}


def get_theme_color(color_name: str, shade: str = "500") -> str:
    """Get a color value from the theme."""
    return colors.get(color_name, {}).get(shade, colors["gray"]["500"])


def get_component_style(component_name: str) -> Dict[str, Any]:
    """Get default styles for a component."""
    return component_styles.get(component_name, {})
