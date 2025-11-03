# Frontend API Endpoints - HIGH PRIORITY

## 📋 Overview

Endpoint-endpoint ini dibuat untuk mendukung frontend React dengan fitur:
- ✅ Destinations listing & detail
- ✅ Activities listing & detail  
- ✅ Review system untuk destinations & activities
- ✅ Personalized recommendations (MAB-based)
- ✅ User interaction tracking

---

## 🚀 Base URL

```
http://localhost:8000/api
```

---

## 📍 Endpoints

### **1. DESTINATIONS**

#### `GET /api/destinations`
Get list of destinations with optional filters

**Query Parameters:**
- `category` (optional): Filter by category name
- `region` (optional): Filter by region/address
- `limit` (optional, default: 50): Number of results
- `offset` (optional, default: 0): Pagination offset

**Response:**
```json
{
  "destinations": [
    {
      "id": 1,
      "name": "Gunung Tampomas",
      "description": "Gunung dengan pemandangan indah...",
      "image": "/assets/images/gunung-tampomas.jpg",
      "region": "Kecamatan Sumedang Utara",
      "category": "Wisata Alam",
      "rating": 4.6,
      "reviewCount": 328,
      "latitude": -6.85,
      "longitude": 107.92
    }
  ],
  "total": 10,
  "offset": 0,
  "limit": 50
}
```

---

#### `GET /api/destinations/{id}`
Get detailed information for a specific destination

**Path Parameters:**
- `id`: Destination ID

**Response:**
```json
{
  "id": 1,
  "name": "Gunung Tampomas",
  "description": "...",
  "category": "Wisata Alam",
  "region": "Sumedang Utara",
  "image": "/assets/images/gunung-tampomas-hero.jpg",
  "rating": 4.6,
  "reviewCount": 328,
  "ticketPrice": "Gratis",
  "openingHours": "24 Jam",
  "highlights": [...],
  "facilities": [...],
  "bestTime": {...},
  "tips": [...],
  "gallery": [...],
  "nearbyAttractions": [...],
  "reviews": [...]
}
```

---

#### `POST /api/destinations/{id}/reviews`
Submit a review for a destination

**Path Parameters:**
- `id`: Destination ID

**Query Parameters:**
- `user_id` (optional): User ID if logged in

**Request Body:**
```json
{
  "name": "John Doe",
  "rating": 5.0,
  "comment": "Amazing place! Highly recommended."
}
```

**Response:**
```json
{
  "message": "Review submitted successfully",
  "review": {
    "id": 123,
    "name": "John Doe",
    "rating": 5.0,
    "comment": "Amazing place!",
    "created_at": "2025-11-03T10:30:00"
  }
}
```

---

#### `GET /api/destinations/{id}/reviews`
Get reviews for a specific destination

**Path Parameters:**
- `id`: Destination ID

**Query Parameters:**
- `limit` (optional, default: 20): Number of reviews
- `offset` (optional, default: 0): Pagination offset

**Response:**
```json
{
  "reviews": [
    {
      "id": 123,
      "name": "John Doe",
      "rating": 5.0,
      "comment": "Amazing place!",
      "date": "03 November 2025",
      "avatar": "/assets/images/avatar-1.jpg"
    }
  ],
  "total": 328,
  "offset": 0,
  "limit": 20
}
```

---

### **2. ACTIVITIES**

#### `GET /api/activities`
Get list of activities

**Query Parameters:**
- `category` (optional): Filter by category
- `limit` (optional, default: 50)
- `offset` (optional, default: 0)

**Response:**
```json
{
  "activities": [
    {
      "id": 8,
      "name": "Wisata Kuliner Tahu Sumedang",
      "description": "...",
      "image": "/assets/images/kuliner-tahu-hero.jpg",
      "category": "Kuliner",
      "rating": 4.8,
      "reviewCount": 245,
      "duration": "2-3 jam",
      "price": "Rp 50.000 - 150.000"
    }
  ],
  "total": 8,
  "offset": 0,
  "limit": 50
}
```

---

#### `GET /api/activities/{id}`
Get detailed information for a specific activity

**Path Parameters:**
- `id`: Activity ID

**Response:**
```json
{
  "id": 8,
  "name": "Wisata Kuliner Tahu Sumedang",
  "category": "Kuliner",
  "description": "...",
  "image": "/assets/images/kuliner-tahu-hero.jpg",
  "rating": 4.8,
  "reviewCount": 245,
  "duration": "2-3 jam",
  "price": "Rp 50.000 - 150.000",
  "highlights": [...],
  "included": [...],
  "gallery": [...],
  "reviews": [...]
}
```

---

#### `POST /api/activities/{id}/reviews`
Submit a review for an activity

**Same structure as destination reviews**

---

#### `GET /api/activities/{id}/reviews`
Get reviews for a specific activity

**Same structure as destination reviews**

---

### **3. PERSONALIZED RECOMMENDATIONS**

#### `GET /api/recommendations/personalized`
Get personalized recommendations for Home page

**Query Parameters:**
- `user_id` (optional): User ID
- `session_id` (optional): Session ID for anonymous users
- `limit` (optional, default: 6): Number of recommendations

**Response:**
```json
{
  "recommendations": [
    {
      "id": 1,
      "name": "Gunung Tampomas",
      "image": "/assets/images/gunung-tampomas.jpg",
      "description": "...",
      "region": "Sumedang",
      "category": "Alam",
      "rating": 4.6,
      "reviewCount": 328
    }
  ],
  "algorithm": "mab",
  "message": "Personalized recommendations based on your preferences"
}
```

