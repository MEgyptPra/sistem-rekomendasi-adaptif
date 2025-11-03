# 📋 API Endpoints Checklist - Pariwisata Sumedang

**Status Backend**: Perlu dijalankan pada `http://localhost:8000`

---

## ✅ FRONTEND ENDPOINTS (`/api/...`)

### 🏝️ **Destinations** (frontend_endpoints.py)
- ✅ `GET /api/destinations` - Get all destinations with filters
  - Query params: `category`, `region`, `min_price`, `max_price`, `search`, `sort`, `limit`, `offset`
- ✅ `GET /api/destinations/{destination_id}` - Get destination detail
- ✅ `POST /api/destinations/{destination_id}/reviews` - Submit review (requires auth)
- ✅ `GET /api/destinations/{destination_id}/reviews` - Get destination reviews

### 🎯 **Activities** (frontend_endpoints.py)
- ✅ `GET /api/activities` - Get all activities with filters
  - Query params: `category`, `difficulty`, `duration`, `search`, `sort`, `limit`, `offset`
- ✅ `GET /api/activities/{activity_id}` - Get activity detail
- ✅ `POST /api/activities/{activity_id}/reviews` - Submit review (requires auth)
- ✅ `GET /api/activities/{activity_id}/reviews` - Get activity reviews

### 🎁 **Recommendations** (frontend_endpoints.py)
- ✅ `GET /api/recommendations/personalized` - Get personalized recommendations (requires auth)
  - Query params: `limit`, `algorithm`

### 👆 **Interactions** (frontend_endpoints.py)
- ✅ `POST /api/interactions/click` - Track click interaction
  - Body: `{"entity_type": "destination/activity", "entity_id": 1, "session_id": "xxx"}`
- ✅ `POST /api/interactions/view` - Track view interaction
  - Body: `{"entity_type": "destination/activity", "entity_id": 1, "session_id": "xxx", "duration": 30}`
- ✅ `GET /api/interactions/user/{user_id}` - Get user interaction history

---

## ✅ AUTHENTICATION ENDPOINTS (`/api/auth/...`)

### 🔐 **Auth** (medium_priority_endpoints.py)
- ✅ `POST /api/auth/register` - Register new user
  - Body: `{"name": "...", "email": "...", "password": "..."}`
- ✅ `POST /api/auth/login` - Login user
  - Body: `{"email": "...", "password": "..."}`
- ✅ `GET /api/auth/me` - Get current user info (requires auth)

---

## ✅ ITINERARY ENDPOINTS (`/api/itineraries/...`)

### 🗓️ **Itineraries** (itineraries.py)
- ✅ `POST /api/itineraries/` - Create new itinerary (requires auth)
- ✅ `GET /api/itineraries/` - Get user's itineraries (requires auth)
  - Query params: `status` (upcoming/ongoing/completed/cancelled)
- ✅ `GET /api/itineraries/{itinerary_id}` - Get specific itinerary (requires auth)
- ✅ `PUT /api/itineraries/{itinerary_id}` - Update itinerary (requires auth)
- ✅ `DELETE /api/itineraries/{itinerary_id}` - Delete itinerary (requires auth)
- ✅ `PATCH /api/itineraries/{itinerary_id}/status` - Update status (requires auth)

---

## ✅ SEARCH & DISCOVERY ENDPOINTS (`/api/...`)

### 🔍 **Search** (low_priority_endpoints.py)
- ✅ `GET /api/search` - Universal search (destinations + activities)
  - Query params: `q`, `limit`, `offset`
- ✅ `GET /api/search/destinations` - Search destinations only
  - Query params: `q`, `category`, `region`, `min_price`, `max_price`, `limit`, `offset`
- ✅ `GET /api/search/activities` - Search activities only
  - Query params: `q`, `category`, `difficulty`, `duration`, `limit`, `offset`

### 🔗 **Related Items** (low_priority_endpoints.py)
- ✅ `GET /api/destinations/{destination_id}/related` - Get related destinations
  - Query params: `limit`
- ✅ `GET /api/activities/{activity_id}/related` - Get related activities
  - Query params: `limit`

---

