#!/usr/bin/env python3
"""
Example script showing how to use python-etf-db-service.
Run with: python3 example.py
"""

import sys
import os

# Add src to path so we can import without installing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from python_etf_db_service.etf import ETF, load_etfs


def main():
    print("=" * 60)
    print("python-etf-db-service Example")
    print("=" * 60)
    print()
    print("Note: This uses cloudscraper to bypass Cloudflare protection.")
    print("=" * 60)
    print()

    # Example 1: List available ETFs
    print("Example 1: List first 20 available ETFs")
    print("-" * 60)
    etfs = load_etfs()
    print(f"Total ETFs available: {len(etfs)}")
    print(f"First 20: {etfs[:20]}")
    print()

    # Example 2: Get basic info for an ETF
    print("Example 2: Get basic info for SPY")
    print("-" * 60)
    print("Fetching data for SPY...")
    spy = ETF('SPY')

    vitals = spy.info['vitals']
    print(f"Name: {vitals.get('etf_name', 'N/A')}")
    print(f"Issuer: {vitals.get('issuer', 'N/A')}")
    print(f"Expense Ratio: {vitals.get('expense_ratio', 'N/A')}")
    print(f"Inception: {vitals.get('inception', 'N/A')}")
    print()

    # Example 3: Get top holdings
    print("Example 3: Top 5 holdings")
    print("-" * 60)
    holdings = spy.holdings.get('top_holdings', [])
    for i, holding in enumerate(holdings[:5], 1):
        symbol = holding.get('symbol', 'N/A')
        name = holding.get('holding', 'N/A')
        share = holding.get('share', 'N/A')
        print(f"{i}. {symbol:6} - {name:40} ({share})")
    print()

    # Example 4: Get performance metrics
    print("Example 4: Performance metrics")
    print("-" * 60)
    performance = spy.performance
    for metric in performance[:3]:  # Show first 3 metrics
        for key, value in metric.items():
            if 'return' in key:
                print(f"{key.replace('_', ' ').title():20}: {value}")
    print()

    print("=" * 60)
    print("For more examples, see USAGE.md")
    print("To use the CLI, install with: pip install -e .")
    print("Then run: pyetfdb SPY")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: This script requires internet connection to scrape data from ETFDB.com")
        sys.exit(1)
