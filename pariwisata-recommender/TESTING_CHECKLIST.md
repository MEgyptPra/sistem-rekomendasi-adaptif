# 🧪 Testing Checklist - Frontend-Backend Integration

## Pre-Testing Setup
- [ ] Backend server running on `http://localhost:8000`
- [ ] Frontend dev server running on `http://localhost:5173`
- [ ] PostgreSQL database accessible
- [ ] Clear browser cache and localStorage
- [ ] Open browser DevTools (Network & Console tabs)

---

## 1. 🔐 Authentication System Testing

### Registration Flow
- [ ] Navigate to `/register`
- [ ] Fill form with valid data:
  - Name: "Test User"
  - Email: "test@example.com"
  - Password: "password123" (min 6 chars)
  - Confirm Password: "password123"
  - Select 2-3 preferences (alam, kuliner, budaya)
- [ ] Click "Daftar Sekarang"
- [ ] ✅ Should redirect to home page (`/`)
- [ ] ✅ Header should show "Halo, Test User" and "Keluar" button
- [ ] ✅ "Favorit" link should appear in navigation
- [ ] Check localStorage:
  - [ ] `access_token` exists
  - [ ] `user` object stored with correct data
- [ ] Check Network tab:
  - [ ] POST `/api/auth/register` returned 200/201
  - [ ] Response contains `access_token` and `user` data

### Registration Validation
- [ ] Try registering with same email
  - [ ] ✅ Should show error "Email sudah terdaftar"
- [ ] Try password mismatch:
  - [ ] ✅ Should show "Password tidak cocok"
- [ ] Try password < 6 characters:
  - [ ] ✅ Should show "Password minimal 6 karakter"

### Login Flow
- [ ] Logout first (click "Keluar" button)
- [ ] ✅ Should redirect to home
- [ ] ✅ Header shows "Masuk" and "Daftar" buttons
- [ ] Navigate to `/login`
- [ ] Enter credentials:
  - Email: "test@example.com"
  - Password: "password123"
- [ ] Click "Masuk"
- [ ] ✅ Should redirect to home page
- [ ] ✅ Header shows "Halo, Test User"
- [ ] Check Network tab:
  - [ ] POST `/api/auth/login` returned 200
  - [ ] Response contains `access_token`

### Login Validation
- [ ] Try wrong password:
  - [ ] ✅ Should show error message
- [ ] Try non-existent email:
  - [ ] ✅ Should show error message

### Logout Flow
- [ ] Click "Keluar" button in header
- [ ] ✅ Should redirect to home
- [ ] ✅ Header shows login/register buttons
- [ ] Check localStorage:
  - [ ] `access_token` removed
  - [ ] `user` removed
- [ ] Check Network tab:
  - [ ] POST `/api/auth/logout` called

---

## 2. 🔒 Protected Routes Testing

### Without Authentication
- [ ] Logout if logged in
- [ ] Try to access `/planning`
  - [ ] ✅ Should redirect to `/login`
- [ ] Try to access `/planning/123`
  - [ ] ✅ Should redirect to `/login`
- [ ] Try to access `/favorites`
  - [ ] ✅ Should redirect to `/login`

### With Authentication
- [ ] Login first
- [ ] Navigate to `/planning`
  - [ ] ✅ Should load Planning page
- [ ] Navigate to `/favorites`
  - [ ] ✅ Should load Favorites page

---

## 3. 🏠 Home Page Testing

### Without Authentication
- [ ] Visit home page (`/`)
- [ ] Check "Rekomendasi Untuk Anda" section:
  - [ ] ✅ Should show login prompt
  - [ ] ✅ Subtitle: "Masuk untuk mendapatkan rekomendasi yang dipersonalisasi"
  - [ ] ✅ Shows "Masuk" and "Daftar" buttons
- [ ] Check "Aktivitas Populer" section:
  - [ ] ✅ Should display activity cards
  - [ ] Check Network: GET `/api/activities?limit=3`

### With Authentication
- [ ] Login first
- [ ] Visit home page
- [ ] Check "Rekomendasi Untuk Anda" section:
  - [ ] ✅ Should show personalized destinations
  - [ ] Check Network: GET `/api/recommendations/personalized`
  - [ ] ✅ Should display 3-6 destination cards
  - [ ] ✅ Info text mentions "sistem AI"

---

## 4. 🏞️ Destinations Page Testing

