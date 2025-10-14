"""The sidebar component for the application."""

import reflex as rx

def sidebar_item(text: str, url: str) -> rx.Component:
    """A single item in the sidebar."""
    return rx.link(
        rx.hstack(rx.text(text)),
        href=url,
        width="100%",
        padding="0.5rem",
        border_radius="0.5rem",
        _hover={
            "background_color": rx.color("gray", 4),
        },
    )

def sidebar() -> rx.Component:
    """The sidebar component."""
    return rx.vstack(
        rx.vstack(
            rx.heading("Quant Dashboard", size="6"),
            rx.divider(),
            sidebar_item("📊 Stock Overview", "/"),
            sidebar_item("🔬 Backtesting", "/backtest"),
            sidebar_item("💼 Portfolio", "/portfolio"),
            sidebar_item("⚠️ Risk Analysis", "/risk"),
            rx.spacer(),
            rx.text("Built with Reflex", size="1", color="gray"),
            width="100%",
            height="100%",
            spacing="4",
            align_items="flex-start",
        ),
        position="fixed",
        left="0px",
        top="0px",
        z_index="5",
        height="100%",
        width="250px",
        padding="1rem",
        background_color=rx.color("gray", 2),
        border_right=f"1px solid {rx.color('gray', 5)}",
    )
