import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import '../styles/planning-detail.css';

const PlanningDetail = () => {
  const { id } = useParams();
  const [itinerary, setItinerary] = useState(null);
  const [loading, setLoading] = useState(true);

  // Data dummy untuk itinerary (ID: 1)
  const itinerariesData = {
    1: {
      id: 1,
      title: 'Petualangan Alam & Kuliner Sumedang 3 Hari',
      startDate: '2025-12-15',
      endDate: '2025-12-17',
      duration: '3 Hari 2 Malam',
      travelers: 4,
      budget: 'Rp 2.500.000',
      categories: ['Wisata Alam', 'Wisata Kuliner'],
      interests: ['Petualangan Outdoor', 'Kuliner & Makanan'],
      status: 'upcoming', // upcoming, ongoing, completed
      coverImage: '/assets/images/itinerary-cover.jpg',
      description: 'Jelajahi keindahan alam Sumedang dan nikmati kuliner khasnya dalam perjalanan 3 hari yang tak terlupakan.',
      days: [
        {
          day: 1,
          date: '15 Desember 2025',
          title: 'Hari 1: Pendakian Gunung Tampomas',
          activities: [
            {
              time: '06:00',
              title: 'Sarapan & Persiapan',
              location: 'Hotel',
              description: 'Sarapan pagi dan persiapan perlengkapan pendakian',
              duration: '1 jam',
              type: 'meal'
            },
            {
              time: '07:00',
              title: 'Berangkat ke Basecamp Gunung Tampomas',
              location: 'Basecamp Cibeusi',
              description: 'Perjalanan menuju basecamp dengan kendaraan pribadi',
              duration: '45 menit',
              type: 'transport',
              destination: {
                id: 1,
                name: 'Gunung Tampomas',
                image: '/assets/images/gunung-tampomas.jpg'
              }
            },
            {
              time: '08:00',
              title: 'Pendakian Gunung Tampomas',
              location: 'Gunung Tampomas',
              description: 'Pendakian menuju puncak Tampomas melalui jalur Cibeusi. Nikmati pemandangan kebun teh dan hutan pinus.',
              duration: '4 jam',
              type: 'activity',
              destination: {
                id: 1,
                name: 'Gunung Tampomas',
                image: '/assets/images/gunung-tampomas.jpg'
              }
            },
            {
              time: '12:00',
              title: 'Istirahat & Makan Siang di Puncak',
              location: 'Puncak Tampomas',
              description: 'Istirahat sambil menikmati pemandangan 360 derajat dan makan siang',
              duration: '2 jam',
              type: 'meal'
            },
            {
              time: '14:00',
              title: 'Turun Gunung',
              location: 'Gunung Tampomas',
              description: 'Perjalanan turun kembali ke basecamp',
              duration: '3 jam',
              type: 'activity'
            },
            {
              time: '17:30',
              title: 'Check-in Hotel & Istirahat',
              location: 'Hotel Sumedang',
              description: 'Check-in hotel, mandi, dan istirahat',
              duration: '2 jam',
              type: 'accommodation'
            },
            {
              time: '19:30',
              title: 'Makan Malam Kuliner Tahu',
              location: 'Rumah Makan Tahu Bletok',
              description: 'Nikmati berbagai varian tahu Sumedang: tahu isi, tahu goreng, dan tahu bacem',
              duration: '1.5 jam',
              type: 'meal',
              destination: {
                id: 8,
                name: 'Wisata Kuliner Tahu',
                image: '/assets/images/kuliner-tahu.jpg'
              }
            }
          ]
        },
        {
          day: 2,
          date: '16 Desember 2025',
          title: 'Hari 2: Wisata Air & Budaya',
          activities: [
            {
              time: '08:00',
              title: 'Sarapan Pagi',
              location: 'Hotel',
              description: 'Sarapan di hotel',
              duration: '1 jam',
              type: 'meal'
            },
            {
              time: '09:00',
              title: 'Kunjungi Situ Ciburuy',
              location: 'Situ Ciburuy',
              description: 'Menikmati keindahan danau Ciburuy, naik perahu, dan foto-foto',
              duration: '3 jam',
              type: 'activity',
              destination: {
                id: 2,
                name: 'Situ Ciburuy',
                image: '/assets/images/situ-ciburuy.jpg'
              }
            },
            {
              time: '12:00',
              title: 'Makan Siang Ikan Bakar',
              location: 'Warung Tepi Danau',
              description: 'Makan siang dengan menu ikan bakar khas Situ Ciburuy',
              duration: '1.5 jam',
              type: 'meal'
            },
            {
              time: '14:00',
              title: 'Kampung Adat Cigugur',
              location: 'Kampung Adat Cigugur',
              description: 'Belajar tentang budaya dan tradisi Sunda di kampung adat yang masih terjaga',
              duration: '2.5 jam',
              type: 'activity',
              destination: {
                id: 3,
                name: 'Kampung Adat Cigugur',
                image: '/assets/images/kampung-cigugur.jpg'
              }
            },
            {
              time: '17:00',
              title: 'Belanja Oleh-oleh',
              location: 'Pusat Oleh-oleh Sumedang',
              description: 'Belanja tahu, peuyeum, dan oleh-oleh khas Sumedang lainnya',
              duration: '1.5 jam',
              type: 'shopping'
            },
            {
              time: '19:00',
              title: 'Makan Malam & Istirahat',
              location: 'Hotel',
              description: 'Makan malam dan istirahat di hotel',
              duration: 'Malam',
              type: 'meal'
            }
          ]
        },
        {
          day: 3,
          date: '17 Desember 2025',
          title: 'Hari 3: Waduk Jatigede & Pulang',
          activities: [
            {
              time: '08:00',
              title: 'Check-out & Sarapan',
              location: 'Hotel',
              description: 'Check-out hotel dan sarapan',
              duration: '1 jam',
              type: 'meal'
            },
            {
              time: '09:00',
              title: 'Waduk Jatigede',
              location: 'Waduk Jatigede',
              description: 'Kunjungi waduk terbesar di Jawa Barat, nikmati pemandangan dan foto-foto',
              duration: '3 jam',
              type: 'activity',
              destination: {
                id: 4,
                name: 'Waduk Jatigede',
                image: '/assets/images/waduk-jatigede.jpg'
              }
            },
            {
              time: '12:00',
              title: 'Makan Siang Terakhir',
              location: 'Restoran Tepi Waduk',
              description: 'Makan siang sambil menikmati pemandangan waduk',
              duration: '1.5 jam',
              type: 'meal'
            },
            {
              time: '14:00',
              title: 'Perjalanan Pulang',
              location: '-',
              description: 'Perjalanan kembali ke rumah dengan kenangan indah',
              duration: '-',
              type: 'transport'
            }
          ]
        }
      ],
      accommodation: {
        name: 'Hotel Sumedang Plaza',
        address: 'Jl. Mayor Abdurachman No. 83, Sumedang',
        checkIn: '15 Desember 2025, 14:00',
        checkOut: '17 Desember 2025, 12:00',
        nights: 2,
        price: 'Rp 800.000'
      },
      transportation: {
        type: 'Mobil Pribadi',
        details: 'Toyota Avanza - 1 unit',
        estimatedDistance: '250 km total',
        fuelCost: 'Rp 400.000'
      },
      budgetBreakdown: [
        { category: 'Akomodasi', amount: 'Rp 800.000' },
        { category: 'Transportasi (BBM)', amount: 'Rp 400.000' },
        { category: 'Makan & Minum', amount: 'Rp 600.000' },
        { category: 'Tiket Masuk', amount: 'Rp 200.000' },
        { category: 'Oleh-oleh', amount: 'Rp 300.000' },
        { category: 'Lain-lain', amount: 'Rp 200.000' }
      ],
      notes: [
        'Bawa jaket tebal untuk pendakian Gunung Tampomas',
        'Gunakan sunscreen dan topi',
        'Siapkan kamera untuk dokumentasi',
        'Bawa obat-obatan pribadi',
        'Konfirmasi hotel H-1 sebelum kedatangan'
      ],
      packingList: [
        'Pakaian ganti 3 hari',
        'Sepatu hiking & sandal',
        'Jaket tebal',
        'Tas ransel',
        'Kamera',
        'Powerbank',
        'Obat-obatan',
        'Perlengkapan mandi',
        'Sunscreen & topi',
        'Botol minum'
      ]
    }
  };

  useEffect(() => {
    // Simulasi fetch data dari API
    setTimeout(() => {
      const data = itinerariesData[id];
      setItinerary(data);
      setLoading(false);
    }, 500);
  }, [id]);

  const getActivityIcon = (type) => {
    const icons = {
      activity: '🎯',
      meal: '🍽️',
      transport: '🚗',
      accommodation: '🏨',
      shopping: '🛍️'
    };
    return icons[type] || '📍';
  };

  const getStatusBadge = (status) => {
    const badges = {
      upcoming: { text: 'Akan Datang', class: 'upcoming' },
      ongoing: { text: 'Sedang Berlangsung', class: 'ongoing' },
      completed: { text: 'Selesai', class: 'completed' }
    };
    return badges[status] || badges.upcoming;
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Memuat itinerary...</p>
      </div>
    );
  }

  if (!itinerary) {
    return (
      <div className="error-container">
        <h2>Itinerary tidak ditemukan</h2>
        <Link to="/planning" className="btn primary">Kembali ke Planning</Link>
      </div>
    );
  }

  const statusBadge = getStatusBadge(itinerary.status);

  return (
    <div className="planning-detail-page">
      {/* Hero Section */}
      <section className="itinerary-hero" style={{ backgroundImage: `url(${itinerary.coverImage})` }}>
        <div className="hero-overlay">
          <div className="container">
            <div className="breadcrumb">
              <Link to="/">Beranda</Link> / <Link to="/planning">Planning</Link> / <span>{itinerary.title}</span>
            </div>
            <div className="hero-content">
              <span className={`status-badge ${statusBadge.class}`}>{statusBadge.text}</span>
              <h1>{itinerary.title}</h1>
              <p className="description">{itinerary.description}</p>
              <div className="itinerary-meta">
                <span className="meta-item">📅 {itinerary.duration}</span>
                <span className="meta-item">👥 {itinerary.travelers} Orang</span>
                <span className="meta-item">💰 {itinerary.budget}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="container itinerary-content">
        {/* Quick Actions */}
        <div className="quick-actions">
          <button className="btn secondary">
            <span>📤</span> Bagikan
          </button>
          <button className="btn secondary">
            <span>📄</span> Unduh PDF
          </button>
          <button className="btn secondary">
            <span>✏️</span> Edit Itinerary
          </button>
          <button className="btn primary">
            <span>📋</span> Duplikat
          </button>
        </div>

        {/* Overview Cards */}
        <div className="overview-cards">
          <div className="overview-card">
            <h3>📅 Tanggal Perjalanan</h3>
            <p className="date-range">{itinerary.startDate} - {itinerary.endDate}</p>
            <p className="duration">{itinerary.duration}</p>
          </div>
          <div className="overview-card">
            <h3>🏨 Akomodasi</h3>
            <p className="name">{itinerary.accommodation.name}</p>
            <p className="details">{itinerary.accommodation.nights} malam · {itinerary.accommodation.price}</p>
          </div>
          <div className="overview-card">
            <h3>🚗 Transportasi</h3>
            <p className="name">{itinerary.transportation.type}</p>
            <p className="details">{itinerary.transportation.details}</p>
          </div>
        </div>

        {/* Daily Itinerary */}
        <section className="daily-itinerary">
          <h2>Rencana Perjalanan Detail</h2>
          
          {itinerary.days.map((day) => (
            <div key={day.day} className="day-section">
              <div className="day-header">
                <div className="day-number">Hari {day.day}</div>
                <div className="day-info">
                  <h3>{day.title}</h3>
                  <p className="day-date">{day.date}</p>
                </div>
              </div>

              <div className="activities-timeline">
                {day.activities.map((activity, index) => (
                  <div key={index} className="activity-item">
                    <div className="activity-time">
                      <span className="time">{activity.time}</span>
                      <span className="duration">{activity.duration}</span>
                    </div>
                    <div className="activity-marker">
                      <span className="icon">{getActivityIcon(activity.type)}</span>
                    </div>
                    <div className="activity-content">
                      <h4>{activity.title}</h4>
                      <p className="location">📍 {activity.location}</p>
                      <p className="description">{activity.description}</p>
                      {activity.destination && (
                        <Link 
                          to={`/destinations/${activity.destination.id}`} 
                          className="destination-link"
                        >
                          <img src={activity.destination.image} alt={activity.destination.name} />
                          <span>Lihat Detail: {activity.destination.name}</span>
                        </Link>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </section>

        {/* Budget Breakdown */}
        <section className="budget-section">
          <h2>Perkiraan Biaya</h2>
          <div className="budget-breakdown">
            {itinerary.budgetBreakdown.map((item, index) => (
              <div key={index} className="budget-item">
                <span className="category">{item.category}</span>
                <span className="amount">{item.amount}</span>
              </div>
            ))}
            <div className="budget-total">
              <span className="category">Total Perkiraan</span>
              <span className="amount">{itinerary.budget}</span>
            </div>
          </div>
        </section>

        {/* Packing List */}
        <section className="packing-section">
          <h2>Daftar Barang Bawaan</h2>
          <div className="packing-list">
            {itinerary.packingList.map((item, index) => (
              <div key={index} className="packing-item">
                <input type="checkbox" id={`pack-${index}`} />
                <label htmlFor={`pack-${index}`}>{item}</label>
              </div>
            ))}
          </div>
        </section>

        {/* Notes */}
        <section className="notes-section">
          <h2>Catatan Penting</h2>
          <div className="notes-list">
            {itinerary.notes.map((note, index) => (
              <div key={index} className="note-item">
                <span className="note-icon">💡</span>
                <p>{note}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Accommodation Details */}
        <section className="accommodation-section">
          <h2>Detail Akomodasi</h2>
          <div className="accommodation-card-detail">
            <h3>{itinerary.accommodation.name}</h3>
            <p className="address">📍 {itinerary.accommodation.address}</p>
            <div className="accommodation-info">
              <div className="info-item">
                <span className="label">Check-in:</span>
                <span className="value">{itinerary.accommodation.checkIn}</span>
              </div>
              <div className="info-item">
                <span className="label">Check-out:</span>
                <span className="value">{itinerary.accommodation.checkOut}</span>
              </div>
              <div className="info-item">
                <span className="label">Malam:</span>
                <span className="value">{itinerary.accommodation.nights} malam</span>
              </div>
              <div className="info-item">
                <span className="label">Total:</span>
                <span className="value">{itinerary.accommodation.price}</span>
              </div>
            </div>
          </div>
        </section>

        {/* Share CTA */}
        <section className="share-cta">
          <div className="cta-content">
            <h2>Bagikan Itinerary Anda</h2>
            <p>Inspirasi orang lain dengan rencana perjalanan Anda!</p>
            <div className="share-buttons">
              <button className="btn secondary">Facebook</button>
              <button className="btn secondary">Twitter</button>
              <button className="btn secondary">WhatsApp</button>
              <button className="btn secondary">Salin Link</button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default PlanningDetail;
