#
# Nama File: seed_sumedang_data.py
# Deskripsi: Script untuk mengisi database dengan data pariwisata Sumedang dari file CSV.
#
# Instruksi untuk menjalankan:
# 1. Pastikan file-file CSV berikut ada di folder yang sama dengan skrip ini:
#    - destinations.csv
#    - categories.csv
#    - destination_categories.csv
#    - users.csv
#    - ratings.csv
# 2. Pastikan Anda sudah mengupdate model 'rating.py' dan 'review.py' dengan kolom 'created_at'.
# 3. Jalankan script ini dari terminal di dalam folder 'backend':
#    python seed_sumedang_data.py
#

import asyncio
import pandas as pd
from sqlalchemy import text
from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.destinations import Destination
from app.models.category import Category
from app.models.rating import Rating
from app.models.review import Review
from app.models.destination_category import destination_categories


async def clear_data():
    async with AsyncSessionLocal() as db:
        print("🔄 Menghapus data lama dari database...")
        await db.execute(text("TRUNCATE TABLE destination_categories, reviews, ratings, users, categories, destinations RESTART IDENTITY CASCADE;"))
        await db.commit()
    print("✅ Data lama berhasil dihapus.")

async def seed_data():
    """
    Membaca semua file CSV yang telah diproses dan memasukkan datanya ke database.
    """
    # Selalu mulai dengan menghapus data lama untuk memastikan kebersihan data
    await clear_data()
    
    # --- PERBAIKAN DI SINI ---
    # Tentukan path ke folder tempat CSV disimpan
    csv_folder_path = '' 

    print(f"\n📚 Membaca file-file CSV dari direktori saat ini...")
    df_dest = pd.read_csv(csv_folder_path + 'destinations.csv') # Ini akan membaca 'destinations.csv'
    df_cat = pd.read_csv(csv_folder_path + 'categories.csv')
    df_dest_cat = pd.read_csv(csv_folder_path + 'destination_categories.csv')
    df_users = pd.read_csv(csv_folder_path + 'users.csv')
    df_ratings = pd.read_csv(csv_folder_path + 'ratings.csv')
    
    # Ubah kolom waktu menjadi objek datetime pandas
    df_ratings['review_time'] = pd.to_datetime(df_ratings['review_time'], errors='coerce')

    async with AsyncSessionLocal() as db:
        print("\n🌱 Memulai proses seeding data Sumedang...")

        print(f"   - Memasukkan {len(df_dest)} data Destinations...")
        for _, row in df_dest.iterrows():
            dest_description = row['description'] if pd.notna(row['description']) else ""
            
            dest = Destination(
                id=row['destination_id'], 
                name=row['name'], 
                description=dest_description, 
                lat=row['latitude'], 
                lon=row['longitude']
            )
            db.add(dest)
        await db.commit()

        print(f"   - Memasukkan {len(df_cat)} data Categories...")
        for _, row in df_cat.iterrows():
            cat = Category(id=row['category_id'], name=row['category_name'])
            db.add(cat)
        await db.commit()
        
        print(f"   - Memasukkan {len(df_dest_cat)} relasi Destination-Categories...")
        for _, row in df_dest_cat.iterrows():
            await db.execute(destination_categories.insert().values(destination_id=row['destination_id'], category_id=row['category_id']))
        await db.commit()

        print(f"   - Memasukkan {len(df_users)} data Users...")
        for _, row in df_users.iterrows():
            # Kita buat data dummy untuk kolom yang tidak ada di CSV
            user = User(id=row['user_id'], name=row['user_name'], email=f"{row['user_name']}@example.com")
            db.add(user)
        await db.commit()

        print(f"   - Memasukkan {len(df_ratings)} data Ratings & Reviews...")
        for _, row in df_ratings.iterrows():
            # Lewati baris jika data waktu atau ID tidak valid
            if pd.isna(row['review_time']) or pd.isna(row['user_id']) or pd.isna(row['destination_id']):
                continue
            
            review_text = row['review_text'] if pd.notna(row['review_text']) else ""
            
            # 2. Buat objek Rating dan Review dengan argumen yang benar
            rating = Rating(user_id=int(row['user_id']), destination_id=int(row['destination_id']), rating=row['rating'], created_at=row['review_time'])
            review = Review(user_id=int(row['user_id']), destination_id=int(row['destination_id']), content=review_text, created_at=row['review_time'])
            
            db.add_all([rating, review])
        await db.commit()

    print("\n🎉 --- Proses Seeding Data Sumedang Selesai! ---")

if __name__ == "__main__":
    # Jalankan fungsi utama
    asyncio.run(seed_data())