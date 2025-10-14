"""The shared application state for the Quant Dashboard."""

import reflex as rx
import yfinance as yf
import polars as pl
import datetime

class State(rx.State):
    """The application state."""
    ticker: str = "AAPL"
    
    # The data for the table, stored as a list of dictionaries.
    data: list[dict] = []
    
    # The columns for the data table.
    table_columns: list[rx.Component] = []

    # Data formatted specifically for the recharts line chart.
    chart_data: list[dict] = []

    is_loading: bool = False

    def set_ticker(self, new_ticker: str):
        """Explicitly set the ticker value."""
        self.ticker = new_ticker

    def fetch_data(self):
        """Fetch stock data from yfinance and update the state."""
        if not self.ticker:
            return

        self.is_loading = True
        try:
            # Download data using yfinance
            raw_data = yf.download(self.ticker, period="1y")

            if raw_data.empty:
                self.is_loading = False
                print(f"No data found for ticker: {self.ticker}")
                return

            # Convert to Polars DataFrame for processing
            polars_df = pl.from_pandas(raw_data.reset_index())

            # Create column definitions for the data table
            self.table_columns = [
                rx.data_table.column(
                    header=col,
                    accessor_key=str(col), # Ensure accessor is a string
                )
                for col in polars_df.columns
            ]
            
            # Convert DataFrame to list of dicts for state storage
            # Also ensure date is in string format for JSON serialization
            dict_data = polars_df.with_columns(pl.col("Date").dt.strftime("%Y-%m-%d")).to_dicts()
            self.data = dict_data
            self.chart_data = dict_data

        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
        finally:
            self.is_loading = False
