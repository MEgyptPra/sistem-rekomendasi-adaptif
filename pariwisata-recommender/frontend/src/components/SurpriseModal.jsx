import React, { useState, useEffect } from 'react';
import { recommendationsAPI } from '../services/api';
import DestinationCard from './destinations/DestinationCard';
import ItineraryCreatorModal from './ItineraryCreatorModal';
import '../styles/surprise-modal.css';

const SurpriseModal = ({ isOpen, onClose }) => {
  const [surpriseDestinations, setSurpriseDestinations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showItineraryCreator, setShowItineraryCreator] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchSurpriseRecommendations();
    }
  }, [isOpen]);

  const fetchSurpriseRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      // ✅ GUNAKAN ML MODEL - Algorithm: Auto (smart selection based on data availability)
      // - Jika ada user_id & preferences: Hybrid (CF+CB) 
      // - Jika user baru tapi ada ratings: Collaborative
      // - Jika tidak ada data: Incremental (trending + context-aware)
      const userId = localStorage.getItem('userId');
      
      if (userId) {
        // User logged-in: Gunakan personalized recommendations dengan algorithm=auto
        try {
          const response = await recommendationsAPI.getPersonalized({
            algorithm: 'auto', // Smart selection (hybrid/incremental/mab)
            num_recommendations: 5
          });
          
          if (response.data.recommendations && response.data.recommendations.length > 0) {
            setSurpriseDestinations(response.data.recommendations);
            console.log('✅ ML Recommendations loaded:', response.data.metadata?.algorithm_used);
            return;
          }
        } catch (mlErr) {
          console.warn('ML recommendations failed, trying incremental:', mlErr);
        }
      }
      
      // Fallback: Gunakan incremental learning (context-aware + trending)
      try {
        const response = await recommendationsAPI.getPersonalized({
          algorithm: 'incremental', // Context-aware incremental sesuai penelitian
          num_recommendations: 5
        });
        setSurpriseDestinations(response.data.recommendations || []);
        console.log('✅ Incremental Recommendations loaded (context-aware)');
      } catch (hybridErr) {
        console.error('Incremental failed, using random fallback:', hybridErr);
        // Last resort: Random
        await loadRandomFallback();
      }
    } catch (err) {
      console.error('Error fetching surprise recommendations:', err);
      setError('Gagal memuat rekomendasi. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };
  
  const loadRandomFallback = async () => {
    const allDestResponse = await recommendationsAPI.getAllDestinations({ limit: 50 });
    const allDest = allDestResponse.data.destinations || [];
    const shuffled = allDest.sort(() => 0.5 - Math.random());
    const randomDest = shuffled.slice(0, 5);
    
    const transformedData = randomDest.map((dest) => ({
      destination_id: dest.id,
      id: dest.id,
      name: dest.name,
      description: dest.description,
      region: dest.region,
      category: dest.category,
      image: dest.image,
      score: 0.8,
      explanation: `Rekomendasi ${dest.category} di ${dest.region}`
    }));
    
    setSurpriseDestinations(transformedData);
  };

  const handleCreateItinerary = () => {
    setShowItineraryCreator(true);
  };

  const handleDestinationClick = (destinationId) => {
    // Open destination in new tab
    window.open(`/destinations/${destinationId}`, '_blank');
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          {/* Header */}
          <div className="modal-header">
            <h2>✨ Kejutan Rekomendasi untuk Anda!</h2>
            <p>Kami telah memilih 5 destinasi menarik khusus untuk Anda</p>
            <button className="modal-close" onClick={onClose}>
              ×
            </button>
          </div>

          {/* Body */}
          <div className="modal-body">
            {loading ? (
              <div className="modal-loading">
                <div className="modal-loading-spinner"></div>
                <p>Memuat rekomendasi...</p>
              </div>
            ) : error ? (
              <div className="modal-error">
                <p>{error}</p>
                <button className="modal-btn modal-btn-primary" onClick={fetchSurpriseRecommendations}>
                  Coba Lagi
                </button>
              </div>
            ) : (
              <div className="modal-destinations-grid">
                {surpriseDestinations.map((destination) => (
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
                        region: destination.region,
                        category: destination.category
                      }} 
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          {!loading && !error && surpriseDestinations.length > 0 && (
            <div className="modal-footer">
              <div className="modal-footer-info">
                <p>💡 Suka dengan rekomendasi ini? Buat itinerary sekarang!</p>
              </div>
              <div className="modal-footer-actions">
                <button className="modal-btn modal-btn-secondary" onClick={fetchSurpriseRecommendations}>
                  🔄 Muat Lagi
                </button>
                <button className="modal-btn modal-btn-primary" onClick={handleCreateItinerary}>
                  📋 Buat Itinerary
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Itinerary Creator Modal */}
      {showItineraryCreator && (
        <ItineraryCreatorModal
          isOpen={showItineraryCreator}
          onClose={() => setShowItineraryCreator(false)}
          selectedDestinations={surpriseDestinations}
        />
      )}
    </>
  );
};

export default SurpriseModal;
