# 🧪 Manual Testing Guide: Verify ML Recommendations

## Cara Test Apakah Website Menggunakan ML Model

### Step 1: Start Backend Server

```powershell
cd pariwisata-recommender/backend
python -m uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

### Step 2: Test API Endpoints (Gunakan Browser atau Postman)

#### Test 1: Check Server
```
http://localhost:8000/
```

**Expected**: `{"message": "Pariwisata API is running"}`

---

#### Test 2: Check ML Model Status
```
http://localhost:8000/api/ml/status
```

**Cek Output**:
- Jika `"is_trained": true` → ML model SUDAH trained
- Jika `"is_trained": false` → ML model BELUM trained

---

#### Test 3: Get Recommendations (Incremental Mode)
```
http://localhost:8000/api/recommendations/personalized?algorithm=incremental&limit=5
```

**Cek Response**:
```json
{
  "algorithm": "incremental_learning",
  "message": "Real-time learning - updates automatically!",
  "info": {
    "uses_ml_model": false,
    "uses_incremental": true
  },
  "recommendations": [...]
}
```

✅ **Ini menggunakan Incremental Learning** (real-time trending)

---

#### Test 4: Get Recommendations (Auto Mode - Smart Selection)
```
http://localhost:8000/api/recommendations/personalized?algorithm=auto&user_id=1&limit=5
```

**Cek Response**:

**Jika ML Model BELUM trained**:
```json
{
  "algorithm": "incremental_default",
  "info": {
    "uses_ml_model": false,
    "uses_incremental": true
  }
}
```
❌ **Website BELUM menggunakan ML model** (fallback ke incremental)

**Jika ML Model SUDAH trained**:
```json
{
  "algorithm": "hybrid_mab_with_incremental",
  "message": "Research-grade ML + Real-time boost!",
  "info": {
    "uses_ml_model": true,
    "uses_incremental": true
  }
}
```
✅ **Website SUDAH menggunakan ML model** (Hybrid CF+CB+MAB+Incremental)

---

#### Test 5: Try Force Hybrid (ML Model)
```
http://localhost:8000/api/recommendations/personalized?algorithm=hybrid&user_id=1&limit=5
```

**Jika ML BELUM trained**:
- Status: 500 Error
- Message: "Hybrid model belum di-train"
❌ **ML model not available**

**Jika ML SUDAH trained**:
- Status: 200 OK
- Algorithm: "hybrid_mab_with_incremental"
✅ **ML model working!**

---

### Step 3: Check Database Data (Optional)

Cek apakah ada cukup data untuk training:

```
http://localhost:8000/api/ml/status
```

Minimum data needed:
- 50+ users dengan ratings
- 500+ total ratings
- 20+ destinations

---

### Step 4: Train ML Model (Jika Belum)

**Jika punya cukup data**, train model dengan:

```powershell
curl -X POST http://localhost:8000/api/ml/train -H "Content-Type: application/json" -d "{\"algorithm\": \"hybrid\", \"force_retrain\": false}"
```

Or use Postman:
- Method: POST
- URL: `http://localhost:8000/api/ml/train`
- Body (JSON):
```json
{
  "algorithm": "hybrid",
  "force_retrain": false
}
```

**Expected**:
```json
{
  "status": "success",
  "training_time": "8.5 minutes",
  "model_saved": true
}
```

---

### Step 5: Re-test After Training

Setelah training selesai, test lagi:

```
http://localhost:8000/api/recommendations/personalized?algorithm=auto&user_id=1
```

**Now should see**:
```json
{
  "algorithm": "hybrid_mab_with_incremental",
  "info": {
    "uses_ml_model": true ✅ 
  }
}
```

---

## 🎯 Quick Verification Checklist

| Test | URL | Expected if ML Trained | Expected if NOT Trained |
|------|-----|----------------------|------------------------|
| Server | `/` | Status OK | Status OK |
| ML Status | `/api/ml/status` | `is_trained: true` | `is_trained: false` |
| Incremental | `/api/recommendations/personalized?algorithm=incremental` | Works (fallback) | Works (primary) |
| Auto Mode | `/api/recommendations/personalized?algorithm=auto` | Uses hybrid_mab | Uses incremental |
| Force Hybrid | `/api/recommendations/personalized?algorithm=hybrid` | 200 OK ✅ | 500 Error ❌ |

---

## 📊 What Each Algorithm Means

### Algorithm: `"incremental_learning"` or `"incremental_default"`
```
Source: Incremental Learner (NEW implementation)
Components:
  - Real-time trending
  - Popularity scores
  - View/click/rating tracking
Technology: Statistical scoring, NO ML training needed
Speed: < 100ms (very fast)
Personalization: Low (popularity-based)
```

### Algorithm: `"hybrid_mab_with_incremental"`
```
Source: ML Service (from notebook research) + Incremental boost
Components:
  - Content-Based Filtering (TF-IDF)
  - Collaborative Filtering (Matrix Factorization)
  - Hybrid (λ-weighted combination)
  - MAB (Multi-Armed Bandit) optimizer
  - Context Awareness (weather, time, season)
  - MMR (Diversification)
  - PLUS: Incremental Learning boost
Technology: Full ML pipeline from research
Speed: 1-2 seconds
Personalization: High (ML-based)
```

---

## 🎓 Conclusion Formula

```python
# Check response algorithm field:

if algorithm == "incremental_learning" or "incremental_default":
    print("❌ Website NOT using ML model yet")
    print("   → Using Incremental Learning (fallback)")
    print("   → Need to train ML model first")

elif algorithm == "hybrid_mab_with_incremental":
    print("✅ Website IS using ML model!")
    print("   → Content-Based + Collaborative Filtering")
    print("   → MAB optimization")
    print("   → Context-aware (weather, time)")
    print("   → MMR diversification")
    print("   → PLUS Incremental Learning boost")
    
elif algorithm == "popular_fallback":
    print("⚠️  Fallback mode (no data yet)")
```

---

## 🚀 Quick Test Commands (Copy-Paste)

```powershell
# 1. Start server
cd pariwisata-recommender/backend
python -m uvicorn main:app --reload

# 2. Open new terminal, test endpoints:

# Check server
curl http://localhost:8000/

# Check ML status
curl http://localhost:8000/api/ml/status

# Test incremental
curl "http://localhost:8000/api/recommendations/personalized?algorithm=incremental&limit=5"

# Test auto mode
curl "http://localhost:8000/api/recommendations/personalized?algorithm=auto&user_id=1&limit=5"

# Try hybrid (will fail if not trained)
curl "http://localhost:8000/api/recommendations/personalized?algorithm=hybrid&user_id=1&limit=5"
```

---

## 📝 Expected Results for New Website

### Phase 1: Just Deployed (No ML Training Yet)
```
✅ Incremental Learning: Working
❌ ML Model: Not trained
→ Algorithm: "incremental_default"
→ Conclusion: Website using ONLY incremental learning
```

### Phase 2: After Collecting Data & Training
```
✅ Incremental Learning: Working
✅ ML Model: Trained
→ Algorithm: "hybrid_mab_with_incremental"
→ Conclusion: Website using FULL ML SYSTEM + Incremental boost!
```

---

**Bottom Line**: Cek field `"algorithm"` dan `"uses_ml_model"` di response untuk tahu sistem mana yang dipakai!
