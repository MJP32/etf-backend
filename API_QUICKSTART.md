# API Quick Start

## TL;DR - Get Your React App Running in 5 Minutes

### Step 1: Start the Backend (Terminal 1)

```bash
# Install API dependencies
pip install -e ".[api]"

# Start the server
python start_api.py
```

The API will run on **http://localhost:8000**

### Step 2: Create React App (Terminal 2)

```bash
# Create a new React app
npm create vite@latest my-etf-app -- --template react
cd my-etf-app

# Install axios
npm install axios

# Copy the example component
# Download react-examples/ETFSearch.jsx from this repo
# Place it in src/components/ETFSearch.jsx
```

### Step 3: Use the Component

Replace `src/App.jsx` with:

```jsx
import ETFSearch from './components/ETFSearch'
import './App.css'

function App() {
  return (
    <div className="App">
      <ETFSearch />
    </div>
  )
}

export default App
```

### Step 4: Run React App

```bash
npm run dev
```

Open **http://localhost:5173** and search for ETFs like "SPY", "QQQ", "VOO"!

## API Endpoints Cheat Sheet

```bash
# List ETFs
GET http://localhost:8000/api/etfs?limit=10

# Get all data for SPY
GET http://localhost:8000/api/etf/SPY

# Get only holdings
GET http://localhost:8000/api/etf/SPY/holdings

# Get only performance
GET http://localhost:8000/api/etf/SPY/performance
```

## Test with curl

```bash
# Get SPY info
curl http://localhost:8000/api/etf/SPY/info

# Get QQQ holdings
curl http://localhost:8000/api/etf/QQQ/holdings
```

## Interactive API Documentation

Visit **http://localhost:8000/docs** to:
- See all available endpoints
- Test API calls directly in the browser
- View request/response schemas

## Example Response

```json
{
  "ticker": "SPY",
  "data": {
    "info": {
      "vitals": {
        "etf_name": "SPDR S&P 500 ETF Trust",
        "issuer": "State Street",
        "expense_ratio": "0.09%",
        "inception": "Jan 22, 1993"
      }
    },
    "holdings": {
      "top_holdings": [
        {
          "symbol": "NVDA",
          "holding": "NVIDIA Corporation",
          "share": "8.07%"
        }
      ]
    }
  }
}
```

## Full Documentation

For complete setup instructions and advanced features, see:
- **[REACT_SETUP.md](REACT_SETUP.md)** - Complete React integration guide
- **[USAGE.md](USAGE.md)** - CLI usage
- **[CLAUDE.md](CLAUDE.md)** - Development guide
