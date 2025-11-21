import { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

function ETFSearch() {
  const [ticker, setTicker] = useState('');
  const [etfData, setEtfData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!ticker.trim()) return;

    setLoading(true);
    setError(null);
    setEtfData(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/etf/${ticker.toUpperCase()}`);
      setEtfData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch ETF data');
      console.error('Error fetching ETF:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>ETF Data Explorer</h1>

      <form onSubmit={handleSearch} style={styles.form}>
        <input
          type="text"
          placeholder="Enter ETF ticker (e.g., SPY, QQQ, VOO)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          disabled={loading}
          style={styles.input}
        />
        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? 'Loading...' : 'Search'}
        </button>
      </form>

      {error && (
        <div style={styles.error}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {etfData && (
        <div style={styles.results}>
          <div style={styles.header}>
            <h2>{etfData.ticker}</h2>
            <h3>{etfData.data.info.vitals.etf_name}</h3>
          </div>

          <div style={styles.infoGrid}>
            <div style={styles.infoCard}>
              <strong>Issuer</strong>
              <p>{etfData.data.info.vitals.issuer}</p>
            </div>
            <div style={styles.infoCard}>
              <strong>Expense Ratio</strong>
              <p>{etfData.data.info.vitals.expense_ratio}</p>
            </div>
            <div style={styles.infoCard}>
              <strong>Inception</strong>
              <p>{etfData.data.info.vitals.inception}</p>
            </div>
            <div style={styles.infoCard}>
              <strong>Index Tracked</strong>
              <p>{etfData.data.info.vitals.index_tracked || 'N/A'}</p>
            </div>
          </div>

          {etfData.data.holdings && etfData.data.holdings.top_holdings && (
            <div style={styles.section}>
              <h3>Top Holdings</h3>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Symbol</th>
                    <th style={styles.th}>Company</th>
                    <th style={styles.th}>Share</th>
                  </tr>
                </thead>
                <tbody>
                  {etfData.data.holdings.top_holdings.slice(0, 10).map((holding, idx) => (
                    <tr key={idx} style={idx % 2 === 0 ? styles.evenRow : styles.oddRow}>
                      <td style={styles.td}><strong>{holding.symbol}</strong></td>
                      <td style={styles.td}>{holding.holding}</td>
                      <td style={styles.td}>{holding.share}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {etfData.data.performance && etfData.data.performance.length > 0 && (
            <div style={styles.section}>
              <h3>Performance</h3>
              <div style={styles.performanceGrid}>
                {etfData.data.performance.map((metric, idx) => {
                  const key = Object.keys(metric)[0];
                  const value = metric[key];
                  return (
                    <div key={idx} style={styles.performanceCard}>
                      <strong>{key.replace(/_/g, ' ').toUpperCase()}</strong>
                      <p style={styles.performanceValue}>{value}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Inline styles for the example
const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif'
  },
  form: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px'
  },
  input: {
    flex: 1,
    padding: '12px',
    fontSize: '16px',
    border: '2px solid #ddd',
    borderRadius: '4px'
  },
  button: {
    padding: '12px 24px',
    fontSize: '16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  error: {
    padding: '12px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    borderRadius: '4px',
    marginBottom: '20px'
  },
  results: {
    marginTop: '20px'
  },
  header: {
    borderBottom: '2px solid #007bff',
    paddingBottom: '10px',
    marginBottom: '20px'
  },
  infoGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '15px',
    marginBottom: '30px'
  },
  infoCard: {
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px',
    border: '1px solid #dee2e6'
  },
  section: {
    marginTop: '30px'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '10px'
  },
  th: {
    textAlign: 'left',
    padding: '12px',
    backgroundColor: '#007bff',
    color: 'white',
    borderBottom: '2px solid #0056b3'
  },
  td: {
    padding: '10px',
    borderBottom: '1px solid #dee2e6'
  },
  evenRow: {
    backgroundColor: '#f8f9fa'
  },
  oddRow: {
    backgroundColor: 'white'
  },
  performanceGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
    marginTop: '10px'
  },
  performanceCard: {
    padding: '15px',
    backgroundColor: '#e7f3ff',
    borderRadius: '4px',
    textAlign: 'center'
  },
  performanceValue: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#007bff',
    margin: '10px 0 0 0'
  }
};

export default ETFSearch;
