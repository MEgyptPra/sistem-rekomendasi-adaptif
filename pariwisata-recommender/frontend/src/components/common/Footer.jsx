import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/footer.css';

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-logo">
            <Link to="/">
              <img src="/assets/logo-white.png" alt="Logo Wisata Sumedang" onError={e => {e.target.onerror=null;e.target.src='/assets/placeholder.webp';}} />
            </Link>
            <p>Jelajahi Keindahan Sumedang</p>
          </div>
          
          <div className="footer-links">
            <div className="footer-column">
              <h3>Jelajahi</h3>
              <ul>
                <li><Link to="/destinations">Destinasi Wisata</Link></li>
                <li><Link to="/activities">Aktivitas Wisata</Link></li>
                <li><Link to="/plan-your-trip">Rencanakan Trip</Link></li>
                <li><Link to="/resources">Panduan Wisata</Link></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h3>Rencanakan</h3>
              <ul>
                <li><Link to="/plan-your-trip#accommodations">Penginapan</Link></li>
                <li><Link to="/plan-your-trip#transportation">Transportasi</Link></li>
                <li><Link to="/plan-your-trip#visitor-centers">Pusat Informasi</Link></li>
                <li><Link to="/plan-your-trip#alerts">Info Perjalanan</Link></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h3>Tentang Kami</h3>
              <ul>
                <li><Link to="/about">Tentang Kami</Link></li>
                <li><Link to="/contact">Kontak</Link></li>
                <li><Link to="/accessibility">Aksesibilitas</Link></li>
                <li><Link to="/privacy">Kebijakan Privasi</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="footer-social">
            <h3>Ikuti Kami</h3>
            <div className="social-icons">
              <a href="https://facebook.com/sumedangtravel" aria-label="Facebook">
                <i className="social-icon facebook">Facebook</i>
              </a>
              <a href="https://instagram.com/sumedangtravel" aria-label="Instagram">
                <i className="social-icon instagram">Instagram</i>
              </a>
              <a href="https://twitter.com/sumedangtravel" aria-label="Twitter">
                <i className="social-icon twitter">Twitter</i>
              </a>
              <a href="https://youtube.com/sumedangtravel" aria-label="YouTube">
                <i className="social-icon youtube">YouTube</i>
              </a>
            </div>
            
            <div className="newsletter-signup-mini">
              <h3>Dapatkan Update</h3>
              <form>
                <input type="email" placeholder="Email Anda" />
                <button type="submit" className="btn">Berlangganan</button>
              </form>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2025 Wisata Sumedang. Hak Cipta Dilindungi.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;