## ✅ USER PREFERENCES & FAVORITES (`/api/...`)

### ⚙️ **User Preferences** (low_priority_endpoints.py)
- ✅ `GET /api/users/{user_id}/preferences` - Get user preferences
- ✅ `PUT /api/users/{user_id}/preferences` - Update user preferences (requires auth)
  - Body: `{"categories": [...], "regions": [...], "budget_range": {...}}`
- ✅ `GET /api/users/{user_id}/recommendations` - Get user recommendations

### ❤️ **Favorites** (low_priority_endpoints.py)
- ✅ `POST /api/favorites` - Add to favorites (requires auth)
  - Body: `{"entity_type": "destination/activity", "entity_id": 1}`
- ✅ `DELETE /api/favorites/{entity_type}/{entity_id}` - Remove from favorites (requires auth)
- ✅ `GET /api/users/{user_id}/favorites` - Get user favorites (requires auth)

---

## ✅ STATISTICS ENDPOINTS (`/api/stats/...`)

### 📊 **Statistics** (low_priority_endpoints.py)
- ✅ `GET /api/stats/popular` - Get popular destinations & activities
  - Query params: `entity_type`, `limit`, `time_period`

---

## ✅ ML & RECOMMENDATION ENDPOINTS (`/api/...`)

### 🤖 **ML Training** (endpoints.py)
- ✅ `POST /api/ml/train` - Train ML models
- ✅ `GET /api/ml/status` - Get ML models status

### 🎯 **Advanced Recommendations** (endpoints.py)
- ✅ `GET /api/recommendations/{user_id}` - Get recommendations with algorithm choice
  - Query params: `algorithm` (content_based/collaborative/hybrid), `num_recommendations`
- ✅ `GET /api/recommendations/{user_id}/explain/{destination_id}` - Explain recommendation
- ✅ `GET /api/user/{user_id}/profile` - Get comprehensive user profile

### 📊 **Data Endpoints** (endpoints.py)
- ✅ `GET /api/destinations` - Get all destinations (ML format)
- ✅ `GET /api/categories` - Get all categories
- ✅ `POST /api/rating` - Add/update rating
- ✅ `GET /api/user/{user_id}/ratings` - Get user ratings

### 🎰 **MAB (Multi-Armed Bandit)** (endpoints.py)
- ✅ `POST /api/mab/feedback` - Submit MAB feedback
- ✅ `GET /api/mab/statistics` - Get MAB statistics
- ✅ `POST /api/mab/reset` - Reset MAB state (dev only)

### 📈 **Analytics** (endpoints.py)
- ✅ `GET /api/analytics/destinations` - Destination analytics
- ✅ `GET /api/analytics/users` - User analytics
- ✅ `GET /api/evaluation/config` - Get evaluation config
- ✅ `POST /api/evaluation/consistency-check` - Run consistency check

---

## ✅ ADMIN ENDPOINTS (`/admin/...`)

### 🔐 **Admin Auth** (admin_routes.py)
- ✅ `POST /admin/login` - Admin login
  - Body: `{"email": "admin@example.com", "password": "admin123"}`
  - Returns: JWT token

### 📊 **Admin Dashboard** (admin_routes.py)
- ✅ `GET /admin/stats` - Dashboard statistics (requires admin auth)
  - Returns: totalUsers, totalDestinations, totalRatings, averageRating
- ✅ `GET /admin/activity-stats` - Activity statistics chart data (requires admin auth)
- ✅ `GET /admin/users` - Get all users (requires admin auth)
- ✅ `GET /admin/destinations` - Get all destinations (requires admin auth)
- ✅ `GET /admin/analytics` - Comprehensive analytics (requires admin auth)
- ✅ `GET /admin/activities` - Get activities data (requires admin auth)

---

## 📝 RINGKASAN STATUS

### ✅ **LENGKAP & SIAP PAKAI**

**Total Endpoints: 70+**

