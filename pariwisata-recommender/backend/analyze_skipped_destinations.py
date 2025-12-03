"""
Analisis destinasi yang di-skip saat import
"""
import pandas as pd
from pathlib import Path
import asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql+asyncpg://user:rekompari@localhost:5432/pariwisata"

async def analyze_skipped():
    # Load Excel data
    excel_path = Path(__file__).parent / 'data' / 'sumedang reviews.xlsx'
    df = pd.read_excel(excel_path)
    
    print("="*80)
    print("📊 ANALISIS DESTINASI YANG DI-SKIP")
    print("="*80)
    
    # Get unique place names from Excel
    excel_places = df['place'].unique()
    print(f"\n📋 Total unique places in Excel: {len(excel_places):,}")
    
    # Connect to database
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Get all destination names from database
        query = text("SELECT name FROM destinations")
        result = await session.execute(query)
        db_destinations = [row[0] for row in result]
        
        print(f"🗄️  Total destinations in database: {len(db_destinations):,}")
        
        # Find places that don't match
        not_found = []
        found_count = 0
        
        for place in excel_places:
            if pd.isna(place) or str(place).strip() == '':
                continue
                
            place_str = str(place).strip()
            
            # Check exact match
            if place_str in db_destinations:
                found_count += 1
            else:
                # Check case-insensitive match
                place_lower = place_str.lower()
                if any(db_dest.lower() == place_lower for db_dest in db_destinations):
                    found_count += 1
                else:
                    # Count how many rows have this place
                    count = len(df[df['place'] == place])
                    not_found.append({
                        'place_name': place_str,
                        'count': count
                    })
        
        print(f"✅ Places found in database: {found_count:,}")
        print(f"❌ Places NOT found: {len(not_found):,}")
        
        if not_found:
            # Sort by count (most skipped first)
            not_found_sorted = sorted(not_found, key=lambda x: x['count'], reverse=True)
            
            # Calculate total skipped rows
            total_skipped = sum(item['count'] for item in not_found_sorted)
            
            print(f"\n⚠️  Total rows skipped due to destination mismatch: {total_skipped:,}\n")
            
            print("="*80)
            print("📋 DAFTAR DESTINASI YANG TIDAK DITEMUKAN (sorted by frequency):")
            print("="*80)
            
            for idx, item in enumerate(not_found_sorted, 1):
                percentage = (item['count'] / total_skipped) * 100
                print(f"{idx:3d}. {item['place_name']:<60} | {item['count']:>5} rows ({percentage:5.2f}%)")
            
            print("\n" + "="*80)
            print("💡 REKOMENDASI:")
            print("="*80)
            print("1. Periksa nama destinasi di database yang mirip")
            print("2. Tambahkan destinasi yang missing ke database")
            print("3. Atau buat mapping nama alternatif untuk matching")
            print("\nContoh nama yang mungkin mirip:")
            
            # Show potential matches (simple substring matching)
            for item in not_found_sorted[:10]:  # Top 10
                place = item['place_name'].lower()
                potential_matches = [
                    db for db in db_destinations 
                    if any(word in db.lower() for word in place.split() if len(word) > 3)
                ]
                if potential_matches:
                    print(f"\n'{item['place_name']}'")
                    print(f"  Mungkin mirip dengan:")
                    for match in potential_matches[:3]:
                        print(f"    - {match}")
        else:
            print("\n✅ Semua destinasi di Excel ditemukan di database!")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(analyze_skipped())
