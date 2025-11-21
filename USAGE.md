# Usage Guide

## Installation

```bash
# Install the package
pip install -e .

# Note: This will install cloudscraper to bypass Cloudflare protection
```

### Requirements

- Python 3.7+
- Internet connection

The package uses **cloudscraper** to:
- Automatically bypass Cloudflare's JavaScript challenges
- No browser installation required
- Pure Python solution - faster and simpler than Selenium

## Command-Line Interface (CLI)

After installation, you can use the `pyetfdb` command:

### List Available ETFs
```bash
pyetfdb --list
```
Output:
```
Total available ETFs: 2500+
First 50 ETFs:
  SPY  IVV  VTI  VOO  QQQ  VEA  IEFA  ...
```

### Get All Data for an ETF
```bash
pyetfdb SPY
```
Output:
```
============================================================
ETF: SPY
Name: SPDR S&P 500 ETF Trust
============================================================

Issuer: State Street Global Advisors
Expense Ratio: 0.09%
Inception: Jan 22, 1993
Index Tracked: S&P 500 Index

Top Holdings:-------------------------------------------
AAPL   Apple Inc.                           7.18%
MSFT   Microsoft Corporation                6.50%
AMZN   Amazon.com, Inc.                     3.32%
...
```

### Get Specific Data Types
```bash
# Basic info only
pyetfdb SPY --info

# Holdings only
pyetfdb SPY --holdings

# Performance metrics
pyetfdb SPY --performance

# Dividend information
pyetfdb SPY --dividend

# Expense analysis
pyetfdb SPY --expense

# Technical indicators
pyetfdb SPY --technicals

# Holdings analysis
pyetfdb SPY --holdings-analysis

# Real-time rankings
pyetfdb SPY --realtime-rankings
```

### JSON Output
```bash
# Get all data as JSON
pyetfdb SPY --json

# Get specific data as JSON
pyetfdb SPY --holdings --json
```

### Help
```bash
pyetfdb --help
```

## Python Library Usage

You can also use it directly in Python code:

```python
from pyetfdb_scraper.etf import ETF, load_etfs

# List all available ETFs
etfs = load_etfs()
print(f"Total ETFs: {len(etfs)}")
print(etfs[:10])  # First 10

# Get data for a specific ETF
spy = ETF('SPY')

# Access different data types
print(spy.info)           # Basic information
print(spy.holdings)       # Top holdings
print(spy.performance)    # Performance metrics
print(spy.dividend)       # Dividend data
print(spy.expense)        # Expense analysis
print(spy.technicals)     # Technical indicators

# Get everything as a dictionary
all_data = spy.to_dict()
print(all_data)
```

## Examples

### Compare Multiple ETFs
```python
from pyetfdb_scraper.etf import ETF

tickers = ['SPY', 'IVV', 'VOO']
for ticker in tickers:
    etf = ETF(ticker)
    info = etf.info['vitals']
    print(f"{ticker}: {info['expense_ratio']} - {info['etf_name']}")
```

### Export to JSON File
```bash
pyetfdb SPY --json > spy_data.json
```

### Get Top Holdings for Analysis
```python
from pyetfdb_scraper.etf import ETF
import pandas as pd

etf = ETF('SPY')
holdings = etf.holdings['top_holdings']

# Convert to DataFrame
df = pd.DataFrame(holdings)
print(df)
```
