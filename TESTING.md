# Testing Guide

This document describes the testing setup for the ETF Backend API.

## Test Coverage

The test suite includes:

### Unit Tests (`tests/test_api.py`)
- All API endpoints (root, health, ETF list, ETF data, cache)
- Request/response validation
- Error handling
- Case-insensitive ticker handling

### CORS Tests (`tests/test_cors.py`)
- **Production frontend**: `https://etfvaluepro.com`
- **Development frontends**: localhost ports (3000, 5173, etc.)
- CORS headers validation
- Credentials handling
- Unauthorized origin rejection

### Backend-Frontend Integration Tests (`tests/test_cors.py`)
- Simulates real frontend API calls
- Preflight OPTIONS requests
- Actual GET requests with CORS headers
- JSON content type validation
- Error response handling with CORS

### Core Tests (`tests/test_etf_core.py`)
- ETF list loading
- Data validation
- Duplicate detection

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_api.py
pytest tests/test_cors.py
```

### Run Specific Test Class
```bash
pytest tests/test_api.py::TestRootEndpoint
pytest tests/test_cors.py::TestCORSConfiguration
```

### Run Specific Test
```bash
pytest tests/test_cors.py::TestCORSConfiguration::test_cors_allows_production_frontend
```

### Run with Coverage
```bash
pytest --cov=src/python_etf_db_service --cov-report=html
```

Then open `htmlcov/index.html` to view coverage report.

### Run with Verbose Output
```bash
pytest -v
```

### Run Only CORS Tests
```bash
pytest tests/test_cors.py -v
```

## Test Results

Current test coverage:
- **39 tests** in total
- **All tests passing** ✅
- **65% code coverage** (excluding CLI and EODHD client)
- **100% coverage** on core modules (etf.py, models)

## Pre-Commit Hooks

Tests run automatically before each commit via pre-commit hooks.

### Install Pre-Commit Hooks
```bash
pip install -e ".[dev]"
pre-commit install
```

### Manually Run Pre-Commit
```bash
pre-commit run --all-files
```

## Continuous Integration

GitHub Actions automatically runs tests on:
- Every push to `master` or `main`
- Every pull request
- Multiple Python versions (3.9, 3.10, 3.11, 3.12)

See `.github/workflows/tests.yml` for configuration.

## Test Dependencies

Install test dependencies:
```bash
pip install -e ".[test]"
```

Test dependencies include:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for FastAPI testing

## Writing New Tests

### Test Structure
```python
class TestMyFeature:
    """Tests for my feature."""

    def test_feature_works(self, client):
        """Test that feature works correctly."""
        response = client.get("/my-endpoint")
        assert response.status_code == 200
```

### Using Fixtures
Available fixtures (see `tests/conftest.py`):
- `client` - FastAPI test client
- `sample_etf_ticker` - Returns "SPY"
- `invalid_etf_ticker` - Returns invalid ticker
- `production_frontend_origin` - Production CORS origin
- `dev_frontend_origins` - Development CORS origins

### Testing CORS
```python
def test_my_cors_scenario(self, client, production_frontend_origin):
    """Test CORS for my scenario."""
    response = client.get(
        "/api/my-endpoint",
        headers={"Origin": production_frontend_origin}
    )
    assert "access-control-allow-origin" in response.headers
```

## Debugging Failed Tests

### View Full Traceback
```bash
pytest --tb=long
```

### Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests Only
```bash
pytest --lf
```

### Print Debugging
```bash
pytest -s  # Shows print() statements
```

## Test Markers

Mark slow tests:
```python
@pytest.mark.slow
def test_slow_operation():
    pass
```

Run only fast tests:
```bash
pytest -m "not slow"
```

## Coverage Goals

- **Overall**: Maintain >60% coverage
- **Core modules** (etf.py, api.py): >90% coverage
- **Critical paths** (CORS, auth): 100% coverage

## Troubleshooting

### Tests Fail Locally
1. Ensure dependencies are installed: `pip install -e ".[test,api]"`
2. Clear pytest cache: `rm -rf .pytest_cache`
3. Check if local server is running (stop it)

### CORS Tests Failing
1. Verify CORS origins in `src/python_etf_db_service/api.py`
2. Check that production domain is correct

### Coverage Not Generated
1. Install coverage: `pip install pytest-cov`
2. Run: `pytest --cov=src/python_etf_db_service`

## Best Practices

1. **Write tests first** for new features (TDD)
2. **Test both success and failure cases**
3. **Use descriptive test names** that explain what's being tested
4. **Keep tests independent** - don't rely on test order
5. **Mock external dependencies** (web scraping, API calls)
6. **Test CORS** for any new endpoints
7. **Verify error responses** include proper CORS headers
