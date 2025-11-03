# MEDIUM PRIORITY API Endpoints

## 📋 Overview

Endpoint-endpoint MEDIUM PRIORITY untuk:
- ✅ **Itinerary Management** - Create, Read, Update, Delete itineraries
- ✅ **Authentication** - User registration, login, and authentication

---

## 🚀 Base URL

```
http://localhost:8000/api
```

---

## 🔐 Authentication Endpoints

### **1. POST /api/auth/register**
Register a new user

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "preferences": "alam,kuliner"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "preferences": "alam,kuliner",
    "created_at": "2025-11-03T10:30:00"
  }
}
```

**Errors:**
- `400` - Email already registered
- `500` - Registration failed

---

### **2. POST /api/auth/login**
Login with email and password

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "preferences": "alam,kuliner",
    "created_at": "2025-11-03T10:30:00"
  }
}
```

**Errors:**
- `401` - Invalid email or password
- `500` - Login failed

---

### **3. GET /api/auth/me**
Get current authenticated user info

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "preferences": "alam,kuliner",
  "created_at": "2025-11-03T10:30:00"
}
```

**Errors:**
- `401` - Not authenticated

---

## 🗓️ Itinerary Management Endpoints

### **4. POST /api/itineraries**
Create a new itinerary (requires authentication)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Liburan ke Sumedang 3D2N",
  "description": "Trip keluarga ke Sumedang",
  "start_date": "2025-12-20",
  "end_date": "2025-12-22",
  "total_budget": 5000000,
  "accommodation": "{\"hotel\": \"Hotel Sumedang\", \"price\": 500000}",
  "transportation": "{\"type\": \"Mobil Pribadi\"}",
  "notes": "Jangan lupa bawa jaket",
  "days": [
    {
      "day_number": 1,
      "date": "2025-12-20",
      "title": "Hari Pertama - Eksplorasi Kota",
      "items": [
        {
          "time": "09:00",
          "activity_type": "destination",
          "entity_id": 1,
          "title": "Gunung Tampomas",
          "description": "Pendakian pagi",
          "location": "Sumedang Utara",
          "duration": "4 jam",
          "cost": 50000,
          "notes": "Bawa bekal",
          "order": 1
        },
        {
          "time": "13:00",
          "activity_type": "meal",
          "title": "Makan Siang - Nasi Timbel",
          "location": "Restoran Sunda",
          "duration": "1 jam",
          "cost": 150000,
          "order": 2
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Liburan ke Sumedang 3D2N",
  "description": "Trip keluarga ke Sumedang",
  "start_date": "2025-12-20",
  "end_date": "2025-12-22",
  "status": "upcoming",
  "total_budget": 5000000,
  "accommodation": "{\"hotel\": \"Hotel Sumedang\", \"price\": 500000}",
  "transportation": "{\"type\": \"Mobil Pribadi\"}",
  "notes": "Jangan lupa bawa jaket",
  "created_at": "2025-11-03T10:30:00",
  "days": [...]
}
```

**Status Auto-Detection:**
- `upcoming` - start_date > today
- `ongoing` - start_date <= today <= end_date
- `completed` - end_date < today

**Errors:**
- `401` - Not authenticated
- `500` - Failed to create itinerary

---

### **5. GET /api/itineraries/{id}**
Get itinerary by ID (public endpoint)

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Liburan ke Sumedang 3D2N",
  "status": "upcoming",
  "start_date": "2025-12-20",
  "end_date": "2025-12-22",
  "days": [
    {
      "id": 1,
      "day_number": 1,
      "date": "2025-12-20",
      "title": "Hari Pertama",
      "items": [
        {
          "id": 1,
          "time": "09:00",
          "activity_type": "destination",
          "title": "Gunung Tampomas",
          "duration": "4 jam",
          "cost": 50000,
          "order": 1
        }
      ]
    }
  ]
}
```

**Errors:**
- `404` - Itinerary not found
- `500` - Failed to fetch itinerary

---

### **6. GET /api/itineraries/user/{user_id}**
Get all itineraries for a specific user

**Query Parameters:**
- `status` (optional): Filter by status ('upcoming', 'ongoing', 'completed', 'cancelled')

**Example:**
```
GET /api/itineraries/user/1?status=upcoming
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Liburan ke Sumedang 3D2N",
    "status": "upcoming",
    "start_date": "2025-12-20",
    "end_date": "2025-12-22",
    "days": [...]
  },
  {
    "id": 2,
    "title": "Weekend di Sumedang",
    "status": "upcoming",
    "start_date": "2025-12-25",
    "end_date": "2025-12-26",
    "days": [...]
  }
]
```

**Errors:**
- `500` - Failed to fetch user itineraries

---

### **7. DELETE /api/itineraries/{id}**
Delete an itinerary (requires authentication, owner only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Itinerary deleted successfully"
}
```

