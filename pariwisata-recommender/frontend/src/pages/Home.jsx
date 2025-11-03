import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { recommendationsAPI, activitiesAPI } from '../services/api';
import '../styles/home.css';
import DestinationCard from '../components/destinations/DestinationCard';
import ActivityCard from '../components/activities/ActivityCard';
import SurpriseModal from '../components/SurpriseModal';

const Home = () => {
  const { isAuthenticated } = useAuth();
  // State untuk rekomendasi personal dari backend
  const [personalizedDestinations, setPersonalizedDestinations] = useState([]);
  const [popularActivities, setPopularActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activitiesLoading, setActivitiesLoading] = useState(true);
  // State untuk Surprise Modal
  const [showSurpriseModal, setShowSurpriseModal] = useState(false);

  // Fetch rekomendasi dari backend (MAB-based)
  // Anonymous: Context-based (cuaca, traffic, waktu, musim)
  // Logged-in: Context + Personalized (preferences, history)
  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        if (isAuthenticated) {
          // Logged-in user: Try Personalized + Context first
          try {
            const response = await recommendationsAPI.getPersonalized();
            setPersonalizedDestinations(response.data.recommendations || []);
          } catch (personalErr) {
            console.warn('Personalized recommendations failed, using fallback:', personalErr);
            await loadFallbackDestinations();
          }
        } else {
          // Anonymous user: Skip API call, go straight to fallback
          // (Model not trained, so API will always fail with 400)
          console.log('Anonymous user: Using random destinations from database');
          await loadFallbackDestinations();
        }
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        await loadFallbackDestinations();
      } finally {
        setLoading(false);
      }
    };

    const loadFallbackDestinations = async () => {
      try {
        const allDestResponse = await recommendationsAPI.getAllDestinations({ limit: 20 });
        const allDest = allDestResponse.data.destinations || [];
        
        // Shuffle and take 6 random
        const shuffled = allDest.sort(() => 0.5 - Math.random());
        const randomDest = shuffled.slice(0, 6);
        
        // Transform to match recommendation format
        const transformedData = randomDest.map((dest) => ({
          destination_id: dest.id,
          id: dest.id,
          name: dest.name,
          description: dest.description,
          region: dest.region,
          category: dest.category,
          image: dest.image,
          score: 0.75,
          explanation: `Rekomendasi ${dest.category} di ${dest.region}`
        }));
        
        setPersonalizedDestinations(transformedData);
      } catch (fallbackErr) {
        console.error('Fallback destinations also failed:', fallbackErr);
        // Last resort: empty array
        setPersonalizedDestinations([]);
      }
    };

    fetchRecommendations();
  }, [isAuthenticated]);

  // Fetch popular activities
  useEffect(() => {
    const fetchPopularActivities = async () => {
      try {
        const response = await activitiesAPI.getAll({ limit: 3 });
        setPopularActivities(response.data.activities || []);
      } catch (error) {
        console.error('Error fetching activities:', error);
        // Fallback data
        setPopularActivities([
          { id: 1, name: 'Wisata Kuliner', image: '/assets/images/kuliner-tahu.jpg', description: 'Nikmati kuliner khas Sumedang seperti Tahu Sumedang dan Peuyeum.', category: 'Kuliner' },
          { id: 2, name: 'Wisata Budaya', image: '/assets/images/budaya-sunda.jpg', description: 'Jelajahi warisan budaya Sunda di berbagai situs bersejarah.', category: 'Budaya' },
          { id: 3, name: 'Wisata Alam', image: '/assets/images/wisata-alam.jpg', description: 'Eksplorasi keindahan alam pegunungan dan air terjun Sumedang.', category: 'Alam' },
        ]);
      } finally {
        setActivitiesLoading(false);
      }
    };

    fetchPopularActivities();
  }, []);

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Jelajahi Sumedang</h1>
          <p>Temukan pesona wisata, budaya, dan kuliner Kota Tahu</p>
          <div className="cta-buttons">
            <Link to="/destinations" className="btn primary">Jelajahi Destinasi</Link>
            <Link to="/planning" className="btn secondary">Rencanakan Perjalanan</Link>
          </div>
        </div>
      </section>

      {/* Personalized Recommendations - Netflix Style Slider */}
      <section className="personalized-recommendations netflix-style">
        <div className="container">
          <div className="section-header-simple">
            <h2>Rekomendasi Untuk Anda</h2>
          </div>
          
          {loading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Memuat rekomendasi personal...</p>
            </div>
          ) : (
            <div className="slider-container">
              <div className="slider-wrapper">
                {personalizedDestinations.map(destination => (
                  <div key={destination.destination_id || destination.id} className="slider-item">
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
            </div>
          )}
        </div>
      </section>

      {/* Popular Activities */}
      <section className="popular-activities">
        <div className="container">
          <h2>Aktivitas Populer</h2>
          {activitiesLoading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Memuat aktivitas...</p>
            </div>
          ) : (
            <>
              <div className="card-grid">
                {Array.isArray(popularActivities) && popularActivities.map(activity => (
                  <ActivityCard key={activity.id} activity={activity} />
                ))}
              </div>
              <Link to="/activities" className="view-all">Lihat Semua Aktivitas</Link>
            </>
          )}
        </div>
      </section>

      {/* Surprise Me Section */}
      <section className="surprise-me">
        <div className="container">
          <div className="surprise-content">
            <h2>Kami tahu, Sumedang itu luas.</h2>
            <p>Tidak yakin mau mulai dari mana? Biarkan kami memberikan rekomendasi acak yang menarik untuk Anda!</p>
            <button 
              className="btn primary large" 
              onClick={() => setShowSurpriseModal(true)}
            >
              Kejutkan Saya
            </button>
          </div>
        </div>
      </section>

      {/* Surprise Modal */}
      <SurpriseModal 
        isOpen={showSurpriseModal} 
        onClose={() => setShowSurpriseModal(false)} 
      />

      {/* Where is Sumedang Section */}
      <section className="where-is-sumedang">
        <div className="container">
          <div className="where-content">
            <div className="where-text">
              <h2>Dimana Letak Sumedang?</h2>
              <p>
                Tidak familiar dengan geografi Jawa Barat? Sumedang berada di wilayah tengah Jawa Barat, 
                berbatasan dengan Bandung, Garut, Majalengka, dan Cirebon. Beberapa orang mengatakan 
                Sumedang adalah permata tersembunyi Jawa Barat, dan tentu saja mereka benar!
              </p>
              <p>
                Terdiri dari 26 kecamatan yang beragam, Sumedang memiliki pegunungan, danau, lembah, 
                persawahan hijau, situs budaya, dan hampir segala sesuatu di antaranya. Dari Gunung Tampomas 
                yang megah hingga Waduk Jatigede yang mempesona, dari Kampung Adat Cigugur yang kaya budaya 
                hingga kuliner Tahu yang legendaris.
              </p>
              <div className="guide-cta">
                <Link to="/resources" className="btn secondary">Panduan Pemula ke Sumedang</Link>
              </div>
            </div>
            <div className="where-map">
              <img src="/assets/images/peta-sumedang-jawa-barat.jpg" alt="Peta Sumedang di Jawa Barat" />
            </div>
          </div>
        </div>
      </section>

      {/* Plan Your Trip CTA */}
      <section className="plan-trip-cta">
        <div className="container">
          <div className="cta-content">
            <h2>Mulai Rencanakan Perjalanan Anda ke Sumedang</h2>
            <p>Dapatkan rekomendasi akomodasi, transportasi, dan tips wisata lokal</p>
            <Link to="/planning" className="btn primary">Rencanakan Sekarang</Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;