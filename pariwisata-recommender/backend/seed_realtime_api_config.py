import asyncio
from app.core.db import AsyncSessionLocal
from app.models.realtime_api_config import RealtimeAPIConfig

async def seed_realtime_api_config():
    async with AsyncSessionLocal() as session:
        configs = [
            RealtimeAPIConfig(
                source_name="weather",
                api_key="",
                api_url="https://api.openweathermap.org/data/2.5/weather",
                status="active",
                notes="API cuaca (OpenWeatherMap)"
            ),
            RealtimeAPIConfig(
                source_name="traffic_google",
                api_key="",
                api_url="https://maps.googleapis.com/maps/api/distancematrix/json",
                status="active",
                notes="API traffic (Google Maps)"
            ),
            RealtimeAPIConfig(
                source_name="traffic_tomtom",
                api_key="",
                api_url="https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/14/json",
                status="active",
                notes="API traffic (TomTom)"
            ),
            RealtimeAPIConfig(
                source_name="social_trend",
                api_key="",
                api_url="",
                status="active",
                notes="Social trend dari user interaction"
            ),
            RealtimeAPIConfig(
                source_name="calendar",
                api_key="",
                api_url="https://api-harilibur.vercel.app/api",
                status="active",
                notes="API Kalender Libur Nasional Indonesia"
            ),
        ]
        for config in configs:
            existing = await session.execute(
                RealtimeAPIConfig.__table__.select().where(RealtimeAPIConfig.source_name == config.source_name)
            )
            if not existing.first():
                session.add(config)
        await session.commit()
        print("Seed realtime_api_config selesai.")

if __name__ == "__main__":
    asyncio.run(seed_realtime_api_config())
