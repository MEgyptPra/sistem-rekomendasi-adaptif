# 🤖 ML Integration Documentation - Frontend

## ✅ COMPLETED: ML Model Integration

Semua rekomendasi di frontend sekarang menggunakan **Machine Learning Models** yang telah di-train!

---

## 📍 Integration Points

### 1. **"Kejutkan Saya" Button (Surprise Modal)**
**File:** `frontend/src/components/SurpriseModal.jsx`

#### ✅ Sebelum:
```javascript
// ❌ Random shuffle dari database
const shuffled = allDest.sort(() => 0.5 - Math.random());
```

#### ✅ Sesudah:
```javascript
// ✅ ML Model dengan smart algorithm selection
algorithm: 'auto'  // Hybrid jika trained, Incremental jika belum
```

**Behavior:**
- **User logged-in** → Personalized (Hybrid CF+CB + MAB)
- **Anonymous user** → Incremental (Context-aware: weather, traffic, trending)
- **Fallback** → Random (jika API gagal)

---

### 2. **Home Page Recommendations**
**File:** `frontend/src/pages/Home.jsx`

#### ✅ Sebelum:
```javascript
// ❌ Anonymous: langsung skip API, pakai random
console.log('Anonymous user: Using random destinations');
await loadFallbackDestinations(); // Random
```

#### ✅ Sesudah:
```javascript
// ✅ Anonymous: Gunakan Incremental Learning (context-aware)
await loadIncrementalRecommendations();
// - Weather-aware (sunny/rainy/cloudy)
// - Time-aware (morning/afternoon/evening/night)
// - Traffic-aware (congestion levels)
// - Trending destinations (popular clicks/views)
```

**Algorithm Flow:**
1. **Logged-in User:**
   - Try: `algorithm='auto'` (ML Model - Hybrid/MAB)
   - Fallback: `algorithm='incremental'` (Context-aware)
   - Last resort: Random

2. **Anonymous User:**
   - Direct: `algorithm='incremental'` (Context-aware tanpa personalization)
   - Fallback: Random

---

### 3. **Planning Page (NEW!)**
**File:** `frontend/src/pages/Planning.jsx`

#### ✅ Sebelum:
```javascript
// ❌ Static form tanpa ML integration
// User submit → Tidak ada action
```

#### ✅ Sesudah:
```javascript
// ✅ ML-powered itinerary generator
const response = await recommendationsAPI.getPersonalized({
  algorithm: 'auto',
  num_recommendations: 10,
  filters: {
    regions: selectedRegions,
    categories: selectedInterests,
    start_date: startDate,
    end_date: endDate
  }
});
```

**Features:**
- User pilih **tanggal**, **wilayah**, **minat**
- Klik **"Buat Itinerary dengan AI"**
- Backend ML model generate recommendations
- Display hasil dalam grid dengan `DestinationCard`
- Show algorithm yang digunakan di console

---

## 🔄 Algorithm Selection Strategy

### `algorithm: 'auto'` (Smart Selection)
Backend akan otomatis pilih algorithm terbaik:

```python
if user.has_preferences and collaborative_model.is_trained:
    return "hybrid"  # CF + CB dengan MAB optimization
elif incremental_learner.has_data:
    return "incremental"  # Context-aware + Trending
else:
    return "random_fallback"
```

### `algorithm: 'incremental'`
Langsung gunakan Incremental Learning:
- ✅ Tidak perlu model training
- ✅ Real-time context awareness
- ✅ Trending destinations (views, clicks, ratings)
- ✅ Weather/Traffic/Time-of-day aware

### `algorithm: 'hybrid'`
Force menggunakan Hybrid Model (CF+CB):
- ⚠️ Butuh model trained
- ✅ Personalized based on user history
- ✅ MAB untuk lambda optimization
- ✅ MMR untuk diversity

### `algorithm: 'mab'`
Full context-aware dengan MAB:
- ✅ Hybrid + MAB lambda selection
- ✅ Real-time context (weather, traffic, time, season)
- ✅ Personalized + Context fusion

---

## 📊 ML Model Status

### Check Model Status:
```bash
cd backend
python train_models_once.py
```

### Server Startup:
```
✅ Content-Based model loaded (trained at: 2025-11-06...)
✅ Collaborative model loaded (trained at: 2025-11-06...)
✅ Hybrid model loaded (trained at: 2025-11-06...)
```

### API Response Metadata:
```json
{
  "recommendations": [...],
  "metadata": {
    "algorithm_used": "hybrid",
    "lambda_value": 0.7,
    "context": {
      "weather": "sunny",
      "traffic": "low",
      "time_of_day": "morning"
    }
  }
}
```

---

## 🧪 Testing

### 1. Test "Kejutkan Saya"
1. Buka Home page
2. Klik **"Kejutkan Saya"**
3. Check Console:
   ```
   ✅ ML Recommendations loaded: hybrid
   atau
   ✅ Incremental Recommendations loaded (context-aware)
   ```

### 2. Test Home Recommendations
1. Login sebagai user
2. Refresh Home page
3. Check Console:
   ```
   ✅ ML Model used: hybrid
   ```
4. Logout
5. Refresh Home page
6. Check Console:
   ```
   Anonymous user: Using context-aware incremental learning
   ✅ Incremental learning loaded (context + trending)
   ```

### 3. Test Planning Page
1. Go to `/planning`
2. Pilih tanggal, wilayah, minat
3. Klik **"Buat Itinerary dengan AI"**
4. Check Console:
   ```
   ✅ ML-based itinerary generated: {
     algorithm: "hybrid",
     count: 10
   }
   ```

---

## 🎯 Benefits

### User Perspective:
✅ **Personalized** recommendations based on preferences & history  
✅ **Context-aware** recommendations (weather, traffic, time)  
✅ **Diverse** results (MMR diversification)  
✅ **Smart** algorithm selection (auto fallback)  
✅ **Real-time** learning (incremental updates)

### Technical Perspective:
✅ **Model persistence** (no retraining on restart)  
✅ **Graceful degradation** (fallback chain)  
✅ **Algorithm transparency** (metadata in response)  
✅ **Incremental learning** (no training required)  
✅ **Context integration** (weather, traffic, time, season)

---

## 🔧 Configuration

### Backend API Endpoint:
```
POST /api/recommendations/personalized
Body: {
  "algorithm": "auto" | "incremental" | "hybrid" | "mab",
  "num_recommendations": 5-20,
  "filters": {
    "regions": ["Jatinangor", "Tanjungsari"],
    "categories": ["Wisata Alam", "Kuliner"],
    "start_date": "2025-11-10",
    "end_date": "2025-11-15"
  }
}
```

### Frontend API Call:
```javascript
import { recommendationsAPI } from '../services/api';

const response = await recommendationsAPI.getPersonalized({
  algorithm: 'auto',
  num_recommendations: 6
});

console.log(response.data.metadata.algorithm_used);
```

---

## 📈 Next Steps (Optional)

1. **A/B Testing**: Test different algorithms untuk user segments
2. **Analytics**: Track conversion rate per algorithm
3. **Feedback Loop**: User ratings → Auto-retrain models
4. **Performance**: Cache recommendations untuk speed
5. **Advanced Filters**: Price range, accessibility, family-friendly

---

## 🎉 Summary

**Semua frontend recommendations sekarang powered by ML!**

✅ Surprise Modal → ML Model  
✅ Home Page → ML Model  
✅ Planning Page → ML Model  
✅ Incremental Learning → Always available  
✅ Graceful Fallbacks → Never fails  

**No more random shuffles!** 🚀
