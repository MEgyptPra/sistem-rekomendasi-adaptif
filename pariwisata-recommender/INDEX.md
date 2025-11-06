# 📚 Documentation Index - Sistem Rekomendasi Adaptif

## 🎯 Quick Navigation

### For Quick Testing:
👉 **[TESTING_ML_RECOMMENDATIONS.md](TESTING_ML_RECOMMENDATIONS.md)** - Step-by-step cara test apakah website pakai ML model atau tidak

### For Complete Understanding:
👉 **[COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md)** - Dokumentasi lengkap arsitektur, hubungan notebook-website, dan testing

### For Architecture Details:
- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** - Visual diagrams sistem
- **[RESEARCH_VS_PRODUCTION_VISUAL.md](RESEARCH_VS_PRODUCTION_VISUAL.md)** - Perbandingan notebook vs production

### For Incremental Learning:
- **[INCREMENTAL_LEARNING_EXPLAINED.md](INCREMENTAL_LEARNING_EXPLAINED.md)** - Penjelasan incremental learning (Bahasa Indonesia)
- **[INCREMENTAL_LEARNING_GUIDE.md](backend/INCREMENTAL_LEARNING_GUIDE.md)** - Technical guide (English)

### For Notebook Integration:
👉 **[NOTEBOOK_TO_PRODUCTION_GUIDE.md](NOTEBOOK_TO_PRODUCTION_GUIDE.md)** - Bagaimana notebook research dipakai di production

---

## 🚀 Quick Start: Test Your System

### 1. Start Backend
```bash
cd pariwisata-recommender/backend
python -m uvicorn main:app --reload
```

### 2. Test API (Open in Browser)
```
http://localhost:8000/api/recommendations/personalized?algorithm=auto&user_id=1
```

### 3. Check Response
**Look for the `"algorithm"` field**:

✅ **If you see**: `"hybrid_mab_with_incremental"`
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
**✅ CONGRATS!** Your website IS using the ML model from your research!
- Content-Based Filtering ✅
- Collaborative Filtering ✅
- MAB Optimizer ✅
- Context Awareness ✅
- MMR Diversification ✅
- Incremental Learning Boost ✅

---

❌ **If you see**: `"incremental_default"` or `"incremental_learning"`
```json
{
  "algorithm": "incremental_default",
  "message": "Trending destinations",
  "info": {
    "uses_ml_model": false,
    "uses_incremental": true
  }
}
```
**⚠️ INFO:** Website using incremental learning only (ML model not trained yet)
- This is NORMAL for new deployments
- Still works well with real-time trending
- Train ML model when you have enough data (500+ ratings)

---

## 📊 Understanding Your System

### Your Research (Notebook)
File: `notebooks/evaluasi_kuantitatif_PRODUCTION.ipynb`

**What it does**:
- Tests algorithms with historical data
- Calculates metrics (Precision, Recall, NDCG)
- Finds optimal parameters (λ, epsilon)
- Generates paper/thesis results

**Output**: Proof that algorithms work! ✅

---

### Your Website (Production)
Files: `pariwisata-recommender/backend/app/services/*.py`

**What it uses**:
- Same algorithms as notebook
- Optimized for real-time
- Added incremental learning
- Context-aware recommendations

**Output**: Live recommendations for users! 🚀

---

### The Connection
```
Notebook Research → Backend Implementation → Website
     (Proof)            (Optimized)         (Live)
```

**Both systems work together!**
- Notebook proves it works (research)
- Backend implements it (production)
- Incremental adds real-time trending (bonus)

---

## 🎯 Architecture Summary

### What Model is Used?

**Full System (when ML trained)**:
```
1. Context Awareness
   └─ Weather, time, season
   
2. MAB Optimizer
   └─ Selects optimal λ based on context
   └─ THIS is real-time adjustment!
   
3. Hybrid (CF + CB)
   └─ Content-Based + Collaborative Filtering
   └─ Weighted by λ from MAB
   
4. MMR Diversification
   └─ Reduces redundancy
   └─ Increases variety
   
5. Incremental Learning
   └─ Real-time trending boost
   └─ From views/clicks/ratings
   
= COMPLETE ML SYSTEM FROM YOUR RESEARCH! ✅
```

**Fallback (if ML not trained)**:
```
1. Incremental Learning
   └─ Real-time trending
   └─ Popularity scores
   └─ Statistical calculations
   
= FAST FALLBACK, ALWAYS WORKS! ✅
```

---

## 🔧 Common Commands

### Start Backend
```bash
cd pariwisata-recommender/backend
python -m uvicorn main:app --reload
```

### Check ML Status
```bash
curl http://localhost:8000/api/ml/status
```

