import React, { useState, useEffect, useCallback } from 'react';
import { recommendationsAPI } from '../services/api';
import DestinationCard from './destinations/DestinationCard';
import ItineraryCreatorModal from './ItineraryCreatorModal';
import '../styles/surprise-modal.css';

const SurpriseModal = ({ isOpen, onClose }) => {
  const [surpriseDestinations, setSurpriseDestinations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showItineraryCreator, setShowItineraryCreator] = useState(false);

  const CANDIDATE_POOL = 20;
  const DISPLAY_COUNT = 5;
  const TOP_N = 2; // always include top-2 to preserve model priority

  // Select weighted subset without replacement
  const selectWeightedSubset = (candidates, k) => {
    const pool = Array.isArray(candidates) ? candidates.slice() : [];
    if (pool.length <= k) return pool.slice(0, k);

    const avail = pool.slice();
    const availScores = avail.map((c, idx) => {
      if (c && typeof c.score === 'number' && !isNaN(c.score)) return Math.max(0, c.score);
      if (c && c.score != null && !isNaN(Number(c.score))) return Math.max(0, Number(c.score));
      // fallback to rank-based weight
      return 1 / (idx + 1);
    });

    const selected = [];
    for (let pick = 0; pick < k; pick++) {
      const total = availScores.reduce((a, b) => a + b, 0);
      if (total <= 0) {
        const idx = Math.floor(Math.random() * avail.length);
        selected.push(avail[idx]);
        avail.splice(idx, 1);
        availScores.splice(idx, 1);
        continue;
      }

      const r = Math.random() * total;
      let acc = 0;
      let idx = 0;
      for (; idx < availScores.length; idx++) {
        acc += availScores[idx];
        if (r <= acc) break;
      }
      if (idx >= avail.length) idx = avail.length - 1;
      selected.push(avail[idx]);
      avail.splice(idx, 1);
      availScores.splice(idx, 1);
      if (avail.length === 0) break;
    }

    return selected;
  };

  const loadRandomFallback = async () => {
    try {
      const allDestResponse = await recommendationsAPI.getAllDestinations({ limit: 50, _cb: Date.now() });
      const allDest = allDestResponse.data.destinations || [];
      const shuffled = allDest.sort(() => 0.5 - Math.random());
      const randomDest = shuffled.slice(0, DISPLAY_COUNT);

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
    } catch (err) {
      console.error('Random fallback failed', err);
      setSurpriseDestinations([]);
    }
  };

  // If backend returns fewer candidates than DISPLAY_COUNT, fill from all destinations
  const fillFromAllDestinations = async (currentCandidates = []) => {
    try {
      const needed = Math.max(0, DISPLAY_COUNT - (currentCandidates.length || 0));
      if (needed <= 0) return currentCandidates.slice(0, DISPLAY_COUNT);

      const resp = await recommendationsAPI.getAllDestinations({ limit: 50, _cb: Date.now() });
      const all = resp.data.destinations || [];

      const existingIds = new Set((currentCandidates || []).map((c) => c.id || c.destination_id));
      const extras = all.filter((d) => !existingIds.has(d.id)).slice(0, needed).map((d) => ({
        destination_id: d.id,
        id: d.id,
        name: d.name,
        description: d.description,
        region: d.region,
        category: d.category,
        image: d.image,
        score: 0
      }));

      return [...(currentCandidates || []), ...extras].slice(0, DISPLAY_COUNT);
    } catch (err) {
      console.warn('fillFromAllDestinations failed', err);
      return currentCandidates.slice(0, DISPLAY_COUNT);
    }
  };

  const fetchSurpriseRecommendations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const userId = localStorage.getItem('userId');
      const cacheBuster = Date.now();

      // Try personalized (auto) with larger candidate pool first
      try {
        const response = await recommendationsAPI.getPersonalized({
          algorithm: 'auto',
          num_recommendations: CANDIDATE_POOL,
          request_id: cacheBuster,
          user_id: userId || undefined
        });

        let candidates = (response.data && response.data.recommendations) || [];
        if (!Array.isArray(candidates)) candidates = [];
        if (candidates.length > 0) {
          // keep top-N deterministically, then sample the rest
          const top = candidates.slice(0, TOP_N).map((c) => ({ ...c, destination_id: c.id || c.destination_id }));
          const remainder = candidates.slice(TOP_N);
          const need = Math.max(0, DISPLAY_COUNT - top.length);
          const sampled = need > 0 ? selectWeightedSubset(remainder, need) : [];
          let selected = [...top, ...sampled].slice(0, DISPLAY_COUNT);
          if (selected.length < DISPLAY_COUNT) {
            // fill missing slots from all destinations to avoid showing too few items
            selected = await fillFromAllDestinations(selected);
          }
          setSurpriseDestinations(selected);
          console.log('✅ Candidate-pool recommendations loaded (auto)');
          return;
        }
      } catch (err) {
        console.warn('Auto recommendations failed, will try incremental/hybrid fallback', err);
      }

      // If personalized not available or empty, try incremental with candidate pool
      try {
        const response = await recommendationsAPI.getPersonalized({
          algorithm: 'incremental',
          num_recommendations: CANDIDATE_POOL,
          request_id: cacheBuster,
          user_id: userId || undefined
        });
        let candidates = (response.data && response.data.recommendations) || [];
        if (!Array.isArray(candidates)) candidates = [];
        if (candidates.length > 0) {
          const top = candidates.slice(0, TOP_N).map((c) => ({ ...c, destination_id: c.id || c.destination_id }));
          const remainder = candidates.slice(TOP_N);
          const need = Math.max(0, DISPLAY_COUNT - top.length);
          const sampled = need > 0 ? selectWeightedSubset(remainder, need) : [];
          let selected = [...top, ...sampled].slice(0, DISPLAY_COUNT);
          if (selected.length < DISPLAY_COUNT) {
            selected = await fillFromAllDestinations(selected);
          }
          setSurpriseDestinations(selected);
          console.log('✅ Incremental candidate-pool loaded');
          return;
        }
      } catch (err) {
        console.warn('Incremental recommendations failed, falling back to random', err);
      }

      // As a last resort, load random fallback
      await loadRandomFallback();
    } catch (err) {
      console.error('Error fetching surprise recommendations:', err);
      setError('Gagal memuat rekomendasi. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isOpen) {
      fetchSurpriseRecommendations();
    }
  }, [isOpen, fetchSurpriseRecommendations]);

  const handleCreateItinerary = () => setShowItineraryCreator(true);
  const handleDestinationClick = (destinationId) => window.open(`/destinations/${destinationId}`, '_blank');

  if (!isOpen) return null;

  return (
    <>
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          {/* Header */}
          <div className="modal-header">
            <h2>✨ Kejutan Rekomendasi untuk Anda!</h2>
            <p>Kami telah memilih 5 destinasi menarik khusus untuk Anda</p>
            <button className="modal-close" onClick={onClose}>×</button>
          </div>

          {/* Body */}
          <div className="modal-body">
            {loading ? (
              <div className="modal-loading">
                <div className="modal-loading-spinner" />
                <p>Memuat rekomendasi...</p>
              </div>
            ) : error ? (
              <div className="modal-error">
                <p>{error}</p>
                <button className="modal-btn modal-btn-primary" onClick={fetchSurpriseRecommendations}>Coba Lagi</button>
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
                <button className="modal-btn modal-btn-secondary" onClick={fetchSurpriseRecommendations}>🔄 Muat Lagi</button>
                <button className="modal-btn modal-btn-primary" onClick={handleCreateItinerary}>📋 Buat Itinerary</button>
              </div>
            </div>
          )}
        </div>
      </div>

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
