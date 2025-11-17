# 🧠 CONTEXT-AWARE COMPONENTS - SISTEM REKOMENDASI ADAPTIF

## ✅ STATUS KOMPONEN LENGKAP

Sistem rekomendasi adaptif ini menggunakan **4 KOMPONEN CONTEXT-AWARE** untuk memberikan rekomendasi yang disesuaikan dengan kondisi real-time:

---

## 1. ✅ CUACA (Weather Context)

### Data yang Dikumpulkan:
- **`weather`**: Kondisi cuaca saat ini
  - Nilai: `cerah`, `berawan`, `hujan_ringan`, `hujan_lebat`
  - Disesuaikan dengan iklim tropis Indonesia (2 musim: Kemarau & Hujan)

- **`temperature_category`**: Kategori suhu
  - Nilai: `sejuk`, `hangat`, `panas`
  - Range suhu Indonesia: 26-30°C sepanjang tahun

- **`humidity_level`**: Level kelembaban
  - Nilai: `sedang`, `tinggi`, `sangat_tinggi`
  - Kelembaban Indonesia: 65-90% sepanjang tahun

### Implementasi:
- **Production Mode**: OpenWeatherMap API
  - API Endpoint: `https://api.openweathermap.org/data/2.5/weather`
  - Caching: 30 menit
  - Lokasi: Yogyakarta, Indonesia (lat: -7.7956, lon: 110.3695)

- **Simulation Mode**: Algoritma probabilistik berdasarkan musim
  - Musim Kemarau (Mei-Oktober): 70% cerah, 25% berawan, 5% hujan
  - Musim Hujan (Nov-April): 30% hujan_lebat, 40% hujan_ringan

### Penggunaan dalam Rekomendasi:
- ☀️ Cuaca **cerah** → Boost untuk destinasi outdoor (pantai, gunung, taman)
- 🌧️ Cuaca **hujan** → Boost untuk destinasi indoor (museum, mall, kuliner)
- 🌡️ Suhu **panas** → Prioritas tempat teduh atau air terjun
- 💧 Kelembaban **tinggi** → Rekomendasi tempat ber-AC

---

## 2. ✅ PENANGGALAN/TEMPORAL (Calendar/Time Context)

### Data yang Dikumpulkan:
- **`is_weekend`**: Apakah hari weekend (Sabtu/Minggu)
  - Nilai: `true` / `false`

- **`day_of_week`**: Nama hari dalam bahasa Indonesia
  - Nilai: `senin`, `selasa`, `rabu`, `kamis`, `jumat`, `sabtu`, `minggu`

- **`hour_of_day`**: Jam saat ini (0-23)
  - Format: Integer

- **`time_period`**: Periode waktu dalam hari
  - Nilai: `pagi` (05:00-09:59), `siang` (10:00-14:59), `sore` (15:00-17:59), `malam` (18:00-20:59), `malam_larut` (21:00-04:59)

- **`season`**: Musim Indonesia
  - Nilai: `kemarau` (Mei-Oktober), `hujan` (November-April)

- **`month`**: Bulan dalam tahun (1-12)

- **`date`**: Tanggal dalam bulan (1-31)

- **`is_holiday_season`**: Musim liburan/hari libur
  - Juni-Juli (liburan sekolah), Desember, Awal Januari, Weekend

### Penggunaan dalam Rekomendasi:
- 🌅 **Pagi**: Prioritas tempat sarapan, pasar tradisional, sunrise spots
- 🌞 **Siang**: Destinasi utama (wisata alam, budaya, adventure)
- 🌇 **Sore**: Sunset spots, café, taman kota
- 🌙 **Malam**: Kuliner malam, night market, hiburan malam
- 📅 **Weekend**: Boost popularitas, antisipasi keramaian
- 🏖️ **Holiday Season**: Prioritas destinasi premium, akomodasi yang perlu booking

---

## 3. ✅ TRAFFIC (Lalu Lintas)

