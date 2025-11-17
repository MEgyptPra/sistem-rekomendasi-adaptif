import React, { useEffect, useState } from 'react';
import { itineraryAPI } from '../services/api';

function ProfileItinerary() {
  const [itineraries, setItineraries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchItineraries = async () => {
      setLoading(true);
      setError('');
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setError('Anda harus login untuk melihat itinerary yang disimpan.');
          setLoading(false);
          return;
        }
        const res = await itineraryAPI.list();
        setItineraries(res.data);
      } catch (err) {
        setError('Gagal mengambil data itinerary.');
      } finally {
        setLoading(false);
      }
    };
    fetchItineraries();
  }, []);

  if (!localStorage.getItem('access_token')) {
    return null;
  }

  return (
    <div className="profile-itinerary-page">
      <h2>🗺️ Itinerary Saya</h2>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && !error && (
        <div>
          {itineraries.length === 0 ? (
            <p>Belum ada itinerary yang disimpan.</p>
          ) : (
            <ul>
              {itineraries.map((it, idx) => (
                <li key={it.id || idx} style={{marginBottom: '1em'}}>
                  <strong>{it.title}</strong> ({it.start_date} - {it.end_date})<br />
                  <span>{it.description}</span>
                  <ul>
                    {it.days && it.days.map((day, i) => (
                      <li key={i}>
                        <strong>Hari {day.day_number} ({day.date})</strong>
                        <ul>
                          {day.items && day.items.map((item, j) => (
                            <li key={j}>{item.title} - {item.location}</li>
                          ))}
                        </ul>
                      </li>
                    ))}
                  </ul>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default ProfileItinerary;
