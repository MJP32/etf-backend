"""
EODHD API Client for fetching ETF data.
"""

import os
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class EODHDClient:
    """Client for interacting with EODHD API."""

    BASE_URL = "https://eodhd.com/api"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize EODHD client.

        Args:
            api_key: EODHD API key. If not provided, will try to get from EODHD_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv('EODHD_API_KEY')
        if not self.api_key:
            raise ValueError(
                "EODHD API key is required. "
                "Provide it as argument or set EODHD_API_KEY environment variable."
            )

    def get_fundamentals(self, ticker: str, exchange: str = "US") -> Dict[str, Any]:
        """
        Get fundamental data for an ETF.

        Args:
            ticker: ETF ticker symbol (e.g., 'SPY', 'QQQ')
            exchange: Exchange code (default: 'US')

        Returns:
            Dictionary containing fundamental data
        """
        symbol = f"{ticker}.{exchange}"
        url = f"{self.BASE_URL}/fundamentals/{symbol}"

        params = {
            'api_token': self.api_key,
            'fmt': 'json'
        }

        try:
            logger.info(f"Fetching fundamentals for {symbol}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching fundamentals for {symbol}: {e}")
            raise

    def get_historical_data(self, ticker: str, exchange: str = "US", period: str = "d") -> Dict[str, Any]:
        """
        Get historical EOD data for an ETF.

        Args:
            ticker: ETF ticker symbol
            exchange: Exchange code (default: 'US')
            period: Period ('d' for daily, 'w' for weekly, 'm' for monthly)

        Returns:
            List of historical data points
        """
        symbol = f"{ticker}.{exchange}"
        url = f"{self.BASE_URL}/eod/{symbol}"

        params = {
            'api_token': self.api_key,
            'fmt': 'json',
            'period': period
        }

        try:
            logger.info(f"Fetching historical data for {symbol}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            raise

    def parse_etf_data(self, fundamentals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse EODHD fundamental data into a structured format.

        Args:
            fundamentals: Raw fundamental data from EODHD API

        Returns:
            Parsed and structured ETF data
        """
        general = fundamentals.get('General', {})
        etf_data = fundamentals.get('ETF_Data', {})
        technicals = fundamentals.get('Technicals', {})
        highlights = fundamentals.get('Highlights', {})
        valuation = fundamentals.get('Valuation', {})
        morningstar = etf_data.get('MorningStar', {})

        return {
            'info': {
                'name': general.get('Name'),
                'code': general.get('Code'),
                'type': general.get('Type'),
                'exchange': general.get('Exchange'),
                'currency_code': general.get('CurrencyCode'),
                'currency_name': general.get('CurrencyName'),
                'currency_symbol': general.get('CurrencySymbol'),
                'country_name': general.get('CountryName'),
                'country_iso': general.get('CountryISO'),
                'open_figi': general.get('OpenFigi'),
                'description': general.get('Description'),
                'category': general.get('Category'),
                'website_url': general.get('WebURL'),
                'vitals': {
                    'assets_under_management': etf_data.get('Net_Assets'),
                    'total_net_assets': etf_data.get('Total_Assets'),
                    'nav': etf_data.get('NAV'),
                    'expense_ratio': etf_data.get('Expense_Ratio'),
                    'net_expense_ratio': etf_data.get('Net_Expense_Ratio'),
                    'inception_date': general.get('IPODate'),
                    'average_market_cap': etf_data.get('Average_Mkt_Cap_Mil'),
                }
            },
            'holdings': {
                'total_holdings': len(etf_data.get('Holdings', {})),
                'top_holdings': self._parse_holdings(etf_data.get('Holdings', {})),
                'holdings_turnover': etf_data.get('Holdings_Turnover')
            },
            'performance': self._parse_performance(fundamentals),
            'risk_metrics': {
                'volatility_1y': etf_data.get('Volatility_Year'),
                'volatility_3y': etf_data.get('Volatility_3Year'),
                'expected_return_3y': etf_data.get('ExpReturn_3Year'),
                'sharpe_ratio_3y': etf_data.get('SharpRatio_3Year'),
                'beta': technicals.get('Beta'),
            },
            'dividend': self._parse_dividend(fundamentals),
            'expense': {
                'expense_ratio': etf_data.get('Expense_Ratio'),
                'net_expense_ratio': etf_data.get('Net_Expense_Ratio'),
                'expense_annual_management_fee': etf_data.get('Management_Fee'),
                'ongoing_charge': etf_data.get('Ongoing_Charge'),
            },
            'technicals': {
                'beta': technicals.get('Beta'),
                '52_week_high': technicals.get('52WeekHigh'),
                '52_week_low': technicals.get('52WeekLow'),
                '50_day_ma': technicals.get('50DayMA'),
                '200_day_ma': technicals.get('200DayMA')
            },
            'valuation': {
                'price_to_earnings': valuation.get('TrailingPE'),
                'price_to_book': valuation.get('PriceToBookMRQ'),
                'price_to_sales': valuation.get('PriceToSalesTTM'),
                'price_to_cash_flow': valuation.get('PriceToCashFlowMRQ'),
                'earnings_growth': valuation.get('EarningsGrowth'),
                'revenue_growth': valuation.get('RevenueGrowth'),
            },
            'morningstar': {
                'rating': morningstar.get('Ratio'),
                'category_benchmark': morningstar.get('Category_Benchmark'),
                'sustainability_ratio': morningstar.get('Sustainability_Ratio'),
            },
            'fixed_income': {
                'coupon': etf_data.get('Coupon'),
                'bond_price': etf_data.get('Price'),
                'yield_to_maturity': etf_data.get('Yield_to_Maturity'),
                'duration': etf_data.get('Duration'),
                'credit_quality': etf_data.get('Credit_Quality'),
            } if etf_data.get('Bond_Positions') else None,
            'sector_weights': etf_data.get('Sector_Weights', {}),
            'asset_allocation': etf_data.get('Asset_Allocation', {}),
            'world_regions': etf_data.get('World_Regions', {}),
        }

    def _parse_holdings(self, holdings_data: Dict[str, Any]) -> list:
        """Parse holdings data into a list."""
        holdings = []
        for code, data in holdings_data.items():
            if isinstance(data, dict):
                holdings.append({
                    'symbol': code,
                    'holding': data.get('Name', code),
                    'share': data.get('Assets_%', '0')
                })

        # Sort by share percentage
        holdings.sort(key=lambda x: float(x['share'] or 0), reverse=True)
        return holdings[:50]  # Return top 50

    def _parse_performance(self, fundamentals: Dict[str, Any]) -> list:
        """Parse performance data into list format matching web scraper format."""
        etf_data = fundamentals.get('ETF_Data', {})
        perf_data = etf_data.get('Performance', {})

        # Return as list of dicts to match web scraper format
        performance = []
        if perf_data.get('Returns_YTD'):
            performance.append({'ytd': perf_data.get('Returns_YTD') + '%'})
        if perf_data.get('Returns_1Y'):
            performance.append({'1_year': perf_data.get('Returns_1Y') + '%'})
        if perf_data.get('Returns_3Y'):
            performance.append({'3_year': perf_data.get('Returns_3Y') + '%'})
        if perf_data.get('Returns_5Y'):
            performance.append({'5_year': perf_data.get('Returns_5Y') + '%'})
        if perf_data.get('Returns_10Y'):
            performance.append({'10_year': perf_data.get('Returns_10Y') + '%'})

        return performance

    def _parse_dividend(self, fundamentals: Dict[str, Any]) -> list:
        """Parse dividend data into list format matching web scraper format."""
        etf_data = fundamentals.get('ETF_Data', {})
        highlights = fundamentals.get('Highlights', {})

        # Return as list of dicts to match web scraper format
        dividends = []

        if etf_data.get('Yield'):
            dividends.append({'dividend_yield': etf_data.get('Yield')})

        if etf_data.get('Dividend_Paying'):
            dividends.append({'dividend_paying': etf_data.get('Dividend_Paying')})

        if highlights.get('DividendDate'):
            dividends.append({'dividend_date': highlights.get('DividendDate')})

        if highlights.get('ExDividendDate'):
            dividends.append({'ex_dividend_date': highlights.get('ExDividendDate')})

        # Add dividend frequency if available
        if isinstance(etf_data.get('Dividends_TTM'), dict):
            freq = etf_data.get('Dividends_TTM', {}).get('Frequency')
            if freq:
                dividends.append({'dividend_frequency': freq})

        return dividends


def get_eodhd_client() -> EODHDClient:
    """Get a singleton EODHD client instance."""
    if not hasattr(get_eodhd_client, '_instance'):
        get_eodhd_client._instance = EODHDClient()
    return get_eodhd_client._instance
