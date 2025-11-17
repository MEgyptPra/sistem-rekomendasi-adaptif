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

  const handleCreateItinerary = async () => {
      const downloadItineraryAsPDF = () => {
        // Simple PDF generator
        const doc = new jsPDF();
        doc.setFontSize(16);
        doc.text(tripName, 10, 20);
        doc.setFontSize(12);
        doc.text(`Tanggal: ${startDate} - ${duration} hari`, 10, 30);
        doc.text(`Catatan: ${notes}`, 10, 40);
        let y = 50;
        for (let i = 0; i < duration; i++) {
          doc.text(`Hari ${i + 1}:`, 10, y);
          y += 8;
          const destinationsPerDay = Math.ceil((Array.isArray(recommendations) ? recommendations.length : 0) / duration);
          const dayStart = i * destinationsPerDay;
          const dayEnd = Math.min((i + 1) * destinationsPerDay, Array.isArray(recommendations) ? recommendations.length : 0);
          const dayDestinations = Array.isArray(recommendations) ? recommendations.slice(dayStart, dayEnd) : [];
          dayDestinations.forEach((dest, idx) => {
            doc.text(`- ${dest.name}`, 15, y);
            y += 7;
          });
          y += 4;
        }
        doc.save(`${tripName.replace(/\s+/g, '_')}.pdf`);
      };
    setLoading(true);
    setError(null);

    try {
      // Check authentication
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Anda harus login terlebih dahulu untuk membuat itinerary.');
        setLoading(false);
        return;
      }

      console.log('Auth token found:', token ? 'Yes' : 'No');
      
      // Calculate end date
      const start = new Date(startDate);
      const end = new Date(start);
      end.setDate(end.getDate() + duration - 1);

      // Distribute destinations across days
      const destinationsPerDay = Math.ceil((Array.isArray(recommendations) ? recommendations.length : 0) / duration);
      const days = [];
      
      for (let i = 0; i < duration; i++) {
        const dayStart = i * destinationsPerDay;
        const dayEnd = Math.min((i + 1) * destinationsPerDay, Array.isArray(recommendations) ? recommendations.length : 0);
        const dayDestinations = Array.isArray(recommendations) ? recommendations.slice(dayStart, dayEnd) : [];
        
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

      // Create itinerary payload (matching backend schema)
      const itineraryData = {
        title: tripName,
        description: `Itinerary dibuat dari rekomendasi hybrid sistem. ${notes}`,
        start_date: startDate,
        end_date: end.toISOString().split('T')[0],
        days: days
      };

      console.log('Creating itinerary with payload:', JSON.stringify(itineraryData, null, 2));

      // Call API
      const response = await itineraryAPI.create(itineraryData);
      
      console.log('Itinerary created successfully:', response.data);

      // Success! Navigate to planning page to see itineraries
      onClose();
      navigate('/planning');
      
    } catch (err) {
      console.error('Error creating itinerary:', err);
      console.error('Error response status:', err.response?.status);
      console.error('Error response data:', JSON.stringify(err.response?.data, null, 2));
      
      // Handle validation errors
      let errorMessage = 'Gagal membuat itinerary.';
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        console.log('Detail type:', typeof detail, 'Is array:', Array.isArray(detail));
        
        if (Array.isArray(detail)) {
          // Validation errors from FastAPI (Pydantic)
          console.log('Validation errors:', detail);
          errorMessage = 'Validasi gagal: ' + detail.map(e => {
            const field = e.loc ? e.loc.join('.') : 'unknown';
            return `${field}: ${e.msg}`;
          }).join('; ');
        } else if (typeof detail === 'string') {
          errorMessage = detail;
        } else if (typeof detail === 'object') {
          errorMessage = JSON.stringify(detail);
        }
      } else if (err.response?.status === 401) {
        errorMessage = 'Silakan login terlebih dahulu untuk membuat itinerary.';
      } else if (!err.response) {
        errorMessage = 'Tidak dapat terhubung ke server. Pastikan backend berjalan.';
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
              const destinationsPerDay = Math.ceil((Array.isArray(recommendations) ? recommendations.length : 0) / duration);
              const dayStart = i * destinationsPerDay;
              const dayEnd = Math.min((i + 1) * destinationsPerDay, Array.isArray(recommendations) ? recommendations.length : 0);
              const dayDestinations = Array.isArray(recommendations) ? recommendations.slice(dayStart, dayEnd) : [];
              
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
            {localStorage.getItem('access_token') ? (
              <button 
                className="btn primary" 
                onClick={handleCreateItinerary}
                disabled={loading || !tripName || !startDate}
              >
                {loading ? '⏳ Membuat...' : '✅ Buat Itinerary'}
              </button>
            ) : (
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
