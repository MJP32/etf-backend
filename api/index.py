"""
Vercel entry point for FastAPI app.
"""
from python_etf_db_service.api import app

# Vercel expects the ASGI app to be named 'app'
# This is already defined in python_etf_db_service.api