### Page Load
- [ ] Navigate to `/destinations`
- [ ] Check Network tab:
  - [ ] GET `/api/destinations` called
  - [ ] ✅ Should return list of destinations
- [ ] ✅ Page shows destination cards
- [ ] ✅ Category filter dropdown visible
- [ ] ✅ Search input visible

### Category Filtering
- [ ] Select "Alam" from dropdown
  - [ ] ✅ Only shows destinations with category "alam"
- [ ] Select "Kuliner"
  - [ ] ✅ Only shows destinations with category "kuliner"
- [ ] Select "Semua Kategori"
  - [ ] ✅ Shows all destinations

### Search Functionality
- [ ] Type "gunung" in search box
- [ ] Wait 500ms
- [ ] Check Network tab:
  - [ ] GET `/api/search/destinations?q=gunung` called after debounce
- [ ] ✅ Results should filter to matching destinations
- [ ] Clear search
  - [ ] ✅ Shows all destinations again

### Click Tracking (CRITICAL for MAB)
- [ ] Click "Explore" on any destination card
- [ ] Check Network tab:
  - [ ] POST `/api/interactions/click` called BEFORE navigation
  - [ ] Request body: `{"item_type": "destination", "item_id": <id>}`
  - [ ] ✅ Should return 200/201
- [ ] ✅ Should navigate to destination detail page

---

## 5. 🎯 Activities Page Testing

### Page Load
- [ ] Navigate to `/activities`
- [ ] Check Network tab:
  - [ ] GET `/api/activities` called
- [ ] ✅ Shows activity cards

### Category Filtering & Search
- [ ] Test category filter with "Kuliner"
  - [ ] ✅ Only shows culinary activities
- [ ] Type "tahu" in search
  - [ ] Wait 500ms
  - [ ] Check Network: GET `/api/search/activities?q=tahu`
  - [ ] ✅ Filters to matching activities

### Click Tracking
- [ ] Click "Learn More" on any activity card
- [ ] Check Network tab:
  - [ ] POST `/api/interactions/click` with `item_type: "activity"`
- [ ] ✅ Navigate to activity detail

---

## 6. 📍 Destination Detail Page Testing

### Page Load & View Tracking Setup
- [ ] Navigate to `/destinations/1`
- [ ] Check Network tab:
  - [ ] GET `/api/destinations/1` called
  - [ ] GET `/api/destinations/1/reviews` called
  - [ ] GET `/api/related/destinations/1` called (for related items)
- [ ] ✅ Page displays destination data
- [ ] ✅ Reviews section shows reviews or "Belum ada ulasan"
- [ ] ✅ Related destinations section shows similar items

### Favorite Button (Authenticated)
- [ ] Login if not logged in
- [ ] Look for favorite button in hero section
- [ ] ✅ Should show "🤍 Tambah Favorit" initially
- [ ] Click favorite button
- [ ] Check Network:
  - [ ] POST `/api/favorites` with body: `{"item_type": "destination", "item_id": 1}`
- [ ] ✅ Button changes to "❤️ Favorit"
- [ ] Click again to unfavorite
- [ ] Check Network:
  - [ ] DELETE `/api/favorites/destination/1`
- [ ] ✅ Button changes back to "🤍 Tambah Favorit"

### Review Submission (Authenticated)
- [ ] Scroll to review form
- [ ] ✅ Should see review form (not login prompt)
- [ ] Select 5 stars
- [ ] Enter comment: "Destinasi yang luar biasa! Pemandangan sangat indah."
- [ ] Click "Kirim Ulasan"
- [ ] Check Network:
  - [ ] POST `/api/destinations/1/reviews` with rating and comment
  - [ ] ✅ Should return 201
  - [ ] GET `/api/destinations/1/reviews` called again (refresh reviews)
- [ ] ✅ New review appears in reviews list
- [ ] ✅ Shows current user name
- [ ] ✅ Shows today's date
- [ ] ✅ Form resets after submission

### View Duration Tracking (CRITICAL for MAB)
- [ ] Stay on page for at least 10 seconds
- [ ] Navigate away (click browser back or go to another page)
- [ ] Check Network tab:
  - [ ] POST `/api/interactions/view` called
  - [ ] Request body: `{"item_type": "destination", "item_id": 1, "duration": <seconds>}`
  - [ ] ✅ Duration should be ≥10 seconds
- [ ] **Database Verification**:
  - [ ] Open pgAdmin or database client
  - [ ] Query: `SELECT * FROM user_interactions WHERE item_type='destination' AND item_id=1 ORDER BY created_at DESC LIMIT 1`
  - [ ] ✅ Should see view interaction with duration

