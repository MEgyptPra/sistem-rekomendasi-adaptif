"""
Real-Time Context Service - INDONESIA CLIMATE VERSION
Mensimulasikan pengambilan data real-time untuk sistem rekomendasi adaptif.
Disesuaikan dengan iklim tropis Indonesia (2 musim: Kemarau dan Hujan)
"""

import random
from datetime import datetime
from typing import Dict, Any

class RealTimeContextService:
    """
    Mensimulasikan pengambilan data real-time.
    ✅ DISESUAIKAN DENGAN IKLIM INDONESIA
    """
    
    def __init__(self):
        # Weather conditions untuk iklim tropis Indonesia
        self.weather_conditions = ["cerah", "berawan", "hujan_ringan", "hujan_lebat"]
        self.traffic_conditions = ["lancar", "sedang", "padat", "macet"]
        self.social_trends = ["normal", "sedang_tren", "viral"]
        
        # ✅ INDONESIA: 2 musim system
        self.seasons = ["kemarau", "hujan"]
        self.kemarau_months = [5, 6, 7, 8, 9, 10]  # Mei - Oktober
        self.hujan_months = [11, 12, 1, 2, 3, 4]    # November - April

    async def get_current_context(self) -> Dict[str, Any]:
        """
        ✅ ASYNC VERSION - Menghasilkan konteks real-time Indonesia
        """
        now = datetime.now()
        
        # Tentukan musim berdasarkan sistem Indonesia
        current_season = self._get_season(now.month)
        
        # Simulasi cuaca berdasarkan musim Indonesia
        current_weather = self._simulate_weather(now, current_season)
        
        # Simulasi lalu lintas 
        current_traffic = self._simulate_traffic(now)
        
        # Context untuk Indonesia
        context = {
            "weather": current_weather,
            "traffic": current_traffic,
            "social_trend": random.choice(self.social_trends),
            "is_weekend": now.weekday() >= 5,  # True jika Sabtu atau Minggu
            "hour_of_day": now.hour,
            "season": current_season,  # ✅ "kemarau" atau "hujan"
            "is_holiday_season": self._is_holiday_season(now),
            "temperature_category": self._get_temperature_category(current_weather),
            "humidity_level": self._get_humidity_level(current_season)
        }
        
        print(f"🌍 CONTEXT GENERATED (Indonesia): {context}")
        return context

    def _get_season(self, month: int) -> str:
        """
        ✅ FIXED: Tentukan musim berdasarkan sistem 2 musim Indonesia
        Musim Kemarau: Mei - Oktober (bulan 5-10)
        Musim Hujan: November - April (bulan 11, 12, 1-4)
        """
        if month in self.kemarau_months:
            return "kemarau"
        else:
            return "hujan"

    def _simulate_weather(self, now: datetime, season: str) -> str:
        """
        ✅ Simulasi cuaca berdasarkan musim Indonesia
        """
        if season == "hujan":
            # Musim hujan: lebih sering hujan, terutama sore/malam
            if 13 <= now.hour <= 19:  # Sore/malam - puncak hujan
                return random.choices(
                    self.weather_conditions,
                    weights=[0.1, 0.2, 0.4, 0.3],  # Lebih besar peluang hujan
                    k=1
                )[0]
            else:  # Pagi/siang
                return random.choices(
                    self.weather_conditions,
                    weights=[0.3, 0.3, 0.3, 0.1],
                    k=1
                )[0]
        else:  # season == "kemarau"  
            # Musim kemarau: lebih sering cerah/berawan
            if 13 <= now.hour <= 18:  # Sore - masih bisa hujan ringan
                return random.choices(
                    self.weather_conditions,
                    weights=[0.5, 0.3, 0.15, 0.05],
                    k=1
                )[0]
            else:  # Pagi/malam - sangat cerah
                return random.choices(
                    self.weather_conditions,
                    weights=[0.7, 0.25, 0.04, 0.01],
                    k=1
                )[0]

    def _simulate_traffic(self, now: datetime) -> str:
        """Simulasi lalu lintas berdasarkan jam sibuk (sama seperti sebelumnya)"""
        if (7 <= now.hour <= 9) or (16 <= now.hour <= 19):  # Jam sibuk
            return random.choices(
                self.traffic_conditions,
                weights=[0.1, 0.3, 0.4, 0.2],
                k=1
            )[0]
        else:  # Jam normal
            return random.choices(
                self.traffic_conditions,
                weights=[0.6, 0.3, 0.09, 0.01],
                k=1
            )[0]

    def _is_holiday_season(self, now: datetime) -> bool:
        """
        ✅ Tentukan musim liburan Indonesia
        """
        return (
            now.month in [6, 7, 12] or  # Juni-Juli (liburan sekolah), Desember
            (now.month == 1 and now.day <= 7) or  # Awal Januari
            now.weekday() >= 5 or  # Weekend
            random.random() < 0.1  # 10% chance libur nasional
        )

    def _get_temperature_category(self, weather: str) -> str:
        """
        ✅ Kategorikan suhu berdasarkan kondisi cuaca Indonesia
        Suhu Indonesia: 26-30°C sepanjang tahun
        """
        temperature_map = {
            "cerah": random.choice(["hangat", "panas"]),
            "berawan": "hangat",
            "hujan_ringan": random.choice(["sejuk", "hangat"]), 
            "hujan_lebat": "sejuk"
        }
        return temperature_map.get(weather, "hangat")

    def _get_humidity_level(self, season: str) -> str:
        """
        ✅ Level kelembaban berdasarkan musim Indonesia
        Indonesia: kelembaban tinggi 65-90% sepanjang tahun
        """
        if season == "hujan":
            return random.choice(["tinggi", "sangat_tinggi"])  # 80-90%
        else:  # kemarau
            return random.choice(["sedang", "tinggi"])  # 65-80%


    async def get_mock_context_for_evaluation(self, user_id: int) -> Dict[str, Any]:
        """
        ✅ Mock context generator untuk evaluation consistency
        """
        random.seed(user_id % 1000)
        
        # Random month untuk menentukan musim Indonesia
        random_month = random.randint(1, 12)
        season = self._get_season(random_month)
        
        # Weather berdasarkan musim Indonesia
        if season == "hujan":
            weather = random.choices(
                self.weather_conditions,
                weights=[0.2, 0.3, 0.3, 0.2]
            )[0]
        else:  # kemarau
            weather = random.choices(
                self.weather_conditions,
                weights=[0.6, 0.3, 0.08, 0.02]
            )[0]
        
        context = {
            'weather': weather,
            'hour_of_day': random.randint(8, 22),
            'is_weekend': random.choice([True, False]),
            'season': season,  # ✅ "kemarau" atau "hujan"
            'timestamp': datetime.now().isoformat(),
            'humidity_level': self._get_humidity_level(season),
            'temperature_category': self._get_temperature_category(weather)
        }
        
        return context

# Legacy function untuk backward compatibility
async def get_weather(lat, lon):
    """Legacy function - updated untuk Indonesia context"""
    service = RealTimeContextService()
    context = await service.get_current_context()
    return {
        "main": context["weather"].replace("_", " ").title(),
        "desc": context["weather"]
    }
