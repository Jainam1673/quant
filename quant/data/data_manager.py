"""Data manager for fetching, caching, and standardizing market data.

This module provides a `DataManager` class that acts as a high-level interface
for accessing market data. It abstracts the underlying data source (yfinance)
and caching mechanism (Database), providing a simple and efficient way to get
the data needed for backtesting and analysis.
"""

from datetime import datetime

import polars as pl
import yfinance as yf

from quant.utils.logger import get_logger

from .database import Database

logger = get_logger(__name__)


class DataManager:
    """Manages the fetching, caching, and storage of market data.

    This class coordinates between the external data source (yfinance) and the
    local database cache to provide a seamless and efficient data pipeline.

    Args:
        db (Optional[Database]): An instance of the Database class. If not
            provided, a new one will be instantiated.
    """

    def __init__(self, db: Database | None = None):
        """Initializes the DataManager with a database instance."""
        self.db = db or Database()

    def fetch_and_store(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d",
        force_update: bool = False,
    ) -> pl.DataFrame:
        """Fetches data from yfinance and stores it in the database.

        This is the primary method for acquiring data. It first checks the local
        cache for recent data. If the data is not present or is stale, it
        fetches new data from yfinance, standardizes it, and saves it to the
        database before returning it.

        Args:
            ticker: The stock ticker symbol (e.g., "AAPL").
            period: The time period to fetch (e.g., "1y", "5d", "max").
            interval: The data interval (e.g., "1d", "1h", "15m").
            force_update: If True, forces a fetch from the API, ignoring the cache.

        Returns:
            A Polars DataFrame containing the OHLCV data.

        Raises:
            ValueError: If the ticker is invalid or no data is found.
        """
        if not ticker or not isinstance(ticker, str):
            msg = "Invalid ticker: must be a non-empty string"
            raise ValueError(msg)

        ticker = ticker.upper().strip()

        # Check if we have recent data in cache
        if not force_update:
            try:
                cached_data = self.db.get_ohlcv(ticker)
                if not cached_data.is_empty():
                    last_timestamp = cached_data["timestamp"].max()
                    if last_timestamp:
                        # Convert to datetime if needed and check age
                        cache_age = datetime.now() - datetime.fromisoformat(str(last_timestamp))
                        if cache_age.days < 1:
                            logger.info(f"Using cached data for {ticker}")
                            return cached_data
            except Exception as e:
                logger.warning(f"Error checking cache for {ticker}: {e}")

        # Fetch from yfinance
        try:
            logger.info(f"Fetching data for {ticker} from yfinance")
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
        except Exception as e:
            logger.exception(f"Error fetching data from yfinance for {ticker}: {e}")
            msg = f"Failed to fetch data for {ticker}: {e}"
            raise ValueError(msg)

        if df.empty:
            logger.error(f"No data found for ticker: {ticker}")
            msg = f"No data found for ticker: {ticker}"
            raise ValueError(msg)

        # Convert to Polars and clean
        df_reset = df.reset_index()
        pl_df = pl.from_pandas(df_reset)

        # Standardize column names
        pl_df = pl_df.rename(
            {
                "Date": "timestamp",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        # Add ticker column
        pl_df = pl_df.with_columns(
            pl.lit(ticker).alias("ticker"),
        )

        # Select and order columns
        pl_df = pl.select(
            [
                "ticker",
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        )

        # Store in database
        try:
            self.db.insert_ohlcv(pl_df)
            logger.info(f"Successfully stored {len(pl_df)} rows for {ticker}")
        except Exception as e:
            logger.exception(f"Error storing data for {ticker}: {e}")
            raise

        return pl_df

    def fetch_multiple(
        self,
        tickers: list[str],
        period: str = "1y",
        interval: str = "1d",
    ) -> pl.DataFrame:
        """Fetches and stores data for multiple tickers.

        Args:
            tickers: A list of stock ticker symbols.
            period: The time period to fetch.
            interval: The data interval.

        Returns:
            A single Polars DataFrame containing the data for all tickers.
        """
        all_data = []

        for ticker in tickers:
            try:
                df = self.fetch_and_store(ticker, period, interval)
                all_data.append(df)
            except Exception as e:
                logger.exception(f"Error fetching {ticker}: {e}")
                continue

        if not all_data:
            return pl.DataFrame()

        return pl.concat(all_data)

    def get_cached_data(
        self,
        ticker: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> pl.DataFrame:
        """Retrieves data directly from the local database cache.

        Args:
            ticker: The stock ticker symbol.
            start_date: The start date in 'YYYY-MM-DD' format.
            end_date: The end date in 'YYYY-MM-DD' format.

        Returns:
            A Polars DataFrame with the cached data.
        """
        return self.db.get_ohlcv(ticker, start_date, end_date)

    def get_latest_price(self, ticker: str) -> float:
        """Gets the most recent closing price for a ticker.

        This method will fetch data for the last day to ensure the price is current.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            The latest closing price as a float.

        Raises:
            ValueError: If no price data can be found for the ticker.
        """
        try:
            df = self.fetch_and_store(ticker, period="1d")
            if df.is_empty():
                msg = f"No price data available for {ticker}"
                raise ValueError(msg)
            return float(df["close"][-1])
        except Exception as e:
            logger.exception(f"Error getting latest price for {ticker}: {e}")
            raise