### Unauthenticated Behavior
- [ ] Logout
- [ ] Visit destination detail page
- [ ] ✅ Favorite button should NOT be visible
- [ ] ✅ Review form should show login prompt instead
- [ ] ✅ Click tracking should still work (view tracking won't work without auth)

---

## 7. 🎪 Activity Detail Page Testing

### Page Load
- [ ] Navigate to `/activities/1`
- [ ] Check Network:
  - [ ] GET `/api/activities/1`
  - [ ] GET `/api/activities/1/reviews`
  - [ ] GET `/api/related/activities/1`
- [ ] ✅ Page displays activity data

### Favorite & Review (Same as Destination)
- [ ] Test favorite add/remove
  - [ ] POST/DELETE `/api/favorites` with `item_type: "activity"`
- [ ] Test review submission
  - [ ] POST `/api/activities/1/reviews`

### View Duration Tracking
- [ ] Stay 15+ seconds
- [ ] Navigate away
- [ ] Check Network:
  - [ ] POST `/api/interactions/view` with `item_type: "activity"`
  - [ ] ✅ Duration ≥15 seconds

---

## 8. 🔍 Universal Search Testing

### Opening Search
- [ ] Click search button in header (🔍 icon)
- [ ] ✅ Search input should appear and auto-focus
- [ ] ✅ Search button replaced with search bar

### Search Execution
- [ ] Type "sumedang" in search
- [ ] Wait 300ms (debounce)
- [ ] Check Network:
  - [ ] GET `/api/search/all?q=sumedang` called
- [ ] ✅ Dropdown shows combined results
- [ ] ✅ Results grouped into "Destinasi" and "Aktivitas" sections
- [ ] ✅ Each result shows: image, name, description snippet, category badge

### No Results
- [ ] Type "xyz123nonexistent"
- [ ] ✅ Should show "Tidak ada hasil untuk 'xyz123nonexistent'"
- [ ] ✅ Shows "Coba kata kunci lain"

### Click Result
- [ ] Search for "tahu"
- [ ] Click on a result
- [ ] ✅ Should navigate to detail page
- [ ] ✅ Search bar closes
- [ ] ✅ Search input clears

### Click Outside
- [ ] Open search
- [ ] Type something
- [ ] Click outside the search component
- [ ] ✅ Search dropdown closes

---

## 9. ❤️ Favorites Page Testing

### Unauthenticated Access
- [ ] Logout
- [ ] Navigate to `/favorites`
- [ ] ✅ Should redirect to `/login`

### Empty State
- [ ] Login with new account (no favorites yet)
- [ ] Navigate to `/favorites`
- [ ] ✅ Should show empty state
- [ ] ✅ Shows "Belum Ada Favorit" message
- [ ] ✅ Shows links to explore destinations/activities

### Adding Favorites
- [ ] Go to destinations page
- [ ] Open a destination detail
- [ ] Add to favorites (❤️ button)
- [ ] Go to `/favorites`
- [ ] Check Network:
  - [ ] GET `/api/favorites` called
- [ ] ✅ Should show the favorited destination in "Destinasi Favorit" section

### Tabs
- [ ] Add 2 destinations and 2 activities to favorites
- [ ] Visit `/favorites`
- [ ] Click "Semua" tab
  - [ ] ✅ Shows total count: "Semua (4)"
  - [ ] ✅ Shows both destinations and activities
- [ ] Click "Destinasi" tab
  - [ ] ✅ Shows "Destinasi (2)"
  - [ ] ✅ Only shows destination cards
- [ ] Click "Aktivitas" tab
  - [ ] ✅ Shows "Aktivitas (2)"
  - [ ] ✅ Only shows activity cards

### Removing Favorites
- [ ] Hover over a favorite card
- [ ] ✅ Should see ❌ button in top-right corner
- [ ] Click ❌ button
- [ ] Check Network:
  - [ ] DELETE `/api/favorites/<item_type>/<item_id>`
- [ ] ✅ Card should disappear from list
- [ ] ✅ Count in tab should update

---

## 10. 📊 MAB Data Collection Verification

### Database Check - User Interactions Table
**This is CRITICAL for your research!**

```sql
-- Check all interactions
SELECT * FROM user_interactions 
ORDER BY created_at DESC 
LIMIT 20;

-- Count interactions by type
SELECT interaction_type, COUNT(*) as count 
FROM user_interactions 
GROUP BY interaction_type;

-- Check click interactions
SELECT ui.*, d.name as destination_name
FROM user_interactions ui
LEFT JOIN destinations d ON ui.item_id = d.id AND ui.item_type = 'destination'
WHERE ui.interaction_type = 'click'
ORDER BY ui.created_at DESC;

-- Check view interactions with duration
SELECT ui.*, ui.extra_data->>'duration' as duration_seconds
FROM user_interactions ui
WHERE ui.interaction_type = 'view'
ORDER BY ui.created_at DESC;

-- User behavior summary
SELECT 
    u.email,
    COUNT(CASE WHEN ui.interaction_type = 'click' THEN 1 END) as clicks,
    COUNT(CASE WHEN ui.interaction_type = 'view' THEN 1 END) as views,
    AVG(CAST(ui.extra_data->>'duration' AS INTEGER)) as avg_view_duration
FROM users u
LEFT JOIN user_interactions ui ON u.id = ui.user_id
GROUP BY u.id, u.email;
```

### Expected Results
- [ ] ✅ Click interactions recorded with:
  - `user_id` (logged in user)
  - `item_type` ('destination' or 'activity')
  - `item_id` (ID of clicked item)
  - `interaction_type` = 'click'
  - `created_at` timestamp

- [ ] ✅ View interactions recorded with:
  - Same user and item data
  - `interaction_type` = 'view'
  - `extra_data` JSON contains `{"duration": <seconds>}`
  - Duration > 0

### Recommendation Algorithm Data
- [ ] Check if recommendations API uses interaction data:
  - [ ] Visit `/api/recommendations/personalized` endpoint
  - [ ] ✅ Should return different results based on user interactions
  - [ ] Test with 2 different users:
    - User A clicks only "alam" destinations
    - User B clicks only "kuliner" destinations
    - [ ] ✅ User A recommendations should favor "alam"
    - [ ] ✅ User B recommendations should favor "kuliner"

---

## 11. 🔄 JWT Token Management Testing

### Token in API Calls
- [ ] Login
- [ ] Open Network tab
- [ ] Navigate to any page that calls APIs
- [ ] Select any API request
- [ ] Check Request Headers:
  - [ ] ✅ `Authorization: Bearer <token>` header present
  - [ ] ✅ Token matches the one in localStorage

### Token Expiration (30 minutes)
**Optional - Time-intensive test**
- [ ] Login
- [ ] Wait 30+ minutes (or modify token expiry in backend to 1 minute for testing)
- [ ] Try any authenticated action (add favorite, submit review)
- [ ] ✅ Should get 401 error
- [ ] ✅ Should auto-logout and redirect to `/login`
- [ ] ✅ localStorage cleared

### Token Invalid
- [ ] Login
- [ ] Open localStorage
- [ ] Modify `access_token` to invalid value: "invalid_token_123"
- [ ] Refresh page
- [ ] ✅ Should auto-logout due to getCurrentUser failure
- [ ] ✅ Redirects to login on any authenticated action

---

## 12. 🎨 UI/UX Testing

### Loading States
- [ ] Check all pages show loading spinner while fetching data
- [ ] ✅ Home: recommendations and activities loading
- [ ] ✅ Destinations/Activities: cards loading
- [ ] ✅ Detail pages: content loading
- [ ] ✅ Favorites: loading state

### Error Handling
- [ ] Stop backend server
- [ ] Try to load destinations page
- [ ] ✅ Should show error or empty state gracefully
- [ ] ✅ No console errors breaking the app

### Responsive Design (Optional)
- [ ] Test on mobile viewport (375px width)
- [ ] ✅ Header menu collapses to hamburger
- [ ] ✅ Cards stack vertically
- [ ] ✅ Search bar adapts to mobile
- [ ] ✅ Forms remain usable

---

## 13. 📝 Reviews System Testing

### Review Display
- [ ] Visit destination/activity detail with existing reviews
- [ ] ✅ Shows review count: "X Ulasan"
- [ ] ✅ Each review shows:
  - User name or initial
  - Star rating (⭐⭐⭐⭐⭐)
  - Date in Indonesian format
  - Comment text

### Multiple Reviews
- [ ] Submit 3 different reviews (different ratings)
- [ ] ✅ All appear in reviews list
- [ ] ✅ Ordered by most recent first
- [ ] ✅ Review count updates

---

## 14. 🔗 Related Items Testing

### Related Destinations
- [ ] Visit a destination with category "alam"
- [ ] Scroll to "Destinasi Terkait" section
- [ ] ✅ Should show 3-4 related destinations
- [ ] ✅ All should have same or similar category
- [ ] ✅ Should NOT include the current destination
- [ ] Click on a related destination
- [ ] ✅ Should navigate to that destination's detail page

### Related Activities
- [ ] Visit an activity detail page
- [ ] Check "Aktivitas Terkait" section
- [ ] ✅ Shows related activities with same category

---

## 15. 🧹 Edge Cases & Error Scenarios

### Invalid IDs
- [ ] Navigate to `/destinations/99999` (non-existent)
- [ ] ✅ Should show "Destinasi tidak ditemukan" error
- [ ] ✅ Shows "Kembali ke Destinasi" button

### Duplicate Favorites
- [ ] Add destination to favorites
- [ ] Try adding same destination again (via API or multiple clicks)
- [ ] ✅ Should handle gracefully (no duplicate in database)

### Empty Search
- [ ] Type spaces only in search: "    "
- [ ] ✅ Should not trigger API call
- [ ] ✅ No results shown

### Network Errors
- [ ] Block API requests in DevTools Network tab
- [ ] Try actions (login, load pages, etc.)
- [ ] ✅ Should show error messages
- [ ] ✅ App doesn't crash

---

## 16. 🔒 Security Testing

### SQL Injection Attempt
- [ ] Try searching: `'; DROP TABLE destinations; --`
- [ ] ✅ Should return no results or safe error
- [ ] ✅ Database tables intact

### XSS Attempt
- [ ] Submit review with: `<script>alert('XSS')</script>`
- [ ] ✅ Should display as text, not execute
- [ ] ✅ No alert popup

### Direct API Access
- [ ] Open new tab
- [ ] Try accessing: `http://localhost:8000/api/favorites`
- [ ] ✅ Should require authentication (401 if no token)

---

## 17. 📈 Performance Testing (Optional)

### API Response Times
- [ ] Check Network tab waterfall
- [ ] ✅ All API calls < 1 second
- [ ] ✅ Parallel requests (destinations + activities) load efficiently

### Bundle Size
- [ ] Check built frontend size
- [ ] Run: `npm run build`
- [ ] ✅ Total bundle < 500KB (gzipped)

---

## ✅ Final Verification Checklist

### Critical Features Working
- [ ] ✅ Users can register and login
- [ ] ✅ JWT authentication working
- [ ] ✅ Click tracking recorded in database
- [ ] ✅ View duration tracking recorded in database
- [ ] ✅ Personalized recommendations loading
- [ ] ✅ Search returns relevant results
- [ ] ✅ Favorites can be added and removed
- [ ] ✅ Reviews can be submitted
- [ ] ✅ Related items display correctly
- [ ] ✅ Protected routes require authentication

### Database Verification
- [ ] ✅ `users` table has registered users
- [ ] ✅ `user_interactions` table has click and view records
- [ ] ✅ `destination_reviews` and `activity_reviews` have submitted reviews
- [ ] ✅ `user_favorites` table has favorite records

### MAB Algorithm Ready
- [ ] ✅ Interaction data collected for at least 3 users
- [ ] ✅ Each user has 10+ clicks and 5+ views
- [ ] ✅ Data includes timestamps and durations
- [ ] ✅ Ready for MAB algorithm evaluation

---

## 🐛 Bug Tracking

**Found Issues:**
1. _[Issue description]_ - Status: _[Fixed/Pending]_
2. _[Issue description]_ - Status: _[Fixed/Pending]_

**Notes:**
- _[Any observations or improvements needed]_

---

## 📊 Test Results Summary

**Date Tested:** ___________
**Tester:** ___________
**Total Tests:** _____ 
**Passed:** _____ 
**Failed:** _____
**Pass Rate:** _____%

**Ready for Production:** [ ] Yes [ ] No

**Next Steps:**
- _[List any remaining tasks]_

---

## 🎓 For Your Research

**MAB Algorithm Data Collection Verified:**
- [ ] User interaction data comprehensive
- [ ] Click-through rates trackable
- [ ] View duration measurable
- [ ] User preferences captured
- [ ] Popularity bias reducible with collected data

**Evaluation Metrics Ready:**
- [ ] Diversity of recommendations
- [ ] Long-tail coverage
- [ ] User engagement metrics
- [ ] Exploration vs exploitation balance

---

**Good luck with testing! 🚀**
