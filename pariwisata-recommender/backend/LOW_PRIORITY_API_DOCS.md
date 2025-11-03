# LOW PRIORITY API Endpoints

## 📋 Overview

Endpoint-endpoint LOW PRIORITY untuk enhancement features:
- ✅ **Search** - Universal search & advanced filtering
- ✅ **Related Items** - Recommendation berdasarkan similarity
- ✅ **User Preferences** - Manage user preferences
- ✅ **Favorites** - Save favorite destinations/activities
- ✅ **Statistics** - Popular items tracking

---

## 🚀 Base URL

```
http://localhost:8000/api
```

---

## 🔍 SEARCH ENDPOINTS

### **1. GET /api/search**
Universal search across destinations and activities

**Query Parameters:**
- `q` (required, min 2 chars): Search query
- `type` (optional): Filter by 'destination' or 'activity'
- `category` (optional): Filter by category
- `limit` (optional, default: 20): Number of results

**Example:**
```
GET /api/search?q=gunung&type=destination&limit=10
```

**Response:**
```json
{
  "query": "gunung",
  "results": [
    {
      "type": "destination",
      "id": 1,
      "name": "Gunung Tampomas",
      "description": "Gunung dengan pemandangan indah...",
      "image": "/assets/images/gunung-tampomas.jpg",
      "category": "Alam",
      "rating": 4.6,
      "reviewCount": 328
    },
    {
      "type": "activity",
      "id": 4,
      "name": "Pendakian Gunung Tampomas",
      "description": "Nikmati pendakian...",
      "image": "/assets/images/pendakian-tampomas.jpg",
      "category": "Alam",
      "rating": 4.8,
      "reviewCount": 156
    }
  ],
  "total": 2
}
```

---

### **2. GET /api/search/destinations**
Advanced search for destinations with filters

**Query Parameters:**
- `q` (required): Search query
- `category` (optional): Filter by category
- `region` (optional): Filter by region
- `min_rating` (optional): Minimum rating (0-5)
- `limit` (optional, default: 20)

**Example:**
```
GET /api/search/destinations?q=museum&region=sumedang&min_rating=4.0
```

**Response:**
```json
{
  "query": "museum",
  "destinations": [
    {
      "id": 5,
      "name": "Museum Prabu Geusan Ulun",
      "description": "...",
      "address": "Sumedang",
      "rating": 4.5
    }
  ],
  "total": 1
}
```

---

### **3. GET /api/search/activities**
Advanced search for activities

**Query Parameters:**
- `q` (required): Search query
- `category` (optional): Filter by category
- `min_price` (optional): Minimum price (not implemented yet)
- `max_price` (optional): Maximum price (not implemented yet)
- `limit` (optional, default: 20)

**Example:**
```
GET /api/search/activities?q=kuliner&category=Kuliner
```

**Response:**
```json
{
  "query": "kuliner",
  "activities": [
    {
      "id": 1,
      "name": "Wisata Kuliner Tahu Sumedang",
      "description": "...",
      "category": "Kuliner",
      "duration": "2-3 jam",
      "price_range": "Rp 50.000 - 150.000",
      "rating": 4.8,
      "reviewCount": 245
    }
  ],
  "total": 1
}
```

---

## 🔗 RELATED ITEMS ENDPOINTS

### **4. GET /api/destinations/{id}/related**
Get related destinations based on categories

**Query Parameters:**
- `limit` (optional, default: 6)

**Example:**
```
GET /api/destinations/1/related?limit=6
```

**Response:**
```json
{
  "destination_id": 1,
  "related": [
    {
      "id": 2,
      "name": "Curug Cinulang",
      "description": "Air terjun yang indah...",
      "image": "/assets/images/curug-cinulang.jpg",
      "rating": 4.5,
      "reviewCount": 189
    }
  ],
  "total": 6
}
```

**Logic:**
- Finds destinations with same categories
- Falls back to popular destinations if no matches

