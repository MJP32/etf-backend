#!/usr/bin/env python3
"""
Script to pre-populate the ETF cache with data for popular ETFs.
Run this overnight or as a cron job to keep cache fresh.

Usage:
    python scripts/populate_cache.py
    python scripts/populate_cache.py --limit 50  # Only cache first 50 ETFs
    python scripts/populate_cache.py --force     # Re-scrape even if cached
"""

import argparse
import time
import logging
from pathlib import Path
import sys

# Add src to path so we can import python_etf_db_service
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from python_etf_db_service.etf import ETF, load_etfs
from python_etf_db_service.cache import get_cache

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def populate_cache(limit: int = None, force: bool = False, delay: int = 10):
    """
    Populate cache with ETF data.

    Args:
        limit: Maximum number of ETFs to cache (None for all)
        force: Force re-scrape even if already cached
        delay: Delay in seconds between requests (to be nice to the server)
    """
    cache = get_cache()
    all_etfs = load_etfs()

    if limit:
        etfs_to_cache = all_etfs[:limit]
        logger.info(f"Caching first {limit} ETFs")
    else:
        etfs_to_cache = all_etfs
        logger.info(f"Caching all {len(etfs_to_cache)} ETFs")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for i, ticker in enumerate(etfs_to_cache, 1):
        try:
            # Check if already cached
            if not force and cache.get(ticker):
                logger.info(f"[{i}/{len(etfs_to_cache)}] {ticker}: Already cached, skipping")
                skipped_count += 1
                continue

            logger.info(f"[{i}/{len(etfs_to_cache)}] {ticker}: Scraping...")

            # Scrape the data
            etf = ETF(ticker)
            data = etf.to_dict()

            # Store in cache
            cache.set(ticker, data)

            success_count += 1
            logger.info(f"[{i}/{len(etfs_to_cache)}] {ticker}: ✓ Cached successfully")

            # Be nice to the server - add delay between requests
            if i < len(etfs_to_cache):
                time.sleep(delay)

        except Exception as e:
            error_count += 1
            logger.error(f"[{i}/{len(etfs_to_cache)}] {ticker}: ✗ Error: {str(e)}")
            # Continue with next ETF even if one fails
            continue

    # Print summary
    logger.info("=" * 60)
    logger.info("CACHE POPULATION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total ETFs processed: {len(etfs_to_cache)}")
    logger.info(f"Successfully cached: {success_count}")
    logger.info(f"Skipped (already cached): {skipped_count}")
    logger.info(f"Errors: {error_count}")
    logger.info("=" * 60)

    # Print cache stats
    stats = cache.get_stats()
    logger.info(f"Cache statistics:")
    logger.info(f"  Total entries: {stats['total_entries']}")
    logger.info(f"  Fresh entries: {stats['fresh_entries']}")
    logger.info(f"  Expired entries: {stats['expired_entries']}")


def main():
    parser = argparse.ArgumentParser(
        description="Pre-populate ETF cache with scraped data"
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Maximum number of ETFs to cache (default: all)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-scrape even if already cached'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=10,
        help='Delay in seconds between requests (default: 10)'
    )

    args = parser.parse_args()

    logger.info("Starting cache population...")
    populate_cache(
        limit=args.limit,
        force=args.force,
        delay=args.delay
    )
    logger.info("Cache population complete!")


if __name__ == "__main__":
    main()
