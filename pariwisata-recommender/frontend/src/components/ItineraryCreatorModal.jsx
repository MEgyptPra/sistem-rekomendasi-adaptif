import React, { useState } from 'react';
import jsPDF from 'jspdf';
import { useNavigate } from 'react-router-dom';
import { itineraryAPI } from '../services/api';
import '../styles/itinerary-creator-modal.css';

const ItineraryCreatorModal = ({ isOpen, onClose, recommendations }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Form state
  const [tripName, setTripName] = useState(`Trip Sumedang ${new Date().toLocaleDateString('id-ID')}`);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [duration, setDuration] = useState(3); // Default 3 hari
  const [notes, setNotes] = useState('Trip otomatis dari rekomendasi Kejutkan Saya');

  // =====================================================================
  // FUNGSI 1: DOWNLOAD PDF (Untuk User Tanpa Login)
  // Posisi: Sejajar dengan handleCreateItinerary (Scope Komponen Utama)
  // =====================================================================
  const downloadItineraryAsPDF = () => {
    try {
      const doc = new jsPDF();
      
      // Judul
      doc.setFontSize(16);
      doc.text(tripName, 10, 20);
      
      // Info Dasar
      doc.setFontSize(12);
      doc.text(`Tanggal: ${startDate} - ${duration} hari`, 10, 30);
      doc.text(`Catatan: ${notes}`, 10, 40);
      
      let y = 50;
      
      // Loop per Hari
      for (let i = 0; i < duration; i++) {
        // Cek halaman baru jika y terlalu bawah (batas A4 ~290mm)
        if (y > 270) {
          doc.addPage();
          y = 20;
        }

        // Header Hari
        doc.setFont(undefined, 'bold');
        doc.text(`Hari ${i + 1}:`, 10, y);
        doc.setFont(undefined, 'normal');
        y += 8;
        
        // Ambil destinasi untuk hari ini
        const recList = Array.isArray(recommendations) ? recommendations : [];
        const destinationsPerDay = Math.ceil(recList.length / duration);
        const dayStart = i * destinationsPerDay;
        const dayEnd = Math.min((i + 1) * destinationsPerDay, recList.length);
        const dayDestinations = recList.slice(dayStart, dayEnd);
        
        // Tulis Destinasi
        if (dayDestinations.length === 0) {
          doc.text(`- (Bebas / Istirahat)`, 15, y);
          y += 7;
        } else {
          dayDestinations.forEach((dest) => {
            doc.text(`- ${dest.name}`, 15, y);
            y += 7;
          });
        }
        y += 4; // Spasi antar hari
      }
      
      // Simpan File
      doc.save(`${tripName.replace(/\s+/g, '_')}.pdf`);
      
    } catch (err) {
      console.error("Gagal download PDF:", err);
      setError("Gagal membuat file PDF. Pastikan library jsPDF terinstall.");
    }
  };

  // =====================================================================
  // FUNGSI 2: CREATE ITINERARY API (Untuk User Login)
  // Posisi: Sejajar dengan downloadItineraryAsPDF
  // =====================================================================
  const handleCreateItinerary = async () => {
    setLoading(true);
    setError(null);

    try {
      // Cek token login
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Anda harus login terlebih dahulu untuk menyimpan ke database.');
        setLoading(false);
        return;
      }

      // Hitung tanggal akhir
      const start = new Date(startDate);
      const end = new Date(start);
      end.setDate(end.getDate() + duration - 1);

      // Distribusi destinasi ke hari-hari (sama logikanya dengan PDF)
      const recList = Array.isArray(recommendations) ? recommendations : [];
      const destinationsPerDay = Math.ceil(recList.length / duration);
      const days = [];
      
      for (let i = 0; i < duration; i++) {
        const dayStart = i * destinationsPerDay;
        const dayEnd = Math.min((i + 1) * destinationsPerDay, recList.length);
        const dayDestinations = recList.slice(dayStart, dayEnd);
        
        const currentDate = new Date(start);
        currentDate.setDate(currentDate.getDate() + i);
        
        days.push({
          day_number: i + 1,
          date: currentDate.toISOString().split('T')[0],
          title: `Hari ${i + 1}`,
          items: dayDestinations.map((dest, idx) => ({
            activity_type: 'destination',
            entity_id: dest.destination_id || dest.id,
            title: dest.name,
            description: dest.description || '',
            location: dest.region || 'Sumedang',
            duration: '2 jam',
            order: idx + 1,
            notes: `Score: ${dest.score ? (dest.score * 100).toFixed(1) + '%' : 'N/A'}\n${dest.explanation || ''}`
          }))
        });
      }

      // Payload untuk API
      const itineraryData = {
        title: tripName,
        description: `Itinerary dibuat dari rekomendasi hybrid sistem. ${notes}`,
        start_date: startDate,
        end_date: end.toISOString().split('T')[0],
        days: days
      };

      // Kirim ke Backend
      await itineraryAPI.create(itineraryData);
      
      // Sukses
      onClose();
      navigate('/planning');
      
    } catch (err) {
      console.error('Error creating itinerary:', err);
      let errorMessage = 'Gagal membuat itinerary.';
      
      // Error handling detail dari backend
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (typeof detail === 'string') {
          errorMessage = detail;
        } else if (Array.isArray(detail)) {
          errorMessage = detail.map(e => e.msg).join('; ');
        }
      } else if (err.response?.status === 401) {
        errorMessage = 'Sesi habis. Silakan login ulang.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content itinerary-creator-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>✨ Buat Itinerary dari Rekomendasi</h2>
          <button className="modal-close" onClick={onClose}>
            <span>&times;</span>
          </button>
        </div>

        <div className="modal-body">
          <p className="modal-intro">
            Ubah {(Array.isArray(recommendations) ? recommendations.length : 0)} rekomendasi ini menjadi rencana perjalanan Anda!
          </p>

          <div className="form-group">
            <label htmlFor="tripName">Nama Trip:</label>
            <input
              type="text"
              id="tripName"
              value={tripName}
              onChange={(e) => setTripName(e.target.value)}
              placeholder="Contoh: Petualangan Sumedang"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="startDate">Tanggal Mulai:</label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="duration">Durasi:</label>
              <select
                id="duration"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value))}
              >
                <option value="1">1 Hari</option>
                <option value="2">2 Hari</option>
                <option value="3">3 Hari</option>
                <option value="4">4 Hari</option>
                <option value="5">5 Hari</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="notes">Catatan (Optional):</label>
            <textarea
              id="notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Tambahkan catatan untuk perjalanan Anda..."
              rows="3"
            />
          </div>

          {/* Preview Distribusi */}
          <div className="distribution-preview">
            <h4>📅 Distribusi Destinasi:</h4>
            {Array.from({ length: duration }, (_, i) => {
              const recList = Array.isArray(recommendations) ? recommendations : [];
              const destinationsPerDay = Math.ceil(recList.length / duration);
              const dayStart = i * destinationsPerDay;
              const dayEnd = Math.min((i + 1) * destinationsPerDay, recList.length);
              const dayDestinations = recList.slice(dayStart, dayEnd);
              
              const date = new Date(startDate);
              date.setDate(date.getDate() + i);
              
              return (
                <div key={i} className="day-preview">
                  <strong>Hari {i + 1}</strong> 
                  <span className="day-date">({date.toLocaleDateString('id-ID', { weekday: 'short', day: 'numeric', month: 'short' })})</span>
                  <ul>
                    {dayDestinations.map((dest, idx) => (
                      <li key={idx}>{dest.name}</li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          {error && (
            <div className="error-message">
              <p>❌ {error}</p>
            </div>
          )}

          <div className="modal-actions">
            <button className="btn secondary" onClick={onClose} disabled={loading}>
              Batal
            </button>
            
            {/* LOGIKA TOMBOL: Cek Token */}
            {localStorage.getItem('access_token') ? (
              // KONDISI LOGIN: Panggil API
              <button 
                className="btn primary" 
                onClick={handleCreateItinerary}
                disabled={loading || !tripName || !startDate}
              >
                {loading ? '⏳ Membuat...' : '✅ Buat Itinerary'}
              </button>
            ) : (
              // KONDISI ANONYMOUS: Download PDF
              <button 
                className="btn primary" 
                onClick={downloadItineraryAsPDF}
                disabled={loading || !tripName || !startDate}
              >
                {'⬇️ Download PDF'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItineraryCreatorModal;