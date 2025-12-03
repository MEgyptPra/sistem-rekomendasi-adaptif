"""
Export missing destinations and users to CSV for manual review
"""
import pandas as pd
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.core.db import get_db
from app.models.destinations import Destination
from app.models.user import User

async def export_missing_data():
    """Export all missing destinations and users to CSV files"""
    
    # Load Excel data
    print("📂 Loading Excel data...")
    excel_path = Path(__file__).parent / "data" / "sumedang reviews.xlsx"
    df = pd.read_excel(excel_path)
    print(f"   Loaded {len(df):,} rows from Excel")
    
    # Connect to database using SQLAlchemy
    print("\n🔗 Connecting to database...")
    async for db in get_db():
        # Get all destinations from database
        result = await db.execute(select(Destination.name))
        db_destinations = result.scalars().all()
        db_dest_names = {name.strip().lower() for name in db_destinations}
        print(f"   Found {len(db_dest_names)} destinations in database")
        
        # Get all GMaps users from database
        result = await db.execute(
            select(User.name).where(User.email.like('%@gmaps.sumedang.com'))
        )
        db_users = result.scalars().all()
        db_user_names = {name.strip().lower() for name in db_users}
        print(f"   Found {len(db_user_names)} GMaps users in database")
        
        # Break after first iteration (we only need one db session)
        break
    
    # ==================================================================
    # PART 1: MISSING DESTINATIONS
    # ==================================================================
    print("\n" + "="*70)
    print("📍 ANALYZING MISSING DESTINATIONS")
    print("="*70)
    
    # Find all unique places in Excel
    excel_places = df['place'].unique()
    
    # Check which places are NOT in database
    missing_destinations = []
    for place in excel_places:
        place_clean = str(place).strip()
        if place_clean.lower() not in db_dest_names:
            # Count how many rows this place has
            count = len(df[df['place'] == place])
            missing_destinations.append({
                'destination_name': place_clean,
                'row_count': count,
                'percentage': (count / len(df)) * 100
            })
    
    # Sort by row count
    missing_destinations.sort(key=lambda x: x['row_count'], reverse=True)
    
    # Create DataFrame and export
    df_missing_dest = pd.DataFrame(missing_destinations)
    csv_dest = 'MISSING_DESTINATIONS.csv'
    df_missing_dest.to_csv(csv_dest, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Exported {len(missing_destinations)} missing destinations to: {csv_dest}")
    print("\n📊 Summary:")
    print(f"   Total unique places in Excel: {len(excel_places)}")
    print(f"   Places in database: {len(excel_places) - len(missing_destinations)}")
    print(f"   Places MISSING: {len(missing_destinations)}")
    print(f"   Total rows affected: {sum(d['row_count'] for d in missing_destinations):,}")
    
    if len(missing_destinations) > 0:
        print(f"\n   Top 10 missing:")
        for i, dest in enumerate(missing_destinations[:10], 1):
            print(f"   {i}. {dest['destination_name'][:50]:<50} ({dest['row_count']:,} rows, {dest['percentage']:.2f}%)")
    
    # ==================================================================
    # PART 2: MISSING USERS (with their ratings)
    # ==================================================================
    print("\n" + "="*70)
    print("👥 ANALYZING MISSING USERS")
    print("="*70)
    
    # Count ratings per user in Excel
    user_ratings = df['user'].value_counts().to_dict()
    
    # Find users NOT in database
    missing_users = []
    for username, rating_count in user_ratings.items():
        username_clean = str(username).strip()
        if username_clean.lower() not in db_user_names:
            missing_users.append({
                'username': username_clean,
                'rating_count': rating_count,
                'percentage': (rating_count / len(df)) * 100
            })
    
    # Sort by rating count
    missing_users.sort(key=lambda x: x['rating_count'], reverse=True)
    
    # Create DataFrame and export
    df_missing_users = pd.DataFrame(missing_users)
    csv_users = 'MISSING_USERS.csv'
    df_missing_users.to_csv(csv_users, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Exported {len(missing_users)} missing users to: {csv_users}")
    print("\n📊 Summary:")
    print(f"   Total unique users in Excel: {len(user_ratings)}")
    print(f"   Users in database: {len(user_ratings) - len(missing_users)}")
    print(f"   Users MISSING: {len(missing_users)}")
    print(f"   Total ratings from missing users: {sum(u['rating_count'] for u in missing_users):,}")
    
    if len(missing_users) > 0:
        print(f"\n   Top 20 missing users:")
        for i, user in enumerate(missing_users[:20], 1):
            print(f"   {i:2d}. {user['username'][:40]:<40} ({user['rating_count']:3d} ratings, {user['percentage']:.2f}%)")
    
    # ==================================================================
    # PART 3: DETAILED BREAKDOWN
    # ==================================================================
    print("\n" + "="*70)
    print("📋 DETAILED BREAKDOWN")
    print("="*70)
    
    # Count rows where BOTH are missing
    both_missing = 0
    dest_only = 0
    user_only = 0
    
    for _, row in df.iterrows():
        place_clean = str(row['place']).strip().lower()
        user_clean = str(row['user']).strip().lower()
        
        place_missing = place_clean not in db_dest_names
        user_missing = user_clean not in db_user_names
        
        if place_missing and user_missing:
            both_missing += 1
        elif place_missing:
            dest_only += 1
        elif user_missing:
            user_only += 1
    
    print(f"\n   Destination NOT found only: {dest_only:,} rows")
    print(f"   User NOT found only: {user_only:,} rows")
    print(f"   BOTH NOT found: {both_missing:,} rows")
    print(f"   TOTAL SKIP: {dest_only + user_only + both_missing:,} rows ({((dest_only + user_only + both_missing) / len(df)) * 100:.1f}%)")
    
    # ==================================================================
    # SUMMARY
    # ==================================================================
    print("\n" + "="*70)
    print("📝 FILES CREATED")
    print("="*70)
    print(f"\n1. {csv_dest}")
    print(f"   - {len(missing_destinations)} destinations yang tidak ditemukan")
    print(f"   - Kolom: destination_name, row_count, percentage")
    print(f"   - Total impact: {sum(d['row_count'] for d in missing_destinations):,} rows\n")
    
    print(f"2. {csv_users}")
    print(f"   - {len(missing_users)} users yang tidak ditemukan")
    print(f"   - Kolom: username, rating_count, percentage")
    print(f"   - Total impact: {sum(u['rating_count'] for u in missing_users):,} ratings\n")
    
    print("="*70)
    print("💡 NEXT STEPS:")
    print("="*70)
    print("""
1. Review MISSING_DESTINATIONS.csv
   - Periksa encoding issues (Café vs Caf├⌐)
   - Cocokkan dengan database destinations
   - Tambahkan destinations yang memang belum ada
   
2. Review MISSING_USERS.csv
   - User dengan rating count tinggi = prioritas
   - Periksa apakah nama sedikit berbeda di database
   - Contoh: "skay dankel" (32 ratings) vs "Skay Dankel" di database
   
3. Setelah perbaikan manual:
   - Re-run import script
   - Target: >95% import success rate
""")

if __name__ == "__main__":
    asyncio.run(export_missing_data())
