import React, { useState, useEffect } from 'react';
import { destinationsAPI } from '../services/api';
import '../styles/destinations.css';
import DestinationCard from '../components/destinations/DestinationCard';

const Destinations = () => {
  const [allDestinations, setAllDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [regions, setRegions] = useState(['Semua Wilayah']);
  const [categories, setCategories] = useState(['Semua Kategori']);
  
  const [selectedRegion, setSelectedRegion] = useState('Semua Wilayah');
  const [selectedCategory, setSelectedCategory] = useState('Semua Kategori');
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch destinations from API
  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await destinationsAPI.getAll({ limit: 100 });
        const destinations = response.data.destinations || [];
        setAllDestinations(destinations);

        // Extract unique regions and categories
        const uniqueRegions = ['Semua Wilayah', ...new Set(destinations.map(d => d.region).filter(Boolean))];
        const uniqueCategories = ['Semua Kategori', ...new Set(destinations.map(d => d.category).filter(Boolean))];
        
        setRegions(uniqueRegions);
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
    const matchesRegion = selectedRegion === 'Semua Wilayah' || dest.region === selectedRegion;
    const matchesCategory = selectedCategory === 'Semua Kategori' || dest.category === selectedCategory;
    const matchesSearch = dest.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          (dest.description && dest.description.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesRegion && matchesCategory && matchesSearch;
  });

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
            
            <div className="region-filter">
              <label>Filter Wilayah:</label>
              <select 
                value={selectedRegion} 
                onChange={(e) => setSelectedRegion(e.target.value)}
              >
                {regions.map(region => (
                  <option key={region} value={region}>{region}</option>
                ))}
              </select>
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
                {selectedRegion !== 'Semua Wilayah' ? selectedRegion : 
                 selectedCategory !== 'Semua Kategori' ? selectedCategory : 
                 'Semua Destinasi'}
              </h2>
              {filteredDestinations.length === 0 ? (
                <p className="no-results">Tidak ada destinasi yang cocok dengan filter Anda. Coba sesuaikan filter.</p>
              ) : (
                <>
                  <p className="result-count">{filteredDestinations.length} destinasi ditemukan</p>
                  <div className="destinations-grid">
                    {filteredDestinations.map(destination => (
                      <DestinationCard key={destination.id} destination={destination} />
                    ))}
                  </div>
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