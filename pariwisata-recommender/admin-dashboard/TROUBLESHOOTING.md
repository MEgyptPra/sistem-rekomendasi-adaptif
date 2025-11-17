# 🔧 Admin Dashboard Troubleshooting Guide

## ❌ Error: 401 Unauthorized

### Penyebab:
- Token tidak dikirim ke backend
- Token expired
- Belum login
- Backend tidak recognize token

### Solusi:

#### 1. Clear Browser Storage & Login Ulang
```javascript
// Buka Browser Console (F12)
localStorage.clear();
// Refresh page (Ctrl+R) dan login lagi
```

#### 2. Verify Token Ada
```javascript
// Di Browser Console
console.log(localStorage.getItem('adminToken'));
// Should show JWT token string
```

#### 3. Check API Service Mengirim Header
```javascript
// Di Network tab (F12), check request headers:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 4. Verify Backend Running
```bash
# Test endpoint
curl http://localhost:8000/
curl http://localhost:8000/admin/stats
```

---

## ❌ Error: Network Error / Failed to fetch

### Penyebab:
- Backend tidak running
- CORS issue
- Port salah

### Solusi:

#### 1. Check Backend Running
```bash
# Terminal check
curl http://localhost:8000/

# Expected response:
{"message":"Pariwisata API is running","status":"ok","version":"1.0.0"}
```

#### 2. Verify .env Configuration
```bash
# File: admin-dashboard/.env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ADMIN_URL=http://localhost:3000
```

#### 3. Check CORS in Backend
```python
# File: backend/main.py
allow_origins=[
    "http://localhost:3000",  # ← Must include admin dashboard
    "http://localhost:5173",
    "http://localhost:8000"
]
```

#### 4. Restart Both Services
```bash
# Stop all
# Then start again
start_all.bat
```

---

## ⚠️ Warning: MUI Grid deprecated props

### Error Messages:
```
MUI Grid: The `item` prop has been removed
MUI Grid: The `xs` prop has been removed
MUI Grid: The `sm` prop has been removed
MUI Grid: The `md` prop has been removed
```

### Penyebab:
Material-UI v7 menggunakan Grid v2 yang berbeda API

### Solusi:
Warnings ini **tidak mempengaruhi functionality**, hanya deprecated warnings. Akan diperbaiki di update selanjutnya.

**Temporary Fix**: Ignore warnings (app tetap jalan normal)

---

## ❌ Error: Cannot read property of undefined

### Penyebab:
- API response structure berbeda dari expected
- Data belum loaded

### Solusi:

#### 1. Check API Response di Network Tab
```
F12 → Network → Click request → Preview tab
```

#### 2. Add Safe Navigation
```javascript
// Before
const name = user.profile.name;

// After
const name = user?.profile?.name || 'N/A';
```

#### 3. Check Loading States
Pastikan loading state sudah handle dengan benar sebelum render data

---

## ❌ Page Blank / White Screen

### Penyebab:
- JavaScript error
- Import error
- Component crash

### Solusi:

#### 1. Check Browser Console (F12)
Look for red error messages

#### 2. Check Import Statements
```javascript
// Make sure all imports correct
import apiService from '../services/api';
```

#### 3. Clear Cache & Rebuild
```bash
cd admin-dashboard

# Clear cache
rm -rf node_modules
rm package-lock.json

# Reinstall
npm install

# Start again
npm start
```

---

## ❌ Login Failed

### Penyebab:
- Wrong credentials
- Backend admin_routes.py issue

### Solusi:

#### 1. Verify Credentials
```
Email: admin@example.com
Password: admin123
```

#### 2. Check Backend Admin Routes
```bash
# File: backend/admin_routes.py
# Line ~40-50
admin_user = {
    "email": "admin@example.com",
    "password": "admin123",
    ...
}
```

#### 3. Test Login Endpoint Directly
```bash
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Expected: { "access_token": "...", "token_type": "bearer" }
```

---

## ❌ Data Tidak Muncul (Empty Table)

### Penyebab:
- Database kosong
- API endpoint belum return data
- Transformation error

### Solusi:

#### 1. Check Database Has Data
```bash
cd backend
python seed_activities.py
```

#### 2. Test API Endpoint
```bash
# Login first to get token
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Use token to get data
curl http://localhost:8000/admin/destinations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### 3. Check Browser Console
```
F12 → Console
Look for:
- API Response: {...}
- Any error messages
```

---

## ❌ Port Already in Use

### Error:
```
Error: listen EADDRINUSE: address already in use :::3000
```

### Solusi:

#### Option 1: Kill Process on Port 3000
```powershell
# Windows PowerShell
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

#### Option 2: Change Port
```bash
# File: admin-dashboard/.env
PORT=3001  # or any available port

# Update start_all.bat accordingly
```

---

## 🔄 Complete Reset Procedure

Jika semua cara di atas tidak berhasil:

### 1. Stop All Services
```bash
# Close all terminal windows
# Or press Ctrl+C on each
```

### 2. Clean Admin Dashboard
```bash
cd admin-dashboard
rm -rf node_modules
rm package-lock.json
rm -rf build
```

### 3. Clean Backend Cache
```bash
cd backend
rm -rf __pycache__
rm -rf app/__pycache__
```

### 4. Reinstall Dependencies
```bash
# Admin dashboard
cd admin-dashboard
npm install

# Backend (if needed)
cd backend
pip install -r requirements.txt
```

### 5. Restart Everything
```bash
cd pariwisata-recommender
start_all.bat
```

---

## 📊 Debug Checklist

- [ ] Backend running on port 8000
- [ ] Admin dashboard running on port 3000
- [ ] No CORS errors in console
- [ ] Token exists in localStorage
- [ ] API calls show Authorization header
- [ ] Backend logs show no errors
- [ ] Database has data

---

## 🆘 Still Having Issues?

### Check These Files:

1. **Admin Dashboard API Service**
   ```bash
   cat admin-dashboard/src/services/api.js
   # Should have apiService with all methods
   ```

2. **Environment Variables**
   ```bash
   cat admin-dashboard/.env
   # Should have REACT_APP_API_URL=http://localhost:8000
   ```

3. **Backend CORS**
   ```bash
   cat backend/main.py
   # Line ~35-45, should include "http://localhost:3000"
   ```

4. **Admin Routes**
   ```bash
   cat backend/admin_routes.py
   # Should have admin_router with all endpoints
   ```

### Test Flow:

1. **Backend Health**
   ```bash
   curl http://localhost:8000/
   # Should return {"message":"...","status":"ok"}
   ```

2. **Admin Login**
   ```bash
   curl -X POST http://localhost:8000/admin/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@example.com","password":"admin123"}'
   # Should return access_token
   ```

3. **Get Data with Token**
   ```bash
   curl http://localhost:8000/admin/stats \
     -H "Authorization: Bearer YOUR_TOKEN"
   # Should return stats object
   ```

---

## ✅ Success Indicators

When everything works correctly:

1. ✅ Login page appears at http://localhost:3000
2. ✅ Can login with admin credentials
3. ✅ Dashboard shows stats cards
4. ✅ Destinations page shows table
5. ✅ No 401 errors in console
6. ✅ No CORS errors in console
7. ✅ All API calls return 200 OK

---

**Last Updated**: After fixing 401 Unauthorized error by implementing centralized apiService
