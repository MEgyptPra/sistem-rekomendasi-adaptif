import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/header.css';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    setIsUserMenuOpen(false);
    navigate('/');
  };

  return (
    <header className="site-header">
      <div className="container">
        <div className="logo">
          <Link to="/">
            <img 
              src="/assets/logo.png" 
              alt="Travel Logo" 
              onError={e => {e.target.onerror=null;e.target.src='/assets/images/placeholder.webp';}}
            />
          </Link>
        </div>
        
        <button 
          className="mobile-menu-toggle" 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle menu"
        >
          <span className={`hamburger ${isMenuOpen ? 'open' : ''}`}></span>
        </button>
        
        <nav className={`main-nav ${isMenuOpen ? 'open' : ''}`}>
          <ul>
            <li><Link to="/destinations">Destinasi</Link></li>
            <li><Link to="/activities">Aktivitas</Link></li>
            <li><Link to="/planning">Perencanaan</Link></li>
            <li><Link to="/resources">Panduan & Sumber Informasi</Link></li>
            {isAuthenticated && (
              <li><Link to="/favorites">Favorit</Link></li>
            )}
          </ul>
        </nav>
        
        <div className="header-actions">
          {isAuthenticated ? (
            <div className="user-menu-wrapper">
              <button 
                className="user-menu-button"
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                aria-label="User menu"
              >
                <span className="user-avatar">
                  {user?.name?.charAt(0).toUpperCase() || 'U'}
                </span>
                <span className="user-name">{user?.name || 'User'}</span>
              </button>
              
              {isUserMenuOpen && (
                <div className="user-dropdown">
                  <div className="user-info">
                    <p className="user-email">{user?.email}</p>
                  </div>
                  <div className="dropdown-divider"></div>
                  <Link to="/planning" onClick={() => setIsUserMenuOpen(false)}>
                    📋 Itinerary Saya
                  </Link>
                  <Link to="/favorites" onClick={() => setIsUserMenuOpen(false)}>
                    ❤️ Favorit
                  </Link>
                  <div className="dropdown-divider"></div>
                  <button onClick={handleLogout} className="logout-button">
                    🚪 Keluar
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="btn-login">Masuk</Link>
              <Link to="/register" className="btn-register">Daftar</Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;