---

### **5. GET /api/activities/{id}/related**
Get related activities based on category

**Query Parameters:**
- `limit` (optional, default: 6)

**Example:**
```
GET /api/activities/1/related?limit=6
```

**Response:**
```json
{
  "activity_id": 1,
  "related": [
    {
      "id": 2,
      "name": "Wisata Peuyeum",
      "description": "...",
      "category": "Kuliner",
      "duration": "1-2 jam",
      "price_range": "Rp 30.000 - 80.000",
      "rating": 4.7,
      "reviewCount": 198
    }
  ],
  "total": 6
}
```

---

## 👤 USER PREFERENCES ENDPOINTS

### **6. GET /api/users/{user_id}/preferences**
Get user preferences (public endpoint)

**Response:**
```json
{
  "user_id": 1,
  "preferences": ["alam", "kuliner", "budaya"],
  "preferences_string": "alam,kuliner,budaya"
}
```

---

### **7. PUT /api/users/{user_id}/preferences**
Update user preferences (requires auth, owner only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "preferences": "alam,kuliner,sejarah"
}
```

**Response:**
```json
{
  "message": "Preferences updated successfully",
  "user_id": 1,
  "preferences": ["alam", "kuliner", "sejarah"]
}
```

**Errors:**
- `401` - Not authenticated
- `403` - Not authorized to update this user's preferences
- `404` - User not found

---

### **8. GET /api/users/{user_id}/recommendations**
Get personalized recommendations based on user preferences

**Query Parameters:**
- `limit` (optional, default: 10)

**Example:**
```
GET /api/users/1/recommendations?limit=10
```

**Response:**
```json
{
  "user_id": 1,
  "recommendations": [
    {
      "type": "destination",
      "id": 1,
      "name": "Gunung Tampomas",
      "description": "...",
      "category": "alam",
      "rating": 4.6,
      "reviewCount": 328,
      "reason": "Based on your interest in alam"
    },
    {
      "type": "destination",
      "id": 8,
      "name": "Tahu Sumedang Factory",
      "description": "...",
      "category": "kuliner",
      "rating": 4.8,
      "reviewCount": 412,
      "reason": "Based on your interest in kuliner"
    }
  ],
  "total": 10
}
```

**Logic:**
1. Matches user preferences with destination categories
2. Gets top 3 preferred categories
3. Finds 5 destinations per category
4. Fills remaining slots with popular destinations

---

## ⭐ FAVORITES ENDPOINTS

### **9. POST /api/favorites**
Add destination or activity to favorites (requires auth)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "entity_type": "destination",
  "entity_id": 1
}
```

**Response:**
```json
{
  "message": "Added to favorites",
  "action": "added",
  "favorite_id": 123
}
```

**If already favorited:**
```json
{
  "message": "Already in favorites",
  "action": "none"
}
```

---

### **10. DELETE /api/favorites/{entity_type}/{entity_id}**
Remove from favorites (requires auth)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:**
```
DELETE /api/favorites/destination/1
```

**Response:**
```json
{
  "message": "Removed from favorites"
}
```

**Errors:**
- `401` - Not authenticated
- `404` - Favorite not found

---

### **11. GET /api/users/{user_id}/favorites**
Get user's favorite destinations and activities

**Query Parameters:**
- `entity_type` (optional): Filter by 'destination' or 'activity'

**Example:**
```
GET /api/users/1/favorites?entity_type=destination
```

**Response:**
```json
{
  "user_id": 1,
  "favorites": [
    {
      "entity_type": "destination",
      "entity_id": 1,
      "name": "Gunung Tampomas",
      "description": "Gunung dengan pemandangan indah...",
      "added_at": "2025-11-03T10:30:00"
    },
    {
      "entity_type": "activity",
      "entity_id": 8,
      "name": "Wisata Kuliner Tahu Sumedang",
      "description": "...",
      "category": "Kuliner",
      "added_at": "2025-11-03T11:15:00"
    }
  ],
  "total": 2
}
```

