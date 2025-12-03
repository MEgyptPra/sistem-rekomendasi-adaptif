"""
Script to seed categories, destination_categories mapping, and reviews from Excel
Melengkapi data yang masih kosong
"""
import asyncio
import pandas as pd
from pathlib import Path
from sqlalchemy import select
from app.core.db import get_db
from app.models.destinations import Destination
from app.models.category import Category
from app.models.review import Review
from app.models.user import User

# Path ke file Excel
EXCEL_DIR = Path(__file__).parent.parent / "data"
REVIEWS_FILE = EXCEL_DIR / "sumedang reviews.xlsx"

# 8 Kategori Wisata Sumedang
CATEGORIES = [
    {
        "name": "Wisata Alam",
        "description": "Destinasi wisata alam seperti gunung, air terjun, waduk, dan pemandangan alam"
    },
    {
        "name": "Wisata Religi",
        "description": "Tempat ziarah, makam keramat, dan destinasi bernuansa spiritual"
    },
    {
        "name": "Wisata Buatan/Rekreasi",
        "description": "Tempat rekreasi buatan manusia seperti taman, resto, villa, dan spot foto"
    },
    {
        "name": "Wisata Budaya & Sejarah",
        "description": "Situs bersejarah, museum, monumen, dan peninggalan budaya"
    },
    {
        "name": "Wisata Keluarga",
        "description": "Destinasi ramah keluarga dengan aktivitas untuk segala usia"
    },
    {
        "name": "Wisata Kesehatan & Wellness",
        "description": "Pemandian air panas, spa, dan tempat untuk relaksasi dan kesehatan"
    },
    {
        "name": "Wisata Petualangan",
        "description": "Aktivitas menantang seperti hiking, camping, dan olahraga outdoor"
    },
    {
        "name": "Wisata Kuliner",
        "description": "Tempat kuliner khas Sumedang dan pengalaman gastronomi"
    }
]

async def seed_categories_and_mappings():
    """Seed categories and map to destinations"""
    print("\n" + "="*60)
    print("🏷️  SEEDING CATEGORIES & MAPPINGS")
    print("="*60 + "\n")
    
    async for db in get_db():
        try:
            # 1. Insert Categories
            print("📁 Menambahkan kategori wisata...")
            categories = {}
            
            for cat_data in CATEGORIES:
                # Check if exists
                result = await db.execute(
                    select(Category).where(Category.name == cat_data["name"])
                )
                existing = result.scalars().first()
                
                if not existing:
                    category = Category(**cat_data)
                    db.add(category)
                    await db.flush()
                    categories[cat_data["name"]] = category
                else:
                    categories[cat_data["name"]] = existing
            
            await db.commit()
            print(f"   ✅ Berhasil menambahkan {len(categories)} kategori")
            
            # Map Destinations to Categories
            print("🔗 Mapping destinasi ke kategori...")
            result = await db.execute(select(Destination))
            destinations = result.scalars().all()
            
            mapping_count = 0
            from sqlalchemy import delete, insert
            from app.models.destinations import destination_categories
            
            for dest in destinations:
                if dest.category and dest.category in categories:
                    # Delete existing mappings for this destination
                    await db.execute(
                        delete(destination_categories).where(
                            destination_categories.c.destination_id == dest.id
                        )
                    )
                    # Insert new mapping
                    await db.execute(
                        insert(destination_categories).values(
                            destination_id=dest.id,
                            category_id=categories[dest.category].id
                        )
                    )
                    mapping_count += 1
            
            await db.commit()
            print(f"   ✅ Berhasil mapping {mapping_count} destinasi ke kategori")
            
            print("\n" + "="*60)
            print("✅ SEEDING CATEGORIES BERHASIL!")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            await db.rollback()
        finally:
            break

async def seed_reviews_from_excel():
    """Seed reviews from Excel file"""
    print("\n" + "="*60)
    print("📝 SEEDING REVIEWS FROM EXCEL")
    print("="*60 + "\n")
    
    async for db in get_db():
        try:
            # Read Excel
            print("📖 Membaca file sumedang reviews.xlsx...")
            df = pd.read_excel(REVIEWS_FILE)
            print(f"   ✅ Berhasil membaca {len(df)} reviews")
            print(f"   Kolom: {list(df.columns)}")
            
            # Get all destinations and users
            dest_result = await db.execute(select(Destination))
            destinations = {d.name: d for d in dest_result.scalars().all()}
            
            user_result = await db.execute(select(User))
            users = list(user_result.scalars().all())
            
            if not users:
                print("   ⚠️  Tidak ada user, membuat user default...")
                default_user = User(
                    name="Anonymous",
                    email="anonymous@sumedang.com",
                    preferences="alam,kuliner"
                )
                db.add(default_user)
                await db.flush()
                users = [default_user]
            
            # Process reviews
            print("💬 Memproses reviews...")
            review_count = 0
            skipped = 0
            
            # Sample: ambil max 500 reviews untuk tidak overload
            sample_size = min(500, len(df))
            df_sample = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
            
            for idx, row in df_sample.iterrows():
                place_name = str(row.get('place', '')).strip()
                review_text = str(row.get('review', '')).strip()
                try:
                    rating = float(row.get('rating', 4.0))
                except (ValueError, TypeError):
                    rating = 4.0  # Default rating if conversion fails
                
                # Find matching destination
                dest = destinations.get(place_name)
                
                if dest and review_text and review_text != 'nan':
                    # Assign to random user
                    user = users[review_count % len(users)]
                    
                    review = Review(
                        user_id=user.id,
                        destination_id=dest.id,
                        title=f"Review {place_name}",
                        content=review_text[:1000]  # Limit to 1000 chars
                    )
                    db.add(review)
                    review_count += 1
                else:
                    skipped += 1
                
                # Commit in batches
                if review_count % 100 == 0:
                    await db.commit()
                    print(f"   📝 Progress: {review_count} reviews added...")
            
            await db.commit()
            print(f"\n   ✅ Berhasil menambahkan {review_count} reviews")
            print(f"   ⚠️  Skipped {skipped} reviews (no matching destination or empty)")
            
            print("\n" + "="*60)
            print("✅ SEEDING REVIEWS BERHASIL!")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            await db.rollback()
        finally:
            break

async def main():
    """Main function to run all seeding"""
    print("\n" + "="*80)
    print("🚀 MELENGKAPI DATA SUMEDANG")
    print("="*80)
    
    # 1. Seed categories and mappings
    await seed_categories_and_mappings()
    
    # 2. Seed reviews from Excel
    await seed_reviews_from_excel()
    
    print("\n" + "="*80)
    print("🎉 SEMUA DATA BERHASIL DILENGKAPI!")
    print("="*80)
    print("\n💡 Selanjutnya:")
    print("   1. Retrain models: docker exec pariwisata-recommender-backend-1 python train_models_once.py")
    print("   2. Restart backend: docker restart pariwisata-recommender-backend-1\n")

if __name__ == "__main__":
    asyncio.run(main())
