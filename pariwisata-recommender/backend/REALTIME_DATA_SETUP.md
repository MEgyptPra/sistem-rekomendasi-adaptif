# Real-Time Data Configuration

## API Keys Setup

Ganti API keys berikut dengan milik Anda:

### 1. Weather Data (OpenWeatherMap)
- **Website**: https://openweathermap.org/api
- **Free Tier**: 1,000 calls/day, 60 calls/minute
- **Get API Key**: https://home.openweathermap.org/api_keys

```env
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
```

### 2. Traffic Data (Google Maps) - OPTIONAL
- **Website**: https://developers.google.com/maps/documentation
- **Free Tier**: $200 credit/month (~40,000 requests)
- **Get API Key**: https://console.cloud.google.com/

```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### 3. Traffic Data Alternative (TomTom) - OPTIONAL
- **Website**: https://developer.tomtom.com/
- **Free Tier**: 2,500 requests/day
- **Get API Key**: https://developer.tomtom.com/user/register

```env
TOMTOM_API_KEY=your_tomtom_api_key_here
```

---

## Configuration in .env

Add to your `.env` file:

```env
# Real-Time Data APIs
OPENWEATHER_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here  # Optional
TOMTOM_API_KEY=your_key_here       # Optional

# Cache Settings
REALTIME_CACHE_DURATION=300  # 5 minutes in seconds
WEATHER_CACHE_DURATION=1800  # 30 minutes (weather changes slowly)

# Location Settings (Sumedang, Indonesia)
DEFAULT_LATITUDE=-6.8568
DEFAULT_LONGITUDE=107.9214
```

---

## Usage

### Automatic Mode (Recommended)
Service will automatically:
1. Try to fetch from real API
2. If API fails → Use cached data
3. If cache expired → Use simulated data
4. Cache successful API responses

### Manual Testing
```bash
# Test weather API
curl "http://localhost:8000/api/ml/context"

# Check cache status
curl "http://localhost:8000/api/ml/context/status"
```

---

## Rate Limits

### OpenWeatherMap (Free)
- ✅ 1,000 calls/day
- ✅ 60 calls/minute
- ✅ Cukup untuk: 1 call/5 min = 288 calls/day

### Google Maps (Free Tier)
- ✅ $200 credit/month
- ✅ ~40,000 requests
- ✅ Cukup untuk: ~1,300 requests/day

### Our Caching Strategy
- Weather: Cache 30 minutes (slow changing)
- Traffic: Cache 5 minutes (fast changing)
- **Daily API calls**: ~48 weather + 288 traffic = 336 total
- **Well within limits!** ✅

---

## Cost Estimation

### Free Tier (Recommended for development)
- OpenWeatherMap: FREE (1k calls/day)
- Google Maps: FREE ($200 credit = 40k requests)
- **Total Cost**: $0/month ✅

### Production Scale (10,000 users/day)
- Weather API: $0 (cached effectively)
- Traffic API: $50-100/month
- **Total Cost**: ~$100/month

---

## Fallback Strategy

```
API Request
    ↓
┌─────────────────────┐
│ Try Real API        │
└─────────────────────┘
    ↓
    ├─→ Success? → Cache & Return ✅
    ├─→ Failed?  → Check Cache
    │               ↓
    │               ├─→ Cache Valid? → Return ✅
    │               └─→ Cache Expired? → Simulated Data ⚠️
    └─→ No API Key? → Simulated Data ⚠️
```

**You'll never get errors - always have data!** 🚀
