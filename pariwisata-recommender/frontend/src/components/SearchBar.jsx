import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { searchAPI } from '../services/api';
import '../styles/searchbar.css';

const SearchBar = ({ onClose }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({ destinations: [], activities: [] });
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  // Debounced search
  useEffect(() => {
    if (!query.trim()) {
      setResults({ destinations: [], activities: [] });
      setShowResults(false);
      return;
    }

    const timeoutId = setTimeout(async () => {
      setLoading(true);
      try {
        const response = await searchAPI.searchAll(query);
        setResults(response.data);
        setShowResults(true);
      } catch (error) {
        console.error('Error searching:', error);
      } finally {
        setLoading(false);
      }
    }, 300); // 300ms debounce

    return () => clearTimeout(timeoutId);
  }, [query]);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
        if (onClose) onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClose]);

  const handleResultClick = (type, id) => {
    setQuery('');
    setShowResults(false);
    if (onClose) onClose();
    navigate(`/${type}/${id}`);
  };

  const totalResults = results.destinations.length + results.activities.length;

  return (
    <div className="search-bar-container" ref={searchRef}>
      <div className="search-input-wrapper">
        <input
          type="text"
          className="search-input"
          placeholder="Cari destinasi atau aktivitas..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
        />
        {loading && <div className="search-loading">🔍</div>}
      </div>

      {showResults && query.trim() && (
        <div className="search-results">
          {totalResults === 0 ? (
            <div className="no-results">
              <p>Tidak ada hasil untuk "{query}"</p>
              <span>Coba kata kunci lain</span>
            </div>
          ) : (
            <>
              {results.destinations.length > 0 && (
                <div className="results-section">
                  <h4 className="results-title">Destinasi ({results.destinations.length})</h4>
                  {results.destinations.map((destination) => (
                    <div
                      key={destination.id}
                      className="result-item"
                      onClick={() => handleResultClick('destinations', destination.id)}
                    >
                      <div className="result-image">
                        <img src={destination.image || '/assets/images/placeholder.jpg'} alt={destination.name} />
                      </div>
                      <div className="result-info">
                        <h5>{destination.name}</h5>
                        <p>{destination.description?.substring(0, 80)}...</p>
                        <span className="result-category">{destination.category}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {results.activities.length > 0 && (
                <div className="results-section">
                  <h4 className="results-title">Aktivitas ({results.activities.length})</h4>
                  {results.activities.map((activity) => (
                    <div
                      key={activity.id}
                      className="result-item"
                      onClick={() => handleResultClick('activities', activity.id)}
                    >
                      <div className="result-image">
                        <img src={activity.image || '/assets/images/placeholder.jpg'} alt={activity.name} />
                      </div>
                      <div className="result-info">
                        <h5>{activity.name}</h5>
                        <p>{activity.description?.substring(0, 80)}...</p>
                        <span className="result-category">{activity.category}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
