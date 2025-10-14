"""DuckDB database management."""

import duckdb
import polars as pl
from pathlib import Path
from typing import Optional


class Database:
    """DuckDB database wrapper for storing and querying market data."""
    
    def __init__(self, db_path: str = "data/quant.duckdb"):
        """Initialize database connection.
        
        Args:
            db_path: Path to the DuckDB database file
        """
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create database tables if they don't exist."""
        # OHLCV data table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ohlcv (
                ticker VARCHAR NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume BIGINT,
                adjusted_close DOUBLE,
                PRIMARY KEY (ticker, timestamp)
            )
        """)
        
        # Ticker metadata
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tickers (
                ticker VARCHAR PRIMARY KEY,
                name VARCHAR,
                sector VARCHAR,
                industry VARCHAR,
                market_cap DOUBLE,
                last_updated TIMESTAMP
            )
        """)
        
        # Strategy runs/backtests
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS backtest_runs (
                run_id VARCHAR PRIMARY KEY,
                strategy_name VARCHAR,
                start_date DATE,
                end_date DATE,
                initial_capital DOUBLE,
                final_value DOUBLE,
                total_return DOUBLE,
                sharpe_ratio DOUBLE,
                max_drawdown DOUBLE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Trades from backtests
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                trade_id VARCHAR PRIMARY KEY,
                run_id VARCHAR,
                ticker VARCHAR,
                timestamp TIMESTAMP,
                side VARCHAR,
                quantity DOUBLE,
                price DOUBLE,
                commission DOUBLE,
                pnl DOUBLE,
                FOREIGN KEY (run_id) REFERENCES backtest_runs(run_id)
            )
        """)
    
    def insert_ohlcv(self, df: pl.DataFrame):
        """Insert OHLCV data into database.
        
        Args:
            df: Polars DataFrame with columns: ticker, timestamp, open, high, low, close, volume
        """
        self.conn.execute("""
            INSERT OR REPLACE INTO ohlcv 
            SELECT * FROM df
        """)
    
    def get_ohlcv(
        self, 
        ticker: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pl.DataFrame:
        """Retrieve OHLCV data for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            
        Returns:
            Polars DataFrame with OHLCV data
        """
        query = "SELECT * FROM ohlcv WHERE ticker = ?"
        params = [ticker]
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp"
        
        result = self.conn.execute(query, params).pl()
        return result
    
    def get_multiple_tickers(
        self, 
        tickers: list[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pl.DataFrame:
        """Retrieve OHLCV data for multiple tickers.
        
        Args:
            tickers: List of stock ticker symbols
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            
        Returns:
            Polars DataFrame with OHLCV data for all tickers
        """
        placeholders = ",".join(["?" for _ in tickers])
        query = f"SELECT * FROM ohlcv WHERE ticker IN ({placeholders})"
        params = tickers
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY ticker, timestamp"
        
        result = self.conn.execute(query, params).pl()
        return result
    
    def save_backtest_run(self, run_data: dict):
        """Save backtest run results.
        
        Args:
            run_data: Dictionary with backtest run information
        """
        self.conn.execute("""
            INSERT INTO backtest_runs 
            (run_id, strategy_name, start_date, end_date, initial_capital, 
             final_value, total_return, sharpe_ratio, max_drawdown)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            run_data["run_id"],
            run_data["strategy_name"],
            run_data["start_date"],
            run_data["end_date"],
            run_data["initial_capital"],
            run_data["final_value"],
            run_data["total_return"],
            run_data["sharpe_ratio"],
            run_data["max_drawdown"]
        ])
    
    def save_trades(self, trades_df: pl.DataFrame):
        """Save trades from a backtest.
        
        Args:
            trades_df: Polars DataFrame with trade information
        """
        self.conn.execute("INSERT INTO trades SELECT * FROM trades_df")
    
    def get_backtest_runs(self, limit: int = 100) -> pl.DataFrame:
        """Get recent backtest runs.
        
        Args:
            limit: Maximum number of runs to return
            
        Returns:
            Polars DataFrame with backtest run information
        """
        return self.conn.execute(
            "SELECT * FROM backtest_runs ORDER BY created_at DESC LIMIT ?",
            [limit]
        ).pl()
    
    def close(self):
        """Close database connection."""
        self.conn.close()
