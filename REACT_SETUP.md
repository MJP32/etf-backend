# React Frontend Setup Guide

This guide shows you how to use the ETF scraper as a backend API for your React website.

## Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  React Frontend │  HTTP   │  FastAPI Server │  Scrape │   ETFDB.com     │
│  (Port 3000)    │ ──────> │  (Port 8000)    │ ──────> │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

## Backend Setup

### 1. Install API Dependencies

```bash
# Install the package with API extras
pip install -e ".[api]"
```

This installs:
- `fastapi` - Modern Python web framework
- `uvicorn` - ASGI server for running FastAPI

### 2. Start the API Server

```bash
# Option 1: Using uvicorn directly
uvicorn python_etf_db_service.api:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python -m uvicorn python_etf_db_service.api:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### 3. Test the API

```bash
# List all ETFs
curl http://localhost:8000/api/etfs?limit=10

# Get SPY data
curl http://localhost:8000/api/etf/SPY

# Get only holdings
curl http://localhost:8000/api/etf/SPY/holdings
```

## Frontend Setup

### 1. Create React App

```bash
# Using Vite (recommended)
npm create vite@latest my-etf-app -- --template react
cd my-etf-app
npm install

# Or using Create React App
npx create-react-app my-etf-app
cd my-etf-app
```

### 2. Install Axios for API calls

```bash
npm install axios
```

### 3. Create API Service

Create `src/services/etfApi.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const etfApi = {
  // Get list of all ETFs
  listETFs: async (limit = 100, offset = 0) => {
    const response = await axios.get(`${API_BASE_URL}/etfs`, {
      params: { limit, offset }
    });
    return response.data;
  },

  // Get all data for an ETF
  getETF: async (ticker) => {
    const response = await axios.get(`${API_BASE_URL}/etf/${ticker}`);
    return response.data;
  },

  // Get specific data types
  getInfo: async (ticker) => {
    const response = await axios.get(`${API_BASE_URL}/etf/${ticker}/info`);
    return response.data;
  },

  getHoldings: async (ticker) => {
    const response = await axios.get(`${API_BASE_URL}/etf/${ticker}/holdings`);
    return response.data;
  },

  getPerformance: async (ticker) => {
    const response = await axios.get(`${API_BASE_URL}/etf/${ticker}/performance`);
    return response.data;
  },

  getDividend: async (ticker) => {
    const response = await axios.get(`${API_BASE_URL}/etf/${ticker}/dividend`);
    return response.data;
  },

  getTechnicals: async (ticker) => {
    const response = await axios.get(`${API_BASE_URL}/etf/${ticker}/technicals`);
    return response.data;
  }
};

export default etfApi;
```

### 4. Create React Components

#### ETF Search Component

Create `src/components/ETFSearch.jsx`:

```jsx
import { useState } from 'react';
import etfApi from '../services/etfApi';

function ETFSearch() {
  const [ticker, setTicker] = useState('');
  const [etfData, setEtfData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!ticker) return;

    setLoading(true);
    setError(null);

    try {
      const data = await etfApi.getETF(ticker.toUpperCase());
      setEtfData(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch ETF data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="etf-search">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Enter ETF ticker (e.g., SPY)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Search'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {etfData && (
        <div className="etf-results">
          <h2>{etfData.ticker}</h2>
          <div className="etf-info">
            <h3>{etfData.data.info.vitals.etf_name}</h3>
            <p>Issuer: {etfData.data.info.vitals.issuer}</p>
            <p>Expense Ratio: {etfData.data.info.vitals.expense_ratio}</p>
            <p>Inception: {etfData.data.info.vitals.inception}</p>
          </div>

          <div className="holdings">
            <h3>Top Holdings</h3>
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Company</th>
                  <th>Share</th>
                </tr>
              </thead>
              <tbody>
                {etfData.data.holdings.top_holdings.slice(0, 10).map((holding, idx) => (
                  <tr key={idx}>
                    <td>{holding.symbol}</td>
                    <td>{holding.holding}</td>
                    <td>{holding.share}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default ETFSearch;
```

#### ETF List Component

Create `src/components/ETFList.jsx`:

```jsx
import { useState, useEffect } from 'react';
import etfApi from '../services/etfApi';

function ETFList() {
  const [etfs, setEtfs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadETFs();
  }, []);

  const loadETFs = async () => {
    try {
      const data = await etfApi.listETFs(50, 0);
      setEtfs(data.etfs);
    } catch (err) {
      console.error('Failed to load ETFs:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading ETFs...</div>;

  return (
    <div className="etf-list">
      <h2>Popular ETFs</h2>
      <div className="etf-grid">
        {etfs.map((ticker) => (
          <div key={ticker} className="etf-card">
            {ticker}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ETFList;
```

### 5. Update App.js

```jsx
import { useState } from 'react';
import ETFSearch from './components/ETFSearch';
import ETFList from './components/ETFList';
import './App.css';

function App() {
  return (
    <div className="App">
      <header>
        <h1>ETF Data Explorer</h1>
      </header>

      <main>
        <ETFSearch />
        <ETFList />
      </main>
    </div>
  );
}

export default App;
```

### 6. Run the App

```bash
npm run dev    # For Vite
# or
npm start      # For Create React App
```

Your React app will run on http://localhost:3000 (or http://localhost:5173 for Vite).

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/etfs` | GET | List all available ETF tickers |
| `/api/etf/{ticker}` | GET | Get all data for an ETF |
| `/api/etf/{ticker}/info` | GET | Get basic info only |
| `/api/etf/{ticker}/holdings` | GET | Get holdings data |
| `/api/etf/{ticker}/performance` | GET | Get performance metrics |
| `/api/etf/{ticker}/dividend` | GET | Get dividend information |
| `/api/etf/{ticker}/expense` | GET | Get expense analysis |
| `/api/etf/{ticker}/technicals` | GET | Get technical indicators |

## Production Deployment

### Backend (FastAPI)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn python_etf_db_service.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (React)

```bash
# Build for production
npm run build

# Deploy to Netlify, Vercel, or any static hosting
```

### Update CORS Origins

In `src/python_etf_db_service/api.py`, update the CORS origins to include your production domain:

```python
allow_origins=[
    "http://localhost:3000",
    "https://your-production-domain.com",
],
```

## Example curl Commands

```bash
# List first 10 ETFs
curl "http://localhost:8000/api/etfs?limit=10"

# Get SPY info
curl "http://localhost:8000/api/etf/SPY/info"

# Get QQQ holdings
curl "http://localhost:8000/api/etf/QQQ/holdings"

# Get VOO performance
curl "http://localhost:8000/api/etf/VOO/performance"
```

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console, make sure:
1. The API server is running
2. Your React dev server port matches the allowed origins in `api.py`
3. Clear browser cache and restart both servers

### Slow Response Times

- Each ETF request requires scraping ETFDB.com (~5-10 seconds)
- Consider implementing caching in the backend
- Use a loading indicator in the React UI

### Rate Limiting

- ETFDB may rate limit excessive requests
- Implement request throttling in your frontend
- Consider caching responses on the backend

## Next Steps

1. Add caching (Redis) to avoid re-scraping
2. Implement pagination for ETF list
3. Add error handling and retry logic
4. Create more detailed visualization components
5. Add search autocomplete
6. Implement favorites/watchlist feature
