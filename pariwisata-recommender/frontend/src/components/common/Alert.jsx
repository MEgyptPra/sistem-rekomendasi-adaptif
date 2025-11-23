import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios'; 

// Mengambil URL dari environment (sesuaikan jika berbeda di setup Anda)
const API_BASE_URL = 'http://localhost:8000/api'; 
const API = axios.create({ baseURL: API_BASE_URL });

const ContextualAlert = () => {
    const [alertData, setAlertData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchContext = async () => {
        setLoading(true);
        setAlertData(null);
        try {
            // Memanggil endpoint context dari backend
            const res = await API.get('/ml/context'); 
            const context = res.data.context;

            // --- Logika Kontekstual Sumedang ---
            let data = null;

            // 1. Peringatan Hujan Lebat (Risiko Longsor/Banjir)
            if (context.weather === 'hujan_lebat' || context.weather === 'thunderstorm') {
                data = {
                    type: 'danger', 
                    title: '⚠️ Peringatan Cuaca Ekstrem',
                    message: 'Hujan lebat di wilayah pegunungan (misal: Cadas Pangeran/Tampomas). Waspada potensi longsor dan genangan air. Tunda wisata alam terbuka.',
                    link: '/plan-your-trip#alerts'
                };
            } 
            // 2. Peringatan Kepadatan Tinggi (Libur Nasional/Lebaran)
            else if (context.holiday_type || context.day_type === 'libur_lebaran') {
                 data = {
                    type: 'warning',
                    title: '🚨 Kepadatan Arus Wisata & Liburan',
                    message: 'Terjadi peningkatan volume kendaraan di jalur utama. Rencanakan waktu perjalanan di luar jam sibuk untuk menghindari macet.',
                    link: '/plan-your-trip#alerts'
                };
            }
            // 3. Peringatan Musim Panas/Kering
            else if (context.season === 'kemarau' && context.temperature > 30) {
                 data = {
                    type: 'info',
                    title: '☀️ Cuaca Kering dan Panas',
                    message: 'Jaga hidrasi dan hindari aktivitas berat pukul 11:00-14:00. Waspada risiko kebakaran lahan di area perbukitan.',
                    link: null
                };
            }
            // 4. Kondisi Lalu Lintas Padat (Non-Liburan)
            else if (context.traffic === 'macet' || context.traffic === 'padat') {
                 data = {
                    type: 'warning',
                    title: '🚗 Info Lalu Lintas',
                    message: `Jalur utama terpantau ${context.traffic} (Kecepatan ~${context.traffic_speed} km/jam). Rencanakan waktu keberangkatan Anda.`,
                    link: null
                };
            }
            // 5. Kondisi Normal
            else {
                 data = {
                    type: 'success', 
                    title: 'Kondisi Normal',
                    message: 'Kondisi cuaca dan lalu lintas saat ini terpantau aman dan lancar. Selamat berlibur!',
                    link: null
                };
            }

            // Hanya tampilkan jika itu bukan success/normal
            if (data.type === 'success') {
                setAlertData(null); 
            } else {
                setAlertData(data);
            }

        } catch (err) {
            console.error("Failed to fetch context for alert:", err);
            // Fallback error jika backend mati
            setAlertData({
                type: 'error',
                title: '❌ Gagal Memuat Data Konteks',
                message: 'Tidak dapat memuat informasi cuaca dan lalu lintas saat ini. Pastikan backend berjalan.',
                link: null
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchContext();
        // Refresh context setiap 10 menit
        const interval = setInterval(fetchContext, 600000); 
        return () => clearInterval(interval);
    }, []);

    if (loading || !alertData) {
        return null;
    }

    const { type, title, message, link } = alertData;
    const badgeMap = {
        danger: '🔴 BAHAYA',
        warning: '⚠️ PERINGATAN',
        info: 'ℹ️ INFORMASI',
        error: '❌ KESALAHAN'
    };

    // Struktur JSX Alert
    return (
        <div className={`contextual-alert alert-box alert-${type}`}>
            <div className="alert-content">
                <span className="alert-badge">{badgeMap[type]}</span>
                <h4 className="alert-title">{title}</h4>
                <p className="alert-message">{message}</p>
            </div>
            {link && (
                <Link to={link} className="alert-link">
                    Lihat Detail →
                </Link>
            )}
        </div>
    );
};

export default ContextualAlert;