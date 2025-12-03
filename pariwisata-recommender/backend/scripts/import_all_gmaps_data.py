"""
Import SEMUA data scraping GMaps (38,697 interactions) ke database
Untuk matching dengan notebook evaluation
"""
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import random
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, delete, func
from app.core.db import get_db
from app.models.destinations import Destination
from app.models.user import User
from app.models.review import Review
from app.models.rating import Rating
from app.models.user_interaction import UserInteraction

# Path ke file Excel
EXCEL_DIR = Path(__file__).parent.parent / "data"
REVIEWS_FILE = EXCEL_DIR / "sumedang reviews.xlsx"

async def import_all_data():
    """Import ALL GMaps data without limits"""
    print("\n" + "="*80)
    print("[*] IMPORTING ALL GMAPS DATA (38,697 INTERACTIONS)")
    print("="*80 + "\n")
    
    async for db in get_db():
        try:
            # 1. Read Excel
            print("[1/4] Membaca file sumedang reviews.xlsx...")
            df = pd.read_excel(REVIEWS_FILE)
            print(f"   [OK] Total data: {len(df):,} interactions")
            print(f"   Kolom: {list(df.columns)}\n")
            
            # 2. Get all destinations with IDs
            print("[2/4] Loading destinations...")
            dest_result = await db.execute(select(Destination))
            db_destinations = dest_result.scalars().all()
            destinations = {d.name: d.id for d in db_destinations}  # Store ID directly
            print(f"   [OK] {len(destinations)} destinations loaded\n")
            
            # 3. Create users from unique GMaps users
            print("[3/4] Creating users from GMaps data...")
            unique_users = df['user'].unique()
            print(f"   Found {len(unique_users):,} unique users")
            
            # DON'T clear existing GMaps users - just update if needed
            # This avoids foreign key constraint issues
            # await db.execute(delete(User).where(User.email.like('%@gmaps.sumedang.com')))
            # await db.commit()
            print("   [INFO] Using existing users + creating new ones")
            
            # Get existing ratings count from GMaps users
            existing_ratings_query = select(func.count(Rating.id)).select_from(Rating).join(
                User, Rating.user_id == User.id
            ).where(User.email.like('%@gmaps.sumedang.com'))
            existing_ratings_result = await db.execute(existing_ratings_query)
            existing_ratings_count = existing_ratings_result.scalar()
            print(f"   [INFO] Existing GMaps ratings: {existing_ratings_count:,}\n")
            
            user_map = {}
            batch_size = 100  # Smaller batch to avoid memory issues
            created_count = 0
            
            # Track used emails to avoid duplicates
            used_emails = set()
            
            for i, username in enumerate(unique_users):
                if pd.isna(username) or str(username).strip() == '':
                    continue
                    
                username_clean = str(username).strip()[:100]
                base_email = f"{username_clean.replace(' ', '_').lower()}@gmaps.sumedang.com"
                
                # Check if user already exists in current batch
                if username in user_map:
                    continue
                
                # SOLUSI: Jika email sudah dipakai, tambahkan suffix unik
                email = base_email
                counter = 1
                while email in used_emails:
                    email = f"{username_clean.replace(' ', '_').lower()}_{counter}@gmaps.sumedang.com"
                    counter += 1
                
                used_emails.add(email)
                
                user = User(
                    name=username_clean,
                    email=email[:255],
                    preferences="alam,kuliner,budaya"
                )
                db.add(user)
                user_map[username] = user
                created_count += 1
                
                # Commit in smaller batches
                if created_count % batch_size == 0:
                    try:
                        await db.commit()
                        print(f"   [INFO] Progress: {created_count:,}/{len(unique_users):,} users created...")
                    except Exception as e:
                        print(f"   [WARN] Batch commit error (continuing): {str(e)[:100]}")
                        await db.rollback()
            
            # Final commit for remaining users
            try:
                await db.commit()
            except Exception as e:
                print(f"   [WARN] Final commit error: {str(e)[:100]}")
                await db.rollback()
            
            # Refresh user_map with committed IDs
            print("   [INFO] Loading user IDs from database...")
            result = await db.execute(
                select(User).where(User.email.like('%@gmaps.sumedang.com'))
            )
            db_users = result.scalars().all()
            
            # Re-map by username untuk lookup
            user_id_map = {}
            for u in db_users:
                # Map dengan name asli (sudah ter-clean saat create)
                user_id_map[u.name] = u.id
                # JUGA map dengan lowercase untuk fallback
                user_id_map[u.name.lower()] = u.id
                # Map dengan truncated name (first 100 chars)
                user_id_map[u.name[:100]] = u.id
            
            print(f"   [OK] {len(db_users):,} user IDs loaded with {len(user_id_map):,} lookup keys\n")
            
            # 4. Import reviews, ratings, and interactions
            print("[4/4] Importing reviews, ratings, and interactions...")
            
            # Clear existing data
            print("   [WARN] Clearing existing reviews/ratings/interactions...")
            await db.execute(delete(Review))
            await db.execute(delete(Rating))
            await db.execute(delete(UserInteraction))
            await db.commit()
            
            review_count = 0
            rating_count = 0
            interaction_count = 0
            skipped = 0
            
            # Base time for interactions (spread over last 2 years)
            base_time = datetime.now()
            
            for idx, row in df.iterrows():
                place_name = str(row.get('place', '')).strip()
                username = row.get('user')
                review_text = str(row.get('review', '')).strip()
                
                try:
                    rating_value = float(row.get('rating', 0))
                    if rating_value < 1 or rating_value > 5:
                        rating_value = 4.0  # Default
                except (ValueError, TypeError):
                    rating_value = 4.0
                
                # Find destination and user IDs
                dest_id = destinations.get(place_name)
                
                # Try multiple username formats for lookup
                username_str = str(username).strip()
                user_id = (
                    user_id_map.get(username_str) or  # Exact match
                    user_id_map.get(username_str.lower()) or  # Lowercase match
                    user_id_map.get(username_str[:100])  # Truncated match
                )
                
                # If destination not found, skip
                if not dest_id:
                    skipped += 1
                    continue
                
                # If user not found, CREATE NEW USER on-the-fly
                if not user_id:
                    username_clean = username_str[:100]
                    base_email = f"{username_clean.replace(' ', '_').lower()}@gmaps.sumedang.com"
                    
                    # Check if email already exists in used_emails
                    email = base_email
                    counter = 1
                    while email in used_emails:
                        email = f"{username_clean.replace(' ', '_').lower()}_{counter}@gmaps.sumedang.com"
                        counter += 1
                    used_emails.add(email)
                    
                    # Create new user
                    new_user = User(
                        name=username_clean,
                        email=email[:255],
                        preferences='alam,kuliner,budaya'
                    )
                    db.add(new_user)
                    await db.flush()  # Get ID without committing
                    
                    # Add to mapping
                    user_id = new_user.id
                    user_id_map[username_str] = user_id
                    user_id_map[username_str.lower()] = user_id
                    user_id_map[username_str[:100]] = user_id
                
                # Random timestamp (spread over 2 years)
                days_ago = random.randint(1, 730)
                interaction_time = base_time - timedelta(days=days_ago)
                
                # 1. Create Review (if has text)
                if review_text and review_text != 'nan' and len(review_text) > 10:
                    review = Review(
                        user_id=user_id,
                        destination_id=dest_id,
                        title=f"Review {place_name[:50]}",
                        content=review_text[:2000],  # Limit to 2000 chars
                        created_at=interaction_time
                    )
                    db.add(review)
                    review_count += 1
                
                # 2. Create Rating
                rating = Rating(
                    user_id=user_id,
                    destination_id=dest_id,
                    rating=rating_value,
                    created_at=interaction_time
                )
                db.add(rating)
                rating_count += 1
                
                # 3. Create UserInteraction (for MAB training)
                interaction = UserInteraction(
                    user_id=user_id,
                    interaction_type='rating',  # Type as string
                    entity_type='destination',
                    entity_id=dest_id,
                    extra_data=f'{{"rating": {rating_value}}}',  # Store rating in extra_data as JSON string
                    created_at=interaction_time
                )
                db.add(interaction)
                interaction_count += 1
                
                # Commit in batches
                if (idx + 1) % batch_size == 0:
                    await db.commit()
                    print(f"   [INFO] Progress: {idx+1:,}/{len(df):,} rows processed...")
                    print(f"      Reviews: {review_count:,} | Ratings: {rating_count:,} | Interactions: {interaction_count:,}")
            
            # Final commit
            await db.commit()
            
            print(f"\n" + "="*80)
            print("[SUCCESS] IMPORT COMPLETED!")
            print("="*80)
            print(f"[STATS] FINAL STATISTICS:")
            print(f"   • Users created:       {len(user_map):,}")
            print(f"   • Reviews added:       {review_count:,}")
            print(f"   • Ratings added:       {rating_count:,}")
            print(f"   • Interactions added:  {interaction_count:,}")
            print(f"   • Skipped (no match):  {skipped:,}")
            print(f"\n   [TOTAL] INTERACTIONS: {rating_count + interaction_count:,}")
            print("="*80)
            
            print("\n[NEXT] Next Steps:")
            print("   1. Re-train models: python train_models_once.py")
            print("   2. Restart backend to load new models")
            print("   3. Models will now match notebook evaluation!\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            await db.rollback()
        finally:
            break

if __name__ == "__main__":
    asyncio.run(import_all_data())

