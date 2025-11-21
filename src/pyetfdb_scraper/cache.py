"""
ETF data caching using SQLite.
Stores scraped ETF data to avoid repeated slow web scraping.
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ETFCache:
    """Cache for ETF data using SQLite database."""

    def __init__(self, db_path: str = 'etf_cache.db', cache_hours: int = 24):
        """
        Initialize the ETF cache.

        Args:
            db_path: Path to SQLite database file
            cache_hours: Number of hours before cache expires (default 24)
        """
        self.db_path = db_path
        self.cache_hours = cache_hours
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def _create_tables(self):
        """Create cache tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS etf_cache (
                ticker TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                cached_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        ''')
        self.conn.commit()

    def get(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get ETF data from cache if it exists and is fresh.

        Args:
            ticker: ETF ticker symbol

        Returns:
            Cached ETF data dict or None if not found/expired
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT data, cached_at FROM etf_cache WHERE ticker = ?',
            (ticker.upper(),)
        )
        row = cursor.fetchone()

        if not row:
            logger.info(f"Cache miss for {ticker}: not found")
            return None

        # Check if cache is expired
        cached_at = datetime.fromisoformat(row['cached_at'])
        expiry_time = cached_at + timedelta(hours=self.cache_hours)

        if datetime.now() > expiry_time:
            logger.info(f"Cache miss for {ticker}: expired")
            return None

        logger.info(f"Cache hit for {ticker}")
        return json.loads(row['data'])

    def set(self, ticker: str, data: Dict[str, Any]):
        """
        Store ETF data in cache.

        Args:
            ticker: ETF ticker symbol
            data: ETF data dictionary to cache
        """
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT OR REPLACE INTO etf_cache (ticker, data, cached_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (ticker.upper(), json.dumps(data), now, now))

        self.conn.commit()
        logger.info(f"Cached data for {ticker}")

    def clear(self, ticker: Optional[str] = None):
        """
        Clear cache for a specific ticker or all tickers.

        Args:
            ticker: Ticker to clear, or None to clear all
        """
        cursor = self.conn.cursor()

        if ticker:
            cursor.execute('DELETE FROM etf_cache WHERE ticker = ?', (ticker.upper(),))
            logger.info(f"Cleared cache for {ticker}")
        else:
            cursor.execute('DELETE FROM etf_cache')
            logger.info("Cleared entire cache")

        self.conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        cursor = self.conn.cursor()

        # Total cached entries
        cursor.execute('SELECT COUNT(*) as count FROM etf_cache')
        total = cursor.fetchone()['count']

        # Fresh vs expired
        expiry_threshold = (datetime.now() - timedelta(hours=self.cache_hours)).isoformat()
        cursor.execute(
            'SELECT COUNT(*) as count FROM etf_cache WHERE cached_at > ?',
            (expiry_threshold,)
        )
        fresh = cursor.fetchone()['count']

        return {
            'total_entries': total,
            'fresh_entries': fresh,
            'expired_entries': total - fresh,
            'cache_hours': self.cache_hours
        }

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


# Global cache instance
_cache = None


def get_cache() -> ETFCache:
    """Get or create the global cache instance."""
    global _cache
    if _cache is None:
        _cache = ETFCache()
    return _cache
