"""DuckDB database management for market data and backtest results.

This module provides a `Database` class that serves as a high-level wrapper
around DuckDB. It is designed for efficient storage and retrieval of financial
time-series data, including OHLCV prices, backtest runs, and individual trades.
"""

from pathlib import Path

import duckdb
import polars as pl

from quant.utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    """A DuckDB database wrapper for storing and querying financial data.

    This class handles the connection to a DuckDB database file and provides
    methods to create the schema, insert data, and query it efficiently using
    Polars DataFrames.

    Args:
        db_path (str): The file path for the DuckDB database.
    """

    def __init__(self, db_path: str = "data/quant.duckdb"):
        """Initializes the database connection and ensures the schema is created."""
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Creates the necessary tables for the application if they do not exist."""
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

    def insert_ohlcv(self, df: pl.DataFrame) -> None:
        """Inserts or replaces OHLCV data in the database.

        This method performs an 'upsert' operation, inserting new rows and
        replacing existing ones based on the primary key (ticker, timestamp).

        Args:
            df: A Polars DataFrame containing OHLCV data.

        Raises:
            ValueError: If the DataFrame is missing required columns.
        """
        required_columns = {"ticker", "timestamp", "open", "high", "low", "close", "volume"}
        missing = required_columns.difference(df.columns)
        if missing:
            msg = f"Missing required OHLCV columns: {sorted(missing)}"
            raise ValueError(msg)

        if "adjusted_close" not in df.columns:
            df = df.with_columns(pl.lit(None).cast(pl.Float64).alias("adjusted_close"))

        # Ensure timestamp column is proper datetime for DuckDB compatibility
        if df["timestamp"].dtype == pl.Utf8:
            df = df.with_columns(pl.col("timestamp").str.strptime(pl.Datetime, strict=False))

        temp_df = df.select(
            [
                "ticker",
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "adjusted_close",
            ]
        )

        self.conn.register("temp_df", temp_df)
        self.conn.execute(
            """
            INSERT OR REPLACE INTO ohlcv (ticker, timestamp, open, high, low, close, volume, adjusted_close)
            SELECT * FROM temp_df
            """,
        )
        self.conn.unregister("temp_df")

    def get_ohlcv(
        self,
        ticker: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> pl.DataFrame:
        """Retrieves OHLCV data for a specific ticker and date range.

        Args:
            ticker: The stock ticker symbol to query.
            start_date: The start date in 'YYYY-MM-DD' format (inclusive).
            end_date: The end date in 'YYYY-MM-DD' format (inclusive).

        Returns:
            A Polars DataFrame with the requested OHLCV data, sorted by timestamp.
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

        return self.conn.execute(query, params).pl()

    def get_multiple_tickers(
        self,
        tickers: list[str],
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> pl.DataFrame:
        """Retrieves OHLCV data for a list of tickers.

        Args:
            tickers: A list of stock ticker symbols.
            start_date: The start date in 'YYYY-MM-DD' format.
            end_date: The end date in 'YYYY-MM-DD' format.

        Returns:
            A Polars DataFrame containing the data for all requested tickers.
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

        return self.conn.execute(query, params).pl()

    def save_backtest_run(self, run_data: dict) -> None:
        """Saves the summary results of a single backtest run.

        Args:
            run_data: A dictionary containing the backtest result metrics.
        """
        self.conn.execute(
            """
            INSERT INTO backtest_runs
            (run_id, strategy_name, start_date, end_date, initial_capital,
             final_value, total_return, sharpe_ratio, max_drawdown)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            [
                run_data["run_id"],
                run_data["strategy_name"],
                run_data["start_date"],
                run_data["end_date"],
                run_data["initial_capital"],
                run_data["final_value"],
                run_data["total_return"],
                run_data["sharpe_ratio"],
                run_data["max_drawdown"],
            ],
        )

    def save_trades(self, trades_df: pl.DataFrame) -> None:
        """Saves the individual trades from a backtest run.

        Args:
            trades_df: A Polars DataFrame of trades.
        """
        self.conn.execute("INSERT INTO trades SELECT * FROM trades_df")

    def get_backtest_runs(self, limit: int = 100) -> pl.DataFrame:
        """Retrieves a summary of recent backtest runs.

        Args:
            limit: The maximum number of runs to retrieve.

        Returns:
            A Polars DataFrame of backtest run summaries.
        """
        return self.conn.execute(
            "SELECT * FROM backtest_runs ORDER BY created_at DESC LIMIT ?",
            [limit],
        ).pl()

    def close(self) -> None:
        """Closes the database connection gracefully."""
        self.conn.close()
