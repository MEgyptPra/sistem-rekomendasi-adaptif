import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.base_recommender import BaseRecommender
from app.services.content_based_recommender import ContentBasedRecommender
from app.services.collaborative_recommender import CollaborativeRecommender
from app.models.user import User
from app.models.rating import Rating

class HybridRecommender(BaseRecommender):
    """Hybrid Recommendation System combining Content-Based and Collaborative Filtering"""
    
    def __init__(self):
        super().__init__()
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeRecommender()
        self.content_weight = 0.6
        self.collaborative_weight = 0.4
        # Store reference to similarity matrix for MMR
        self.similarity_matrix = None
        self.destinations_df = None
    
    async def train(self, db: AsyncSession):
        """Train both recommenders"""
        try:
            results = {}
            
            # Train content-based recommender
            try:
                content_result = await self.content_recommender.train(db)
                results['content_based'] = content_result
            except Exception as e:
                results['content_based'] = {"status": "failed", "error": str(e)}
            
            # Train collaborative recommender
            try:
                collab_result = await self.collaborative_recommender.train(db)
                results['collaborative'] = collab_result
            except Exception as e:
                results['collaborative'] = {"status": "failed", "error": str(e)}
            
            # Model is trained if at least one component is trained
            self.is_trained = (
                self.content_recommender.is_trained or 
                self.collaborative_recommender.is_trained
            )
            
            # Store similarity matrix and destinations dataframe from content recommender for MMR
            if self.content_recommender.is_trained:
                self.similarity_matrix = self.content_recommender.similarity_matrix
                self.destinations_df = self.content_recommender.destinations_df
            
            return results
            
        except Exception as e:
            raise Exception(f"Hybrid training failed: {str(e)}")
    
    def _rerank_with_mmr(self, recommendations, lambda_val, num_final_recs):
        """
        Melakukan re-ranking pada daftar rekomendasi menggunakan algoritma MMR.

        Args:
            recommendations (List[Dict]): List rekomendasi awal dengan key 'destination_id' dan 'score'.
            lambda_val (float): Parameter untuk menyeimbangkan relevansi dan keberagaman (antara 0 dan 1).
            num_final_recs (int): Jumlah rekomendasi final yang diinginkan.

        Returns:
            List[Dict]: List rekomendasi yang sudah di-rerank.
        """
        if not recommendations or self.similarity_matrix is None or self.destinations_df is None:
            return recommendations[:num_final_recs]

        # Convert to DataFrame for easier manipulation
        candidates_df = pd.DataFrame(recommendations)
        
        # Create mapping from destination_id to dataframe index for similarity matrix lookup
        dest_id_to_idx = {}
        for idx, row in self.destinations_df.iterrows():
            dest_id_to_idx[row['id']] = idx
        
        # Filter candidates that exist in similarity matrix
        valid_candidates = []
        for _, candidate in candidates_df.iterrows():
            if candidate['destination_id'] in dest_id_to_idx:
                valid_candidates.append(candidate.to_dict())
        
        if not valid_candidates:
            return recommendations[:num_final_recs]
        
        # Inisialisasi daftar rekomendasi final
        reranked_recs = []
        remaining_candidates = valid_candidates.copy()
        
        # Pilih item pertama dengan skor relevansi tertinggi
        if remaining_candidates:
            # Find candidate with highest score
            best_candidate = max(remaining_candidates, key=lambda x: x['score'])
            reranked_recs.append(best_candidate)
            remaining_candidates.remove(best_candidate)

        # Lakukan proses iteratif untuk memilih sisa item
        while len(reranked_recs) < num_final_recs and remaining_candidates:
            best_item = None
            best_mmr_score = -float('inf')

            for candidate_item in remaining_candidates:
                candidate_id = candidate_item['destination_id']
                relevance_score = candidate_item['score']
                
                # Get candidate index in similarity matrix
                candidate_idx = dest_id_to_idx[candidate_id]
                
                # Hitung similarity dengan item yang sudah terpilih
                similarity_scores = []
                for selected_item in reranked_recs:
                    selected_id = selected_item['destination_id']
                    if selected_id in dest_id_to_idx:
                        selected_idx = dest_id_to_idx[selected_id]
                        # Ambil nilai similarity dari matriks
                        sim = self.similarity_matrix[candidate_idx, selected_idx]
                        similarity_scores.append(sim)

                max_similarity = max(similarity_scores) if similarity_scores else 0

                # Hitung MMR Score
                mmr_score = lambda_val * relevance_score - (1 - lambda_val) * max_similarity
                
                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_item = candidate_item
            
            if best_item is not None:
                reranked_recs.append(best_item)
                remaining_candidates.remove(best_item)
            else:
                # Jika tidak ada item lagi yang bisa dipilih, hentikan
                break
                
        return reranked_recs
    
    async def predict(self, user_id: int, num_recommendations: int = 10, db: AsyncSession = None) -> List[Dict[str, Any]]:
        """Generate hybrid recommendations"""
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        try:
            content_recs = []
            collab_recs = []
            
            # Get content-based recommendations
            if self.content_recommender.is_trained:
                try:
                    content_recs = await self.content_recommender.predict(
                        user_id, num_recommendations * 2, db  # Get more candidates for MMR
                    )
                except Exception as e:
                    print(f"Content-based prediction failed: {e}")
            
            # Get collaborative recommendations
            if self.collaborative_recommender.is_trained:
                try:
                    collab_recs = await self.collaborative_recommender.predict(
                        user_id, num_recommendations * 2, db  # Get more candidates for MMR
                    )
                except Exception as e:
                    print(f"Collaborative prediction failed: {e}")
            
            # Combine recommendations
            if not content_recs and not collab_recs:
                raise ValueError("Both recommenders failed to generate recommendations")
            
            # Create hybrid scores
            hybrid_scores = {}
            
            # Add content-based scores
            for rec in content_recs:
                dest_id = rec['destination_id']
                hybrid_scores[dest_id] = {
                    'content_score': rec['score'] * self.content_weight,
                    'collab_score': 0,
                    'destination': rec
                }
            
            # Add collaborative scores
            for rec in collab_recs:
                dest_id = rec['destination_id']
                if dest_id in hybrid_scores:
                    hybrid_scores[dest_id]['collab_score'] = rec['score'] * self.collaborative_weight
                else:
                    hybrid_scores[dest_id] = {
                        'content_score': 0,
                        'collab_score': rec['score'] * self.collaborative_weight,
                        'destination': rec
                    }
            
            # Calculate final hybrid scores
            candidates_for_mmr = []
            for dest_id, scores in hybrid_scores.items():
                final_score = scores['content_score'] + scores['collab_score']
                rec = scores['destination'].copy()
                rec['score'] = round(final_score, 4)
                rec['algorithm'] = 'hybrid'
                rec['explanation'] = f"Hybrid: Content({scores['content_score']:.3f}) + Collaborative({scores['collab_score']:.3f})"
                candidates_for_mmr.append(rec)
            
            # Sort candidates by relevance score first
            candidates_for_mmr.sort(key=lambda x: x['score'], reverse=True)
            
            # Apply MMR re-ranking for diversity
            # Use lambda_val=0.7 to balance relevance and diversity
            lambda_for_mmr = 0.7
            final_recommendations = self._rerank_with_mmr(
                recommendations=candidates_for_mmr,
                lambda_val=lambda_for_mmr,
                num_final_recs=num_recommendations
            )
            
            return final_recommendations
            
        except Exception as e:
            raise Exception(f"Hybrid prediction failed: {str(e)}")
    
    async def explain(self, user_id: int, destination_id: int, db: AsyncSession = None) -> Dict[str, Any]:
        """Explain hybrid recommendation"""
        try:
            explanations = {}
            
            # Get content-based explanation
            if self.content_recommender.is_trained:
                try:
                    content_exp = await self.content_recommender.explain(user_id, destination_id, db)
                    explanations['content_based'] = content_exp
                except Exception as e:
                    explanations['content_based'] = {"error": str(e)}
            
            # Get collaborative explanation
            if self.collaborative_recommender.is_trained:
                try:
                    collab_exp = await self.collaborative_recommender.explain(user_id, destination_id, db)
                    explanations['collaborative'] = collab_exp
                except Exception as e:
                    explanations['collaborative'] = {"error": str(e)}
            
            return {
                "explanation": "Hybrid recommendation combining multiple algorithms",
                "weights": {
                    "content_based": self.content_weight,
                    "collaborative": self.collaborative_weight
                },
                "component_explanations": explanations
            }
            
        except Exception as e:
            raise Exception(f"Hybrid explanation failed: {str(e)}")
    
    async def get_user_profile(self, user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get comprehensive user profile for recommendations"""
        try:
            user = await db.get(User, user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Get user rating statistics
            from sqlalchemy import func
            rating_stats = await db.execute(
                select(
                    func.count(Rating.id).label('rating_count'),
                    func.avg(Rating.rating).label('avg_rating'),
                    func.min(Rating.rating).label('min_rating'),
                    func.max(Rating.rating).label('max_rating')
                ).where(Rating.user_id == user_id)
            )
            stats = rating_stats.first()
            
            return {
                "user_id": user.id,
                "name": user.name,
                "preferences": user.preferences.split(',') if user.preferences else [],
                "rating_stats": {
                    "total_ratings": stats.rating_count or 0,
                    "average_rating": round(float(stats.avg_rating), 2) if stats.avg_rating else 0,
                    "min_rating": float(stats.min_rating) if stats.min_rating else 0,
                    "max_rating": float(stats.max_rating) if stats.max_rating else 0
                },
                "recommendation_readiness": {
                    "content_based": bool(user.preferences),
                    "collaborative": (stats.rating_count or 0) >= 3,
                    "hybrid": bool(user.preferences) or (stats.rating_count or 0) >= 3
                }
            }
            
        except Exception as e:
            raise Exception(f"Get user profile failed: {str(e)}")