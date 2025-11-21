# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

python-etf-db-service is a Python library that scrapes ETF data from ETFDB.com. It provides structured access to comprehensive ETF information including vitals, holdings, performance metrics, dividends, and technical indicators.

## Development Commands

### Setup
```bash
# Create conda environment
conda create -n etfdb python=3.9
conda activate pyetfdb

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install

# Note: Uses cloudscraper to bypass Cloudflare protection
```

### Running the CLI
```bash
# List available ETFs
etfdb --list

# Get all data for an ETF
etfdb SPY

# Get specific data types
etfdb SPY --info
etfdb SPY --holdings
etfdb SPY --performance

# Output as JSON
etfdb SPY --json
```

### Running the API Server (for React/Web Apps)
```bash
# Install API dependencies
pip install -e ".[api]"

# Start the API server
python start_api.py

# Or use uvicorn directly
uvicorn python_etf_db_service.api:app --reload --port 8000

# API will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

See [REACT_SETUP.md](REACT_SETUP.md) for complete React integration guide.

### Code Formatting
```bash
# Black formatting (line length: 79)
black src/

# Run pre-commit checks manually
pre-commit run --all-files
```

### Building and Distribution
```bash
# Build package
python -m build

# Install locally for testing
pip install -e .
```

## Architecture

### Core Components

**CLI Module** (`src/python_etf_db_service/cli.py`)
- Command-line interface for the library
- Provides `pyetfdb` command after installation
- Supports listing ETFs, fetching specific data types, and JSON output
- Entry point defined in `setup.py` console_scripts

**ETF Class** (`src/python_etf_db_service/etf.py`)
- Main user-facing interface that inherits from `ETFScraper`
- Provides property-based access to all ETF data categories
- `to_dict()` method aggregates all data into a single dictionary
- `load_etfs()` function loads available ETF tickers from `data/etfdb.json`

**ETFScraper Class** (`src/python_etf_db_service/etf_scraper.py`)
- Base scraping engine that handles HTTP requests to ETFDB.com
- Manages user-agent rotation from `data/user-agents.txt` to avoid rate limiting
- Implements retry logic with exponential backoff (handles 429 rate limit errors)
- Parses HTML using BeautifulSoup and extracts the main `etf-ticker-body` div
- Delegates specific data extraction to tab-specific modules

**Tab Modules** (`src/python_etf_db_service/tabs/`)
- Each tab corresponds to a section on the ETFDB website
- Modules: `info.py`, `expense.py`, `holdings.py`, `holdings_analysis.py`, `performance.py`, `dividend.py`, `technicals.py`, `realtime_ratings.py`
- All use shared utilities from `utils.py` for consistent scraping patterns

**Utilities** (`src/python_etf_db_service/utils.py`)
- `_scrape_div_class_ticker_assets()`: Extracts data from divs with class "ticker-assets"
- `_scrape_table()`: Parses HTML tables into dictionaries (handles both vertical and horizontal layouts)
- `jump_siblings()`: Navigates DOM tree by jumping between sibling elements
- `unpack_tag_contents()`: Recursively unpacks nested HTML tags to extract clean text
- `get_nested()`: Safe nested dictionary access with None fallback

**Models** (`src/python_etf_db_service/models/`)
- Pydantic models for type validation: `InfoModel`, `BaseInfoModel`, `ExpenseModel`

### Data Flow

1. User creates `ETF('TICKER')` instance
2. `ETFScraper.__init__` makes HTTP request with random user-agent
3. BeautifulSoup parses response and extracts `etf-ticker-body` div
4. User accesses properties (e.g., `etf.info`, `etf.holdings`)
5. Each property calls corresponding tab module function
6. Tab module uses utils to scrape specific sections from the soup
7. Data is transformed into clean dictionaries using pydantic models

### Web Scraping Strategy

- **Cloudscraper**: Uses cloudscraper library to bypass Cloudflare protection
  - Automatically solves JavaScript challenges
  - Mimics browser behavior (Chrome on Windows)
  - No external browser needed - pure Python solution
  - Much faster than Selenium-based approaches
- **User-Agent Rotation**: Random selection from `data/user-agents.txt` to avoid detection
- **Retry Logic**: 2 retries with random 5-10 second delays on failure
- **Rate Limiting**: Handles 429 responses with 60-second sleep and retry
- **HTML Navigation**: Uses regex patterns to find section headers, then jumps to sibling elements containing data
- **Error Handling**: Graceful degradation with `get_nested()` returning None for missing data

## Code Style

- Line length: 79 characters (enforced by Black)
- Black formatter with isort integration
- Type hints required (mypy configuration in pyproject.toml)
- Commit message format follows Angular convention (see CONTRIBUTING.md)

## Important Notes

- The scraper depends on ETFDB.com's HTML structure - breaking changes to their website will require updates
- Always test with multiple ETF tickers to ensure scraping patterns work across different ETF types
- When modifying tab modules, ensure the output format matches the pydantic models
- User-agent rotation is critical for avoiding rate limits - maintain the `user-agents.txt` file
- The `data/etfdb.json` file contains the master list of available ETF tickers and should be updated periodically