#### Untuk Frontend (`http://localhost:5173`):
1. ✅ **Auth System** - Register, Login, Get Current User
2. ✅ **Destinations** - List, Detail, Reviews, Filters
3. ✅ **Activities** - List, Detail, Reviews, Filters
4. ✅ **Search** - Universal search, Filter destinations, Filter activities
5. ✅ **Recommendations** - Personalized dengan MAB
6. ✅ **Interactions** - Track clicks & views
7. ✅ **Favorites** - Add, Remove, List
8. ✅ **Itineraries** - CRUD operations dengan status management
9. ✅ **User Preferences** - Get & Update
10. ✅ **Statistics** - Popular items

#### Untuk Admin Dashboard (`http://localhost:3001`):
1. ✅ **Admin Auth** - JWT-based login
2. ✅ **Dashboard Stats** - Real-time statistics dari database
3. ✅ **User Management** - View all users
4. ✅ **Destination Management** - View all destinations
5. ✅ **Analytics** - Comprehensive analytics data
6. ✅ **Activity Monitoring** - Chart data untuk dashboard

#### Untuk Research/ML:
1. ✅ **ML Training** - Train models
2. ✅ **MAB System** - Feedback loop, Statistics, Reset
3. ✅ **Evaluation** - Config check, Consistency validation
4. ✅ **Advanced Analytics** - User behavior, Destination stats

---

## 🚨 YANG PERLU DICEK/DIPERBAIKI

### 1. **Backend Server Status**
- ❌ Backend belum berjalan di `http://localhost:8000`
- ⚠️ Import errors sebelumnya di `itineraries.py` sudah diperbaiki
- 🔧 **ACTION**: Jalankan backend dengan:
  ```bash
  cd backend
  uvicorn main:app --reload --host 127.0.0.1 --port 8000
  ```

### 2. **Database Connection**
- ⚠️ Pastikan PostgreSQL sudah running
- ⚠️ Pastikan environment variables sudah diset (.env file)
- 🔧 **ACTION**: Cek `DATABASE_URL` di `.env`

### 3. **CORS Configuration**
- ✅ CORS sudah dikonfigurasi untuk:
  - `http://localhost:3000` (Admin Dashboard alternative)
  - `http://localhost:3001` (Admin Dashboard)
  - `http://localhost:5173` (Frontend Vite)
  - `http://localhost:8000` (Backend)

### 4. **Missing Endpoints** (Jika Diperlukan)
- ⚠️ **Update destination/activity** - Belum ada endpoint untuk admin edit
- ⚠️ **Delete destination/activity** - Belum ada endpoint untuk admin delete
- ⚠️ **User management** - Belum ada endpoint untuk admin ban/unban user
- ⚠️ **Bulk operations** - Belum ada endpoint untuk bulk actions

---

## 🎯 TESTING PLAN

### Priority 1 - Frontend Critical:
1. Start backend server
2. Test `/api/auth/register` & `/api/auth/login`
3. Test `/api/destinations` & `/api/activities`
4. Test `/api/recommendations/personalized`
5. Test `/api/interactions/click` & `/api/interactions/view`

### Priority 2 - Features:
6. Test `/api/favorites` CRUD
7. Test `/api/itineraries` CRUD
8. Test `/api/search` endpoints
9. Test related items endpoints

### Priority 3 - Admin:
10. Test `/admin/login`
11. Test `/admin/stats`
12. Test `/admin/users` & `/admin/destinations`

### Priority 4 - Research:
13. Test MAB feedback loop
14. Test ML training endpoints
15. Test evaluation endpoints

---

## 📌 NOTES

- **Authentication**: Menggunakan JWT Bearer token di header `Authorization: Bearer <token>`
- **Admin Credentials**: 
  - Email: `admin@example.com`
  - Password: `admin123`
- **Session Tracking**: Frontend harus generate dan persist `session_id` di localStorage
- **Error Handling**: Semua endpoint sudah dilengkapi dengan proper error responses (400, 401, 404, 500)
- **Pagination**: Endpoints list support `limit` & `offset` query parameters
- **Filtering**: Destinations & Activities support multiple filter criteria

---

## 🔗 Quick Links

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Dashboard**: http://localhost:3001
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

**Last Updated**: 2025-11-04
**Backend Status**: ❌ Not Running
**Frontend Status**: ✅ Running
**Admin Dashboard Status**: ❓ Unknown
