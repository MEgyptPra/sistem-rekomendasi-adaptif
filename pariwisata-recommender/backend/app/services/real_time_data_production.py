import os
import json
import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from app.services.social_trend_service import SocialTrendService

class RealTimeContextService:
    def __init__(self):
        self.CACHE_DIR = Path("data/cache")
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.DEFAULT_LAT = -6.200000
        self.DEFAULT_LON = 106.816666
        self.WEATHER_CACHE_FILE = self.CACHE_DIR / "weather_cache.json"
        self.WEATHER_CACHE_DURATION = 600
        self.TRAFFIC_CACHE_FILE = self.CACHE_DIR / "traffic_cache.json"
        self.TRAFFIC_CACHE_DURATION = 600
        self.kemarau_months = [5, 6, 7, 8, 9, 10]
        self.hujan_months = [11, 12, 1, 2, 3, 4]
        self.trend_service = SocialTrendService()
        print(f"🌍 RealTimeContextService initialized")

    async def get_current_context(self, lat: float = None, lon: float = None) -> Dict[str, Any]:
        lat = lat if lat is not None else self.DEFAULT_LAT
        lon = lon if lon is not None else self.DEFAULT_LON
        
        # Default Fallback Values
        weather_data = self._simulate_weather()
        traffic_data = self._simulate_traffic()
        trending_info = {"overall_trend": "normal", "trending_destinations": []}

        # 1. Get Weather (Safe)
        try:
            weather_data = await self._get_weather(lat, lon)
        except Exception as e:
            print(f"⚠️ Weather fetch failed: {e}")
            weather_data = self._simulate_weather()

        # 2. Get Traffic (Safe)
        try:
            traffic_data = await self._get_traffic(lat, lon)
        except Exception as e:
            print(f"⚠️ Traffic fetch failed: {e}")
            traffic_data = self._simulate_traffic()

        # 3. Get Trends (Safe)
        try:
            trending_info = self.trend_service.get_trending_status()
        except Exception as e:
            print(f"⚠️ Trend fetch failed: {e}")

        now = datetime.now()
        season = self._get_season(now.month)
        is_weekend = now.weekday() >= 5
        time_period = self._get_time_period(now.hour)

        return {
            "weather": weather_data.get("condition", "cerah"),
            "weather_description": weather_data.get("description", "simulasi"),
            "temperature": weather_data.get("temperature", 28),
            "traffic": traffic_data.get("condition", "lancar"),
            "social_trend": trending_info.get("overall_trend", "normal"),
            "is_weekend": is_weekend,
            "season": season,
            "time_period": time_period,
            "hour_of_day": now.hour
        }

    async def _get_weather(self, lat, lon):
        cached = self._load_cache(self.WEATHER_CACHE_FILE, self.WEATHER_CACHE_DURATION)
        if cached: return cached
        return self._simulate_weather()

    async def _get_traffic(self, lat, lon):
        return self._simulate_traffic()

    def _simulate_weather(self):
        import random
        return {
            "condition": random.choice(["cerah", "berawan"]),
            "description": "cerah berawan",
            "temperature": 28,
            "source": "simulation",
            "fetched_at": datetime.now().isoformat()
        }

    def _simulate_traffic(self):
        return {
            "condition": "lancar",
            "speed": 40,
            "source": "simulation",
            "fetched_at": datetime.now().isoformat()
        }

    def _load_cache(self, cache_file, duration):
        try:
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                age = (datetime.now() - datetime.fromisoformat(data["fetched_at"])).total_seconds()
                if age < duration: return data
        except: pass
        return None

    def _save_cache(self, cache_file, data):
        try:
            data["fetched_at"] = datetime.now().isoformat()
            with open(cache_file, 'w') as f: json.dump(data, f)
        except: pass

    def _get_season(self, month):
        return "kemarau" if month in self.kemarau_months else "hujan"

    def _get_time_period(self, hour):
        if 5 <= hour < 10: return "pagi"
        elif 10 <= hour < 15: return "siang"
        elif 15 <= hour < 18: return "sore"
        else: return "malam"