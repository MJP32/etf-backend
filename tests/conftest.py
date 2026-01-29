"""Shared pytest fixtures for testing."""

import pytest
from fastapi.testclient import TestClient
from python_etf_db_service.api import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_etf_ticker():
    """Return a sample ETF ticker for testing."""
    return "SPY"


@pytest.fixture
def invalid_etf_ticker():
    """Return an invalid ETF ticker for testing."""
    return "NOTANETF123"


@pytest.fixture
def production_frontend_origin():
    """Return the production frontend origin."""
    return "https://etfvaluepro.com"


@pytest.fixture
def dev_frontend_origins():
    """Return development frontend origins."""
    return [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
