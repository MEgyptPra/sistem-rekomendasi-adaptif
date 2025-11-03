"""
Seed data untuk Activities table
Run this script to populate activities for testing
"""

import asyncio
from app.core.db import AsyncSessionLocal, engine
from app.models.activity import Activity

async def seed_activities():
    activities_data = [
        {
            "name": "Wisata Kuliner Tahu Sumedang",
            "description": "Jelajahi kelezatan legendaris Tahu Sumedang yang telah terkenal di seluruh Indonesia. Kunjungi sentra produksi, pabrik, dan restoran tahu terbaik di Sumedang.",
            "category": "Kuliner",
            "duration": "2-3 jam",
            "price_range": "Rp 50.000 - 150.000",
            "image_url": "/assets/images/kuliner-tahu-hero.jpg"
        },
        {
            "name": "Wisata Peuyeum",
            "description": "Kunjungi sentra pembuatan peuyeum khas Sumedang dan pelajari proses pembuatannya yang unik.",
            "category": "Kuliner",
            "duration": "1-2 jam",
            "price_range": "Rp 30.000 - 80.000",
            "image_url": "/assets/images/peuyeum.jpg"
        },
        {
            "name": "Tour Budaya Sunda",
            "description": "Jelajahi warisan budaya Sunda di berbagai situs bersejarah dengan pemandu lokal.",
            "category": "Budaya",
            "duration": "4-5 jam",
            "price_range": "Rp 150.000 - 300.000",
            "image_url": "/assets/images/budaya-sunda.jpg"
        },
        {
            "name": "Pendakian Gunung Tampomas",
            "description": "Nikmati pendakian ke puncak Gunung Tampomas dengan pemandangan spektakuler.",
            "category": "Alam",
            "duration": "6-8 jam",
            "price_range": "Gratis - Rp 50.000 (guide)",
            "image_url": "/assets/images/pendakian-tampomas.jpg"
        },
        {
            "name": "Wisata Kuliner Nasi Timbel",
            "description": "Cicip berbagai varian nasi timbel khas Sunda di restoran pilihan.",
            "category": "Kuliner",
            "duration": "2-3 jam",
            "price_range": "Rp 40.000 - 100.000",
            "image_url": "/assets/images/nasi-timbel.jpg"
        },
        {
            "name": "Fotografi Alam Sumedang",
            "description": "Tour fotografi dengan guide profesional ke spot-spot terbaik di Sumedang.",
            "category": "Alam",
            "duration": "5-6 jam",
            "price_range": "Rp 200.000 - 400.000",
            "image_url": "/assets/images/fotografi-alam.jpg"
        },
        {
            "name": "Workshop Kerajinan Tangan",
            "description": "Belajar membuat kerajinan tangan khas Sumedang dari pengrajin lokal.",
            "category": "Budaya",
            "duration": "3-4 jam",
            "price_range": "Rp 100.000 - 200.000",
            "image_url": "/assets/images/workshop-kerajinan.jpg"
        },
        {
            "name": "Kopi Sumedang Tour",
            "description": "Kunjungi perkebunan kopi dan pelajari proses dari biji hingga secangkir kopi.",
            "category": "Kuliner",
            "duration": "3-4 jam",
            "price_range": "Rp 80.000 - 150.000",
            "image_url": "/assets/images/kopi.jpg"
        }
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            for activity_data in activities_data:
                activity = Activity(**activity_data)
                session.add(activity)
            
            await session.commit()
            print(f"✅ Successfully seeded {len(activities_data)} activities")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding activities: {e}")
        finally:
            await session.close()

if __name__ == "__main__":
    print("Seeding activities...")
    asyncio.run(seed_activities())
