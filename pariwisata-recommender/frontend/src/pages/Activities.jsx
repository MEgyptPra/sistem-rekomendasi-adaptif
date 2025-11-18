import React, { useState, useEffect } from 'react';
import { activitiesAPI } from '../services/api';
import '../styles/activities.css';
import ActivityCard from '../components/activities/ActivityCard';

const Activities = () => {
  const [allActivities, setAllActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState(['Semua Kategori']);
  const [selectedCategory, setSelectedCategory] = useState('Semua Kategori');
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch activities from API
  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await activitiesAPI.getAll({ limit: 100 });
        const activities = response.data.activities || [];
        setAllActivities(activities);

        // Extract unique categories
        const uniqueCategories = ['Semua Kategori', ...new Set(activities.map(a => a.category).filter(Boolean))];
        setCategories(uniqueCategories);
      } catch (error) {
        console.error('Error fetching activities:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  const filteredActivities = allActivities.filter(activity => {
    const matchesCategory = selectedCategory === 'Semua Kategori' || activity.category === selectedCategory;
    const matchesSearch = activity.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         (activity.description && activity.description.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="activities-page">
      <section className="page-header">
        <div className="container">
          <h1>Aktivitas Wisata</h1>
          <p>Temukan berbagai aktivitas dan pengalaman menarik di Sumedang</p>
        </div>
      </section>

      <section className="activities-content">
        <div className="container">
          {/* Filters */}
          <div className="activity-filters">
            <div className="search-box">
              <input 
                type="text" 
                placeholder="Cari aktivitas..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            
            <div className="category-filter">
              <label>Filter Kategori:</label>
              <select 
                value={selectedCategory} 
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>
          </div>

          {loading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Memuat aktivitas...</p>
            </div>
          ) : (
            <>
              {/* Featured Activities */}
              <div className="featured-activity">
                <div className="featured-content">
                  <h2>Unggulan: Petualangan Outdoor Sumedang</h2>
                  <p>Dari hiking di pegunungan hingga wisata alam, Sumedang menawarkan pengalaman outdoor kelas dunia untuk semua musim.</p>
                  <button className="btn primary">Jelajahi Petualangan Outdoor</button>
                </div>
                <div className="featured-image">
                  <img src="/assets/images/outdoor-adventure.jpg" alt="Petualangan outdoor Sumedang" onError={e => {e.target.onerror=null;e.target.src='/assets/placeholder.webp';}} />
                </div>
              </div>

              {/* Activities Grid */}
              <h2>{selectedCategory === 'Semua Kategori' ? 'Semua Aktivitas' : selectedCategory}</h2>
              {filteredActivities.length === 0 ? (
                <p className="no-results">Tidak ada aktivitas yang cocok dengan pencarian Anda. Coba sesuaikan filter.</p>
              ) : (
                <>
                  <p className="result-count">{filteredActivities.length} aktivitas ditemukan</p>
                  <div className="activities-grid">
                    {filteredActivities.map(activity => (
                      <ActivityCard key={activity.id} activity={activity} />
                    ))}
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </section>

      {/* Seasonal Activities */}
      <section className="seasonal-activities">
        <div className="container">
          <h2>Aktivitas Musiman</h2>
          <div className="seasons-container">
            <div className="season-card">
              <img src="/assets/images/spring.jpg" alt="Musim Hujan di Sumedang" onError={e => {e.target.onerror=null;e.target.src='/assets/placeholder.webp';}} />
              <h3>Musim Hujan</h3>
              <p>Air terjun penuh, pemandangan hijau, dan udara sejuk pegunungan</p>
            </div>
            <div className="season-card">
              <img src="/assets/images/summer.jpg" alt="Musim Kemarau di Sumedang" onError={e => {e.target.onerror=null;e.target.src='/assets/placeholder.webp';}} />
              <h3>Musim Kemarau</h3>
              <p>Wisata alam, hiking, dan festival budaya lokal</p>
            </div>
            <div className="season-card">
              <img src="/assets/images/fall.jpg" alt="Musim Panen di Sumedang" onError={e => {e.target.onerror=null;e.target.src='/assets/placeholder.webp';}} />
              <h3>Musim Panen</h3>
              <p>Festival panen, wisata agro, dan kuliner khas Sumedang</p>
            </div>
            <div className="season-card">
              <img src="/assets/images/winter.jpg" alt="Akhir Tahun di Sumedang" onError={e => {e.target.onerror=null;e.target.src='/assets/placeholder.webp';}} />
              <h3>Akhir Tahun</h3>
              <p>Liburan keluarga, wisata religi, dan perayaan tahun baru</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Activities;