**Errors:**
- `401` - Not authenticated
- `403` - Not authorized to delete this itinerary
- `404` - Itinerary not found
- `500` - Failed to delete itinerary

---

### **8. PUT /api/itineraries/{id}/status**
Update itinerary status (requires authentication, owner only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` (required): New status ('upcoming', 'ongoing', 'completed', 'cancelled')

**Example:**
```
PUT /api/itineraries/1/status?status=completed
```

**Response:**
```json
{
  "message": "Itinerary status updated successfully",
  "status": "completed"
}
```

**Errors:**
- `400` - Invalid status
- `401` - Not authenticated
- `403` - Not authorized to update this itinerary
- `404` - Itinerary not found
- `500` - Failed to update itinerary status

---

## 🗄️ Database Models

### New Models Created:

**1. Itinerary**
- id, user_id, title, description
- start_date, end_date, status
- total_budget, accommodation (JSON), transportation (JSON)
- notes, created_at, updated_at

**2. ItineraryDay**
- id, itinerary_id, day_number, date, title

**3. ItineraryItem**
- id, day_id, time, activity_type, entity_id
- title, description, location, duration, cost
- notes, order

**4. User (Updated)**
- Added: `password_hash` column

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install passlib[bcrypt] python-jose[cryptography] python-multipart email-validator
```

### 2. Run Database Migration

```bash
python migrate_medium_priority.py
```

This will:
- Add `password_hash` column to `users` table
- Create `itineraries` table
- Create `itinerary_days` table
- Create `itinerary_items` table

### 3. Restart Backend

```bash
uvicorn main:app --reload
```

### 4. Test API

Open Swagger UI: `http://localhost:8000/docs`

Look for **"medium-priority"** tag

---

## 🧪 Testing Examples

### Test User Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "preferences": "alam,kuliner"
  }'
```

### Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from response.

### Test Get Current User

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your_access_token>"
```

### Test Create Itinerary

```bash
curl -X POST http://localhost:8000/api/itineraries \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekend Trip",
    "start_date": "2025-12-20",
    "end_date": "2025-12-22",
    "total_budget": 2000000,
    "days": []
  }'
```

### Test Get User Itineraries

```bash
curl http://localhost:8000/api/itineraries/user/1
```

---

## 📝 Notes

1. **Authentication**: JWT tokens expire after 30 minutes (configurable in `app/core/auth.py`)

2. **Password Security**: Passwords are hashed using bcrypt before storing

3. **Itinerary Status**: Automatically determined based on dates:
   - `upcoming` if start_date > today
   - `ongoing` if today is between start_date and end_date
   - `completed` if end_date < today

4. **Ownership**: Only the itinerary owner can delete or update status

5. **Public Access**: GET itinerary endpoints are public (no auth required)

6. **JSON Fields**: `accommodation` and `transportation` are stored as JSON strings for flexibility

7. **Cascade Delete**: Deleting an itinerary will automatically delete all related days and items

---

## ✅ Checklist

MEDIUM PRIORITY Endpoints:
- ✅ POST /api/auth/register
- ✅ POST /api/auth/login
- ✅ GET /api/auth/me
- ✅ POST /api/itineraries
- ✅ GET /api/itineraries/{id}
- ✅ GET /api/itineraries/user/{user_id}
- ✅ DELETE /api/itineraries/{id}
- ✅ PUT /api/itineraries/{id}/status

Models:
- ✅ Itinerary
- ✅ ItineraryDay
- ✅ ItineraryItem
- ✅ User (updated with password_hash)

Authentication:
- ✅ Password hashing (bcrypt)
- ✅ JWT token generation
- ✅ Token validation
- ✅ Protected routes

Database:
- ⏳ Run migration to create tables
- ⏳ Test all endpoints

Frontend Integration:
- ⏳ Update API calls
- ⏳ Add authentication flow
- ⏳ Test itinerary creation/viewing

---

## 🚀 Next Steps

After testing MEDIUM PRIORITY:

**LOW PRIORITY** features to implement:
1. Search functionality (destinations/activities)
2. Related items recommendations
3. User preferences management
4. Advanced filtering and sorting
5. Export itinerary to PDF
6. Share itinerary feature
7. Image upload for user profile
8. Social features (comments, likes)
