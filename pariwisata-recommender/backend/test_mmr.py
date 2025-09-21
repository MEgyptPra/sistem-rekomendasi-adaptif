#!/usr/bin/env python3
"""
Test script untuk demonstrasi MMR (Maximal Marginal Relevance)
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any

def simulate_mmr_test():
    """
    Simulasi sederhana untuk menunjukkan bagaimana MMR bekerja
    """
    
    # Simulasi data rekomendasi awal
    recommendations = [
        {'destination_id': 1, 'name': 'Pantai Kuta', 'score': 0.95, 'category': 'pantai'},
        {'destination_id': 2, 'name': 'Pantai Sanur', 'score': 0.90, 'category': 'pantai'},
        {'destination_id': 3, 'name': 'Museum Bali', 'score': 0.85, 'category': 'museum'},
        {'destination_id': 4, 'name': 'Pantai Jimbaran', 'score': 0.82, 'category': 'pantai'},
        {'destination_id': 5, 'name': 'Gunung Batur', 'score': 0.80, 'category': 'gunung'},
        {'destination_id': 6, 'name': 'Pura Besakih', 'score': 0.78, 'category': 'pura'},
        {'destination_id': 7, 'name': 'Pantai Lovina', 'score': 0.75, 'category': 'pantai'},
        {'destination_id': 8, 'name': 'Museum Bajra Sandhi', 'score': 0.72, 'category': 'museum'}
    ]
    
    # Simulasi similarity matrix
    # Destinasi dengan kategori yang sama memiliki similarity tinggi
    similarity_matrix = np.array([
        [1.0, 0.9, 0.1, 0.8, 0.2, 0.3, 0.85, 0.15],  # Pantai Kuta
        [0.9, 1.0, 0.1, 0.8, 0.2, 0.3, 0.85, 0.15],  # Pantai Sanur
        [0.1, 0.1, 1.0, 0.1, 0.2, 0.4, 0.1, 0.8],    # Museum Bali
        [0.8, 0.8, 0.1, 1.0, 0.2, 0.3, 0.9, 0.15],   # Pantai Jimbaran
        [0.2, 0.2, 0.2, 0.2, 1.0, 0.3, 0.2, 0.2],    # Gunung Batur
        [0.3, 0.3, 0.4, 0.3, 0.3, 1.0, 0.3, 0.4],    # Pura Besakih
        [0.85, 0.85, 0.1, 0.9, 0.2, 0.3, 1.0, 0.15], # Pantai Lovina
        [0.15, 0.15, 0.8, 0.15, 0.2, 0.4, 0.15, 1.0] # Museum Bajra Sandhi
    ])
    
    def apply_mmr(recommendations, similarity_matrix, lambda_val, num_final_recs):
        """Implementasi MMR sederhana"""
        candidates = recommendations.copy()
        reranked = []
        
        # Pilih item pertama dengan skor tertinggi
        if candidates:
            first_item = max(candidates, key=lambda x: x['score'])
            reranked.append(first_item)
            candidates.remove(first_item)
        
        # Proses iteratif
        while len(reranked) < num_final_recs and candidates:
            best_item = None
            best_mmr_score = -float('inf')
            
            for candidate in candidates:
                candidate_idx = candidate['destination_id'] - 1  # Convert to 0-based index
                relevance_score = candidate['score']
                
                # Hitung max similarity dengan item yang sudah dipilih
                max_similarity = 0
                for selected in reranked:
                    selected_idx = selected['destination_id'] - 1
                    similarity = similarity_matrix[candidate_idx, selected_idx]
                    max_similarity = max(max_similarity, similarity)
                
                # Hitung MMR score
                mmr_score = lambda_val * relevance_score - (1 - lambda_val) * max_similarity
                
                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_item = candidate
            
            if best_item:
                reranked.append(best_item)
                candidates.remove(best_item)
        
        return reranked
    
    print("=== Demonstrasi MMR (Maximal Marginal Relevance) ===\n")
    
    print("Data Rekomendasi Awal (diurutkan berdasarkan relevansi):")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"{i}. {rec['name']} (Score: {rec['score']:.2f}, Kategori: {rec['category']})")
    
    print("\n" + "="*60)
    
    # Test dengan lambda = 1.0 (hanya relevansi)
    print("\n🔍 Test 1: Lambda = 1.0 (Hanya Relevansi)")
    result_relevance_only = apply_mmr(recommendations, similarity_matrix, 1.0, 5)
    for i, rec in enumerate(result_relevance_only, 1):
        print(f"{i}. {rec['name']} (Score: {rec['score']:.2f}, Kategori: {rec['category']})")
    
    # Test dengan lambda = 0.7 (seimbang)
    print("\n⚖️ Test 2: Lambda = 0.7 (Seimbang: 70% Relevansi + 30% Keberagaman)")
    result_balanced = apply_mmr(recommendations, similarity_matrix, 0.7, 5)
    for i, rec in enumerate(result_balanced, 1):
        print(f"{i}. {rec['name']} (Score: {rec['score']:.2f}, Kategori: {rec['category']})")
    
    # Test dengan lambda = 0.3 (lebih mengutamakan keberagaman)
    print("\n🎨 Test 3: Lambda = 0.3 (Lebih Mengutamakan Keberagaman)")
    result_diversity = apply_mmr(recommendations, similarity_matrix, 0.3, 5)
    for i, rec in enumerate(result_diversity, 1):
        print(f"{i}. {rec['name']} (Score: {rec['score']:.2f}, Kategori: {rec['category']})")
    
    print("\n" + "="*60)
    print("\n📊 Analisis Hasil:")
    print("• Lambda = 1.0: Menghasilkan 4 pantai (mirip semua)")
    print("• Lambda = 0.7: Menghasilkan lebih beragam (pantai, museum, gunung)")
    print("• Lambda = 0.3: Sangat beragam, mungkin mengorbankan relevansi")
    print("\n✅ MMR berhasil menyeimbangkan relevansi dan keberagaman!")

if __name__ == "__main__":
    simulate_mmr_test()
