"""
FastAPI backend for Python ETF DB Service.
This provides REST API endpoints that can be consumed by a React frontend.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
# Look for .env in the project root directory
env_path = Path(__file__).parent.parent.parent / '.env'
logger.info(f"Loading .env from: {env_path}")
logger.info(f".env file exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# Check if API key was loaded
api_key = os.getenv('EODHD_API_KEY')
logger.info(f"EODHD_API_KEY loaded: {bool(api_key)}")
if api_key:
    logger.info(f"API Key (first 20 chars): {api_key[:20]}...")

from python_etf_db_service.etf import ETF, load_etfs
from python_etf_db_service.cache import get_cache
from python_etf_db_service.eodhd_client import EODHDClient

# Initialize FastAPI app
app = FastAPI(
    title="ETF Data API",
    description="REST API for scraping ETF data from ETFDB.com",
    version="1.0.1"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Production
        "https://etfvaluepro.com",
        "https://www.etfvaluepro.com",
        "https://etf-backend-production.up.railway.app",  # Railway backend
        # Development
        "http://localhost:3000",  # React default dev server
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:5174",  # Vite alternate port
        "http://localhost:5175",  # Vite alternate port
        "http://localhost:5176",  # Vite alternate port
        "http://localhost:5177",  # Vite alternate port
        "http://localhost:5178",  # Vite alternate port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "http://127.0.0.1:5177",
        "http://127.0.0.1:5178",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EODHD client (if API key is available)
eodhd_client = None
if os.getenv('EODHD_API_KEY'):
    try:
        eodhd_client = EODHDClient()
        logger.info("EODHD client initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize EODHD client: {e}")
        logger.warning("Falling back to web scraping")
else:
    logger.warning("EODHD_API_KEY not found. Using web scraping fallback.")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ETF Data API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "list_etfs": "/api/etfs",
            "get_etf": "/api/etf/{ticker}",
            "get_etf_info": "/api/etf/{ticker}/info",
            "get_etf_holdings": "/api/etf/{ticker}/holdings",
            "get_etf_performance": "/api/etf/{ticker}/performance",
        }
    }


@app.get("/api/etfs")
async def list_etfs(
    limit: Optional[int] = Query(None, description="Limit number of results"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    """
    Get list of all available ETF tickers.

    Parameters:
    - limit: Maximum number of tickers to return
    - offset: Starting position for pagination
    """
    try:
        all_etfs = load_etfs()

        if limit:
            etfs = all_etfs[offset:offset + limit]
        else:
            etfs = all_etfs[offset:]

        return {
            "total": len(all_etfs),
            "count": len(etfs),
            "offset": offset,
            "etfs": etfs
        }
    except Exception as e:
        logger.error(f"Error loading ETFs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/etf/{ticker}")
async def get_etf(ticker: str, force_refresh: bool = False, source: str = "auto"):
    """
    Get all data for a specific ETF ticker.

    Parameters:
    - ticker: ETF ticker symbol (e.g., SPY, IVV, QQQ)
    - force_refresh: Skip cache and force fresh fetch (default: False)
    - source: Data source - "eodhd", "scrape", or "auto" (default: "auto")
    """
    try:
        cache = get_cache()
        ticker_upper = ticker.upper()

        # Try to get from cache first (unless force refresh)
        if not force_refresh:
            cached_data = cache.get(ticker_upper)
            if cached_data:
                logger.info(f"Returning cached data for {ticker}")
                return {
                    "ticker": ticker_upper,
                    "data": cached_data,
                    "cached": True,
                    "source": cached_data.get("_source", "unknown")
                }

        # Determine data source
        use_eodhd = False
        logger.info(f"Source parameter: {source}, eodhd_client available: {eodhd_client is not None}")
        if source == "eodhd" or (source == "auto" and eodhd_client is not None):
            use_eodhd = True
        logger.info(f"Will use EODHD: {use_eodhd}")

        # Initialize variables
        data = None
        data_source = None

        # Fetch fresh data
        if use_eodhd and eodhd_client:
            logger.info(f"Fetching data from EODHD for {ticker}")
            try:
                fundamentals = eodhd_client.get_fundamentals(ticker_upper)
                data = eodhd_client.parse_etf_data(fundamentals)
                data["_source"] = "eodhd"
                data_source = "eodhd"
            except Exception as e:
                logger.error(f"EODHD fetch failed for {ticker}, falling back to scraping: {e}")
                if source == "eodhd":  # If explicitly requested EODHD, raise error
                    raise HTTPException(
                        status_code=500,
                        detail=f"EODHD API error for {ticker}: {str(e)}"
                    )
                # Otherwise fall back to scraping
                use_eodhd = False

        if not use_eodhd:
            logger.info(f"Scraping fresh data for {ticker}")
            etf = ETF(ticker_upper)
            data = etf.to_dict()
            data["_source"] = "scrape"
            data_source = "scrape"

        # Store in cache
        cache.set(ticker_upper, data)

        return {
            "ticker": ticker_upper,
            "data": data,
            "cached": False,
            "source": data_source
        }
    except Exception as e:
        logger.error(f"Error fetching {ticker}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch data for {ticker}: {str(e)}"
        )


@app.get("/api/etf/{ticker}/info")
async def get_etf_info(ticker: str):
    """Get basic info for an ETF."""
    try:
        logger.info(f"Fetching info for {ticker}")
        etf = ETF(ticker.upper())

        return {
            "ticker": ticker.upper(),
            "info": etf.info
        }
    except Exception as e:
        logger.error(f"Error fetching info for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/etf/{ticker}/holdings")
async def get_etf_holdings(ticker: str):
    """Get holdings data for an ETF."""
    try:
        logger.info(f"Fetching holdings for {ticker}")
        etf = ETF(ticker.upper())

        return {
            "ticker": ticker.upper(),
            "holdings": etf.holdings
        }
    except Exception as e:
        logger.error(f"Error fetching holdings for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/etf/{ticker}/performance")
async def get_etf_performance(ticker: str):
    """Get performance metrics for an ETF."""
    try:
        logger.info(f"Fetching performance for {ticker}")
        etf = ETF(ticker.upper())

        return {
            "ticker": ticker.upper(),
            "performance": etf.performance
        }
    except Exception as e:
        logger.error(f"Error fetching performance for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/etf/{ticker}/dividend")
async def get_etf_dividend(ticker: str):
    """Get dividend information for an ETF."""
    try:
        logger.info(f"Fetching dividend for {ticker}")
        etf = ETF(ticker.upper())

        return {
            "ticker": ticker.upper(),
            "dividend": etf.dividend
        }
    except Exception as e:
        logger.error(f"Error fetching dividend for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/etf/{ticker}/expense")
async def get_etf_expense(ticker: str):
    """Get expense analysis for an ETF."""
    try:
        logger.info(f"Fetching expense for {ticker}")
        etf = ETF(ticker.upper())

        return {
            "ticker": ticker.upper(),
            "expense": etf.expense
        }
    except Exception as e:
        logger.error(f"Error fetching expense for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/etf/{ticker}/technicals")
async def get_etf_technicals(ticker: str):
    """Get technical indicators for an ETF."""
    try:
        logger.info(f"Fetching technicals for {ticker}")
        etf = ETF(ticker.upper())

        return {
            "ticker": ticker.upper(),
            "technicals": etf.technicals
        }
    except Exception as e:
        logger.error(f"Error fetching technicals for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/cache/stats")
async def cache_stats():
    """Get cache statistics."""
    cache = get_cache()
    return cache.get_stats()


@app.delete("/api/cache/{ticker}")
async def clear_cache(ticker: str):
    """Clear cache for a specific ticker."""
    cache = get_cache()
    cache.clear(ticker.upper())
    return {"message": f"Cache cleared for {ticker.upper()}"}


@app.delete("/api/cache")
async def clear_all_cache():
    """Clear entire cache."""
    cache = get_cache()
    cache.clear()
    return {"message": "Entire cache cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
