import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { activitiesAPI, relatedAPI, interactionsAPI, favoritesAPI } from '../services/api';
import '../styles/activity-detail.css';

const ActivityDetail = () => {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [activity, setActivity] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [relatedActivities, setRelatedActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    comment: ''
  });
  const [submittingReview, setSubmittingReview] = useState(false);
  const viewStartTime = useRef(Date.now());

  // Data dummy untuk aktivitas kuliner tahu (ID: 8)
  const activitiesData = {
    8: {
      id: 8,
      name: 'Wisata Kuliner Tahu Sumedang',
      category: 'Kuliner',
      image: '/assets/images/kuliner-tahu-hero.jpg',
      rating: 4.8,
      reviewCount: 245,
      duration: '2-3 jam',
      price: 'Rp 50.000 - 150.000',
      description: 'Jelajahi kelezatan legendaris Tahu Sumedang yang telah terkenal di seluruh Indonesia. Kunjungi sentra produksi, pabrik, dan restoran tahu terbaik di Sumedang.',
      highlights: [
        'Kunjungan ke pabrik tahu tradisional',
        'Demo cara membuat tahu Sumedang',
        'Cicip berbagai varian tahu (goreng, isi, bacem)',
        'Beli tahu fresh langsung dari produsen',
        'Photo spot Instagram-able',
        'Belajar sejarah tahu Sumedang'
      ],
      included: [
        'Pemandu wisata lokal',
        'Snack tahu gratis (3 potong)',
        'Voucher belanja tahu',
        'Dokumentasi foto',
        'Transportasi antar lokasi'
      ],
      itinerary: [
        {
          time: '09:00',
          title: 'Meeting Point',
          description: 'Berkumpul di Pusat Informasi Wisata Sumedang'
        },
        {
          time: '09:30',
          title: 'Pabrik Tahu Tradisional',
          description: 'Kunjungan ke pabrik tahu yang masih menggunakan metode tradisional. Lihat langsung proses pembuatan dari kedelai hingga menjadi tahu.'
        },
        {
          time: '10:30',
          title: 'Demo & Workshop',
          description: 'Ikut mencoba membuat tahu sendiri dan belajar resep rahasia bumbu kacang khas Sumedang.'
        },
        {
          time: '11:30',
          title: 'Tasting Session',
          description: 'Cicip berbagai varian tahu: tahu goreng original, tahu isi, tahu bacem, dan tahu bulat.'
        },
        {
          time: '12:30',
          title: 'Lunch & Shopping',
          description: 'Makan siang di restoran tahu terkenal dan belanja oleh-oleh tahu untuk dibawa pulang.'
        }
      ],
      locations: [
        {
          name: 'Tahu Bu Rohman',
          address: 'Jl. Mayor Abdurachman No.124, Sumedang',
          distance: '1.2 km dari pusat kota',
          type: 'Pabrik & Toko'
        },
        {
          name: 'Sentra Tahu Cipameungpeuk',
          address: 'Cipameungpeuk, Sumedang',
          distance: '3.5 km dari pusat kota',
          type: 'Sentra Produksi'
        },
        {
          name: 'Rumah Makan Tahu Bletok',
          address: 'Jl. Raya Sumedang, Sumedang',
          distance: '0.8 km dari pusat kota',
          type: 'Restoran'
        }
      ],
      tips: [
        'Datang di pagi hari untuk melihat proses produksi yang fresh',
        'Bawa kantong belanja untuk membeli tahu dalam jumlah banyak',
        'Tahu paling enak dimakan selagi hangat',
        'Jangan lupa coba tahu isi dengan berbagai varian (daging, sayur, ayam)',
        'Minta digoreng di tempat untuk pengalaman terbaik'
      ],
      gallery: [
        '/assets/images/tahu-1.jpg',
        '/assets/images/tahu-2.jpg',
        '/assets/images/tahu-3.jpg',
        '/assets/images/tahu-4.jpg',
        '/assets/images/tahu-5.jpg',
        '/assets/images/tahu-6.jpg'
      ],
      reviews: [
        {
          name: 'Dewi Lestari',
          rating: 5,
          date: '15 Oktober 2025',
          comment: 'Pengalaman yang luar biasa! Tahu Sumedang memang juara. Guide-nya ramah dan informatif. Anak-anak suka banget workshop bikin tahunya!',
          avatar: '/assets/images/avatar-1.jpg'
        },
        {
          name: 'Budi Santoso',
          rating: 5,
          date: '10 Oktober 2025',
          comment: 'Must try! Tahu di sini beda banget sama yang di Jakarta. Fresh, renyah, dan bumbunya enak. Beli banyak buat oleh-oleh keluarga.',
          avatar: '/assets/images/avatar-2.jpg'
        },
        {
          name: 'Siti Nurhaliza',
          rating: 4,
          date: '5 Oktober 2025',
          comment: 'Sangat recommended untuk pecinta kuliner. Pabriknya bersih dan proses pembuatannya menarik untuk dipelajari.',
          avatar: '/assets/images/avatar-3.jpg'
        }
      ],
      relatedActivities: [
        { id: 2, name: 'Wisata Peuyeum', image: '/assets/images/peuyeum.jpg', category: 'Kuliner' },
        { id: 5, name: 'Kuliner Nasi Timbel', image: '/assets/images/nasi-timbel.jpg', category: 'Kuliner' },
        { id: 9, name: 'Kopi Sumedang Tour', image: '/assets/images/kopi.jpg', category: 'Kuliner' }
      ]
    }
  };

  // Fetch activity data
  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const response = await activitiesAPI.getById(id);
        setActivity(response.data || activitiesData[id]);
        
        // Fetch reviews
        const reviewsResponse = await activitiesAPI.getReviews(id);
        setReviews(reviewsResponse.data.reviews || []);
        
        // Fetch related activities
        const relatedResponse = await relatedAPI.getRelatedActivities(id);
        setRelatedActivities(relatedResponse.data.activities || []);
      } catch (error) {
        console.error('Error fetching activity:', error);
        // Fallback to dummy data
        setActivity(activitiesData[id]);
      } finally {
        setLoading(false);
      }
    };

    fetchActivity();
  }, [id]);

  // Track view duration on unmount
  useEffect(() => {
    return () => {
      if (isAuthenticated && activity) {
        const duration = Math.floor((Date.now() - viewStartTime.current) / 1000);
        interactionsAPI.trackView('activity', parseInt(id), duration)
          .catch(error => console.error('Error tracking view:', error));
      }
    };
  }, [id, activity, isAuthenticated]);

  // Handle review submission
  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      alert('Silakan login terlebih dahulu untuk memberikan ulasan');
      return;
    }

    setSubmittingReview(true);
    try {
      await activitiesAPI.submitReview(id, {
        rating: reviewForm.rating,
        comment: reviewForm.comment
      });
      
      // Refresh reviews
      const reviewsResponse = await activitiesAPI.getReviews(id);
      setReviews(reviewsResponse.data.reviews || []);
      
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
        await favoritesAPI.remove('activity', id);
        setIsFavorite(false);
      } else {
        await favoritesAPI.add('activity', id);
        setIsFavorite(true);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Memuat detail aktivitas...</p>
      </div>
    );
  }

  if (!activity) {
    return (
      <div className="error-container">
        <h2>Aktivitas tidak ditemukan</h2>
        <Link to="/activities" className="btn primary">Kembali ke Aktivitas</Link>
      </div>
    );
  }

  return (
    <div className="activity-detail-page">
      {/* Hero Section */}
      <section className="activity-hero" style={{ backgroundImage: `url(${activity.image})` }}>
        <div className="hero-overlay">
          <div className="container">
            <div className="breadcrumb">
              <Link to="/">Beranda</Link> / <Link to="/activities">Aktivitas</Link> / <span>{activity.name}</span>
            </div>
            <h1>{activity.name}</h1>
            <div className="activity-meta">
              <span className="category">{activity.category}</span>
              <span className="rating">⭐ {activity.rating} ({activity.reviewCount} ulasan)</span>
              <span className="duration">🕐 {activity.duration}</span>
              <span className="price">💰 {activity.price}</span>
            </div>
          </div>
        </div>
      </section>

      <div className="container activity-content">
        <div className="main-content">
          {/* Description */}
          <section className="description-section">
            <h2>Tentang Aktivitas Ini</h2>
            <p>{activity.description}</p>
          </section>

          {/* Highlights */}
          {activity.highlights && activity.highlights.length > 0 && (
            <section className="highlights-section">
              <h2>Highlights</h2>
              <ul className="highlights-list">
                {activity.highlights.map((highlight, index) => (
                  <li key={index}>
                    <span className="check-icon">✓</span>
                    {highlight}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Itinerary */}
          {activity.itinerary && activity.itinerary.length > 0 && (
            <section className="itinerary-section">
              <h2>Itinerary</h2>
              <div className="timeline">
                {activity.itinerary.map((item, index) => (
                  <div key={index} className="timeline-item">
                    <div className="timeline-time">{item.time}</div>
                    <div className="timeline-content">
                      <h3>{item.title}</h3>
                      <p>{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Locations */}
          {activity.locations && activity.locations.length > 0 && (
            <section className="locations-section">
              <h2>Lokasi yang Dikunjungi</h2>
              <div className="locations-grid">
                {activity.locations.map((location, index) => (
                  <div key={index} className="location-card">
                    <h3>{location.name}</h3>
                    <p className="address">📍 {location.address}</p>
                    <p className="distance">{location.distance}</p>
                    <span className="location-type">{location.type}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Gallery */}
          {activity.gallery && activity.gallery.length > 0 && (
            <section className="gallery-section">
              <h2>Galeri Foto</h2>
              <div className="photo-gallery">
                {activity.gallery.map((photo, index) => (
                  <div key={index} className="gallery-item">
                    <img src={photo} alt={`Gallery ${index + 1}`} />
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Tips */}
          {activity.tips && activity.tips.length > 0 && (
            <section className="tips-section">
              <h2>Tips & Saran</h2>
              <div className="tips-box">
                <ul>
                  {activity.tips.map((tip, index) => (
                    <li key={index}>💡 {tip}</li>
                  ))}
                </ul>
              </div>
            </section>
          )}

          {/* Reviews */}
          <section className="reviews-section">
            <h2>Ulasan Pengunjung</h2>
            
            {/* Add Review Form */}
            <div className="add-review-form">
              <h3>Tambahkan Ulasan Anda</h3>
              <form className="review-form">
                <div className="form-row">
                  <div className="form-group">
                    <label>Nama Anda</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="Masukkan nama Anda"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Rating</label>
                    <div className="star-rating-input">
                      <input type="radio" name="rating" value="5" id="star5" />
                      <label htmlFor="star5">⭐</label>
                      <input type="radio" name="rating" value="4" id="star4" />
                      <label htmlFor="star4">⭐</label>
                      <input type="radio" name="rating" value="3" id="star3" />
                      <label htmlFor="star3">⭐</label>
                      <input type="radio" name="rating" value="2" id="star2" />
                      <label htmlFor="star2">⭐</label>
                      <input type="radio" name="rating" value="1" id="star1" />
                      <label htmlFor="star1">⭐</label>
                    </div>
                  </div>
                </div>

                <div className="form-group">
                  <label>Ulasan Anda</label>
                  <textarea 
                    className="form-control" 
                    rows="4"
                    placeholder="Ceritakan pengalaman Anda dengan aktivitas ini..."
                    required
                  ></textarea>
                </div>

                <button type="submit" className="btn primary">
                  Kirim Ulasan
                </button>
              </form>
            </div>

            {/* Reviews List */}
            {activity.reviews && activity.reviews.length > 0 ? (
              <div className="reviews-list">
                <h3 className="reviews-count">{activity.reviewCount || activity.reviews.length} Ulasan</h3>
                {activity.reviews.map((review, index) => (
                  <div key={index} className="review-card">
                    <div className="review-header">
                      <img src={review.avatar} alt={review.name} className="avatar" />
                      <div className="review-info">
                        <h4>{review.name}</h4>
                        <div className="review-meta">
                          <span className="stars">{'⭐'.repeat(review.rating)}</span>
                          <span className="date">{review.date}</span>
                        </div>
                      </div>
                    </div>
                    <p className="review-text">{review.comment}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-reviews">Belum ada ulasan. Jadilah yang pertama memberikan ulasan!</p>
            )}
          </section>

          {/* Related Activities */}
          {activity.relatedActivities && activity.relatedActivities.length > 0 && (
            <section className="related-section">
              <h2>Aktivitas Terkait</h2>
              <div className="related-grid">
                {activity.relatedActivities.map((related) => (
                  <Link key={related.id} to={`/activities/${related.id}`} className="related-card">
                    <img src={related.image} alt={related.name} />
                    <div className="related-info">
                      <h3>{related.name}</h3>
                      <span className="category-badge">{related.category}</span>
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

export default ActivityDetail;
