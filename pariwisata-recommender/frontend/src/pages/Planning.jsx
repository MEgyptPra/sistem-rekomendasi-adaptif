import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/planning.css';

const Planning = () => {
  return (
    <div className="planning-page">
      <section className="page-header">
        <div className="container">
          <h1>Rencanakan Perjalanan Anda</h1>
          <p>Semua yang Anda butuhkan untuk menciptakan petualangan sempurna di Sumedang</p>
        </div>
      </section>

      <section className="planning-content">
        <div className="container">
          {/* Trip Planner Tool */}
          <div className="trip-planner">
            <h2>Perencana Wisata Sumedang</h2>
            <p>Buat itinerary personal Anda untuk menjelajahi Sumedang</p>
            <div className="planner-tool">
              <div className="planner-form">
                <div className="form-group">
                  <label>Kapan Anda berkunjung?</label>
                  <div className="date-inputs">
                    <input type="date" placeholder="Tanggal Mulai" />
                    <input type="date" placeholder="Tanggal Selesai" />
                  </div>
                </div>
                <div className="form-group">
                  <label>Wilayah mana yang Anda minati?</label>
                  <div className="checkbox-group">
                    <label><input type="checkbox" /> Sumedang Utara</label>
                    <label><input type="checkbox" /> Sumedang Selatan</label>
                    <label><input type="checkbox" /> Jatinangor</label>
                    <label><input type="checkbox" /> Tanjungsari</label>
                    <label><input type="checkbox" /> Darmaraja</label>
                    <label><input type="checkbox" /> Situraja</label>
                    <label><input type="checkbox" /> Cimalaka</label>
                  </div>
                </div>
                <div className="form-group">
                  <label>Apa minat Anda?</label>
                  <div className="checkbox-group">
                    <label><input type="checkbox" /> Wisata Alam</label>
                    <label><input type="checkbox" /> Kuliner</label>
                    <label><input type="checkbox" /> Seni & Budaya</label>
                    <label><input type="checkbox" /> Wisata Keluarga</label>
                    <label><input type="checkbox" /> Belanja</label>
                    <label><input type="checkbox" /> Situs Bersejarah</label>
                  </div>
                </div>
                <button className="btn primary">Buat Itinerary Saya</button>
              </div>
            </div>
          </div>

          {/* Accommodations */}
          <div className="accommodations planning-section">
            <h2>Tempat Menginap</h2>
            <div className="accommodation-types">
              <div className="accommodation-card">
                <img src="/assets/images/hotels.jpg" alt="Hotels" />
                <h3>Hotel & Penginapan</h3>
                <p>Temukan pilihan akomodasi nyaman di Sumedang</p>
                <button className="btn secondary">Lihat Hotel</button>
              </div>
              <div className="accommodation-card">
                <img src="/assets/images/camping.jpg" alt="Camping" />
                <h3>Camping & Area Berkemah</h3>
                <p>Terhubung dengan alam di lokasi camping indah</p>
                <button className="btn secondary">Cari Lokasi Camping</button>
              </div>
              <div className="accommodation-card">
                <img src="/assets/images/vacation-rentals.jpg" alt="Vacation Rentals" />
                <h3>Villa & Homestay</h3>
                <p>Vila, guest house, dan tempat menginap unik</p>
                <button className="btn secondary">Jelajahi Penginapan</button>
              </div>
            </div>
          </div>

          {/* Transportation */}
          <div className="transportation planning-section">
            <h2>Transportasi</h2>
            <div className="transportation-options">
              <div className="transport-card">
                <h3>Kendaraan Pribadi</h3>
                <p>Informasi kondisi jalan, rute wisata, dan area parkir di Sumedang</p>
              </div>
              <div className="transport-card">
                <h3>Transportasi Umum</h3>
                <p>Angkutan umum, travel, dan ojek online di Sumedang</p>
              </div>
              <div className="transport-card">
                <h3>Rental Kendaraan</h3>
                <p>Sewa mobil dan motor untuk kemudahan perjalanan Anda</p>
              </div>
            </div>
            <div className="road-conditions">
              <h3>Kondisi Jalan Terkini</h3>
              <p>Cek informasi jalan, penutupan rute, dan konstruksi jalan</p>
              <button className="btn secondary">Lihat Kondisi Jalan</button>
            </div>
          </div>

          {/* Visitor Centers */}
          <div className="visitor-centers planning-section">
            <h2>Pusat Informasi Wisata</h2>
            <p>Kunjungi pusat informasi wisata Sumedang untuk mendapatkan wawasan lokal, peta, dan brosur</p>
            <div className="center-map">
              <img src="/assets/images/visitor-center-map.jpg" alt="Peta Pusat Informasi" />
              <p>Peta interaktif akan terintegrasi di sini</p>
            </div>
            <button className="btn secondary">Cari Pusat Informasi</button>
          </div>

          {/* Travel Alerts */}
          <div className="travel-alerts planning-section">
            <h2>Pengumuman & Kondisi Perjalanan</h2>
            <div className="alert-box">
              <h3>Pengumuman Terkini</h3>
              <ul className="alerts-list">
                <li className="alert-item">
                  <span className="alert-type warning">Cuaca</span>
                  <p>Peringatan cuaca buruk di wilayah pegunungan. Cek kondisi jalan sebelum bepergian.</p>
                </li>
                <li className="alert-item">
                  <span className="alert-type info">Wisata</span>
                  <p>Penutupan sementara di beberapa objek wisata. Cek website untuk detail.</p>
                </li>
              </ul>
              <button className="btn secondary">Lihat Semua Pengumuman</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Planning;