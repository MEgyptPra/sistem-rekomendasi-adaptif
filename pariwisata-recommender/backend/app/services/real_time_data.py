"""
Real-Time Context Service
Mensimulasikan pengambilan data real-time untuk sistem rekomendasi adaptif.
Dalam implementasi nyata, kelas ini akan memanggil API eksternal.
Untuk saat ini, ia menghasilkan data dummy untuk tujuan pengembangan dan pengujian.
"""

import random
from datetime import datetime
from typing import Dict, Any

class RealTimeContextService:
    """
    Mensimulasikan pengambilan data real-time.
    Menghasilkan konteks yang realistis berdasarkan waktu dan kondisi random.
    """
    
    def __init__(self):
        self.weather_conditions = ["cerah", "berawan", "hujan", "badai"]
        self.traffic_conditions = ["lancar", "sedang", "padat", "macet"]
        self.social_trends = ["normal", "sedang_tren", "viral"]
        
    def get_current_context(self) -> Dict[str, Any]:
        """
        Menghasilkan sebuah dictionary yang merepresentasikan konteks saat ini.
        
        Returns:
            Dict: Konteks dengan berbagai faktor lingkungan dan temporal
        """
        now = datetime.now()
        
        # Simulasikan kondisi cuaca berdasarkan waktu
        current_weather = self._simulate_weather(now)
        
        # Simulasikan kondisi lalu lintas berdasarkan jam
        current_traffic = self._simulate_traffic(now)
        
        # Konteks tambahan
        context = {
            "weather": current_weather,
            "traffic": current_traffic,
            "social_trend": random.choice(self.social_trends),
            "is_weekend": now.weekday() >= 5,  # True jika Sabtu atau Minggu
            "hour_of_day": now.hour,
            "season": self._get_season(now.month),
            "is_holiday_season": self._is_holiday_season(now),
            "temperature_category": self._get_temperature_category(current_weather)
        }
        
        print(f"🌍 CONTEXT GENERATED: {context}")
        return context
    
    def _simulate_weather(self, now: datetime) -> str:
        """Simulasi cuaca berdasarkan waktu hari"""
        if 13 <= now.hour <= 18:  # Sore hari - peluang hujan lebih besar
            return random.choices(
                self.weather_conditions, 
                weights=[0.2, 0.3, 0.4, 0.1], 
                k=1
            )[0]
        else:  # Pagi/malam - lebih sering cerah
            return random.choices(
                self.weather_conditions, 
                weights=[0.6, 0.3, 0.09, 0.01], 
                k=1
            )[0]
    
    def _simulate_traffic(self, now: datetime) -> str:
        """Simulasi lalu lintas berdasarkan jam sibuk"""
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
    
    def _get_season(self, month: int) -> str:
        """Tentukan musim berdasarkan bulan"""
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
    
    def _is_holiday_season(self, now: datetime) -> bool:
        """Tentukan apakah sedang musim liburan"""
        # Simulasi musim liburan: Desember, Juli (liburan sekolah), dan weekend
        return (now.month in [12, 7] or 
                now.weekday() >= 5 or 
                random.random() < 0.1)  # 10% chance random holiday
    
    def _get_temperature_category(self, weather: str) -> str:
        """Kategorikan suhu berdasarkan cuaca"""
        temperature_map = {
            "cerah": random.choice(["hangat", "panas"]),
            "berawan": random.choice(["sejuk", "hangat"]),
            "hujan": random.choice(["dingin", "sejuk"]),
            "badai": "dingin"
        }
        return temperature_map.get(weather, "sedang")

# Legacy function untuk backward compatibility
async def get_weather(lat, lon):
    """Legacy function - akan di-migrate ke RealTimeContextService"""
    service = RealTimeContextService()
    context = service.get_current_context()
    return {
        "main": context["weather"].title(), 
        "desc": context["weather"]
    }