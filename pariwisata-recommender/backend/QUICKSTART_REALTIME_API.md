# 🌍 Real-Time Data Integration - Quick Start Guide

## 📋 What You Need

### 1. **OpenWeatherMap API** (Required for Weather)
- **Cost**: FREE
- **Limit**: 1,000 calls/day (more than enough!)
- **Sign up**: https://home.openweathermap.org/users/sign_up

### 2. **Google Maps API** (Optional for Traffic)
- **Cost**: FREE tier ($200 credit/month)
- **Limit**: ~40,000 requests/month
- **Sign up**: https://console.cloud.google.com/

### 3. **TomTom API** (Alternative for Traffic)
- **Cost**: FREE
- **Limit**: 2,500 requests/day
- **Sign up**: https://developer.tomtom.com/user/register

---

## 🚀 Setup Steps

### Step 1: Get API Keys

#### OpenWeatherMap (Weather Data):
1. Go to https://home.openweathermap.org/users/sign_up
2. Create free account
3. Go to https://home.openweathermap.org/api_keys
4. Copy your API key

#### Google Maps (Traffic Data - Optional):
1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable "Distance Matrix API"
4. Go to "Credentials" → Create API key
5. Copy your API key

---

### Step 2: Install Dependencies

```bash
cd backend
pip install aiohttp requests
```

---

### Step 3: Configure .env

Create or edit `.env` file:

```env
# Weather API (Required)
OPENWEATHER_API_KEY=paste_your_key_here

# Traffic API (Optional - choose one)
GOOGLE_MAPS_API_KEY=paste_your_key_here
# OR
TOMTOM_API_KEY=paste_your_key_here

# Cache Settings (Optional)
WEATHER_CACHE_DURATION=1800  # 30 minutes
REALTIME_CACHE_DURATION=300  # 5 minutes

# Location (Sumedang, Indonesia - Default)
DEFAULT_LATITUDE=-6.8568
DEFAULT_LONGITUDE=107.9214
```

---

### Step 4: Test Configuration

```bash
python check_realtime_api.py
```

Expected output:
```
✅ Configuration checked
✅ Context retrieved successfully
🎉 All data is from real APIs!
```

---

### Step 5: Start Server

```bash
python -m uvicorn main:app --reload
```

Check logs for:
```
🌍 Using PRODUCTION Real-Time Data Service (Real APIs)
```

---

## 🧪 Testing

### Test from Command Line:

```bash
# Check context service status
curl http://localhost:8000/api/ml/context/status

# Get current context
curl http://localhost:8000/api/ml/context
```

### Expected Response (Production Mode):

```json
{
  "status": "success",
  "context": {
    "weather": "cerah",
    "temperature": 28.5,
    "humidity": 75,
    "traffic": "sedang",
    "traffic_speed": 35,
    "data_source": {
      "weather": "openweathermap_api",
      "traffic": "google_maps_api"
    }
  },
  "mode": "production"
}
```

### Expected Response (Simulation Mode):

```json
{
  "context": {
    "weather": "berawan",
    "data_source": {
      "weather": "simulation",
      "traffic": "simulation"
    }
  },
  "mode": "simulation"
}
```

---

## 📊 How It Works

### Fallback Chain:

```
Request Context
    ↓
Try Real API
    ↓ (if configured)
    ├─→ Success? → Cache & Return ✅
    ├─→ Failed?  → Check Cache
    │               ↓
    │               ├─→ Valid? → Return Cached ✅
    │               └─→ Expired? → Simulation ⚠️
    └─→ No API Key? → Simulation ⚠️
```

### Caching Strategy:

- **Weather**: Cached for 30 minutes (slow changing)
- **Traffic**: Cached for 5 minutes (fast changing)
- **Benefits**:
  - Reduces API calls
  - Faster responses
  - Works offline (if cache valid)
  - Never exceeds rate limits

---

## 💰 Cost Analysis

### Our Usage Pattern:
- Weather: 1 call per 30 min = 48 calls/day
- Traffic: 1 call per 5 min = 288 calls/day
- **Total**: ~336 calls/day

### vs API Limits:
- OpenWeather: 1,000/day → **33% usage** ✅
- Google Maps: 40,000/month → **~1% usage** ✅

**Conclusion**: Well within FREE tier limits! 🎉

---

## 🔧 Troubleshooting

### Problem: "Using simulation" despite having API key

**Solution**:
1. Check .env file has correct key (no spaces, quotes)
2. Restart server after changing .env
3. Run `python check_realtime_api.py` to debug

### Problem: API call failed

**Solution**:
1. Check internet connection
2. Verify API key is valid (not expired)
3. Check API rate limits
4. System will automatically use cache or simulation

### Problem: High latency

**Solution**:
1. Cache is working (check logs for "Using cached")
2. Increase cache duration in .env
3. Use simulation mode for development

---

## 🎯 Production Checklist

Before going to production:

- [ ] Get valid OpenWeatherMap API key
- [ ] (Optional) Get Google Maps or TomTom API key
- [ ] Add keys to .env (never commit .env!)
- [ ] Test with `check_realtime_api.py`
- [ ] Verify "production" mode in logs
- [ ] Monitor API usage in provider dashboards
- [ ] Set up alerts for rate limit warnings

---

## 📈 Next Steps

### Optional Enhancements:

1. **Add more locations**: Support multiple cities
2. **Historical data**: Store context history for analysis
3. **Predictive caching**: Pre-fetch during low traffic
4. **Monitoring**: Track API success rates
5. **Alerts**: Notify when fallback to simulation

---

## ✅ Summary

**What you get**:
- ✅ Real weather data from OpenWeatherMap
- ✅ Real traffic data from Google Maps/TomTom
- ✅ Smart caching (never exceed limits)
- ✅ Automatic fallbacks (never fails)
- ✅ Context-aware recommendations
- ✅ FREE tier compatible

**You're ready to go!** 🚀

Just add your API keys and the system will automatically switch to production mode!
