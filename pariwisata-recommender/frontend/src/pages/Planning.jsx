import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import jsPDF from 'jspdf';
import { itineraryAPI, recommendationsAPI, categoriesAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Alert from '../components/common/Alert';
import '../styles/planning.css';
import '../styles/planning-detail.css'; 

// Kunci Session Storage
const PREVIEW_KEY = 'planning_preview_itinerary';

// Komponen Kartu Itinerary (Tetap Sama)
const ItineraryCard = ({ itinerary }) => {
  const navigate = useNavigate();
  const start = new Date(itinerary.start_date);
  const end = new Date(itinerary.end_date);
  const diffTime = Math.abs(end - start);
  const durationDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
  const isUpcoming = new Date() < start;
  const coverImage = itinerary.days?.[0]?.items?.[0]?.destination?.image || '/assets/images/planning-placeholder.jpg';

  return (
    <div className="itinerary-card" onClick={() => navigate(`/planning/${itinerary.id}`)}>
      <div className="card-image-wrapper">
        <img src={coverImage} alt={itinerary.title} className="card-image" />
        <span className={`status-badge ${isUpcoming ? 'upcoming' : 'completed'}`}>
          {isUpcoming ? 'Akan Datang' : 'Selesai'}
        </span>
      </div>
      <div className="card-content">
        <h3 className="card-title">{itinerary.title}</h3>
        <div className="card-meta">
          <span className="meta-item">📅 {start.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })}</span>
          <span className="meta-dot">•</span>
          <span className="meta-item">⏳ {durationDays} Hari</span>
        </div>
        <div className="card-footer">
          <button className="btn-text">Lihat Detail →</button>
        </div>
      </div>
    </div>
  );
};