---

### **4. USER INTERACTIONS**

#### `POST /api/interactions/click`
Track user click on destination/activity card

**Request Body:**
```json
{
  "user_id": 1,
  "session_id": "abc123",
  "interaction_type": "click",
  "entity_type": "destination",
  "entity_id": 1,
  "metadata": "{\"source\": \"home_page\"}"
}
```

**Response:**
```json
{
  "message": "Click tracked successfully",
  "interaction_id": 456
}
```

---

#### `POST /api/interactions/view`
Track page view with duration

**Request Body:**
```json
{
  "user_id": 1,
  "session_id": "abc123",
  "interaction_type": "view",
  "entity_type": "destination",
  "entity_id": 1,
  "duration": 45.5,
  "metadata": "{\"page\": \"destination_detail\"}"
}
```

**Response:**
```json
{
  "message": "View tracked successfully",
  "interaction_id": 457
}
```

---

#### `GET /api/interactions/user/{user_id}`
Get user interaction history

**Path Parameters:**
- `user_id`: User ID

**Query Parameters:**
- `interaction_type` (optional): Filter by type (click, view, favorite, share)
- `entity_type` (optional): Filter by entity (destination, activity)
- `limit` (optional, default: 50)

**Response:**
```json
{
  "interactions": [
    {
      "id": 456,
      "interaction_type": "click",
      "entity_type": "destination",
      "entity_id": 1,
      "duration": null,
      "created_at": "2025-11-03T10:30:00"
    }
  ],
  "total": 50
}
```

---

## 🗄️ Database Models

### New Models Created:

1. **Activity**
   - id, name, description, category, duration, price_range, image_url, created_at

2. **ActivityReview**
   - id, user_id, activity_id, name, rating, comment, created_at

3. **DestinationReview**
   - id, user_id, destination_id, name, rating, comment, created_at

4. **UserInteraction**
   - id, user_id, session_id, interaction_type, entity_type, entity_id, duration, metadata, created_at

---

## 🔧 Setup Instructions

### 1. Run Database Migrations

```bash
# The new models will be automatically created if using SQLAlchemy with create_all()
# Or run your migration tool (Alembic)
```

### 2. Seed Activities Data

```bash
cd backend
python seed_activities.py
```

### 3. Start Backend

```bash
cd backend
python main.py
```

### 4. Test API

Open browser to: `http://localhost:8000/docs`

You'll see all new endpoints in the Swagger UI under **"frontend"** tag.

---

## 🧪 Testing

### Test Destinations

```bash
curl http://localhost:8000/api/destinations
curl http://localhost:8000/api/destinations/1
```

### Test Activities

```bash
curl http://localhost:8000/api/activities
curl http://localhost:8000/api/activities/8
```

### Test Reviews

```bash
curl -X POST http://localhost:8000/api/destinations/1/reviews \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "rating": 5.0, "comment": "Great place!"}'
```

### Test Recommendations

```bash
curl http://localhost:8000/api/recommendations/personalized?limit=6
```

### Test Interactions

```bash
curl -X POST http://localhost:8000/api/interactions/click \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "interaction_type": "click",
    "entity_type": "destination",
    "entity_id": 1
  }'
```

---

## 📝 Notes

1. **User Authentication**: Currently optional. `user_id` can be NULL for anonymous users. Use `session_id` for tracking.

2. **Images**: Using placeholder paths. Update with actual image URLs after uploading assets.

3. **MAB Integration**: The `/recommendations/personalized` endpoint currently returns popular destinations. Will integrate with MAB algorithm once ML models are trained.

4. **Related Items**: `nearbyAttractions` and related activities logic not implemented yet. Can be added later based on distance calculation or category similarity.

5. **Search**: Search functionality not included in HIGH PRIORITY. Can be added as enhancement.

---

## 🔄 Integration with Frontend

Frontend pages that use these APIs:

- **Home.jsx** → `/api/recommendations/personalized`
- **Destinations.jsx** → `/api/destinations`
- **DestinationDetail.jsx** → `/api/destinations/{id}`, `/api/destinations/{id}/reviews`
- **Activities.jsx** → `/api/activities`
- **ActivityDetail.jsx** → `/api/activities/{id}`, `/api/activities/{id}/reviews`
- **All pages** → `/api/interactions/click`, `/api/interactions/view`

---

## ✅ Checklist

HIGH PRIORITY Endpoints:
- ✅ GET /api/destinations
- ✅ GET /api/destinations/{id}
- ✅ POST /api/destinations/{id}/reviews
- ✅ GET /api/destinations/{id}/reviews
- ✅ GET /api/activities
- ✅ GET /api/activities/{id}
- ✅ POST /api/activities/{id}/reviews
- ✅ GET /api/activities/{id}/reviews
- ✅ GET /api/recommendations/personalized
- ✅ POST /api/interactions/click
- ✅ POST /api/interactions/view
- ✅ GET /api/interactions/user/{user_id}

Models:
- ✅ Activity
- ✅ ActivityReview
- ✅ DestinationReview
- ✅ UserInteraction

Database:
- ⏳ Run migrations to create new tables
- ⏳ Seed activities data
- ⏳ Test endpoints

Frontend Integration:
- ⏳ Update API calls in frontend components
- ⏳ Test with actual backend
