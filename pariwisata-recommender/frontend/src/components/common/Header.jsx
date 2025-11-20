import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/header.css';
import logo from '../../assets/favicon.svg';
import SmartImage from './SmartImage';
import placeholder from '../../assets/placeholder.svg';
// External/public image (optional) that may be replaced at runtime.
const PUBLIC_HEADER_IMAGE = '/assets/favicon.png?v=2';

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

  const [imgSrc, setImgSrc] = useState(logo);

  // Behavior:
  // - By default use the local imported `logo` (stable, bundled by Vite).
  // - If the user performs a full browser refresh (navigation type 'reload'),
  //   attempt to fetch the public header image once (no-cache). If successful,
  //   use it and remember in sessionStorage that it exists; otherwise fall back
  //   to the bundled `logo` or public placeholder.
  // - Do NOT attempt automatic re-fetches on HMR or runtime updates.

  useEffect(() => {
    try {
      const navEntries = (performance.getEntriesByType && performance.getEntriesByType('navigation')) || [];
      const navType = (navEntries[0] && navEntries[0].type) || (performance.navigation && performance.navigation.type === 1 ? 'reload' : 'navigate');

      const cached = sessionStorage.getItem('headerImageExists');

      // Only try to fetch the public image when this load was a real browser reload
      // or if we have a cached positive flag.
      if (navType === 'reload') {
        // Attempt a single fetch with no-cache to verify existence
        fetch(PUBLIC_HEADER_IMAGE, { method: 'GET', cache: 'no-store' })
          .then(resp => {
            if (resp.ok) {
              sessionStorage.setItem('headerImageExists', 'true');
              setImgSrc(PUBLIC_HEADER_IMAGE);
            } else {
              sessionStorage.setItem('headerImageExists', 'false');
              setImgSrc(logo);
            }
          })
          .catch(() => {
            sessionStorage.setItem('headerImageExists', 'false');
            setImgSrc(logo);
          });
      } else if (cached === 'true') {
        // If earlier we found the public image exists, use it — but do not re-fetch.
        setImgSrc(PUBLIC_HEADER_IMAGE);
      } else {
        // Default: use bundled logo to avoid network fetches during HMR/dev.
        setImgSrc(logo);
      }
    } catch (e) {
      setImgSrc(logo);
    }
  }, []);

  return (
    <header className="site-header">
      <div className="container">
        <div className="logo">
          <Link to="/">
            <SmartImage publicSrc={imgSrc && imgSrc.startsWith('/assets') ? imgSrc : undefined} bundledSrc={logo} placeholder={placeholder} alt="Hayu Ka Sumedang" />
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