// =========================================================
// KOMPONEN UTAMA PLANNING
// =========================================================
const Planning = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedInterests, setSelectedInterests] = useState([]);
  
  const [categories, setCategories] = useState([]);
  const [itineraries, setItineraries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);
  // State diinisialisasi dari session storage
  const [previewItinerary, setPreviewItinerary] = useState(() => {
    const saved = sessionStorage.getItem(PREVIEW_KEY);
    return saved ? JSON.parse(saved) : null;
  });

  // Effect: Load Data Awal & State Persistence
  useEffect(() => {
    const initData = async () => {
      setLoading(true);
      try {
        // Load Kategori
        try {
          const catRes = await categoriesAPI.getAll();
          setCategories(catRes.data || []);
        } catch (err) {
          setCategories([{ name: "Wisata Alam" }, { name: "Kuliner" }]);
        }

        // Load Itinerary (Hanya jika login)
        if (isAuthenticated) {
          const itinRes = await itineraryAPI.getAll();
          setItineraries(itinRes.data || []);
        }
        
        // [BARU] Jika ada preview yang dimuat, scroll ke sana
        if (previewItinerary) {
             setTimeout(() => {
                document.getElementById('preview-section')?.scrollIntoView({ behavior: 'smooth' });
             }, 100);
        }

      } catch (err) { console.error(err); } 
      finally { setLoading(false); }
    };
    initData();
  }, [isAuthenticated]);

  // Effect: Simpan ke Session Storage setiap kali preview berubah
  useEffect(() => {
    if (previewItinerary) {
      sessionStorage.setItem(PREVIEW_KEY, JSON.stringify(previewItinerary));
    } else {
      sessionStorage.removeItem(PREVIEW_KEY);
    }
  }, [previewItinerary]);


  const handleInterestChange = (interestName) => {
    setSelectedInterests(prev => 
      prev.includes(interestName) ? prev.filter(i => i !== interestName) : [...prev, interestName]
    );
  };

  const calculateDistance = (lat1, lon1, lat2, lon2) => {
      if (!lat1 || !lon1 || !lat2 || !lon2) return 9999;
      const R = 6371; 
      const dLat = (lat2 - lat1) * (Math.PI / 180);
      const dLon = (lon2 - lon1) * (Math.PI / 180);
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c;
  };

  const optimizeRoute = (places) => {
      if (places.length < 2) return places;
      let startNode = places.reduce((prev, current) => (prev.latitude > current.latitude) ? prev : current);
      const sortedRoute = [startNode];
      const unvisited = places.filter(p => p !== startNode);
      let currentNode = startNode;

      while (unvisited.length > 0) {
          let nearest = null;
          let minDist = Infinity;
          let nearestIdx = -1;

          for (let i = 0; i < unvisited.length; i++) {
              const dist = calculateDistance(
                  currentNode.latitude, currentNode.longitude,
                  unvisited[i].latitude, unvisited[i].longitude
              );
              if (dist < minDist) {
                  minDist = dist;
                  nearest = unvisited[i];
                  nearestIdx = i;
              }
          }

          if (nearest) {
              sortedRoute.push(nearest);
              currentNode = nearest;
              unvisited.splice(nearestIdx, 1);
          } else {
              sortedRoute.push(...unvisited);
              break;
          }
      }
      return sortedRoute;
  };

  const generateAndDownloadPDF = (itineraryData) => {
    try {
      const doc = new jsPDF();
      doc.setFontSize(18);
      doc.text(itineraryData.title, 10, 20);
      doc.setFontSize(12);
      doc.text(`Tanggal: ${itineraryData.start_date} s/d ${itineraryData.end_date}`, 10, 30);
      
      let y = 50;
      itineraryData.days.forEach((day) => {
        if (y > 270) { doc.addPage(); y = 20; }
        doc.setFont(undefined, 'bold');
        doc.text(`Hari ${day.day_number}:`, 10, y);
        doc.setFont(undefined, 'normal');
        y += 7;
        
        if (day.items.length === 0) {
            doc.text("- (Istirahat / Bebas)", 15, y);
            y += 7;
        } else {
            day.items.forEach((item) => {
                if (y > 280) { doc.addPage(); y = 20; }
                doc.text(`- ${item.title} (${item.category})`, 15, y);
                doc.setFontSize(10);
                doc.text(`  ${item.location}`, 15, y + 4);
                doc.setFontSize(12);
                y += 12;
            });
        }
        y += 5;
      });
      
      doc.save('Rencana_Perjalanan_Sumedang.pdf');
      alert("✅ Itinerary berhasil diunduh sebagai PDF! (Login untuk menyimpan ke akun)");
      
    } catch (err) {
      console.error("PDF Error:", err);
      alert("Gagal mengunduh PDF.");
    }
  };

  // --- FUNGSI UTAMA: GENERATE ---
  const handleGenerateItinerary = async () => {
    if (!startDate || !endDate) {
      alert('Mohon pilih Tanggal Mulai dan Tanggal Selesai (Wajib).');
      return;
    }

    if (new Date(startDate) > new Date(endDate)) {
      alert('Tanggal selesai tidak boleh sebelum tanggal mulai.');
      return;
    }

    setGenerating(true);
    setPreviewItinerary(null); // Clear preview saat mulai generate

    try {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const diffTime = Math.abs(end - start);
      const durationDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
      const totalRecsNeeded = durationDays * 3; 
      
      const response = await recommendationsAPI.getPersonalized({
        algorithm: 'auto',
        num_recommendations: totalRecsNeeded, 
        filters: {
            categories: selectedInterests.length > 0 ? selectedInterests : undefined,
            start_date: startDate,
            end_date: endDate
        }
      });
      
      let recs = response.data.recommendations || [];
      
      if (recs.length === 0) {
        alert("Sistem tidak menemukan rekomendasi yang cocok. Coba ubah tanggal atau minat.");
        setGenerating(false);
        return;
      }

      // 1. OPTIMASI RUTE (Nearest Neighbor)
      const optimizedRecs = optimizeRoute(recs);

      // 2. Distribusi ke Hari
      const days = [];
      const itemsPerDay = Math.ceil(optimizedRecs.length / durationDays);

      for (let i = 0; i < durationDays; i++) {
        const dayStart = i * itemsPerDay;
        const dayEnd = Math.min((i + 1) * itemsPerDay, optimizedRecs.length);
        const dayDestinations = optimizedRecs.slice(dayStart, dayEnd);
        
        // Info Rute Harian
        let dayRouteInfo = "Rute Efisien";
        if (dayDestinations.length > 1) {
             const dist = calculateDistance(
                 dayDestinations[0].latitude, dayDestinations[0].longitude,
                 dayDestinations[dayDestinations.length-1].latitude, dayDestinations[dayDestinations.length-1].longitude
             );
             dayRouteInfo = `Estimasi Jarak: ~${dist.toFixed(1)} km`;
        }

        const currentDate = new Date(start);
        currentDate.setDate(currentDate.getDate() + i);
        
        days.push({
          day_number: i + 1,
          date: currentDate.toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long' }),
          route_info: dayRouteInfo,
          items: dayDestinations.map((dest, idx) => ({
            activity_type: 'destination',
            entity_id: dest.destination_id || dest.id,
            title: dest.name,
            category: dest.category || 'Wisata', 
            location: dest.address || dest.region || 'Sumedang',
            duration: '2 jam', 
            order: idx + 1,
            notes: `Rekomendasi AI (Skor: ${(dest.score * 100).toFixed(0)}%)`
          }))
        });
      }

      const itineraryData = {
        title: `Trip Sumedang (${selectedInterests.join(', ') || 'Best Route'})`,
        description: `Itinerary cerdas dengan optimasi rute perjalanan (Nearest Neighbor).`,
        start_date: startDate,
        end_date: endDate,
        days: days
      };

      // Aksi Akhir: Simpan atau Preview
      if (isAuthenticated) {
          await itineraryAPI.create(itineraryData);
          alert("✅ Berhasil! Rencana perjalanan telah disimpan ke akun Anda.");
          const updatedList = await itineraryAPI.getAll();
          setItineraries(updatedList.data || []);
      } else {
          // ANONYMOUS: Set Preview (dipersistensi via useEffect)
          setPreviewItinerary(itineraryData);
          setTimeout(() => {
             document.getElementById('preview-section')?.scrollIntoView({ behavior: 'smooth' });
          }, 100);
      }

    } catch (err) {
      console.error("Gagal generate:", err);
      alert("Terjadi kesalahan saat membuat rekomendasi.");
    } finally {
      setGenerating(false);
    }
  };

  const handleResetPreview = () => {
    // [BARU] Hapus dari Session Storage
    sessionStorage.removeItem(PREVIEW_KEY);
    setPreviewItinerary(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="planning-page">
      <section className="page-header">
        <div className="container header-content">
          <div><h1>Rencana Perjalanan Saya</h1><p>Kelola semua rencana liburan Anda di Sumedang.</p></div>
        </div>
      </section>

      <section className="planning-content">
        <div className="container">
          <div className="trip-planner">
            <h2>🤖 Generator Itinerary Cerdas (Geo-Optimized)</h2>
            <p>Sistem akan memilih tempat terbaik (MMR) lalu mengurutkan rutenya agar hemat waktu di jalan.</p>
            
            <div className="planner-form">
              <div className="form-group">
                <label>Kapan Anda berkunjung?</label>
                <div className="date-inputs">
                  <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="form-control" />
                  <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="form-control" />
                </div>
              </div>

              <div className="form-group">
                <label>Apa minat spesifik Anda? (Opsional)</label>
                {categories.length > 0 ? (
                  <div className="checkbox-group">
                    {categories.map(cat => (
                      <label key={cat.id || cat.name}>
                        <input type="checkbox" checked={selectedInterests.includes(cat.name)} onChange={() => handleInterestChange(cat.name)} /> {cat.name}
                      </label>
                    ))}
                  </div>
                ) : <p className="text-muted">Memuat...</p>}
              </div>

              <button className="btn primary" onClick={handleGenerateItinerary} disabled={generating} style={{width: '100%', marginTop: '1rem'}}>
                {generating ? '⏳ Mengoptimalkan Rute...' : '✨ Generate Itinerary Optimal'}
              </button>
            </div>
          </div>

          {isAuthenticated ? (
            <>
              <h2 style={{marginTop: '3rem'}}>Rencana Tersimpan</h2>
              {error && <Alert type="error" message={error} />}
              {loading ? (
                <LoadingSpinner text="Memuat rencana perjalanan..." />
              ) : itineraries.length > 0 ? (
                <div className="itineraries-grid">
                  {itineraries.map(itin => <ItineraryCard key={itin.id} itinerary={itin} />)}
                </div>
              ) : (
                <div className="empty-state">
                  <h3>Belum Ada Rencana Tersimpan</h3>
                  <p>Gunakan alat generator di atas untuk membuat rencana pertama Anda.</p>
                </div>
              )}
            </>
          ) : (
            <div id="preview-section" style={{marginTop: '3rem'}}>
              {previewItinerary ? (
                <div className="daily-itinerary" style={{ background: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 15px rgba(0,0,0,0.05)' }}>
                   <div style={{textAlign: 'center', marginBottom: '2rem', borderBottom: '2px solid #f0f0f0', paddingBottom: '1rem'}}>
                      <span className="status-badge upcoming" style={{position: 'relative', display: 'inline-block'}}>Preview Rute</span>
                      <h2>{previewItinerary.title}</h2>
                      <p style={{color: '#28a745'}}>✓ Rute dioptimalkan berdasarkan lokasi (Nearest Neighbor)</p>
                   </div>

                   {previewItinerary.days.map(day => (
                      <div key={day.day_number} className="day-section">
                          <div className="day-header">
                              <div className="day-number">Hari {day.day_number}</div>
                              <div className="day-info">
                                  <h3>{day.date}</h3>
                                  <small style={{color: '#667eea'}}>{day.route_info}</small>
                              </div>
                          </div>
                          <div className="activities-timeline">
                              {day.items.map((item, idx) => (
                                  <div key={idx} className="activity-item">
                                      <div className="activity-time"><span className="time">{String(idx*3 + 8).padStart(2,'0')}:00</span></div>
                                      <div className="activity-marker"><span className="icon">📍</span></div>
                                      <div className="activity-content">
                                          <h4>
                                              <Link to={`/destinations/${item.entity_id}`} className="text-primary hover:underline" style={{color: '#667eea', textDecoration: 'none'}}>
                                                  {item.title}
                                              </Link>
                                          </h4>
                                          <span style={{fontSize: '0.8rem', background: '#f0f0f0', padding: '2px 8px', borderRadius: '4px', color: '#555', marginBottom: '0.5rem', display: 'inline-block'}}>
                                              {item.category}
                                          </span>
                                          <p className="location" style={{fontSize: '0.9rem', color: '#666', marginTop: '4px'}}>
                                              📍 {item.location}
                                          </p>
                                      </div>
                                  </div>
                              ))}
                          </div>
                      </div>
                   ))}
                   <div className="modal-actions" style={{marginTop: '2rem', textAlign: 'center'}}>
                      <button className="btn secondary" onClick={handleResetPreview}>🗑️ Buat Ulang</button>
                      <button className="btn primary" onClick={() => generateAndDownloadPDF(previewItinerary)} style={{marginLeft: '1rem'}}>⬇️ Download PDF</button>
                   </div>
                   <div style={{textAlign: 'center', marginTop: '1rem'}}>
                     <Link to="/login">Login untuk menyimpan</Link>
                   </div>
                </div>
              ) : (
                <div className="empty-state">
                    <h3>Login untuk Menyimpan</h3>
                    <Link to="/login" className="btn primary">Login Sekarang</Link>
                </div>
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Planning;