### Data yang Dikumpulkan:
- **`traffic`**: Kondisi lalu lintas saat ini
  - Nilai: `lancar`, `sedang`, `padat`, `macet`

### Implementasi:
- **Production Mode**: Google Maps Distance Matrix API / TomTom Traffic API
  - Google Maps: `https://maps.googleapis.com/maps/api/distancematrix/json`
  - TomTom: `https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json`
  - Caching: 5 menit
  - Area monitoring: Rute utama Yogyakarta

- **Simulation Mode**: Algoritma berbasis jam sibuk
  - Jam Sibuk (07:00-09:00, 16:00-19:00): 20% macet, 40% padat
  - Jam Normal: 60% lancar, 30% sedang

### Penggunaan dalam Rekomendasi:
- 🚗 **Lancar**: Rekomendasi destinasi jarak jauh, luar kota
- 🚦 **Sedang**: Destinasi dalam kota, fleksibel
- 🚥 **Padat/Macet**: Prioritas destinasi dekat, atau adjust departure time
- 📍 Integrated dengan Google Maps untuk estimasi waktu tempuh

---

## 4. ✅ SOCIAL TRENDS (Tren Viral/Trending)

### Data yang Dikumpulkan:
- **`social_trend`**: Tren keseluruhan saat ini
  - Nilai: `normal`, `trending`, `viral`

- **`trending_destinations`**: Array destinasi yang sedang trending
  - Format: `[{destination_id, name, score, views_24h}, ...]`
  - Kriteria: 50-100 views dalam 24 jam terakhir

- **`viral_destinations`**: Array destinasi yang viral
  - Format: `[{destination_id, name, score, views_24h}, ...]`
  - Kriteria: 100+ views dalam 24 jam terakhir

### Implementasi:
- **Service**: `SocialTrendService` (app/services/social_trend_service.py)
- **Data Source**: Incremental Learner cache (`data/cache/destination_scores.json`)
- **Caching**: 5 menit
- **Scoring Algorithm**:
  ```python
  base_score = (views * 1.0) + (clicks * 2.0) + (ratings * 3.0) + (favorites * 5.0)
  
  # Recency boost (24 jam terakhir)
  if hours_since_activity < 24:
      recency_multiplier = 1.0 + (1.0 - hours_since_activity / 24.0)
      final_score = base_score * recency_multiplier
  ```

### Analisis Real-Time:
- 📊 Tracks: Views, Clicks, Ratings, Favorites
- ⏱️ Recency Boost: Aktivitas dalam 24 jam mendapat multiplier hingga 2x
- 🔥 Viral Detection: Otomatis mendeteksi destinasi dengan aktivitas tinggi
- 📈 Trending Score: Menggabungkan engagement metrics dengan time decay

### Penggunaan dalam Rekomendasi:
- 🔥 **Viral**: Boost recommendation score 2x (priority tinggi)
- 📈 **Trending**: Boost recommendation score 1.5x (priority menengah)
- 📊 **Normal**: Boost 1x (tidak ada pengaruh)
- 🎯 Membantu cold-start problem dengan menampilkan destinasi populer
- 🌟 "Wisata Trending Minggu Ini" section di homepage

---

## 📊 INTEGRASI DALAM SISTEM

### Architecture Flow:
```
1. User Request → FastAPI Endpoint
2. ML Service → RealTimeContextService.get_current_context()
3. Context Service → Collects all 4 components:
   ├─ Weather Service (OpenWeatherMap / Simulation)
   ├─ Traffic Service (Google Maps / Simulation)
   ├─ Time/Calendar (datetime built-in)
   └─ Social Trend Service (Incremental Learner data)
4. Context → Passed to ML Algorithms:
   ├─ Content-Based Filtering (TF-IDF with context weights)
   ├─ Collaborative Filtering (NMF with context adjustment)
   ├─ Hybrid Recommender (MAB optimization with context)
   └─ Incremental Learner (Real-time learning with context)
5. Recommendations → Ranked with context-aware scoring
6. Final Results → Returned to Frontend
```