### Train ML Model (if enough data)
```bash
curl -X POST http://localhost:8000/api/ml/train \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "hybrid", "force_retrain": false}'
```

### Test Recommendations
```bash
# Auto mode (smart selection)
curl "http://localhost:8000/api/recommendations/personalized?algorithm=auto&user_id=1"

# Force incremental
curl "http://localhost:8000/api/recommendations/personalized?algorithm=incremental"

# Force hybrid (will fail if not trained)
curl "http://localhost:8000/api/recommendations/personalized?algorithm=hybrid&user_id=1"
```

---

## ❓ FAQ Quick Answer

### Q: Apakah website pakai model dari notebook?
**A**: Ya! Kalau ML model sudah trained, website pakai algoritma yang sama dari notebook research Anda.

### Q: Kalau belum train model, website pakai apa?
**A**: Incremental learning (real-time trending). Fast, always works, no training needed!

### Q: Harus train model setiap hari?
**A**: TIDAK! Incremental learning auto-update setiap detik. ML model cukup retrain weekly/monthly.

### Q: MMR itu untuk apa?
**A**: Diversification (kurangi similarity), BUKAN real-time adjustment.

### Q: MAB itu untuk apa?
**A**: Pilih λ optimal untuk Hybrid (CF vs CB weight) based on context. INI yang real-time adjustment!

### Q: Bagaimana tahu website pakai ML atau tidak?
**A**: Cek response field `"algorithm"`:
- `"hybrid_mab_*"` = Pakai ML ✅
- `"incremental_*"` = Fallback only

---

## 📝 File Structure

```
pariwisata-recommender/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── content_based_recommender.py    ← From notebook
│   │   │   ├── collaborative_recommender.py    ← From notebook
│   │   │   ├── hybrid_recommender.py           ← From notebook
│   │   │   ├── mab_optimizer.py                ← From notebook
│   │   │   ├── real_time_data.py               ← Context awareness
│   │   │   ├── incremental_learner.py          ← NEW (real-time)
│   │   │   └── ml_service.py                   ← Orchestrator
│   │   │
│   │   └── api/
│   │       └── frontend_endpoints.py           ← API endpoints
│   │
│   ├── test_ml_recommendations.py              ← Test script
│   └── main.py                                 ← FastAPI app
│
├── notebooks/
│   └── evaluasi_kuantitatif_PRODUCTION.ipynb  ← Research notebook
│
└── Documentation/
    ├── COMPLETE_DOCUMENTATION.md               ← Full docs (THIS IS KEY!)
    ├── TESTING_ML_RECOMMENDATIONS.md           ← Testing guide
    ├── NOTEBOOK_TO_PRODUCTION_GUIDE.md         ← Notebook → Website
    ├── ARCHITECTURE_DIAGRAM.md                 ← Visual diagrams
    ├── RESEARCH_VS_PRODUCTION_VISUAL.md        ← Comparison
    ├── INCREMENTAL_LEARNING_EXPLAINED.md       ← Indonesian guide
    └── INDEX.md                                ← This file
```

---

## 🎯 Next Steps

### If ML Model Not Trained:
1. ✅ Website running with incremental learning (OK!)
2. 📊 Collect more data (users interact with website)
3. ⏰ Wait until 500+ ratings collected
4. 🤖 Train ML model: `POST /api/ml/train`
5. 🎉 Website automatically uses ML model!

### If ML Model Already Trained:
1. ✅ Verify with test: Check `"algorithm"` field
2. 📈 Monitor performance
3. 🔄 Optional: Setup weekly retrain
4. 🎉 Enjoy production-ready ML system!

---

## 📞 Quick Reference Card

| Want to... | File to Read | Time |
|-----------|--------------|------|
| Test if ML working | `TESTING_ML_RECOMMENDATIONS.md` | 5 min |
| Understand architecture | `COMPLETE_DOCUMENTATION.md` | 20 min |
| See diagrams | `ARCHITECTURE_DIAGRAM.md` | 10 min |
| Learn incremental | `INCREMENTAL_LEARNING_EXPLAINED.md` | 15 min |
| Connect notebook-website | `NOTEBOOK_TO_PRODUCTION_GUIDE.md` | 15 min |

---

## ✅ Verification Checklist

- [ ] Backend server running
- [ ] Can access `/api/ml/status`
- [ ] Can get recommendations from `/api/recommendations/personalized`
- [ ] Checked `"algorithm"` field in response
- [ ] Understand if using ML model or incremental
- [ ] Know next steps (train or monitor)

---

**All documentation created! Ready for production!** 🚀

For questions about specific topics, refer to the appropriate file above.
