import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { itineraryAPI } from '../services/api'; // Import API
import { useAuth } from '../contexts/AuthContext';
import LoadingSpinner from '../components/common/LoadingSpinner';
import '../styles/planning-detail.css';

const PlanningDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  
  const [itinerary, setItinerary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleting, setDeleting] = useState(false);

  // Fetch Data Asli dari Backend
  useEffect(() => {
    const fetchItineraryDetail = async () => {
      try {
        setLoading(true);
        const response = await itineraryAPI.getById(id);
        setItinerary(response.data);
      } catch (err) {
        console.error("Gagal load detail:", err);
        setError("Itinerary tidak ditemukan atau Anda tidak memiliki akses.");
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchItineraryDetail();
    }
  }, [id]);

  // Fungsi Hapus
  const handleDelete = async () => {
    if (!window.confirm("Apakah Anda yakin ingin menghapus rencana perjalanan ini?")) return;
    
    setDeleting(true);
    try {
      await itineraryAPI.delete(id);
      navigate('/planning'); // Kembali ke daftar
    } catch (err) {
      alert("Gagal menghapus itinerary.");
      setDeleting(false);
    }
  };

  const getActivityIcon = (type) => {
    const icons = {
      destination: '📍',
      activity: '🎯',
      meal: '🍽️',
      transport: '🚗',
      accommodation: '🏨',
      shopping: '🛍️'
    };
    return icons[type] || '📍';
  };

  if (loading) return <div className="loading-container"><LoadingSpinner /></div>;
  
  if (error || !itinerary) {
    return (
      <div className="error-container">
        <h2>Gagal Memuat</h2>
        <p>{error || "Data tidak ditemukan"}</p>
        <Link to="/planning" className="btn primary">Kembali ke Planning</Link>
      </div>
    );
  }

  // Format Tanggal
  const startDate = new Date(itinerary.start_date).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
  const endDate = new Date(itinerary.end_date).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });

  // Gambar cover (ambil dari item pertama, atau placeholder)
  const coverImage = itinerary.days?.[0]?.items?.[0]?.destination?.image 
    || '/assets/images/planning-placeholder.jpg';

  return (
    <div className="planning-detail-page">
      {/* Hero Section */}
      <section className="itinerary-hero" style={{ backgroundImage: `url(${coverImage})` }}>
        <div className="hero-overlay">
          <div className="container">
            <div className="breadcrumb">
              <Link to="/">Beranda</Link> / <Link to="/planning">Planning</Link> / <span>{itinerary.title}</span>
            </div>
            <div className="hero-content">
              <span className="status-badge upcoming">Rencana Perjalanan</span>
              <h1>{itinerary.title}</h1>
              <p className="description">{itinerary.description || "Tidak ada deskripsi."}</p>
              <div className="itinerary-meta">
                <span className="meta-item">📅 {startDate} - {endDate}</span>
                <span className="meta-item">📍 {itinerary.days?.length || 0} Hari</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="container itinerary-content">
        {/* Quick Actions */}
        <div className="quick-actions">
          <button className="btn secondary" onClick={() => window.print()}>
            <span>🖨️</span> Cetak / PDF
          </button>
          <button className="btn btn-danger" onClick={handleDelete} disabled={deleting} style={{backgroundColor: '#ff4d4d', color: 'white'}}>
            <span>🗑️</span> {deleting ? 'Menghapus...' : 'Hapus Itinerary'}
          </button>
        </div>

        <div className="row-layout">
            {/* Daily Itinerary */}
            <section className="daily-itinerary" style={{flex: 2}}>
              <h2>Rencana Harian</h2>
              
              {itinerary.days && itinerary.days.map((day) => (
                <div key={day.id || day.day_number} className="day-section">
                  <div className="day-header">
                    <div className="day-number">Hari {day.day_number}</div>
                    <div className="day-info">
                      <h3>{new Date(day.date).toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long' })}</h3>
                    </div>
                  </div>

                  <div className="activities-timeline">
                    {day.items && day.items.map((item, index) => (
                      <div key={item.id || index} className="activity-item">
                        <div className="activity-time">
                          <span className="time">{String(index + 8).padStart(2, '0')}:00</span> {/* Simulasi Jam */}
                          <span className="duration">{item.duration || '2 jam'}</span>
                        </div>
                        <div className="activity-marker">
                          <span className="icon">{getActivityIcon(item.activity_type || 'destination')}</span>
                        </div>
                        <div className="activity-content">
                          <h4>{item.title || item.destination?.name}</h4>
                          <p className="location">📍 {item.location || item.destination?.address || 'Sumedang'}</p>
                          {item.notes && <p className="description note">{item.notes}</p>}
                          
                          {/* Link ke detail destinasi */}
                          {item.entity_id && (
                            <Link to={`/destinations/${item.entity_id}`} className="destination-link">
                                Lihat Detail Destinasi →
                            </Link>
                          )}
                        </div>
                      </div>
                    ))}
                    
                    {(!day.items || day.items.length === 0) && (
                        <p className="text-muted" style={{marginLeft: '80px'}}>Belum ada aktivitas di hari ini.</p>
                    )}
                  </div>
                </div>
              ))}
            </section>

            {/* Sidebar Info */}
            <aside className="sidebar-info" style={{flex: 1, paddingLeft: '2rem'}}>
                <div className="overview-card">
                    <h3>📝 Catatan</h3>
                    <p>{itinerary.description || "Gunakan bagian ini untuk mencatat hal penting."}</p>
                </div>
                
                <div className="overview-card">
                    <h3>💰 Estimasi Biaya</h3>
                    <p className="text-muted">Fitur estimasi biaya otomatis akan segera hadir.</p>
                </div>
            </aside>
        </div>
      </div>
    </div>
  );
};

export default PlanningDetail;