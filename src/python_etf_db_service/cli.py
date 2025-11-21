#!/usr/bin/env python
"""Command-line interface for python-etf-db-service."""

import argparse
import json
import sys
from typing import Optional

from python_etf_db_service.etf import ETF, load_etfs


def list_etfs():
    """List all available ETF tickers."""
    etfs = load_etfs()
    print(f"Total available ETFs: {len(etfs)}")
    print("\nFirst 50 ETFs:")
    for i, ticker in enumerate(etfs[:50], 1):
        print(f"  {ticker}", end="")
        if i % 10 == 0:
            print()
    if len(etfs) > 50:
        print(f"\n... and {len(etfs) - 50} more")
    print(f"\nUse: pyetfdb <ticker> to get data for a specific ETF")


def get_etf_data(
    ticker: str,
    data_type: Optional[str] = None,
    output_format: str = "pretty"
):
    """Get ETF data for a specific ticker."""
    try:
        print(f"Fetching data for {ticker}...\n")
        etf = ETF(ticker.upper())

        if data_type == "info":
            data = etf.info
        elif data_type == "holdings":
            data = etf.holdings
        elif data_type == "performance":
            data = etf.performance
        elif data_type == "dividend":
            data = etf.dividend
        elif data_type == "expense":
            data = etf.expense
        elif data_type == "technicals":
            data = etf.technicals
        elif data_type == "holdings_analysis":
            data = etf.holdings_analysis
        elif data_type == "realtime_rankings":
            data = etf.realtime_rankings
        else:
            # Get all data
            data = etf.to_dict()

        if output_format == "json":
            print(json.dumps(data, indent=2))
        else:
            print_pretty(data, ticker)

    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}", file=sys.stderr)
        sys.exit(1)


def print_pretty(data: dict, ticker: str):
    """Pretty print ETF data."""
    if "info" in data:
        # Full data
        info = data["info"]["vitals"]
        print(f"{'='*60}")
        print(f"ETF: {ticker.upper()}")
        print(f"Name: {info.get('etf_name', 'N/A')}")
        print(f"{'='*60}\n")

        print(f"Issuer: {info.get('issuer', 'N/A')}")
        print(f"Expense Ratio: {info.get('expense_ratio', 'N/A')}")
        print(f"Inception: {info.get('inception', 'N/A')}")
        print(f"Index Tracked: {info.get('index_tracked', 'N/A')}")

        if "holdings" in data and data["holdings"].get("top_holdings"):
            print(f"\n{'Top Holdings:':-<60}")
            for holding in data["holdings"]["top_holdings"][:5]:
                symbol = holding.get("symbol", "N/A")
                name = holding.get("holding", "N/A")
                share = holding.get("share", "N/A")
                print(f"  {symbol:6} {name:35} {share:>8}")

        if "performance" in data and data["performance"]:
            print(f"\n{'Performance:':-<60}")
            for perf in data["performance"]:
                for key, value in perf.items():
                    if "return" in key:
                        print(f"  {key.replace('_', ' ').title():20} {value}")

        if "dividends" in data and data["dividends"]:
            print(f"\n{'Dividends:':-<60}")
            for div in data["dividends"]:
                for key, value in div.items():
                    if key != "etf_database_category_average" and key != "factset_segment_average":
                        print(f"  {key.replace('_', ' ').title():25} {value}")

        print(f"\n{'='*60}")
        print("Use --json flag to get full data in JSON format")
    else:
        # Specific data type
        print(json.dumps(data, indent=2))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape ETF data from ETFDB.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyetfdb --list              # List available ETFs
  pyetfdb SPY                 # Get all data for SPY
  pyetfdb SPY --info          # Get only info for SPY
  pyetfdb SPY --holdings      # Get only holdings for SPY
  pyetfdb SPY --json          # Get all data in JSON format
        """
    )

    parser.add_argument(
        "ticker",
        nargs="?",
        help="ETF ticker symbol (e.g., SPY, IVV, QQQ)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available ETF tickers"
    )

    parser.add_argument(
        "--info",
        action="store_const",
        const="info",
        dest="data_type",
        help="Get only basic info"
    )

    parser.add_argument(
        "--holdings",
        action="store_const",
        const="holdings",
        dest="data_type",
        help="Get only holdings data"
    )

    parser.add_argument(
        "--performance",
        action="store_const",
        const="performance",
        dest="data_type",
        help="Get only performance data"
    )

    parser.add_argument(
        "--dividend",
        action="store_const",
        const="dividend",
        dest="data_type",
        help="Get only dividend data"
    )

    parser.add_argument(
        "--expense",
        action="store_const",
        const="expense",
        dest="data_type",
        help="Get only expense data"
    )

    parser.add_argument(
        "--technicals",
        action="store_const",
        const="technicals",
        dest="data_type",
        help="Get only technical indicators"
    )

    parser.add_argument(
        "--holdings-analysis",
        action="store_const",
        const="holdings_analysis",
        dest="data_type",
        help="Get holdings analysis"
    )

    parser.add_argument(
        "--realtime-rankings",
        action="store_const",
        const="realtime_rankings",
        dest="data_type",
        help="Get real-time rankings"
    )

    parser.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="output_format",
        default="pretty",
        help="Output in JSON format"
    )

    args = parser.parse_args()

    if args.list:
        list_etfs()
    elif args.ticker:
        get_etf_data(args.ticker, args.data_type, args.output_format)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
