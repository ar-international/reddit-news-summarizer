import React, { useState, useEffect } from 'react';
import NewsTile from './components/NewsTile';
import './App.css';

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchNews = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/news');
      if (!response.ok) {
        throw new Error('Failed to fetch news');
      }
      const data = await response.json();
      setNews(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      const response = await fetch('http://localhost:8000/api/refresh', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to refresh news');
      }
      await fetchNews();
    } catch (err) {
      setError(err.message);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Reddit AI News Summarizer</h1>
        <button
          className="refresh-button"
          onClick={handleRefresh}
          disabled={refreshing}
        >
          {refreshing ? 'Sourcing...' : 'Source File'}
        </button>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="news-grid">
        {news.map((item, index) => (
          <NewsTile key={index} item={item} />
        ))}
      </div>

      {news.length === 0 && !loading && !error && (
        <div className="empty-state">No news available. Click "Source File" to fetch.</div>
      )}
    </div>
  );
}

export default App;
