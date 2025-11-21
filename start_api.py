#!/usr/bin/env python3
"""
Startup script for the ETF Data API server.
Usage: python start_api.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("ERROR: uvicorn not installed!")
        print("Install with: pip install -e \".[api]\"")
        sys.exit(1)

    print("=" * 60)
    print("Starting ETF Data API Server")
    print("=" * 60)
    print()
    print("API will be available at:")
    print("  - API: http://localhost:8000")
    print("  - Interactive docs: http://localhost:8000/docs")
    print("  - Alternative docs: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    uvicorn.run(
        "pyetfdb_scraper.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
