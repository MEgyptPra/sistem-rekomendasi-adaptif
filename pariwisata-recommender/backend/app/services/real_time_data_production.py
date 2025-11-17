"""
Real-Time Context Service - PRODUCTION VERSION WITH REAL APIs
Mengambil data real-time dari API eksternal (Weather, Traffic, Social Trends)
dengan caching dan fallback strategy
"""

import os
from app.models.realtime_api_config import RealtimeAPIConfig
from app.core.db import AsyncSessionLocal
from sqlalchemy.future import select
import json
import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path
from app.services.social_trend_service import SocialTrendService

class RealTimeContextService:
    """
    Production-ready Real-Time Data Service
    - Fetches from real APIs (OpenWeatherMap, Google Maps, TomTom)
    - Caches responses to avoid rate limits
    - Falls back to simulation if API fails
    """
    
    # API Configuration (will be loaded from DB)
    _api_config_cache = None
    _api_config_cache_time = None
    _api_config_cache_duration = 300  # seconds
    
    # Default location: Sumedang, Indonesia
    DEFAULT_LAT = float(os.getenv("DEFAULT_LATITUDE", "-6.8568"))
    DEFAULT_LON = float(os.getenv("DEFAULT_LONGITUDE", "107.9214"))
    
    # Cache settings
    CACHE_DIR = Path("data/cache")
    WEATHER_CACHE_FILE = CACHE_DIR / "weather_cache.json"
    TRAFFIC_CACHE_FILE = CACHE_DIR / "traffic_cache.json"
    
    WEATHER_CACHE_DURATION = int(os.getenv("WEATHER_CACHE_DURATION", "1800"))  # 30 min
    TRAFFIC_CACHE_DURATION = int(os.getenv("REALTIME_CACHE_DURATION", "300"))  # 5 min
    
    async def _load_api_config(self):
        """Load API config from DB, cache for short period"""
        now = datetime.now()
        if self._api_config_cache and self._api_config_cache_time:
            age = (now - self._api_config_cache_time).total_seconds()
            if age < self._api_config_cache_duration:
                return self._api_config_cache
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RealtimeAPIConfig).where(RealtimeAPIConfig.status == "active"))
            configs = result.scalars().all()
            config_dict = {c.source_name: c for c in configs}
            self._api_config_cache = config_dict
            self._api_config_cache_time = now
            return config_dict

    async def get_api_key(self, source_name):
        configs = await self._load_api_config()
        config = configs.get(source_name)
        return config.api_key if config else None

    async def get_api_url(self, source_name):
        configs = await self._load_api_config()
        config = configs.get(source_name)
        return config.api_url if config else None

    def __init__(self):
        # Create cache directory
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Indonesia seasons
        self.kemarau_months = [5, 6, 7, 8, 9, 10]  # Mei - Oktober
        self.hujan_months = [11, 12, 1, 2, 3, 4]    # November - April
        
        # Initialize Social Trend Service
        self.trend_service = SocialTrendService()
        
        print(f"🌍 RealTimeContextService initialized (DB-driven API config)")

    async def get_current_context(self, lat: Optional[float] = None, lon: Optional[float] = None) -> Dict[str, Any]:
        """
        Get current real-time context
        Priority: Real API → Cache → Simulation
        """
        lat = lat or self.DEFAULT_LAT
        lon = lon or self.DEFAULT_LON
        now = datetime.now()
        
        # 1. Get Weather (real or cached or simulated)
        weather_data = await self._get_weather(lat, lon)

        # 2. Get Traffic (real or cached or simulated)
        traffic_data = await self._get_traffic(lat, lon)

        # 3. Get Social Trends (from user interactions)
        trend_data = self.trend_service.get_trending_status()

        # 4. Get Calendar/Holiday info (API Kalender Indonesia)
        calendar_data = await self._get_calendar_info(now)

        # 5. Build context
        current_season = self._get_season(now.month)
        
        context = {
            # Weather context
            "weather": weather_data["condition"],
            "weather_description": weather_data.get("description", ""),
            "temperature": weather_data.get("temperature", 28),
            "humidity": weather_data.get("humidity", 75),

            # Traffic context
            "traffic": traffic_data["condition"],
            "traffic_speed": traffic_data.get("speed", 40),

            # Temporal context (penanggalan)
            "is_weekend": now.weekday() >= 5,
            "day_of_week": now.strftime("%A"),
            "hour_of_day": now.hour,
            "time_period": self._get_time_period(now.hour),
            "season": current_season,
            "month": now.month,
            "date": now.date().isoformat(),

            # Calendar/Holiday info (dinamis dari API)
            "is_holiday": calendar_data.get("is_holiday", False),
            "holiday_name": calendar_data.get("holiday_name", None),
            "holiday_type": calendar_data.get("holiday_type", None),

            # Social trend context
            "social_trend": trend_data["overall_trend"],
            "trending_destinations": trend_data["trending_destinations"][:5],  # Top 5
            "viral_destinations": trend_data["viral_destinations"][:3],  # Top 3

            # Metadata
            "data_source": {
                "weather": weather_data["source"],
                "traffic": traffic_data["source"],
                "calendar": calendar_data.get("source", "calendar_api"),
                "social_trend": "user_interactions"
            },
            "timestamp": now.isoformat()
        }
        
        print(f"🌍 Context Generated: {context['weather']} weather, {context['traffic']} traffic, {context['social_trend']} trend, holiday: {context['is_holiday']} {context['holiday_name']}")
        async def _get_calendar_info(self, now: datetime) -> Dict[str, Any]:
            """
            Ambil info libur nasional/cuti bersama dari API Kalender Indonesia
            Contoh API: https://api-harilibur.vercel.app/api
            Endpoint dan API key diambil dari config 'calendar' di database
            """
            api_url = await self.get_api_url("calendar")
            api_key = await self.get_api_key("calendar")
            if not api_url:
                return {"is_holiday": False, "source": "calendar_api"}
            date_str = now.strftime("%Y-%m-%d")
            url = f"{api_url}?date={date_str}"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Contoh response: {"is_holiday": true, "holiday_name": "Hari Pahlawan", "holiday_type": "Nasional"}
                            return {
                                "is_holiday": data.get("is_holiday", False),
                                "holiday_name": data.get("holiday_name"),
                                "holiday_type": data.get("holiday_type"),
                                "source": "calendar_api"
                            }
            except Exception as e:
                print(f"⚠️ Calendar API failed: {e}")
            return {"is_holiday": False, "source": "calendar_api"}
            async def _get_calendar_info(self, now: datetime) -> Dict[str, Any]:
                """
                Ambil info libur nasional/cuti bersama dari API Kalender Indonesia
                Contoh API: https://api-harilibur.vercel.app/api
                Endpoint dan API key diambil dari config 'calendar' di database
                """
                api_url = await self.get_api_url("calendar")
                api_key = await self.get_api_key("calendar")
                if not api_url:
                    return {"is_holiday": False, "source": "calendar_api"}
                date_str = now.strftime("%Y-%m-%d")
                url = f"{api_url}?date={date_str}"
                headers = {}
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=headers, timeout=10) as response:
                            if response.status == 200:
                                data = await response.json()
                                # Contoh response: {"is_holiday": true, "holiday_name": "Hari Pahlawan", "holiday_type": "Nasional"}
                                return {
                                    "is_holiday": data.get("is_holiday", False),
                                    "holiday_name": data.get("holiday_name"),
                                    "holiday_type": data.get("holiday_type"),
                                    "source": "calendar_api"
                                }
                except Exception as e:
                    print(f"⚠️ Calendar API failed: {e}")
                return {"is_holiday": False, "source": "calendar_api"}
        return context

    async def _get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get weather data with fallback chain:
        1. Real API (OpenWeatherMap)
        2. Cache (if valid)
        3. Simulation
        """
        # Try cache first (fast path)
        cached = self._load_cache(self.WEATHER_CACHE_FILE, self.WEATHER_CACHE_DURATION)
        
        # Try real API if key is configured
        openweather_api_key = await self.get_api_key("weather")
        if openweather_api_key:
            try:
                real_data = await self._fetch_openweather(lat, lon, openweather_api_key)
                if real_data:
                    self._save_cache(self.WEATHER_CACHE_FILE, real_data)
                    return real_data
            except Exception as e:
                print(f"⚠️ Weather API failed: {e}")
        
        # Return cache if valid
        if cached:
            print("📦 Using cached weather data")
            return cached
        
        # Fallback to simulation
        print("🎲 Using simulated weather data")
        return self._simulate_weather()

    async def _fetch_openweather(self, lat: float, lon: float, api_key: str) -> Optional[Dict[str, Any]]:
        """Fetch real weather from OpenWeatherMap API"""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "lang": "id"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Map to our format
                    weather_main = data["weather"][0]["main"].lower()
                    weather_map = {
                        "clear": "cerah",
                        "clouds": "berawan",
                        "rain": "hujan_ringan" if data.get("rain", {}).get("1h", 0) < 5 else "hujan_lebat",
                        "drizzle": "hujan_ringan",
                        "thunderstorm": "hujan_lebat",
                        "snow": "berawan",
                        "mist": "berawan",
                        "fog": "berawan"
                    }
                    
                    return {
                        "condition": weather_map.get(weather_main, "cerah"),
                        "description": data["weather"][0]["description"],
                        "temperature": round(data["main"]["temp"], 1),
                        "humidity": data["main"]["humidity"],
                        "source": "openweathermap_api",
                        "fetched_at": datetime.now().isoformat()
                    }
                else:
                    print(f"⚠️ OpenWeather API error: {response.status}")
                    return None

    async def _get_traffic(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get traffic data with fallback chain:
        1. Real API (Google Maps or TomTom)
        2. Cache (if valid)
        3. Simulation
        """
        # Try cache first
        cached = self._load_cache(self.TRAFFIC_CACHE_FILE, self.TRAFFIC_CACHE_DURATION)
        
        # Try real API if key is configured
        google_maps_api_key = await self.get_api_key("traffic_google")
        tomtom_api_key = await self.get_api_key("traffic_tomtom")
        if google_maps_api_key:
            try:
                real_data = await self._fetch_google_traffic(lat, lon, google_maps_api_key)
                if real_data:
                    self._save_cache(self.TRAFFIC_CACHE_FILE, real_data)
                    return real_data
            except Exception as e:
                print(f"⚠️ Google Maps API failed: {e}")
        elif tomtom_api_key:
            try:
                real_data = await self._fetch_tomtom_traffic(lat, lon, tomtom_api_key)
                if real_data:
                    self._save_cache(self.TRAFFIC_CACHE_FILE, real_data)
                    return real_data
            except Exception as e:
                print(f"⚠️ TomTom API failed: {e}")
        
        # Return cache if valid
        if cached:
            print("📦 Using cached traffic data")
            return cached
        
        # Fallback to simulation
        print("🎲 Using simulated traffic data")
        return self._simulate_traffic()

    async def _fetch_google_traffic(self, lat: float, lon: float, api_key: str) -> Optional[Dict[str, Any]]:
        """Fetch traffic from Google Maps Distance Matrix API"""
        # Sample nearby destination (5km north)
        dest_lat = lat + 0.045
        dest_lon = lon
        
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": f"{lat},{lon}",
            "destinations": f"{dest_lat},{dest_lon}",
            "departure_time": "now",
            "traffic_model": "best_guess",
            "key": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data["status"] == "OK":
                        element = data["rows"][0]["elements"][0]
                        duration = element["duration"]["value"]  # seconds
                        duration_in_traffic = element.get("duration_in_traffic", {}).get("value", duration)
                        
                        # Calculate traffic ratio
                        traffic_ratio = duration_in_traffic / duration if duration > 0 else 1.0
                        
                        # Map to condition
                        if traffic_ratio < 1.1:
                            condition = "lancar"
                        elif traffic_ratio < 1.3:
                            condition = "sedang"
                        elif traffic_ratio < 1.6:
                            condition = "padat"
                        else:
                            condition = "macet"
                        
                        # Estimate speed (km/h)
                        distance_km = element["distance"]["value"] / 1000
                        time_hours = duration_in_traffic / 3600
                        speed = round(distance_km / time_hours, 1) if time_hours > 0 else 40
                        
                        return {
                            "condition": condition,
                            "speed": speed,
                            "traffic_ratio": round(traffic_ratio, 2),
                            "source": "google_maps_api",
                            "fetched_at": datetime.now().isoformat()
                        }
                
                return None

    async def _fetch_tomtom_traffic(self, lat: float, lon: float, api_key: str) -> Optional[Dict[str, Any]]:
        """Fetch traffic from TomTom Traffic Flow API"""
        # Zoom level for traffic tile
        zoom = 14
        
        url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/{zoom}/json"
        params = {
            "key": api_key,
            "point": f"{lat},{lon}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    current_speed = data["flowSegmentData"]["currentSpeed"]
                    free_flow_speed = data["flowSegmentData"]["freeFlowSpeed"]
                    
                    # Calculate traffic ratio
                    traffic_ratio = free_flow_speed / current_speed if current_speed > 0 else 1.0
                    
                    # Map to condition
                    if traffic_ratio < 1.2:
                        condition = "lancar"
                    elif traffic_ratio < 1.5:
                        condition = "sedang"
                    elif traffic_ratio < 2.0:
                        condition = "padat"
                    else:
                        condition = "macet"
                    
                    return {
                        "condition": condition,
                        "speed": current_speed,
                        "traffic_ratio": round(traffic_ratio, 2),
                        "source": "tomtom_api",
                        "fetched_at": datetime.now().isoformat()
                    }
                
                return None

    def _simulate_weather(self) -> Dict[str, Any]:
        """Simulate weather based on Indonesia climate"""
        import random
        now = datetime.now()
        season = self._get_season(now.month)
        
        if season == "hujan":
            if 13 <= now.hour <= 19:  # Afternoon/evening - rain peak
                condition = random.choices(
                    ["cerah", "berawan", "hujan_ringan", "hujan_lebat"],
                    weights=[0.1, 0.2, 0.4, 0.3]
                )[0]
            else:
                condition = random.choices(
                    ["cerah", "berawan", "hujan_ringan", "hujan_lebat"],
                    weights=[0.3, 0.3, 0.3, 0.1]
                )[0]
        else:  # kemarau
            condition = random.choices(
                ["cerah", "berawan", "hujan_ringan", "hujan_lebat"],
                weights=[0.6, 0.3, 0.08, 0.02]
            )[0]
        
        temp_map = {"cerah": 30, "berawan": 28, "hujan_ringan": 26, "hujan_lebat": 24}
        humidity_map = {"cerah": 65, "berawan": 70, "hujan_ringan": 80, "hujan_lebat": 90}
        
        return {
            "condition": condition,
            "description": condition.replace("_", " "),
            "temperature": temp_map.get(condition, 28),
            "humidity": humidity_map.get(condition, 75),
            "source": "simulation",
            "fetched_at": datetime.now().isoformat()
        }

    def _simulate_traffic(self) -> Dict[str, Any]:
        """Simulate traffic based on time of day"""
        import random
        now = datetime.now()
        
        if (7 <= now.hour <= 9) or (16 <= now.hour <= 19):  # Rush hour
            condition = random.choices(
                ["lancar", "sedang", "padat", "macet"],
                weights=[0.1, 0.3, 0.4, 0.2]
            )[0]
        else:
            condition = random.choices(
                ["lancar", "sedang", "padat", "macet"],
                weights=[0.6, 0.3, 0.09, 0.01]
            )[0]
        
        speed_map = {"lancar": 50, "sedang": 35, "padat": 20, "macet": 10}
        
        return {
            "condition": condition,
            "speed": speed_map.get(condition, 40),
            "traffic_ratio": 1.0,
            "source": "simulation",
            "fetched_at": datetime.now().isoformat()
        }

    def _load_cache(self, cache_file: Path, max_age_seconds: int) -> Optional[Dict[str, Any]]:
        """Load cache if exists and not expired"""
        try:
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                fetched_at = datetime.fromisoformat(cached["fetched_at"])
                age = (datetime.now() - fetched_at).total_seconds()
                
                if age < max_age_seconds:
                    return cached
                else:
                    print(f"⏰ Cache expired ({age:.0f}s > {max_age_seconds}s)")
        except Exception as e:
            print(f"⚠️ Cache load failed: {e}")
        
        return None

    def _save_cache(self, cache_file: Path, data: Dict[str, Any]):
        """Save data to cache file"""
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Cache save failed: {e}")

    def _get_season(self, month: int) -> str:
        """Get season based on Indonesia climate"""
        return "kemarau" if month in self.kemarau_months else "hujan"

    def _is_holiday_season(self, now: datetime) -> bool:
        """Check if holiday season in Indonesia"""
        return (
            now.month in [6, 7, 12] or  # School holidays
            (now.month == 1 and now.day <= 7) or  # New year
            now.weekday() >= 5  # Weekend
        )
    
    def _get_time_period(self, hour: int) -> str:
        """Get time period of day"""
        if 5 <= hour < 10:
            return "pagi"  # morning
        elif 10 <= hour < 15:
            return "siang"  # midday
        elif 15 <= hour < 18:
            return "sore"  # afternoon
        elif 18 <= hour < 21:
            return "malam"  # evening
        else:
            return "malam_larut"  # late night

    async def get_mock_context_for_evaluation(self, user_id: int) -> Dict[str, Any]:
        """Mock context for evaluation consistency"""
        import random
        random.seed(user_id % 1000)
        
        random_month = random.randint(1, 12)
        season = self._get_season(random_month)
        
        weather_conditions = ["cerah", "berawan", "hujan_ringan", "hujan_lebat"]
        if season == "hujan":
            weather = random.choices(weather_conditions, weights=[0.2, 0.3, 0.3, 0.2])[0]
        else:
            weather = random.choices(weather_conditions, weights=[0.6, 0.3, 0.08, 0.02])[0]
        
        return {
            'weather': weather,
            'hour_of_day': random.randint(8, 22),
            'is_weekend': random.choice([True, False]),
            'season': season,
            'timestamp': datetime.now().isoformat()
        }

# Legacy compatibility
async def get_weather(lat, lon):
    """Legacy function"""
    service = RealTimeContextService()
    context = await service.get_current_context(lat, lon)
    return {
        "main": context["weather"].replace("_", " ").title(),
        "desc": context["weather_description"]
    }
