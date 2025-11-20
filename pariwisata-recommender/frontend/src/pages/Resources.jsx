import React from 'react';
import '../styles/resources.css';
import SmartImage from '../components/common/SmartImage';
import placeholder from '../assets/placeholder.svg';

const Resources = () => {
  return (
    <div className="resources-page">
      <section className="page-header">
        <div className="container">
          <h1>Panduan & Sumber Informasi</h1>
          <p>Materi gratis untuk membantu Anda merencanakan perjalanan sempurna di Sumedang</p>
        </div>
      </section>

      <section className="resources-content">
        <div className="container">
          {/* Free Travel Guides */}
          <div className="travel-guides">
            <h2>Panduan Wisata Gratis</h2>
            <p>Unduh panduan wisata resmi Kabupaten Sumedang</p>
            
            <div className="guides-container">
              <div className="guide-item">
                <SmartImage publicSrc="/assets/images/oregon-guide.jpg" bundledSrc={placeholder} alt="Panduan Wisata Sumedang" />
                <div className="guide-info">
                  <h3>Panduan Wisata Resmi Sumedang</h3>
                  <p>Panduan lengkap menampilkan atraksi wisata, akomodasi, dan itinerary di Sumedang</p>
                  <div className="guide-buttons">
                    <button className="btn primary">Unduh PDF</button>
                    <button className="btn secondary">Pesan Versi Cetak</button>
                  </div>
                </div>
              </div>
              
              <div className="guide-item">
                <SmartImage publicSrc="/assets/images/oregon-map.jpg" bundledSrc={placeholder} alt="Peta Wisata Sumedang" />
                <div className="guide-info">
                  <h3>Peta Wisata Sumedang</h3>
                  <p>Peta rinci termasuk rute wisata, area istirahat, dan titik menarik di Sumedang</p>
                  <div className="guide-buttons">
                    <button className="btn primary">Unduh PDF</button>
                    <button className="btn secondary">Pesan Versi Cetak</button>
                  </div>
                </div>
              </div>
              
              <div className="guide-item">
                <SmartImage publicSrc="/assets/images/biking-guide.jpg" bundledSrc={placeholder} alt="Panduan Kuliner Sumedang" />
                <div className="guide-info">
                  <h3>Panduan Kuliner Sumedang</h3>
                  <p>Daftar kuliner khas, restoran, dan tips wisata kuliner di Sumedang</p>
                  <div className="guide-buttons">
                    <button className="btn primary">Unduh PDF</button>
                    <button className="btn secondary">Pesan Versi Cetak</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Newsletter Signup */}
          <div className="newsletter-section">
            <h2>Newsletter Email</h2>
            <p>Daftar untuk menerima inspirasi wisata, ide perjalanan, dan berita Sumedang</p>
            
            <div className="newsletter-signup">
              <form className="newsletter-form">
                <div className="form-group">
                  <label htmlFor="email">Alamat Email</label>
                  <input type="email" id="email" required placeholder="nama@email.com" />
                </div>
                
                <div className="form-group">
                  <label>Minat (pilih semua yang sesuai)</label>
                  <div className="checkbox-group">
                    <label><input type="checkbox" name="interests" value="outdoor" /> Wisata Alam</label>
                    <label><input type="checkbox" name="interests" value="food" /> Kuliner</label>
                    <label><input type="checkbox" name="interests" value="events" /> Event & Festival</label>
                    <label><input type="checkbox" name="interests" value="family" /> Wisata Keluarga</label>
                    <label><input type="checkbox" name="interests" value="deals" /> Promo Wisata</label>
                  </div>
                </div>
                
                <div className="form-group">
                  <label>Frekuensi Newsletter</label>
                  <select name="frequency">
                    <option value="weekly">Mingguan</option>
                    <option value="monthly">Bulanan</option>
                    <option value="quarterly">Per 3 Bulan</option>
                  </select>
                </div>
                
                <button type="submit" className="btn primary">Berlangganan</button>
                <p className="form-disclaimer">Anda dapat berhenti berlangganan kapan saja. Lihat Kebijakan Privasi kami.</p>
              </form>
            </div>
          </div>

          {/* Additional Resources */}
          <div className="additional-resources">
            <h2>Sumber Informasi Tambahan</h2>
            
            <div className="resources-grid">
              <div className="resource-card">
                <SmartImage publicSrc="/assets/images/accessibility.jpg" bundledSrc={placeholder} alt="Panduan Aksesibilitas" />
                <h3>Panduan Aksesibilitas</h3>
                <p>Informasi tentang atraksi, jalur, dan akomodasi yang mudah diakses</p>
                <button className="btn secondary">Pelajari Lebih Lanjut</button>
              </div>
              
              <div className="resource-card">
                <SmartImage publicSrc="/assets/images/responsible-travel.jpg" bundledSrc={placeholder} alt="Wisata Bertanggung Jawab" />
                <h3>Wisata Bertanggung Jawab</h3>
                <p>Tips meminimalkan dampak lingkungan saat menjelajahi Sumedang</p>
                <button className="btn secondary">Pelajari Lebih Lanjut</button>
              </div>
              
              <div className="resource-card">
                <SmartImage publicSrc="/assets/images/travel-tips.jpg" bundledSrc={placeholder} alt="Tips Wisata Musiman" />
                <h3>Tips Wisata Musiman</h3>
                <p>Apa yang diharapkan dan cara mempersiapkan setiap musim di Sumedang</p>
                <button className="btn secondary">Pelajari Lebih Lanjut</button>
              </div>
              
              <div className="resource-card">
                <SmartImage publicSrc="/assets/images/travel-faqs.jpg" bundledSrc={placeholder} alt="FAQ Wisata" />
                <h3>FAQ Wisata</h3>
                <p>Jawaban untuk pertanyaan umum tentang berwisata di Sumedang</p>
                <button className="btn secondary">Pelajari Lebih Lanjut</button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Resources;