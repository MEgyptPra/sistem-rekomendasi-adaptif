import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { recommendationsAPI } from '../services/api';
import { itineraryAPI } from '../services/api';
import DestinationCard from '../components/destinations/DestinationCard';
import '../styles/planning.css';

const Planning = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedRegions, setSelectedRegions] = useState([]);
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  // State for user itineraries
  const [userItineraries, setUserItineraries] = useState([]);
  const [itineraryLoading, setItineraryLoading] = useState(true);
  const [itineraryError, setItineraryError] = useState('');

  useEffect(() => {
    const fetchItineraries = async () => {
      setItineraryLoading(true);
      setItineraryError('');
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setItineraryError('Anda harus login untuk melihat itinerary yang disimpan.');
          setItineraryLoading(false);
          return;
        }
        const res = await itineraryAPI.list();
        setUserItineraries(res.data);
      } catch (err) {
        setItineraryError('Gagal mengambil data itinerary.');
      } finally {
        setItineraryLoading(false);
      }
    };
    fetchItineraries();
  }, []);

  const handleRegionChange = (region) => {
    setSelectedRegions(prev => 
      prev.includes(region) 
        ? prev.filter(r => r !== region)
        : [...prev, region]
    );
  };

  const handleInterestChange = (interest) => {
    setSelectedInterests(prev => 
      prev.includes(interest) 
        ? prev.filter(i => i !== interest)
        : [...prev, interest]
    );
  };

  const handleGenerateItinerary = async () => {
    if (!startDate || !endDate) {
      alert('Mohon pilih tanggal mulai dan selesai');
      return;
    }

    setLoading(true);
    setShowResults(false);

    try {
      // ✅ GUNAKAN ML MODEL untuk generate recommendations
      // Algorithm: 'auto' akan smart select (hybrid jika trained, incremental jika belum)
      const response = await recommendationsAPI.getPersonalized({
        algorithm: 'auto', // Smart selection
        num_recommendations: 10,
        // Filter berdasarkan user selections (backend akan apply)
        filters: {
          regions: selectedRegions.length > 0 ? selectedRegions : undefined,
          categories: selectedInterests.length > 0 ? selectedInterests : undefined,
          start_date: startDate,
          end_date: endDate
        }
      });

      setRecommendations(response.data.recommendations || []);
      setShowResults(true);
      
      console.log('✅ ML-based itinerary generated:', {
        algorithm: response.data.metadata?.algorithm_used,
        count: response.data.recommendations?.length
      });
    } catch (error) {
      console.error('Error generating itinerary:', error);
      alert('Gagal membuat itinerary. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="planning-page">
      {/* User's Saved Itineraries Section */}
      <section className="user-itineraries-section">
        <div className="container">
          <h2>🗺️ Itinerary Saya</h2>
          {itineraryLoading && <p>Loading...</p>}
          {itineraryError && <p style={{ color: 'red' }}>{itineraryError}</p>}
          {!itineraryLoading && !itineraryError && (
            <div>
              {userItineraries.length === 0 ? (
                <p>Belum ada itinerary yang disimpan.</p>
              ) : (
                <ul>
                  {userItineraries.map((it, idx) => (
                    <li key={it.id || idx} style={{marginBottom: '1em'}}>
                      <strong>{it.title}</strong> ({it.start_date} - {it.end_date})<br />
                      <span>{it.description}</span>
                      <ul>
                        {it.days && it.days.map((day, i) => (
                          <li key={i}>
                            <strong>Hari {day.day_number} ({day.date})</strong>
                            <ul>
                              {day.items && day.items.map((item, j) => (
                                <li key={j}>{item.title} - {item.location}</li>
                              ))}
                            </ul>
                          </li>
                        ))}
                      </ul>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      </section>
      <section className="page-header">
        <div className="container">
          <h1>Rencanakan Perjalanan Anda</h1>
          <p>Buat itinerary personal dengan rekomendasi berbasis AI dari model Machine Learning kami</p>
        </div>
      </section>

      <section className="planning-content">
        <div className="container">
          {/* Trip Planner Tool */}
          <div className="trip-planner">
            <h2>🤖 Perencana Wisata AI</h2>
            <p>Sistem kami akan menggunakan Machine Learning untuk memberikan rekomendasi terbaik berdasarkan preferensi Anda</p>
            <div className="planner-tool">
              <div className="planner-form">
                <div className="form-group">
                  <label>Kapan Anda berkunjung?</label>
                  <div className="date-inputs">
                    <input 
                      type="date" 
                      placeholder="Tanggal Mulai" 
                      value={startDate}
                      onChange={(e) => setStartDate(e.target.value)}
                    />
                    <input 
                      type="date" 
                      placeholder="Tanggal Selesai" 
                      value={endDate}
                      onChange={(e) => setEndDate(e.target.value)}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>Wilayah mana yang Anda minati?</label>
                  <div className="checkbox-group">
                    <label><input type="checkbox" onChange={() => handleRegionChange('Sumedang Utara')} /> Sumedang Utara</label>
                    <label><input type="checkbox" onChange={() => handleRegionChange('Sumedang Selatan')} /> Sumedang Selatan</label>
                    <label><input type="checkbox" onChange={() => handleRegionChange('Jatinangor')} /> Jatinangor</label>
                    <label><input type="checkbox" onChange={() => handleRegionChange('Tanjungsari')} /> Tanjungsari</label>
                    <label><input type="checkbox" onChange={() => handleRegionChange('Darmaraja')} /> Darmaraja</label>
                    <label><input type="checkbox" onChange={() => handleRegionChange('Situraja')} /> Situraja</label>
                    <label><input type="checkbox" onChange={() => handleRegionChange('Cimalaka')} /> Cimalaka</label>
                  </div>
                </div>
                <div className="form-group">
                  <label>Apa minat Anda?</label>
                  <div className="checkbox-group">
                    <label><input type="checkbox" onChange={() => handleInterestChange('Wisata Alam')} /> Wisata Alam</label>
                    <label><input type="checkbox" onChange={() => handleInterestChange('Kuliner')} /> Kuliner</label>
                    <label><input type="checkbox" onChange={() => handleInterestChange('Seni & Budaya')} /> Seni & Budaya</label>
                    <label><input type="checkbox" onChange={() => handleInterestChange('Wisata Keluarga')} /> Wisata Keluarga</label>
                    <label><input type="checkbox" onChange={() => handleInterestChange('Belanja')} /> Belanja</label>
                    <label><input type="checkbox" onChange={() => handleInterestChange('Situs Bersejarah')} /> Situs Bersejarah</label>
                  </div>
                </div>
                <button 
                  className="btn primary" 
                  onClick={handleGenerateItinerary}
                  disabled={loading}
                >
                  {loading ? '🤖 Menganalisis dengan AI...' : '🚀 Buat Itinerary dengan AI'}
                </button>
              </div>
            </div>
          </div>

          {/* ML-Generated Recommendations */}
          {showResults && (
            <div className="ml-recommendations-section">
              <h2>✨ Rekomendasi untuk Anda</h2>
              <p className="ml-info">
                <strong>🤖 Powered by Machine Learning:</strong> Rekomendasi ini dihasilkan oleh model Hybrid Collaborative Filtering + Content-Based dengan Multi-Armed Bandit optimization
              </p>
              {recommendations.length > 0 ? (
                <div className="recommendations-grid">
                  {recommendations.map((dest) => (
                    <DestinationCard 
                      key={dest.destination_id || dest.id}
                      destination={{
                        id: dest.destination_id || dest.id,
                        name: dest.name,
                        description: dest.description,
                        image: dest.image,
                        region: dest.region,
                        category: dest.category
                      }}
                    />
                  ))}
                </div>
              ) : (
                <p>Tidak ada rekomendasi yang sesuai dengan kriteria Anda. Coba ubah filter.</p>
              )}
            </div>
          )}


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