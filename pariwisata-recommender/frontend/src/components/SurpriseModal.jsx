import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext'; // Import Auth
import { recommendationsAPI } from '../services/api';
import DestinationCard from './destinations/DestinationCard';
import ItineraryCreatorModal from './ItineraryCreatorModal';
import '../styles/surprise-modal.css';

const SurpriseModal = ({ isOpen, onClose }) => {
  const { user } = useAuth(); // Ambil user untuk personalisasi
  
  // State 1: Yang ditampilkan ke user (5 item)
  const [displayDestinations, setDisplayDestinations] = useState([]);
  // State 2: Bank data kandidat dari backend (20 item)
  const [candidatePool, setCandidatePool] = useState([]);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showItineraryCreator, setShowItineraryCreator] = useState(false);

  const CANDIDATE_POOL_SIZE = 20; // Ambil banyak untuk variasi
  const DISPLAY_COUNT = 5;        // Tampilkan sedikit
  const TOP_N_PRIORITY = 1;       // Pertahankan 1 terbaik agar relevan

  // Fungsi Seleksi Cerdas (Client-side Shuffle)
  const selectFromPool = useCallback((pool) => {
    if (!pool || pool.length === 0) return;

    // 1. Ambil Top N terbaik (Jangan diacak)
    const topItems = pool.slice(0, TOP_N_PRIORITY);
    
    // 2. Ambil sisanya
    const remainder = pool.slice(TOP_N_PRIORITY);
    
    // 3. Acak sisanya
    const shuffledRemainder = remainder.sort(() => 0.5 - Math.random());
    
    // 4. Gabungkan
    const needed = DISPLAY_COUNT - topItems.length;
    const randomSelection = shuffledRemainder.slice(0, needed);
    
    const finalSelection = [...topItems, ...randomSelection];
    
    setDisplayDestinations(finalSelection);
  }, []);

  // Fetch Data dari Backend (Hybrid/MAB)
  const fetchSurpriseRecommendations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Panggil API dengan mode 'auto'
      const response = await recommendationsAPI.getPersonalized({
        algorithm: 'auto',
        num_recommendations: CANDIDATE_POOL_SIZE,
        user_id: user?.id // Kirim ID user jika login
      });

      let candidates = response.data.recommendations || [];
      
      // Jika kosong, pakai fallback
      if (!Array.isArray(candidates) || candidates.length === 0) {
        await loadRandomFallback();
        return;
      }

      // Normalisasi ID (jaga-jaga beda format)
      candidates = candidates.map(c => ({
        ...c,
        destination_id: c.destination_id || c.id
      }));

      // SIMPAN KE POOL & TAMPILKAN
      setCandidatePool(candidates);
      selectFromPool(candidates);
      
    } catch (err) {
      console.error('Error fetching surprise recommendations:', err);
      await loadRandomFallback();
    } finally {
      setLoading(false);
    }
  }, [user, selectFromPool]);

  // Fallback jika backend error/mati
  const loadRandomFallback = async () => {
    try {
      const allDestResponse = await recommendationsAPI.getAllDestinations({ limit: 50 });
      const allDest = allDestResponse.data.destinations || [];
      const shuffled = allDest.sort(() => 0.5 - Math.random());
      
      const fallbackPool = shuffled.slice(0, CANDIDATE_POOL_SIZE).map((dest) => ({
        destination_id: dest.id,
        id: dest.id,
        name: dest.name,
        description: dest.description,
        region: dest.region,
        category: dest.category,
        image: dest.image,
        score: 0.5,
        explanation: `Rekomendasi Populer`
      }));
      
      setCandidatePool(fallbackPool);
      selectFromPool(fallbackPool);
    } catch (err) {
      setError('Gagal memuat rekomendasi.');
    }
  };

  // Efek saat modal dibuka
  useEffect(() => {
    if (isOpen) {
      setCandidatePool([]); // Reset
      setDisplayDestinations([]);
      fetchSurpriseRecommendations();
    }
  }, [isOpen, fetchSurpriseRecommendations]);

  // Tombol "Muat Lagi" (Cepat, tanpa request ulang)
  const handleRefresh = () => {
    if (candidatePool.length > 0) {
      setLoading(true);
      setTimeout(() => {
        selectFromPool(candidatePool);
        setLoading(false);
      }, 300); // Fake loading biar kerasa "mikir"
    } else {
      fetchSurpriseRecommendations();
    }
  };

  const handleCreateItinerary = () => setShowItineraryCreator(true);
  const handleDestinationClick = (destinationId) => window.open(`/destinations/${destinationId}`, '_blank');

  if (!isOpen) return null;

  return (
    <>
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="modal-header">
            <h2>✨ Kejutan Rekomendasi untuk {user ? user.name : 'Anda'}!</h2>
            <p>Kami memilihkan destinasi terbaik berdasarkan cuaca & tren saat ini.</p>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>

          <div className="modal-body">
            {loading ? (
              <div className="modal-loading">
                <div className="modal-loading-spinner" />
                <p>Sedang meracik rekomendasi...</p>
              </div>
            ) : error ? (
              <div className="modal-error">
                <p>{error}</p>
                <button className="modal-btn modal-btn-primary" onClick={fetchSurpriseRecommendations}>Coba Lagi</button>
              </div>
            ) : (
              <div className="modal-destinations-grid">
                {displayDestinations.map((destination) => (
                  <div
                    key={destination.destination_id || destination.id}
                    onClick={() => handleDestinationClick(destination.destination_id || destination.id)}
                    style={{ cursor: 'pointer' }}
                  >
                    <DestinationCard
                      destination={{
                        id: destination.destination_id || destination.id,
                        name: destination.name,
                        description: destination.description,
                        image: destination.image,
                        region: destination.region || destination.address || 'Sumedang',
                        category: destination.category,
                        score: destination.score,
                        algorithm: destination.algorithm
                      }}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          {!loading && !error && displayDestinations.length > 0 && (
            <div className="modal-footer">
              <div className="modal-footer-info">
                <p>💡 Kurang cocok? Klik Muat Lagi untuk variasi lain.</p>
              </div>
              <div className="modal-footer-actions">
                <button className="modal-btn modal-btn-secondary" onClick={handleRefresh}>🔄 Muat Lagi</button>
                <button className="modal-btn modal-btn-primary" onClick={handleCreateItinerary}>📋 Buat Itinerary</button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* MODAL ITINERARY CREATOR */}
      {showItineraryCreator && (
        <ItineraryCreatorModal
          isOpen={showItineraryCreator}
          onClose={() => setShowItineraryCreator(false)}
          // 👇 INI PERBAIKANNYA: Gunakan prop 'recommendations' agar sesuai dengan ItineraryCreatorModal
          recommendations={displayDestinations} 
        />
      )}
    </>
  );
};

export default SurpriseModal;