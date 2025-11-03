# 🔐 Kredensial Login Admin Dashboard

## Informasi Akun Admin Default

Gunakan kredensial berikut untuk login ke Admin Dashboard:

```
Email    : admin@example.com
Password : admin123
```

## 🚀 Cara Mengakses Admin Dashboard

### 1. Jalankan Backend (Port 8000)
```powershell
cd pariwisata-recommender\backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend akan berjalan di: **http://localhost:8000**

### 2. Jalankan Admin Dashboard (Port 3001)
```powershell
cd pariwisata-recommender\admin-dashboard
npm install
npm start
```

Admin Dashboard akan berjalan di: **http://localhost:3001/login**

### 3. Jalankan Frontend User (Port 5173)
```powershell
cd pariwisata-recommender\frontend
npm install
npm run dev
```

Frontend akan berjalan di: **http://localhost:5173**

## 📋 URL Akses

| Service | URL | Deskripsi |
|---------|-----|-----------|
| Backend API | http://localhost:8000 | REST API Server |
| Admin Dashboard | http://localhost:3001/login | Panel Admin |
| Frontend User | http://localhost:5173 | Website User |
| API Docs | http://localhost:8000/docs | Dokumentasi API (Swagger) |

## 🔑 Endpoint Admin API

- **POST** `/admin/login` - Login admin
- **GET** `/admin/stats` - Statistik dashboard
- **GET** `/admin/activity-stats` - Statistik aktivitas

## ⚠️ Catatan Keamanan

> **PENTING**: Kredensial ini adalah default untuk development. 
> Untuk production, pastikan untuk:
> - Mengganti password default
> - Menggunakan hashed password (bcrypt)
> - Menggunakan SECRET_KEY yang aman
> - Mengaktifkan HTTPS
> - Implementasi rate limiting

## 🔧 Troubleshooting

### Backend tidak bisa diakses
- Pastikan port 8000 tidak digunakan aplikasi lain
- Check firewall settings
- Jalankan dengan `--reload` untuk auto-restart saat development

### Login gagal
- Pastikan backend sudah berjalan
- Check CORS settings di backend
- Buka browser console untuk lihat error details

### Admin dashboard tidak muncul
- Clear browser cache
- Check console untuk error
- Pastikan npm dependencies sudah terinstall

## 📞 Support

Jika ada masalah, check:
1. Terminal output untuk error messages
2. Browser console (F12)
3. Network tab di browser DevTools
