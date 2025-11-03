import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { favoritesAPI } from '../services/api';
import DestinationCard from '../components/destinations/DestinationCard';
import ActivityCard from '../components/activities/ActivityCard';
import '../styles/favorites.css';

const Favorites = () => {
  const { isAuthenticated, user } = useAuth();
  const [favorites, setFavorites] = useState({ destinations: [], activities: [] });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'destinations', 'activities'

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }

    const fetchFavorites = async () => {
      try {
        const response = await favoritesAPI.getByUser();
        
        // Group by item_type
        const destinations = response.data.filter(fav => fav.item_type === 'destination');
        const activities = response.data.filter(fav => fav.item_type === 'activity');
        
        setFavorites({ destinations, activities });
      } catch (error) {
        console.error('Error fetching favorites:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
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

  return (
    <div className="favorites-page">
      <section className="page-header">
        <div className="container">
          <h1>Favorit Saya</h1>
          <p>Koleksi destinasi dan aktivitas favorit Anda</p>
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
        </div>

        {totalFavorites === 0 ? (
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
      </div>
    </div>
  );
};

export default Favorites;
