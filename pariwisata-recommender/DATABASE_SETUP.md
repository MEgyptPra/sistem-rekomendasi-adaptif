# 🗄️ Menghubungkan Admin Dashboard ke Database PostgreSQL

## 📋 Yang Sudah Dikonfigurasi

✅ Admin routes sudah diupdate untuk menggunakan database PostgreSQL  
✅ Endpoint `/admin/stats` sekarang mengambil data real dari database  
✅ Endpoint `/admin/users` menampilkan user dari database  
✅ Endpoint `/admin/destinations` menampilkan destinasi dari database  
✅ CORS sudah dikonfigurasi dengan benar  

## 🚀 Langkah-Langkah Setup Database

### 1. Jalankan PostgreSQL dengan Docker Compose

```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender
docker-compose up -d db
```

Ini akan start PostgreSQL container dengan:
- **User**: `user`
- **Password**: `rekompari`
- **Database**: `pariwisata`
- **Port**: `5432`

### 2. Verifikasi Database Berjalan

```powershell
docker ps
```

Harusnya muncul container `pariwisata-recommender-db-1` yang running.

### 3. Install Dependencies Python untuk Database

```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend
pip install asyncpg sqlalchemy[asyncio] python-dotenv
```

### 4. Test Koneksi Database

```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend
python setup_database.py
```

Pilih opsi 1 untuk test koneksi.

### 5. Create Database Tables (Jika Belum Ada)

```powershell
python setup_database.py
```

Pilih opsi 2 untuk create tables, atau opsi 3 untuk create tables dan test koneksi.

### 6. Seed Data (Isi Data Sample)

```powershell
# Jika sudah ada seed script
python seed_sumedang_data.py
# atau
python seed_test_data.py
```

### 7. Restart Backend

Stop backend yang sedang berjalan (Ctrl+C), lalu jalankan lagi:

```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Atau gunakan batch file:
```powershell
C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend\start_backend.bat
```

## 📊 Endpoint Admin yang Sudah Tersedia

### Stats & Analytics
- `GET /admin/stats` - Statistik total users, destinations, ratings
- `GET /admin/analytics` - Data analytics lengkap
- `GET /admin/activity-stats` - Statistik aktivitas per bulan

### Data Management
- `GET /admin/users` - List semua users dari database
- `GET /admin/destinations` - List semua destinasi dari database
- `GET /admin/activities` - List activities (placeholder)

## 🔧 Konfigurasi Database

File `.env` di folder `backend`:
```properties
DATABASE_URL=postgresql+asyncpg://user:rekompari@localhost:5432/pariwisata
```

**Ubah jika database Anda berbeda:**
- `user` - username PostgreSQL
- `rekompari` - password PostgreSQL  
- `localhost` - host database (gunakan `db` jika dari Docker)
- `5432` - port PostgreSQL
- `pariwisata` - nama database

## 🐛 Troubleshooting

### Database Connection Failed

**Error**: `Could not connect to database`

**Solusi**:
1. Pastikan PostgreSQL running:
   ```powershell
   docker-compose up -d db
   ```

2. Check container status:
   ```powershell
   docker ps | findstr postgres
   ```

3. Check logs:
   ```powershell
   docker-compose logs db
   ```

### Tables Not Found

**Error**: `relation "users" does not exist`

**Solusi**:
```powershell
python setup_database.py
# Pilih opsi 2 (Create tables)
```

### No Data Showing

**Solusi**:
Seed data ke database:
```powershell
python seed_sumedang_data.py
```

### Port 5432 Already in Use

**Solusi**:
Ada PostgreSQL lain yang running. Stop atau gunakan port berbeda di `docker-compose.yml`.

## 📝 Manual Database Check

### Connect ke PostgreSQL Container

```powershell
docker exec -it pariwisata-recommender-db-1 psql -U user -d pariwisata
```

### Query Manual

```sql
-- Check tables
\dt

-- Count users
SELECT COUNT(*) FROM users;

-- Count destinations
SELECT COUNT(*) FROM destinations;

-- Show sample data
SELECT * FROM users LIMIT 5;
SELECT * FROM destinations LIMIT 5;

-- Exit
\q
```

## ✅ Verifikasi Integrasi Berhasil

1. **Backend berjalan** di http://localhost:8000
2. **Database berjalan** di localhost:5432
3. **Test endpoint**:
   ```powershell
   curl http://localhost:8000/admin/stats
   ```
   Harusnya return data real dari database, bukan dummy data.

4. **Admin Dashboard** di http://localhost:3001 sekarang menampilkan data real!

## 🎯 Next Steps

Setelah database terhubung:
1. ✅ Dashboard akan menampilkan data real
2. ✅ User list akan dari database
3. ✅ Destination list akan dari database
4. ✅ Statistics akan akurat
5. Tambahkan CRUD operations untuk edit/delete data
6. Tambahkan pagination untuk data besar
7. Tambahkan search & filter functionality

## 🔐 Security Notes

⚠️ **PENTING untuk Production**:
- Ganti password database default (`rekompari`)
- Ganti SECRET_KEY di admin_routes.py
- Gunakan environment variables untuk credentials
- Enable SSL untuk database connection
- Implement proper user authentication dengan hashed passwords
