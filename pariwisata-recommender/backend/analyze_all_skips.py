"""
Analisis LENGKAP semua skip causes
"""
import pandas as pd
from pathlib import Path
import asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:rekompari@localhost:5432/pariwisata"

async def full_skip_analysis():
    # Load Excel data
    excel_path = Path(__file__).parent / 'data' / 'sumedang reviews.xlsx'
    df = pd.read_excel(excel_path)
    
    print("="*80)
    print("📊 ANALISIS LENGKAP SEMUA SKIP CAUSES")
    print("="*80)
    print(f"\n📋 Total rows in Excel: {len(df):,}")
    
    # Connect to database
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Get destinations
        query = text("SELECT id, name FROM destinations")
        result = await session.execute(query)
        db_destinations = {row[1]: row[0] for row in result}
        
        # Get users
        query = text("SELECT id, name, email FROM users WHERE email LIKE '%@gmaps.sumedang.com'")
        result = await session.execute(query)
        db_users = {row[1]: row[0] for row in result}
        
        print(f"🗄️  Database destinations: {len(db_destinations):,}")
        print(f"👥 Database GMaps users: {len(db_users):,}")
        
        # Analyze each row
        skip_reasons = {
            'destination_not_found': [],
            'user_not_found': [],
            'both_not_found': [],
            'successfully_imported': 0
        }
        
        for idx, row in df.iterrows():
            place_name = str(row.get('place', '')).strip()
            username = str(row.get('user', '')).strip()
            
            dest_found = place_name in db_destinations or place_name.lower() in [d.lower() for d in db_destinations.keys()]
            user_found = username in db_users or username.lower() in [u.lower() for u in db_users.keys()]
            
            if not dest_found and not user_found:
                skip_reasons['both_not_found'].append({
                    'place': place_name,
                    'user': username,
                    'row': idx + 2  # Excel row (1-indexed + header)
                })
            elif not dest_found:
                skip_reasons['destination_not_found'].append({
                    'place': place_name,
                    'row': idx + 2
                })
            elif not user_found:
                skip_reasons['user_not_found'].append({
                    'place': place_name,
                    'user': username,
                    'row': idx + 2
                })
            else:
                skip_reasons['successfully_imported'] += 1
        
        total_skipped = len(skip_reasons['destination_not_found']) + \
                       len(skip_reasons['user_not_found']) + \
                       len(skip_reasons['both_not_found'])
        
        print(f"\n✅ Successfully imported: {skip_reasons['successfully_imported']:,} rows")
        print(f"❌ Total skipped: {total_skipped:,} rows")
        
        print("\n" + "="*80)
        print("📊 SKIP BREAKDOWN:")
        print("="*80)
        
        # Destination not found
        dest_skip = len(skip_reasons['destination_not_found'])
        print(f"\n1️⃣  Destination NOT found only: {dest_skip:,} rows")
        if dest_skip > 0:
            # Group by place
            places_count = {}
            for item in skip_reasons['destination_not_found']:
                place = item['place']
                places_count[place] = places_count.get(place, 0) + 1
            
            print("\n   Top destinations not found:")
            for place, count in sorted(places_count.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   • {place:<60} : {count:>4} rows")
        
        # User not found
        user_skip = len(skip_reasons['user_not_found'])
        print(f"\n2️⃣  User NOT found only: {user_skip:,} rows")
        if user_skip > 0:
            # Group by user
            users_count = {}
            for item in skip_reasons['user_not_found']:
                user = item['user']
                users_count[user] = users_count.get(user, 0) + 1
            
            print(f"\n   Unique users not found: {len(users_count):,}")
            print("   Top 10 missing users:")
            for user, count in sorted(users_count.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   • {user:<60} : {count:>4} rows")
        
        # Both not found
        both_skip = len(skip_reasons['both_not_found'])
        print(f"\n3️⃣  BOTH destination AND user NOT found: {both_skip:,} rows")
        
        print("\n" + "="*80)
        print("📈 SUMMARY:")
        print("="*80)
        print(f"Total Excel rows:        {len(df):,}")
        print(f"Successfully imported:   {skip_reasons['successfully_imported']:,} ({skip_reasons['successfully_imported']/len(df)*100:.1f}%)")
        print(f"Destination only skip:   {dest_skip:,} ({dest_skip/len(df)*100:.1f}%)")
        print(f"User only skip:          {user_skip:,} ({user_skip/len(df)*100:.1f}%)")
        print(f"Both skip:               {both_skip:,} ({both_skip/len(df)*100:.1f}%)")
        print(f"TOTAL SKIPPED:           {total_skipped:,} ({total_skipped/len(df)*100:.1f}%)")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(full_skip_analysis())