### Context-Aware Scoring Example:
```python
final_score = base_ml_score * context_multipliers

context_multipliers = {
    'weather_match': 1.2 if weather_compatible else 0.8,
    'time_match': 1.3 if time_period_optimal else 1.0,
    'traffic_penalty': 0.7 if traffic == 'macet' else 1.0,
    'social_boost': 2.0 if viral else (1.5 if trending else 1.0)
}
```

---

## 🔧 KONFIGURASI & TESTING

### Environment Variables (.env):
```bash
# Weather API
OPENWEATHER_API_KEY=your_openweathermap_api_key_here

# Traffic API (Choose one)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
TOMTOM_API_KEY=your_tomtom_api_key_here

# Default location (Yogyakarta)
DEFAULT_LATITUDE=-7.7956
DEFAULT_LONGITUDE=110.3695
```

### Testing Tools:
1. **`check_realtime_api.py`** - Test API configuration
   ```bash
   cd backend
   python check_realtime_api.py
   ```

2. **API Endpoints**:
   - `GET /api/ml/context` - Get current context
   - `GET /api/ml/context/status` - Check service status

### Mode Switching:
- **Automatic**: System detects API keys and switches mode
  - Keys present → Production Mode (real APIs)
  - Keys missing → Simulation Mode (fallback)

- **Manual Override** (optional): Set in `ml_service.py`
  ```python
  USE_PRODUCTION_API = bool(os.getenv("OPENWEATHER_API_KEY")) and False  # Force simulation
  ```

---

## 📈 PERFORMANCE & OPTIMIZATION

### Caching Strategy:
- ✅ Weather: 30 minutes (API quota: 1,000 calls/day)
- ✅ Traffic: 5 minutes (high volatility)
- ✅ Social Trends: 5 minutes (real-time updates needed)
- ✅ Prevents rate limiting: 336 calls/day vs 1,000 limit (safe margin)

### Fallback Mechanism:
```
1. Try Real API → Success? Return
2. Check Cache → Fresh? Return
3. Use Simulation → Always works
```

### Daily API Usage Estimate:
- Weather: 48 calls/day (every 30 min)
- Traffic: 288 calls/day (every 5 min)
- **Total**: 336 calls/day (within free tier limits)

---

## ✅ VERIFICATION CHECKLIST

- [x] **Cuaca (Weather)**: Implemented with OpenWeatherMap + Simulation
- [x] **Penanggalan (Calendar/Temporal)**: Full temporal context (hour, day, season)
- [x] **Traffic (Lalu Lintas)**: Google Maps API + TomTom fallback
- [x] **Trend/Viral (Social Trends)**: SocialTrendService with real-time analytics

### Files Involved:
1. `app/services/real_time_data_production.py` - Production service
2. `app/services/real_time_data.py` - Simulation service
3. `app/services/social_trend_service.py` - Social trend analyzer
4. `app/services/ml_service.py` - ML orchestrator
5. `check_realtime_api.py` - Testing tool

---

## 🚀 NEXT STEPS

1. **Add API Keys** to `.env` file:
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit and add your keys
   nano .env  # or use text editor
   ```

2. **Test Production Mode**:
   ```bash
   python check_realtime_api.py
   ```

3. **Restart Backend**:
   ```bash
   cd pariwisata-recommender
   ./start_all.bat
   ```

4. **Monitor Logs**:
   - Production mode: "🌍 CONTEXT GENERATED (Indonesia) - PRODUCTION MODE"
   - Simulation mode: "🌍 CONTEXT GENERATED (Indonesia) - SIMULATION MODE"

---

## 📞 SUPPORT

Jika ada pertanyaan atau masalah:
1. Check logs: Backend terminal output
2. Test APIs: `python check_realtime_api.py`
3. Verify config: Check `.env` file

**Status**: ✅ ALL 4 CONTEXT-AWARE COMPONENTS IMPLEMENTED & READY
