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
            rx.heading("Quant Platform", size="6", weight="bold"),
            rx.text("Trading Analytics", size="2", color="gray"),
            rx.divider(margin_y="1rem"),
            
            # Main navigation
            rx.text("Navigation", size="2", weight="bold", color="gray", margin_bottom="0.5rem"),
            sidebar_item("🏠 Dashboard", "/"),
            sidebar_item("📊 Stock Data", "/"),
            
            rx.divider(margin_y="0.5rem"),
            
            # Trading section
            rx.text("Trading", size="2", weight="bold", color="gray", margin_bottom="0.5rem"),
            sidebar_item("🔬 Backtesting", "/backtest"),
            sidebar_item("⚙️ Strategy Builder", "/strategy"),
            
            rx.divider(margin_y="0.5rem"),
            
            # Analytics section
            rx.text("Analytics", size="2", weight="bold", color="gray", margin_bottom="0.5rem"),
            sidebar_item("💼 Portfolio", "/portfolio"),
            sidebar_item("⚠️ Risk Analysis", "/risk"),
            
            rx.spacer(),
            
            # Footer
            rx.vstack(
                rx.divider(margin_y="0.5rem"),
                rx.text("Quantitative Finance", size="1", color="gray", weight="bold"),
                rx.text("Built with Reflex", size="1", color="gray"),
                spacing="1",
                width="100%",
            ),
            
            width="100%",
            height="100%",
            spacing="2",
            align_items="flex-start",
        ),
        position="fixed",
        left="0px",
        top="0px",
        z_index="5",
        height="100%",
        width="250px",
        padding="1.5rem",
        background_color=rx.color("gray", 2),
        border_right=f"2px solid {rx.color('gray', 5)}",
    )
