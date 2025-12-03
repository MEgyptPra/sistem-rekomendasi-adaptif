"""
Add 6 missing destinations to database to match Excel data
"""
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.core.db import get_db
from app.models.destinations import Destination

# 6 destinations yang missing (dari MISSING_DESTINATIONS.csv)
MISSING_DESTINATIONS = [
    {
        'name': 'Kampung Wisata Pangjugjugan',
        'row_count': 709,
        'description': 'Kampung wisata budaya di Sumedang'
    },
    {
        'name': 'Ponyo® Resto & Wedding - Ciherang Sumedang',
        'row_count': 289,
        'description': 'Restoran dan tempat wedding di Ciherang, Sumedang'
    },
    {
        'name': "LIMASAN's FINEST - CAFE",
        'row_count': 186,
        'description': 'Kafe dengan konsep modern di Sumedang'
    },
    {
        'name': 'Clover Leaf Café & Resto',
        'row_count': 171,
        'description': 'Kafe dan restoran di Sumedang'
    },
    {
        'name': 'Komplek Pemakaman Cut Nyak Dien',
        'row_count': 100,
        'description': 'Komplek pemakaman bersejarah Cut Nyak Dien'
    },
    {
        'name': 'Saung bapak undang',
        'row_count': 3,
        'description': 'Saung kuliner tradisional di Sumedang'
    }
]

async def add_missing_destinations():
    """Add missing destinations to database"""
    
    print("=" * 70)
    print("🏛️  MENAMBAHKAN DESTINASI YANG HILANG")
    print("=" * 70)
    
    async for db in get_db():
        # Check which destinations already exist
        existing_count = 0
        added_count = 0
        
        for dest_info in MISSING_DESTINATIONS:
            dest_name = dest_info['name']
            
            # Check if already exists
            result = await db.execute(
                select(Destination).where(Destination.name == dest_name)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"⏭️  Skip (sudah ada): {dest_name}")
                existing_count += 1
            else:
                # Add new destination
                new_dest = Destination(
                    name=dest_name,
                    description=dest_info['description'],
                    category='Wisata',  # Default category
                    address='Sumedang, Jawa Barat',
                    lat=None,
                    lon=None
                )
                db.add(new_dest)
                print(f"✅ Ditambahkan: {dest_name} ({dest_info['row_count']} ratings akan tersedia)")
                added_count += 1
        
        # Commit all changes
        if added_count > 0:
            await db.commit()
            print(f"\n💾 Saved {added_count} new destinations to database")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"Total destinations to add: {len(MISSING_DESTINATIONS)}")
        print(f"Already existed: {existing_count}")
        print(f"Newly added: {added_count}")
        
        if added_count > 0:
            total_impact = sum(d['row_count'] for d in MISSING_DESTINATIONS)
            print(f"\n💡 Impact: {total_impact:,} ratings will now be importable")
            print("\n🔄 NEXT STEPS:")
            print("1. Re-run import script: python scripts/import_all_gmaps_data.py")
            print(f"2. Expected improvement: +{total_impact:,} ratings")
            print("3. New skip rate: ~12.4% (user issues only)")
        
        break

if __name__ == "__main__":
    asyncio.run(add_missing_destinations())
