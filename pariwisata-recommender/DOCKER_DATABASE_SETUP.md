# 🐳 Setup Database PostgreSQL dengan Docker

## 📋 Prerequisites

1. **Docker Desktop** harus ter-install
2. **Docker Desktop** harus berjalan

## 🚀 Quick Start

### 1. Start Docker Desktop
```
Buka aplikasi Docker Desktop
Tunggu sampai status "Docker Desktop is running"
```

### 2. Start PostgreSQL Container
```powershell
cd C:\Users\ACER\Documents\GitHub\sistem-rekomendasi-adaptif\pariwisata-recommender
docker-compose up -d db
```

### 3. Verify Container Running
```powershell
docker ps
```

Harusnya muncul:
```
CONTAINER ID   IMAGE         PORTS                    NAMES
xxxxx          postgres:15   0.0.0.0:5432->5432/tcp   pariwisata-recommender-db-1
```

### 4. Test Connection
```powershell
cd backend
python -c "import asyncio; from app.core.db import engine; from sqlalchemy import text; asyncio.run((lambda: engine.connect()).__call__())"
```

## 🔧 Troubleshooting

### Error: "The system cannot find the file specified"
**Penyebab**: Docker Desktop tidak berjalan

**Solusi**:
1. Buka Docker Desktop
2. Tunggu sampai fully started
3. Try command lagi

### Error: "port 5432 already in use"
**Penyebab**: PostgreSQL lain sudah running di port 5432

**Solusi Option 1** - Stop PostgreSQL lain:
```powershell
# Cek process di port 5432
netstat -ano | findstr :5432

# Kill process (ganti PID dengan hasil di atas)
taskkill /PID <PID> /F
```

**Solusi Option 2** - Gunakan port berbeda:
Edit `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Host:Container
```

Lalu update `.env`:
```properties
DATABASE_URL=postgresql+asyncpg://user:rekompari@localhost:5433/pariwisata
```

### Error: "connection refused"
**Penyebab**: Container belum fully started

**Solusi**:
```powershell
# Check logs
docker-compose logs db

# Restart container
docker-compose restart db
```

## 📊 Database Info

**Credentials** (dari docker-compose.yml):
```
Host: localhost
Port: 5432
Database: pariwisata
User: user
Password: rekompari
```

**Connection String**:
```
postgresql+asyncpg://user:rekompari@localhost:5432/pariwisata
```

## 🗄️ Database Management

### Connect ke Database
```powershell
docker exec -it pariwisata-recommender-db-1 psql -U user -d pariwisata
```

### Useful psql Commands
```sql
\dt              -- List tables
\d tablename     -- Describe table
\l               -- List databases
\du              -- List users
\q               -- Exit
```

### View Data
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM destinations;
SELECT COUNT(*) FROM ratings;

SELECT * FROM users LIMIT 5;
SELECT * FROM destinations LIMIT 5;
```

### Backup Database
```powershell
docker exec pariwisata-recommender-db-1 pg_dump -U user pariwisata > backup.sql
```

### Restore Database
```powershell
docker exec -i pariwisata-recommender-db-1 psql -U user -d pariwisata < backup.sql
```

## 🔄 Container Management

### Start
```powershell
docker-compose up -d db
```

### Stop
```powershell
docker-compose stop db
```

### Restart
```powershell
docker-compose restart db
```

### Remove (⚠️ Data akan hilang!)
```powershell
docker-compose down db
# atau dengan volumes
docker-compose down -v
```

### View Logs
```powershell
docker-compose logs db
# atau follow logs
docker-compose logs -f db
```

## 📝 Create Tables & Seed Data

### 1. Create Tables
```powershell
cd backend
python setup_database.py
# Pilih opsi 2 (Create tables)
```

### 2. Seed Data
```powershell
# Data Sumedang
python seed_sumedang_data.py

# atau Test Data
python seed_test_data.py
```

## ✅ Verification Checklist

- [ ] Docker Desktop running
- [ ] Container `pariwisata-recommender-db-1` running
- [ ] Port 5432 accessible
- [ ] Tables created
- [ ] Data seeded
- [ ] Backend can connect (no errors in logs)
- [ ] Admin dashboard showing `dataSource: "database"`

## 🎯 Integration with Backend

Setelah database ready:

1. **Restart backend** agar koneksi ter-establish
2. **Refresh admin dashboard** (F5)
3. **Check response** - harusnya `dataSource: "database"`

Backend akan otomatis connect ke database jika:
- ✅ Docker container running
- ✅ Port 5432 accessible
- ✅ Credentials benar di `.env`
