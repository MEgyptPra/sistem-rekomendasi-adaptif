import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { favoritesAPI, itineraryAPI } from '../services/api';
import DestinationCard from '../components/destinations/DestinationCard';
import ActivityCard from '../components/activities/ActivityCard';
import '../styles/favorites.css';

const Favorites = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState({ destinations: [], activities: [] });
  const [itineraries, setItineraries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'destinations', 'activities', 'itineraries'

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }

    const fetchFavorites = async () => {
      try {
        const response = await favoritesAPI.getAll();
        
        // Group by item_type
        const destinations = response.data.filter(fav => fav.item_type === 'destination');
        const activities = response.data.filter(fav => fav.item_type === 'activity');
        
        setFavorites({ destinations, activities });
      } catch (error) {
        console.error('Error fetching favorites:', error);
        setFavorites({ destinations: [], activities: [] });
      }
    };

    const fetchItineraries = async () => {
      try {
        const response = await itineraryAPI.getAll();
        setItineraries(response.data || []);
      } catch (error) {
        console.error('Error fetching itineraries:', error);
        setItineraries([]);
      }
    };

    Promise.all([fetchFavorites(), fetchItineraries()]).finally(() => setLoading(false));
  }, [isAuthenticated]);

  const handleRemoveFavorite = async (itemType, itemId) => {
    try {
      await favoritesAPI.remove(itemType, itemId);
      
      // Update local state
      setFavorites(prev => ({
        destinations: prev.destinations.filter(f => !(f.item_type === itemType && f.item_id === itemId)),
        activities: prev.activities.filter(f => !(f.item_type === itemType && f.item_id === itemId))
      }));
    } catch (error) {
      console.error('Error removing favorite:', error);
      alert('Gagal menghapus favorit. Silakan coba lagi.');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="favorites-page">
        <div className="container">
          <div className="login-required">
            <h2>Login Diperlukan</h2>
            <p>Silakan login untuk melihat daftar favorit Anda</p>
            <Link to="/login" className="btn primary">Login Sekarang</Link>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="favorites-page">
        <div className="container">
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Memuat favorit...</p>
          </div>
        </div>
      </div>
    );
  }

  const totalFavorites = favorites.destinations.length + favorites.activities.length;
  const displayDestinations = activeTab === 'all' || activeTab === 'destinations';
  const displayActivities = activeTab === 'all' || activeTab === 'activities';
  const displayItineraries = activeTab === 'itineraries';

  // Itinerary Card Component
  const ItineraryCard = ({ itinerary }) => {
    const start = new Date(itinerary.start_date);
    const end = new Date(itinerary.end_date);
    const diffTime = Math.abs(end - start);
    const durationDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    const isUpcoming = new Date() < start;

    return (
      <div className="itinerary-card" onClick={() => navigate(`/planning/${itinerary.id}`)}>
        <div className="card-content">
          <h3>{itinerary.title}</h3>
          <p style={{color: '#666', fontSize: '0.9rem', marginBottom: '0.5rem'}}>{itinerary.description}</p>
          <div className="card-meta">
            <span className="meta-item">📅 {start.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
            <span className="meta-dot">•</span>
            <span className="meta-item">⏳ {durationDays} Hari</span>
            <span className="meta-dot">•</span>
            <span className={`status-badge ${isUpcoming ? 'upcoming' : 'completed'}`}>
              {isUpcoming ? 'Akan Datang' : 'Selesai'}
            </span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="favorites-page">
      <section className="page-header">
        <div className="container">
          <h1>Favorit Saya</h1>
          <p>Koleksi destinasi, aktivitas, dan itinerary favorit Anda</p>
        </div>
      </section>

      <div className="container">
        <div className="favorites-tabs">
          <button 
            className={`tab ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            Semua ({totalFavorites})
          </button>
          <button 
            className={`tab ${activeTab === 'destinations' ? 'active' : ''}`}
            onClick={() => setActiveTab('destinations')}
          >
            Destinasi ({favorites.destinations.length})
          </button>
          <button 
            className={`tab ${activeTab === 'activities' ? 'active' : ''}`}
            onClick={() => setActiveTab('activities')}
          >
            Aktivitas ({favorites.activities.length})
          </button>
          <button 
            className={`tab ${activeTab === 'itineraries' ? 'active' : ''}`}
            onClick={() => setActiveTab('itineraries')}
          >
            Itinerary ({itineraries.length})
          </button>
        </div>

        {activeTab !== 'itineraries' && totalFavorites === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">❤️</div>
            <h2>Belum Ada Favorit</h2>
            <p>Mulai tambahkan destinasi dan aktivitas favorit Anda</p>
            <div className="empty-actions">
              <Link to="/destinations" className="btn primary">Jelajahi Destinasi</Link>
              <Link to="/activities" className="btn secondary">Jelajahi Aktivitas</Link>
            </div>
          </div>
        ) : (
          <>
            {displayDestinations && favorites.destinations.length > 0 && (
              <section className="favorites-section">
                <h2>Destinasi Favorit</h2>
                <div className="favorites-grid">
                  {favorites.destinations.map((fav) => (
                    <div key={fav.id} className="favorite-item">
                      <DestinationCard destination={fav.destination_data || fav} />
                      <button 
                        className="remove-favorite-btn"
                        onClick={() => handleRemoveFavorite('destination', fav.item_id)}
                        title="Hapus dari favorit"
                      >
                        ❌
                      </button>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {displayActivities && favorites.activities.length > 0 && (
              <section className="favorites-section">
                <h2>Aktivitas Favorit</h2>
                <div className="favorites-grid">
                  {favorites.activities.map((fav) => (
                    <div key={fav.id} className="favorite-item">
                      <ActivityCard activity={fav.activity_data || fav} />
                      <button 
                        className="remove-favorite-btn"
                        onClick={() => handleRemoveFavorite('activity', fav.item_id)}
                        title="Hapus dari favorit"
                      >
                        ❌
                      </button>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}

        {/* Itineraries Tab */}
        {displayItineraries && (
          itineraries.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📋</div>
              <h2>Belum Ada Itinerary Tersimpan</h2>
              <p>Buat itinerary pertama Anda di halaman Planning</p>
              <Link to="/planning" className="btn primary">Buat Itinerary</Link>
            </div>
          ) : (
            <section className="favorites-section">
              <h2>Itinerary Tersimpan</h2>
              <div className="favorites-grid">
                {itineraries.map((itin) => (
                  <ItineraryCard key={itin.id} itinerary={itin} />
                ))}
              </div>
            </section>
          )
        )}
      </div>
    </div>
  );
};

export default Favorites;
