import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
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
        # Simpan similarity matrix dari content_recommender untuk digunakan oleh MMR
        self.similarity_matrix = None
    
    async def train(self, db: AsyncSession):
        """Train both recommenders"""
        try:
            results = {}
            
            # Train content-based recommender
            try:
                content_result = await self.content_recommender.train(db)
                results['content_based'] = content_result
                # Simpan similarity matrix dari content_recommender setelah training
                self.similarity_matrix = self.content_recommender.similarity_matrix
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
            
            return results
            
        except Exception as e:
            raise Exception(f"Hybrid training failed: {str(e)}")
    
    def _rerank_with_mmr(self, recommendations: List[Dict[str, Any]], lambda_val: float, num_final_recs: int) -> List[Dict[str, Any]]:
        """
        Melakukan re-ranking pada daftar rekomendasi menggunakan algoritma MMR.

        Args:
            recommendations (List[Dict]): List rekomendasi awal dengan 'destination_id' dan 'score'.
            lambda_val (float): Parameter untuk menyeimbangkan relevansi dan keberagaman (antara 0 dan 1).
            num_final_recs (int): Jumlah rekomendasi final yang diinginkan.

        Returns:
            List[Dict]: List rekomendasi yang sudah di-rerank.
        """
        if not recommendations or self.similarity_matrix is None:
            return recommendations[:num_final_recs]

        # Convert ke DataFrame untuk memudahkan manipulasi
        candidates_df = pd.DataFrame(recommendations)
        
        # Pastikan ada kolom yang diperlukan
        if 'destination_id' not in candidates_df.columns or 'score' not in candidates_df.columns:
            return recommendations[:num_final_recs]
        
        # Inisialisasi daftar rekomendasi final
        reranked_recs = []
        remaining_candidates = candidates_df.copy()
        
        # Pilih item pertama dengan skor relevansi tertinggi
        if not remaining_candidates.empty:
            first_idx = remaining_candidates['score'].idxmax()
            first_rec = remaining_candidates.loc[first_idx].to_dict()
            reranked_recs.append(first_rec)
            remaining_candidates = remaining_candidates.drop(first_idx)

        # Lakukan proses iteratif untuk memilih sisa item
        while len(reranked_recs) < num_final_recs and not remaining_candidates.empty:
            best_item = None
            best_mmr_score = -float('inf')
            best_idx = None

            for idx, candidate_row in remaining_candidates.iterrows():
                candidate_id = candidate_row['destination_id']
                relevance_score = candidate_row['score']
                
                # Hitung similarity dengan item yang sudah terpilih
                similarity_scores = []
                for selected_item in reranked_recs:
                    selected_id = selected_item['destination_id']
                    try:
                        # Cari index destination di destinations_df
                        if (self.content_recommender.destinations_df is not None and 
                            'id' in self.content_recommender.destinations_df.columns):
                            
                            candidate_df_idx = self.content_recommender.destinations_df[
                                self.content_recommender.destinations_df['id'] == candidate_id
                            ].index
                            selected_df_idx = self.content_recommender.destinations_df[
                                self.content_recommender.destinations_df['id'] == selected_id
                            ].index
                            
                            if len(candidate_df_idx) > 0 and len(selected_df_idx) > 0:
                                candidate_matrix_idx = candidate_df_idx[0]
                                selected_matrix_idx = selected_df_idx[0]
                                sim = self.similarity_matrix[candidate_matrix_idx, selected_matrix_idx]
                                similarity_scores.append(sim)
                            else:
                                similarity_scores.append(0)
                        else:
                            similarity_scores.append(0)
                    except (KeyError, IndexError, TypeError):
                        # Jika salah satu ID tidak ada di matriks, anggap similarity 0
                        similarity_scores.append(0)

                max_similarity = max(similarity_scores) if similarity_scores else 0

                # Hitung MMR Score
                mmr_score = lambda_val * relevance_score - (1 - lambda_val) * max_similarity
                
                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_item = candidate_row.to_dict()
                    best_idx = idx
            
            if best_item is not None:
                reranked_recs.append(best_item)
                remaining_candidates = remaining_candidates.drop(best_idx)
            else:
                # Jika tidak ada item lagi yang bisa dipilih, hentikan
                break
                
        return reranked_recs
    
    async def predict(self, user_id: int, num_recommendations: int = 10, db: AsyncSession = None, lambda_mmr: float = 0.7, mab_optimizer=None, context: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], Optional[int]]:
        """
        Generate hybrid recommendations with contextual MMR diversification
        
        Args:
            user_id: ID pengguna
            num_recommendations: Jumlah rekomendasi yang diinginkan
            db: Database session
            lambda_mmr: Parameter MMR untuk menyeimbangkan relevansi (0-1) - used as fallback
            mab_optimizer: MAB optimizer instance untuk dynamic lambda selection
            context: Real-time context data dari RealTimeContextService
                       
        Returns:
            Tuple: (recommendations, arm_index) where arm_index is the selected MAB arm
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        try:
            content_recs = []
            collab_recs = []
            
            # Get content-based recommendations (ambil lebih banyak kandidat untuk MMR)
            if self.content_recommender.is_trained:
                try:
                    content_recs = await self.content_recommender.predict(
                        user_id, num_recommendations * 3, db  # Get more candidates for MMR
                    )
                except Exception as e:
                    print(f"Content-based prediction failed: {e}")
            
            # Get collaborative recommendations (ambil lebih banyak kandidat untuk MMR)
            if self.collaborative_recommender.is_trained:
                try:
                    collab_recs = await self.collaborative_recommender.predict(
                        user_id, num_recommendations * 3, db  # Get more candidates for MMR
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
            candidate_recommendations = []
            for dest_id, scores in hybrid_scores.items():
                final_score = scores['content_score'] + scores['collab_score']
                rec = scores['destination'].copy()
                rec['score'] = round(final_score, 4)
                rec['algorithm'] = 'hybrid'
                rec['explanation'] = f"Hybrid: Content({scores['content_score']:.3f}) + Collaborative({scores['collab_score']:.3f})"
                candidate_recommendations.append(rec)
            
            # Sort candidates by relevance score
            candidate_recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            # Determine lambda value using Contextual MAB or fallback
            selected_arm_index = None
            if mab_optimizer is not None:
                # Contextual MAB selects the optimal arm based on current context
                selected_arm_index = mab_optimizer.select_arm(context)
                dynamic_lambda = mab_optimizer.get_lambda_value(selected_arm_index)
                
                # Log contextual decision
                if context:
                    print(f"🤖 Contextual MAB Decision: λ={dynamic_lambda:.2f} "
                          f"for weather={context.get('weather', 'unknown')}, "
                          f"weekend={context.get('is_weekend', 'unknown')}")
            else:
                # Fallback to provided lambda_mmr if MAB not available
                dynamic_lambda = lambda_mmr
                print(f"⚠️ Fallback to static λ={dynamic_lambda:.2f} (no MAB/context)")
            
            # Apply MMR re-ranking for diversification using contextual lambda
            if self.similarity_matrix is not None and len(candidate_recommendations) > num_recommendations:
                # Apply MMR only if we have similarity matrix and enough candidates
                final_recommendations = self._rerank_with_mmr(
                    recommendations=candidate_recommendations,
                    lambda_val=dynamic_lambda,
                    num_final_recs=num_recommendations
                )
                
                print(f"✅ MMR applied with λ={dynamic_lambda:.2f}: "
                      f"{len(candidate_recommendations)} candidates → {len(final_recommendations)} final")
            else:
                # Fallback to traditional top-N if MMR cannot be applied
                final_recommendations = candidate_recommendations[:num_recommendations]
                print(f"⚠️ MMR skipped: using top-{num_recommendations} by relevance only")
            
            return final_recommendations, selected_arm_index
            
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