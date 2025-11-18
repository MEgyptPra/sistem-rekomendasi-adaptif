import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { destinationsAPI, relatedAPI, interactionsAPI, favoritesAPI } from '../services/api';
import '../styles/destination-detail.css';

const DestinationDetail = () => {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [destination, setDestination] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [relatedDestinations, setRelatedDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    comment: ''
  });
  const [submittingReview, setSubmittingReview] = useState(false);
  const viewStartTime = useRef(Date.now());

  // Fetch destination data
  useEffect(() => {
    const fetchDestination = async () => {
      try {
        const response = await destinationsAPI.getById(id);
        setDestination(response.data);
        
        // Fetch reviews
        const reviewsResponse = await destinationsAPI.getReviews(id);
        setReviews(reviewsResponse.data.reviews || []);
        
        // Fetch related destinations
        const relatedResponse = await relatedAPI.getRelatedDestinations(id);
        setRelatedDestinations(relatedResponse.data.destinations || []);
      } catch (error) {
        console.error('Error fetching destination:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDestination();
  }, [id]);

  // Track view duration on unmount
  useEffect(() => {
    return () => {
      if (isAuthenticated && destination) {
        const duration = Math.floor((Date.now() - viewStartTime.current) / 1000);
        interactionsAPI.trackView('destination', parseInt(id), duration)
          .catch(error => console.error('Error tracking view:', error));
      }
    };
  }, [id, destination, isAuthenticated]);

  // Handle review submission
  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      alert('Silakan login terlebih dahulu untuk memberikan ulasan');
      return;
    }

    setSubmittingReview(true);
    try {
      await destinationsAPI.submitReview(id, {
        rating: reviewForm.rating,
        comment: reviewForm.comment
      });
      
      // Refresh reviews
      const reviewsResponse = await destinationsAPI.getReviews(id);
      setReviews(reviewsResponse.data || []);
      
      // Reset form
      setReviewForm({ rating: 5, comment: '' });
      alert('Ulasan berhasil dikirim!');
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('Gagal mengirim ulasan. Silakan coba lagi.');
    } finally {
      setSubmittingReview(false);
    }
  };

  // Handle favorite toggle
  const handleFavoriteToggle = async () => {
    if (!isAuthenticated) {
      alert('Silakan login terlebih dahulu untuk menambahkan favorit');
      return;
    }

    try {
      if (isFavorite) {
        await favoritesAPI.remove('destination', id);
        setIsFavorite(false);
      } else {
        await favoritesAPI.add('destination', id);
        setIsFavorite(true);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  // Data dummy untuk Gunung Tampomas (ID: 1) - FALLBACK
  const destinationsData = {
    1: {
      id: 1,
      name: 'Gunung Tampomas',
      category: 'Wisata Alam',
      region: 'Kecamatan Sumedang Utara',
      image: '/assets/images/gunung-tampomas-hero.jpg',
      rating: 4.6,
      reviewCount: 328,
      ticketPrice: 'Gratis',
      openingHours: '24 Jam',
      description: 'Gunung Tampomas adalah gunung berapi tidak aktif yang menjadi ikon Kabupaten Sumedang. Dengan ketinggian 1.684 meter di atas permukaan laut, gunung ini menawarkan pemandangan spektakuler hamparan sawah, kebun teh, dan kota Sumedang dari puncaknya. Destinasi favorit untuk pendaki dan pecinta alam yang mencari ketenangan.',
      highlights: [
        'Pemandangan sunrise dari puncak yang menakjubkan',
        'Pemandangan 360 derajat Waduk Jatigede dan Gunung Ciremai',
        'Hutan pinus dan kebun teh yang menyegarkan',
        'Spot foto instagramable di banyak titik',
        'Udara sejuk dan segar khas pegunungan',
        'Cocok untuk hiking dan camping'
      ],
      facilities: [
        'Area parkir kendaraan',
        'Toilet umum',
        'Warung makan',
        'Musala',
        'Tempat istirahat',
        'Gazebo'
      ],
      bestTime: {
        season: 'Musim Kemarau (April - Oktober)',
        avoid: 'Hindari saat musim hujan untuk keamanan',
        recommendation: 'Datang pagi hari untuk cuaca yang lebih sejuk'
      },
      tips: [
        'Gunakan alas kaki yang nyaman untuk berjalan',
        'Bawa air minum yang cukup',
        'Gunakan sunscreen dan topi untuk perlindungan matahari',
        'Bawa kamera untuk mengabadikan pemandangan',
        'Datang di pagi hari untuk menghindari keramaian',
        'Jaga kebersihan dengan tidak membuang sampah sembarangan',
        'Ikuti peraturan dan petunjuk yang ada di lokasi',
        'Hormati lingkungan dan budaya setempat'
      ],
      gallery: [
        '/assets/images/tampomas-1.jpg',
        '/assets/images/tampomas-2.jpg',
        '/assets/images/tampomas-3.jpg',
        '/assets/images/tampomas-4.jpg',
        '/assets/images/tampomas-5.jpg',
        '/assets/images/tampomas-6.jpg'
      ],
      nearbyAttractions: [
        {
          name: 'Kebun Teh Tambi',
          distance: '5 km',
          description: 'Perkebunan teh dengan pemandangan hijau menyegarkan'
        },
        {
          name: 'Kampung Adat Cigugur',
          distance: '12 km',
          description: 'Kampung adat dengan budaya Sunda yang masih terjaga'
        },
        {
          name: 'Situ Ciburuy',
          distance: '18 km',
          description: 'Danau alami dengan suasana tenang'
        }
      ],
      reviews: [
        {
          name: 'Andi Pratama',
          rating: 5,
          date: '20 Oktober 2025',
          comment: 'Sunrise di puncak Tampomas luar biasa! Jalur pendakiannya juga nggak terlalu susah, cocok buat pemula. Pemandangan dari puncak bisa lihat Waduk Jatigede dan Gunung Ciremai. Recommended banget!',
          avatar: '/assets/images/avatar-1.jpg'
        },
        {
          name: 'Siti Rahma',
          rating: 5,
          date: '15 Oktober 2025',
          comment: 'Pertama kali naik gunung dan pilih Tampomas. Ternyata nggak sesulit yang dibayangkan! Jalur jelas, ada pos istirahat, dan pemandangan keren. Puas banget!',
          avatar: '/assets/images/avatar-2.jpg'
        },
        {
          name: 'Dedi Supardi',
          rating: 4,
          date: '10 Oktober 2025',
          comment: 'Bagus untuk pendakian weekend. Jalurnya relatif mudah. Saranku datang pagi buta biar bisa lihat sunrise, karena kalau siang bakal panas banget di jalur terbuka.',
          avatar: '/assets/images/avatar-3.jpg'
        },
        {
          name: 'Rina Wulandari',
          rating: 5,
          date: '5 Oktober 2025',
          comment: 'Gunung favorit! Udah 3x naik kesini dan nggak pernah bosen. Setiap musim punya pemandangan berbeda. Hutan pinusnya keren buat foto-foto!',
          avatar: '/assets/images/avatar-4.jpg'
        }
      ],
      relatedDestinations: [
        { 
          id: 2, 
          name: 'Situ Ciburuy', 
          image: '/assets/images/situ-ciburuy.jpg', 
          category: 'Wisata Alam',
          rating: 4.5
        },
        { 
          id: 4, 
          name: 'Waduk Jatigede', 
          image: '/assets/images/waduk-jatigede.jpg', 
          category: 'Wisata Alam',
          rating: 4.7
        },
        { 
          id: 5, 
          name: 'Air Terjun Cikahuripan', 
          image: '/assets/images/air-terjun.jpg', 
          category: 'Wisata Alam',
          rating: 4.4
        }
      ]
    }
  };



  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Memuat detail destinasi...</p>
      </div>
    );
  }

  if (!destination) {
    return (
      <div className="error-container">
        <h2>Destinasi tidak ditemukan</h2>
        <Link to="/destinations" className="btn primary">Kembali ke Destinasi</Link>
      </div>
    );
  }

  return (
    <div className="destination-detail-page">
      {/* Hero Section */}
      <section className="destination-hero" style={{ backgroundImage: `url(${destination.image})` }}>
        <div className="hero-overlay">
          <div className="container">
            <div className="breadcrumb">
              <Link to="/">Beranda</Link> / <Link to="/destinations">Destinasi</Link> / <span>{destination.name}</span>
            </div>
            <h1>{destination.name}</h1>
            <div className="destination-meta">
              <span className="category">{destination.category}</span>
              <span className="rating">⭐ {destination.rating || 0} ({reviews.length} ulasan)</span>
              <span className="location">📍 {destination.region || destination.location}</span>
              {isAuthenticated && (
                <button 
                  className={`favorite-btn ${isFavorite ? 'active' : ''}`}
                  onClick={handleFavoriteToggle}
                >
                  {isFavorite ? '❤️ Favorit' : '🤍 Tambah Favorit'}
                </button>
              )}
            </div>
          </div>
        </div>
      </section>

      <div className="container destination-content">
        <div className="main-content">
          {/* Quick Info */}
          <section className="quick-info-section">
            <div className="info-boxes">
              <div className="info-box">
                <span className="icon">🎫</span>
                <div className="info-text">
                  <p className="label">Harga Tiket</p>
                  <p className="value">{destination.ticketPrice}</p>
                </div>
              </div>
              <div className="info-box">
                <span className="icon">🕐</span>
                <div className="info-text">
                  <p className="label">Jam Buka</p>
                  <p className="value">{destination.openingHours}</p>
                </div>
              </div>
              <div className="info-box">
                <span className="icon">📍</span>
                <div className="info-text">
                  <p className="label">Lokasi</p>
                  <p className="value">{destination.region}</p>
                </div>
              </div>
              <div className="info-box">
                <span className="icon">⭐</span>
                <div className="info-text">
                  <p className="label">Rating</p>
                  <p className="value">{destination.rating} / 5.0</p>
                </div>
              </div>
            </div>
          </section>

          {/* Description */}
          <section className="description-section">
            <h2>Tentang {destination.name}</h2>
            <p>{destination.description}</p>
          </section>

          {/* Highlights */}
          <section className="highlights-section">
            <h2>Yang Bisa Anda Nikmati</h2>
            <ul className="highlights-list">
              {destination.highlights.map((highlight, index) => (
                <li key={index}>
                  <span className="check-icon">✓</span>
                  {highlight}
                </li>
              ))}
            </ul>
          </section>

          {/* Best Time to Visit */}
          <section className="best-time-section">
            <h2>Waktu Terbaik Berkunjung</h2>
            <div className="time-info">
              <div className="time-card best">
                <span className="icon">☀️</span>
                <h3>Waktu Ideal</h3>
                <p>{destination.bestTime.season}</p>
              </div>
              <div className="time-card avoid">
                <span className="icon">⚠️</span>
                <h3>Hindari</h3>
                <p>{destination.bestTime.avoid}</p>
              </div>
              <div className="time-card tips">
                <span className="icon">💡</span>
                <h3>Rekomendasi</h3>
                <p>{destination.bestTime.recommendation}</p>
              </div>
            </div>
          </section>

          {/* Facilities */}
          <section className="facilities-section">
            <h2>Fasilitas Tersedia</h2>
            <div className="facilities-grid">
              {destination.facilities.map((facility, index) => (
                <div key={index} className="facility-item">
                  <span className="facility-icon">✓</span>
                  <span>{facility}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Tips */}
          <section className="tips-section">
            <h2>Tips & Saran</h2>
            <div className="tips-box">
              <ul>
                {destination.tips.map((tip, index) => (
                  <li key={index}>💡 {tip}</li>
                ))}
              </ul>
            </div>
          </section>

          {/* Gallery */}
          <section className="gallery-section">
            <h2>Galeri Foto</h2>
            <div className="photo-gallery">
              {destination.gallery.map((photo, index) => (
                <div key={index} className="gallery-item">
                  <img src={photo} alt={`${destination.name} ${index + 1}`} onError={e => {e.target.onerror=null;e.target.src='/assets/images/placeholder.webp';}} />
                </div>
              ))}
            </div>
          </section>

          {/* Nearby Attractions */}
          <section className="nearby-section">
            <h2>Destinasi Terdekat</h2>
            <div className="nearby-list">
              {destination.nearbyAttractions.map((nearby, index) => (
                <div key={index} className="nearby-card">
                  <h3>{nearby.name}</h3>
                  <p>{nearby.description}</p>
                  <span className="distance">📍 {nearby.distance}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Reviews */}
          <section className="reviews-section">
            <h2>Ulasan Pengunjung</h2>
            
            {/* Add Review Form */}
            {isAuthenticated ? (
              <div className="add-review-form">
                <h3>Tambahkan Ulasan Anda</h3>
                <form className="review-form" onSubmit={handleReviewSubmit}>
                  <div className="form-group">
                    <label>Rating</label>
                    <div className="star-rating-input">
                      {[5, 4, 3, 2, 1].map(star => (
                        <React.Fragment key={star}>
                          <input 
                            type="radio" 
                            name="rating" 
                            value={star} 
                            id={`star${star}`}
                            checked={reviewForm.rating === star}
                            onChange={(e) => setReviewForm({...reviewForm, rating: parseInt(e.target.value)})}
                          />
                          <label htmlFor={`star${star}`}>⭐</label>
                        </React.Fragment>
                      ))}
                    </div>
                  </div>

                  <div className="form-group">
                    <label>Ulasan Anda</label>
                    <textarea 
                      className="form-control" 
                      rows="4"
                      placeholder="Ceritakan pengalaman Anda mengunjungi tempat ini..."
                      value={reviewForm.comment}
                      onChange={(e) => setReviewForm({...reviewForm, comment: e.target.value})}
                      required
                    ></textarea>
                  </div>

                  <button type="submit" className="btn primary" disabled={submittingReview}>
                    {submittingReview ? 'Mengirim...' : 'Kirim Ulasan'}
                  </button>
                </form>
              </div>
            ) : (
              <div className="login-prompt-review">
                <p>Silakan <Link to="/login">login</Link> untuk memberikan ulasan</p>
              </div>
            )}

            {/* Reviews List */}
            <div className="reviews-list">
              <h3 className="reviews-count">{reviews.length} Ulasan</h3>
              {reviews.length === 0 ? (
                <p className="no-reviews">Belum ada ulasan. Jadilah yang pertama memberikan ulasan!</p>
              ) : (
                reviews.map((review, index) => (
                  <div key={index} className="review-card">
                    <div className="review-header">
                      <div className="avatar-placeholder">{review.user_name?.charAt(0) || 'U'}</div>
                      <div className="review-info">
                        <h4>{review.user_name || 'Anonymous'}</h4>
                        <div className="review-meta">
                          <span className="stars">{'⭐'.repeat(review.rating)}</span>
                          <span className="date">{new Date(review.created_at).toLocaleDateString('id-ID')}</span>
                        </div>
                      </div>
                    </div>
                    <p className="review-text">{review.comment}</p>
                  </div>
                ))
              )}
            </div>
          </section>

          {/* Related Destinations */}
          {relatedDestinations.length > 0 && (
            <section className="related-section">
              <h2>Destinasi Terkait</h2>
              <div className="related-grid">
                {relatedDestinations.map((related) => (
                  <Link key={related.id} to={`/destinations/${related.id}`} className="related-card">
                    <img src={related.image || '/assets/images/placeholder.jpg'} alt={related.name} />
                    <div className="related-info">
                      <h3>{related.name}</h3>
                      <div className="related-meta">
                        <span className="category-badge">{related.category}</span>
                        <span className="rating-badge">⭐ {related.rating || 0}</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  );
};

export default DestinationDetail;
