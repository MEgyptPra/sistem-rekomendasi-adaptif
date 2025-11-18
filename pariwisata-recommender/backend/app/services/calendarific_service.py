import os
import aiohttp
from datetime import datetime
from typing import List, Dict, Any, Optional

class CalendarificService:
    """
    Service untuk mengambil data hari libur nasional dari Calendarific API
    """
    def __init__(self):
        self.api_key = os.getenv("CALENDARIFIC_API_KEY")
        self.base_url = "https://calendarific.com/api/v2/holidays"

    async def get_holidays(self, country: str = "ID", year: Optional[int] = None) -> List[Dict[str, Any]]:
        if not self.api_key:
            print("⚠️ CALENDARIFIC_API_KEY belum di-set di .env!")
            return []
        year = year or datetime.now().year
        params = {
            "api_key": self.api_key,
            "country": country,
            "year": year
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    holidays = data.get("response", {}).get("holidays", [])
                    return holidays
                else:
                    print(f"⚠️ Calendarific API error: {response.status}")
                    return []

# Contoh pemakaian (di endpoint atau service lain):
# from app.services.calendarific_service import CalendarificService
# service = CalendarificService()
# holidays = await service.get_holidays(country="ID", year=2025)
# print(holidays)
