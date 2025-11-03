# 🚀 Quick Start Guide - Pariwisata Recommender

## Cara Menjalankan Semua Service

### ⭐ CARA TERMUDAH (RECOMMENDED)
**Double-click file `start_all.bat`** di folder `pariwisata-recommender`

Script ini akan otomatis:
1. ✅ Start PostgreSQL database (Docker)
2. ✅ Start Backend API server (Port 8000)
3. ✅ Start Admin Dashboard (Port 3000)
4. ✅ Buka browser ke Admin Dashboard

### 🛑 Cara Menghentikan
**Double-click file `stop_all.bat`**

---

### Manual (Jika ingin jalankan satu-satu)

#### 1. Start Database
```bash
cd pariwisata-recommender
docker-compose up -d db
```

#### 2. Start Backend
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 3. Start Admin Dashboard
```bash
cd admin-dashboard
npm start
```

## 🌐 URL Akses

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:3000

## 🔐 Login Credentials

- **Email**: admin@example.com
- **Password**: admin123

## 🛑 Cara Menghentikan Service

### Metode 1: Otomatis
Double-click file `stop_all.bat`

### Metode 2: Manual
- Tekan `CTRL+C` di setiap terminal window
- Atau tutup semua command prompt windows

## � Tentang Docker Desktop

**Q: Apakah perlu buka Docker Desktop manual?**  
**A: TIDAK!** `start_all.bat` sudah otomatis:
1. Cek apakah Docker Desktop running
2. Jika belum → Start otomatis
3. Tunggu sampai ready (30 detik)
4. Baru jalankan database

**Q: Docker Desktop untuk apa?**  
**A:** Menjalankan PostgreSQL database dalam container Docker.

## �📋 Port yang Digunakan

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| Admin Dashboard | 3000 | http://localhost:3000 |
| PostgreSQL DB | 5432 | Internal only |
| Frontend User | 5173 | http://localhost:5173 |

## ⚠️ Troubleshooting

### Database tidak bisa connect
- **OTOMATIS**: `start_all.bat` sudah auto-start Docker Desktop
- Jika masih error, restart database manual: `docker-compose restart db`
- Atau restart Docker Desktop dari system tray

### Error: "Cannot stop Docker Compose" / "ENOENT dockerBackendApiServer"
**Penyebab**: Docker Desktop daemon tidak merespons

**Solusi 1** - Gunakan force stop:
```
Double-click: force_stop_all.bat
```

**Solusi 2** - Manual:
1. Tutup Docker Desktop dari system tray (klik kanan → Quit)
2. Tunggu 10 detik
3. Buka Task Manager → Cari "Docker" → End Task semua
4. Restart Docker Desktop

### Port sudah digunakan
- Jalankan `stop_all.bat` terlebih dahulu
- Jika gagal, gunakan `force_stop_all.bat`
- Atau manually kill process di port tersebut

### Backend error "getaddrinfo failed"
- Database belum ready, tunggu 5-10 detik lalu restart backend
- Cek Docker container: `docker ps`
- Pastikan Docker Desktop benar-benar running

## 📝 Development Notes

- Backend menggunakan `reload=False` untuk stabilitas
- Database credentials ada di file `.env`
- CORS sudah dikonfigurasi untuk semua port yang dibutuhkan
