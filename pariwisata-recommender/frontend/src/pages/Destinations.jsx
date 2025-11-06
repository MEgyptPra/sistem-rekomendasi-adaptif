import React, { useState, useEffect } from 'react';
import { destinationsAPI } from '../services/api';
import '../styles/destinations.css';
import DestinationCard from '../components/destinations/DestinationCard';

const Destinations = () => {
  const [allDestinations, setAllDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState(['Semua Kategori']);
  
  const [selectedCategory, setSelectedCategory] = useState('Semua Kategori');
  const [searchQuery, setSearchQuery] = useState('');
  const [displayCount, setDisplayCount] = useState(12); // Menampilkan 12 destinasi pertama

  // Fetch destinations from API
  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await destinationsAPI.getAll({ limit: 100 });
        const destinations = response.data.destinations || [];
        setAllDestinations(destinations);

        // Extract unique categories
        const uniqueCategories = ['Semua Kategori', ...new Set(destinations.map(d => d.category).filter(Boolean))];
        setCategories(uniqueCategories);
      } catch (error) {
        console.error('Error fetching destinations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  const filteredDestinations = allDestinations.filter(dest => {
    const matchesCategory = selectedCategory === 'Semua Kategori' || dest.category === selectedCategory;
    const matchesSearch = dest.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          (dest.description && dest.description.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  // Destinasi yang ditampilkan (limit jika tidak ada pencarian)
  const displayedDestinations = searchQuery 
    ? filteredDestinations // Tampilkan semua hasil jika sedang search
    : filteredDestinations.slice(0, displayCount); // Batasi jumlah jika tidak search

  const hasMore = !searchQuery && filteredDestinations.length > displayCount;

  const handleLoadMore = () => {
    setDisplayCount(prev => prev + 12); // Tambah 12 destinasi setiap klik
  };

  return (
    <div className="destinations-page">
      <section className="page-header">
        <div className="container">
          <h1>Destinasi Wisata Sumedang</h1>
          <p>Jelajahi berbagai destinasi menarik di Kabupaten Sumedang</p>
        </div>
      </section>

      <section className="destinations-content">
        <div className="container">
          {/* Filters */}
          <div className="destination-filters">
            <div className="search-box">
              <input 
                type="text" 
                placeholder="Cari destinasi..." 
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
              <p>Memuat destinasi...</p>
            </div>
          ) : (
            <>
              {/* Destinations Grid */}
              <h2>
                {selectedCategory !== 'Semua Kategori' ? selectedCategory : 'Semua Destinasi'}
              </h2>
              {filteredDestinations.length === 0 ? (
                <p className="no-results">Tidak ada destinasi yang cocok dengan filter Anda. Coba sesuaikan filter.</p>
              ) : (
                <>
                  <p className="result-count">
                    {searchQuery 
                      ? `${filteredDestinations.length} destinasi ditemukan` 
                      : `Menampilkan ${displayedDestinations.length} dari ${filteredDestinations.length} destinasi`
                    }
                  </p>
                  <div className="destinations-grid">
                    {displayedDestinations.map(destination => (
                      <DestinationCard key={destination.id} destination={destination} />
                    ))}
                  </div>
                  
                  {/* Load More Button */}
                  {hasMore && (
                    <div className="load-more-container">
                      <button onClick={handleLoadMore} className="btn-load-more">
                        Tampilkan Lebih Banyak
                      </button>
                    </div>
                  )}
                </>
              )}
            </>
          )}
        </div>
      </section>
    </div>
  );
};

export default Destinations;