---

## 📊 STATISTICS ENDPOINTS

### **12. GET /api/stats/popular**
Get most popular destinations/activities based on user interactions

**Query Parameters:**
- `type` (optional): Filter by 'destination' or 'activity'
- `period` (optional): 'week', 'month', 'all' (default: 'all')
- `limit` (optional, default: 10)

**Example:**
```
GET /api/stats/popular?type=destination&limit=10
```

**Response:**
```json
{
  "popular_items": [
    {
      "type": "destination",
      "id": 1,
      "name": "Gunung Tampomas",
      "interaction_count": 1245
    },
    {
      "type": "destination",
      "id": 5,
      "name": "Museum Prabu Geusan Ulun",
      "interaction_count": 892
    }
  ],
  "total": 10
}
```

**Logic:**
- Counts clicks and views from `user_interactions` table
- Sorts by interaction count (descending)
- Combines destinations and activities if no type filter

---

## 📝 Implementation Notes

### Search Functionality
- Uses PostgreSQL `ILIKE` for case-insensitive search
- Searches in: name, description, address (for destinations)
- Returns combined results from destinations and activities
- Includes rating and review count for each result

### Related Items
- **Destinations**: Matches by shared categories
- **Activities**: Matches by same category
- Falls back to popular items if no matches found

### User Preferences
- Stored as comma-separated string: `"alam,kuliner,budaya"`
- Split into array for frontend consumption
- Used for personalized recommendations

### Favorites System
- Uses `user_interactions` table with `interaction_type = 'favorite'`
- Prevents duplicate favorites
- Supports both destinations and activities
- Owner can remove their own favorites

### Statistics
- Tracks popularity via clicks and views
- Real-time counting from interactions table
- Can filter by time period (not yet implemented)

---

## ✅ Checklist

LOW PRIORITY Endpoints:
- ✅ GET /api/search (universal search)
- ✅ GET /api/search/destinations (advanced filtering)
- ✅ GET /api/search/activities (advanced filtering)
- ✅ GET /api/destinations/{id}/related
- ✅ GET /api/activities/{id}/related
- ✅ GET /api/users/{user_id}/preferences
- ✅ PUT /api/users/{user_id}/preferences
- ✅ GET /api/users/{user_id}/recommendations
- ✅ POST /api/favorites
- ✅ DELETE /api/favorites/{entity_type}/{entity_id}
- ✅ GET /api/users/{user_id}/favorites
- ✅ GET /api/stats/popular

Features:
- ✅ Universal search (destinations + activities)
- ✅ Advanced filtering (category, region, rating)
- ✅ Related items recommendation
- ✅ User preferences management
- ✅ Favorites system
- ✅ Popularity statistics

Database:
- ✅ No new tables needed (uses existing UserInteraction)
- ✅ Favorites stored as interaction_type='favorite'

---

## 🚀 Ready to Use

All LOW PRIORITY endpoints are ready to test!

**Swagger UI:** `http://localhost:8000/docs`
- Look for tag **"low-priority"**
- 12 new endpoints available

**No migration needed** - all endpoints use existing database tables.

---

## 🎯 Summary - ALL PRIORITIES COMPLETE

### ✅ HIGH PRIORITY - DONE
- Destinations CRUD
- Activities CRUD
- Reviews system
- Personalized recommendations
- User interaction tracking

### ✅ MEDIUM PRIORITY - DONE
- Authentication (register, login, JWT)
- Itinerary management (CRUD)
- Owner-based permissions

### ✅ COMPLETE LOW PRIORITY - DONE
- Universal search
- Advanced filtering
- Related items
- User preferences
- Favorites system
- Statistics

---

**Total Endpoints Created: 35+**
- HIGH: 15 endpoints
- MEDIUM: 8 endpoints
- LOW: 12 endpoints

🎉 **Backend API is now COMPLETE!**
