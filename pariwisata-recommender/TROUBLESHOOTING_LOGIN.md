# 🔧 Troubleshooting Login Admin Dashboard

## ✅ Status Saat Ini

### Backend Server
- **Status**: ✅ Running
- **URL**: http://localhost:8000
- **Port**: 8000

### Admin Dashboard
- **URL Login**: http://localhost:3001/login
- **Port**: 3001

## 🔑 Kredensial Login

```
Email    : admin@example.com
Password : admin123
```

## 📋 Checklist Sebelum Login

### 1. Backend HARUS Berjalan
Jalankan di terminal terpisah:
```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Atau gunakan batch file:
```powershell
C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend\start_backend.bat
```

### 2. Admin Dashboard HARUS Berjalan  
Jalankan di terminal terpisah:
```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\admin-dashboard
npm start
```

Admin dashboard akan berjalan di http://localhost:3001

### 3. Cek Koneksi Backend
Buka browser dan akses: http://localhost:8000/
Harusnya muncul:
```json
{"message": "Pariwisata API is running", "status": "ok"}
```

## 🐛 Debugging Login Failed

### Jika Login Gagal, Cek:

#### 1. Browser Developer Tools
- Tekan `F12` untuk buka DevTools
- Pergi ke tab **Console** - lihat error messages
- Pergi ke tab **Network** - lihat request ke `/admin/login`

#### 2. Cek Request di Network Tab
Setelah klik Login, cari request ke `http://localhost:8000/admin/login`:
- **Status 200**: Login berhasil ✅
- **Status 401**: Email/password salah ❌
- **Status 0** atau **CORS error**: Backend tidak berjalan atau CORS issue ❌
- **Failed to fetch**: Backend tidak bisa diakses ❌

#### 3. Common Errors & Solutions

| Error | Penyebab | Solusi |
|-------|----------|--------|
| "Failed to fetch" | Backend tidak berjalan | Start backend di port 8000 |
| "CORS policy" | CORS tidak dikonfigurasi | Sudah diperbaiki di main.py |
| "401 Unauthorized" | Email/password salah | Gunakan `admin@example.com` / `admin123` |
| "Network Error" | Port salah | Pastikan backend di port 8000 |

#### 4. Test Login Manual dengan cURL
Buka terminal baru dan jalankan:
```powershell
curl -X POST http://localhost:8000/admin/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@example.com","password":"admin123"}'
```

Harusnya return:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

## 🔍 Verifikasi Sistem

### Cek Backend Status
```powershell
# Test root endpoint
curl http://localhost:8000/

# Test login endpoint
curl -X POST http://localhost:8000/admin/login -H "Content-Type: application/json" -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

### Cek Port yang Digunakan
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :3001
```

## 📝 Langkah-Langkah Login

1. ✅ Pastikan backend berjalan di port 8000
2. ✅ Pastikan admin dashboard berjalan di port 3001
3. ✅ Buka browser ke http://localhost:3001/login
4. ✅ Masukkan email: `admin@example.com`
5. ✅ Masukkan password: `admin123`
6. ✅ Klik Login
7. ✅ Harusnya redirect ke dashboard

## 🆘 Jika Masih Gagal

1. **Clear browser cache** dan **cookies**
2. **Restart** kedua service (backend & admin dashboard)
3. **Cek browser console** untuk error spesifik
4. **Screenshot** error message dan share
5. **Check** apakah ada firewall/antivirus yang block port 8000

## 📞 Quick Commands

### Start Everything
```powershell
# Terminal 1: Backend
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Admin Dashboard
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender\admin-dashboard
npm start
```

### Test Login
```powershell
curl -X POST http://localhost:8000/admin/login -H "Content-Type: application/json" -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```
