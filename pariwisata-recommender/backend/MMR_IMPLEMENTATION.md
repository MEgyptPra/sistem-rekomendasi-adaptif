# MMR Implementation - Maximal Marginal Relevance

## Overview
Implementasi MMR (Maximal Marginal Relevance) telah berhasil ditambahkan ke `HybridRecommender` untuk meningkatkan keberagaman rekomendasi sambil tetap mempertahankan relevansi.

## What's Changed

### 1. Modified `HybridRecommender.__init__()`
- Menambahkan `self.similarity_matrix = None` untuk menyimpan matriks kemiripan

### 2. Updated `HybridRecommender.train()`
- Menyimpan similarity matrix dari content-based recommender setelah training:
```python
self.similarity_matrix = self.content_recommender.similarity_matrix
```

### 3. Added `_rerank_with_mmr()` Method
- Implementasi core algorithm MMR
- Menggunakan greedy approach untuk memilih item yang optimal
- Menyeimbangkan relevansi dan keberagaman menggunakan parameter lambda

### 4. Enhanced `predict()` Method
- Menambahkan parameter `lambda_mmr` (default: 0.7)
- Mengambil lebih banyak kandidat (3x) untuk memberikan ruang diversifikasi
- Menerapkan MMR re-ranking sebelum mengembalikan hasil

## How MMR Works

MMR menggunakan formula:
```
MMR(Di) = λ × Rel(Di) - (1-λ) × max Sim(Di, Dj)
```

Dimana:
- `λ` (lambda): Parameter keseimbangan (0-1)
- `Rel(Di)`: Skor relevansi destinasi i
- `Sim(Di, Dj)`: Similarity antara destinasi i dan j yang sudah terpilih

## Lambda Values Guide

| Lambda | Behavior | Use Case |
|--------|----------|----------|
| 1.0 | Hanya relevansi (seperti sistem lama) | Ketika user sangat spesifik |
| 0.7 | **Seimbang** (70% relevansi, 30% diversity) | **Recommended default** |
| 0.5 | Equal balance | Eksplorasi dan eksploitasi seimbang |
| 0.3 | Lebih mengutamakan diversity | User ingin eksplorasi banyak jenis |
| 0.0 | Hanya diversity (tidak recommended) | Testing only |

## Testing MMR

Jalankan script demonstrasi:
```bash
python test_mmr.py
```

Script ini menunjukkan bagaimana MMR mengubah urutan rekomendasi berdasarkan nilai lambda yang berbeda.

## API Usage

```python
# Basic usage (lambda = 0.7)
recommendations = await hybrid_recommender.predict(user_id=1, num_recommendations=10, db=db)

# Custom lambda for more diversity
recommendations = await hybrid_recommender.predict(
    user_id=1, 
    num_recommendations=10, 
    db=db,
    lambda_mmr=0.5  # More diversity
)

# Pure relevance (disable MMR)
recommendations = await hybrid_recommender.predict(
    user_id=1, 
    num_recommendations=10, 
    db=db,
    lambda_mmr=1.0  # No diversification
)
```

## Benefits

1. **Improved User Experience**: Rekomendasi lebih beragam dan menarik
2. **Reduced Echo Chamber**: Menghindari rekomendasi yang terlalu mirip
3. **Flexible Control**: Parameter lambda dapat disesuaikan per user atau context
4. **Research Ready**: Foundation untuk implementasi Multi-Armed Bandit (MAB)

## Next Steps

- [ ] Implement Multi-Armed Bandit untuk optimasi lambda secara adaptive
- [ ] A/B testing dengan nilai lambda yang berbeda
- [ ] User feedback integration untuk learning lambda optimal
- [ ] Performance monitoring dan evaluation metrics

## Performance Notes

- MMR menambahkan kompleksitas O(n²) dimana n = jumlah kandidat
- Untuk performa optimal, batasi kandidat maksimal 50-100 item
- Similarity matrix sudah dihitung sekali saat training, jadi overhead minimal

## Fallback Behavior

Jika similarity matrix tidak tersedia atau kandidat terlalu sedikit, sistem akan fallback ke urutan berdasarkan relevansi tradisional.
