"""Data manager for fetching and storing market data."""

import yfinance as yf
import polars as pl
from datetime import datetime, timedelta
from typing import Optional
from .database import Database


class DataManager:
    """Manages data fetching, caching, and storage."""
    
    def __init__(self, db: Optional[Database] = None):
        """Initialize data manager.
        
        Args:
            db: Database instance for data persistence
        """
        self.db = db or Database()
    
    def fetch_and_store(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d",
        force_update: bool = False
    ) -> pl.DataFrame:
        """Fetch data from yfinance and store in database.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            force_update: Force fetching new data even if cached
            
        Returns:
            Polars DataFrame with OHLCV data
        """
        # Check if we have recent data in cache
        if not force_update:
            cached_data = self.db.get_ohlcv(ticker)
            if not cached_data.is_empty():
                last_date = cached_data["timestamp"].max()
                if (datetime.now() - last_date).days < 1:
                    return cached_data
        
        # Fetch from yfinance
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        # Convert to Polars and clean
        df_reset = df.reset_index()
        pl_df = pl.from_pandas(df_reset)
        
        # Standardize column names
        pl_df = pl_df.rename({
            "Date": "timestamp",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })
        
        # Add ticker column
        pl_df = pl_df.with_columns(
            pl.lit(ticker).alias("ticker")
        )
        
        # Select and order columns
        pl_df = pl_df.select([
            "ticker",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ])
        
        # Store in database
        self.db.insert_ohlcv(pl_df)
        
        return pl_df
    
    def fetch_multiple(
        self,
        tickers: list[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> pl.DataFrame:
        """Fetch data for multiple tickers.
        
        Args:
            tickers: List of stock ticker symbols
            period: Time period
            interval: Data interval
            
        Returns:
            Polars DataFrame with OHLCV data for all tickers
        """
        all_data = []
        
        for ticker in tickers:
            try:
                df = self.fetch_and_store(ticker, period, interval)
                all_data.append(df)
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
                continue
        
        if not all_data:
            return pl.DataFrame()
        
        return pl.concat(all_data)
    
    def get_cached_data(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pl.DataFrame:
        """Get data from cache/database.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Polars DataFrame with cached data
        """
        return self.db.get_ohlcv(ticker, start_date, end_date)
    
    def get_latest_price(self, ticker: str) -> float:
        """Get the most recent close price for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Latest close price
        """
        df = self.fetch_and_store(ticker, period="1d")
        return float(df["close"][-1])
