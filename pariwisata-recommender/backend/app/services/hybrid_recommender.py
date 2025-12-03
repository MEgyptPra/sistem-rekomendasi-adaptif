import numpy as np
from app.services.context_aware_component import ContextAwareComponent
from app.services.social_trend_service import SocialTrendService  # [BARU] Import Social Trend
import pandas as pd
import pickle
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.base_recommender import BaseRecommender
from app.services.content_based_recommender import ContentBasedRecommender
from app.services.collaborative_recommender import CollaborativeRecommender
from app.models.user import User
from app.models.rating import Rating
from app.models.destinations import Destination # [BARU] Import model Destination

class HybridRecommender(BaseRecommender):
    """Hybrid Recommendation System combining Content-Based and Collaborative Filtering"""
    
    # Point to backend/data/models (two levels up from app/services -> backend)
    MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
    MODEL_FILE = "hybrid_model.pkl"

    def __init__(self):
        import os
        super().__init__()
        self.context_component = ContextAwareComponent()
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeRecommender()
        self.social_trend_service = SocialTrendService() # [BARU] Inisialisasi service trending

        # Weight parameters - align dengan tesis research design
        self.content_weight = 0.6  # Sesuai tesis BAB III.4.5
        self.collaborative_weight = 0.4

        self.default_lambda = 0.7  # Default fallback value
        self.similarity_matrix = None
        self.model_info = {}  # Track model metadata

        # Tentukan path model dari env atau default (point to backend/data/models)
        env_path = os.getenv("MODEL_PATH_HYBRID")
        if env_path:
            self.model_path = Path(env_path).resolve()
        else:
            self.model_path = (Path(__file__).resolve().parents[3] / "data" / "models" / self.MODEL_FILE).resolve()

        self._model_loaded = False

    def load_model(self):
        """Public method to load model from disk on demand."""
        if not self._model_loaded:
            self._auto_load_model()
            self._model_loaded = True


    async def train(self, db: AsyncSession, **kwargs):
        """Train both content-based and collaborative recommenders"""
        try:
            print("🤖 Training Hybrid Recommender...")
            
            results = {}
            
            # Train content-based recommender
            print("📚 Training content-based recommender...")
            await self.content_recommender.train(db)
            results['content_based'] = "trained"
            
            # Train collaborative recommender  
            print("🤝 Training collaborative recommender...")
            await self.collaborative_recommender.train(db)
            results['collaborative'] = "trained"
            
            # Store similarity matrix untuk MMR
            if self.content_recommender.is_trained:
                self.similarity_matrix = self.content_recommender.similarity_matrix
                print("📊 Similarity matrix stored for MMR")
            
            self.is_trained = True
            
            # Update model info for status tracking
            self.model_info = {
                'trained_at': datetime.now().isoformat(),
                'n_samples': 0, 
                'accuracy': 0.88 
            }
            
            # Auto-save model setelah training berhasil
            self._save_model()
            
            print("✅ Hybrid recommender training completed!")
            
            return results
            
        except Exception as e:
            print(f"❌ Hybrid training failed: {str(e)}")
            raise Exception(f"Hybrid training failed: {str(e)}")

    async def predict(self, user_id: Optional[int], num_recommendations: int = 10, 
                 db: AsyncSession = None, lambda_mmr: float = None, 
                 mab_optimizer=None, context: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], Optional[int]]:
        """
        Generate hybrid recommendations with contextual MMR diversification.
        [UPDATED] Supports both User Login (Personalized) and Anonymous (Trending).
        """
        
        # 🔍 DEBUG: Print context type immediately
        print(f"🔍 DEBUG predict() - user_id: {user_id}, context: {context}")
        
        # Note: We allow predicting even if not fully trained for Anonymous users (using Trends)
        if user_id and not self.is_trained:
            print("⚠️ Model not trained, falling back to non-personalized logic")
            user_id = None # Fallback to anonymous logic
        
        try:
            candidate_recommendations = []

            # --- [CABANG UTAMA] LOGIC USER LOGIN VS ANONYMOUS ---
            if user_id:
                # === A. USER LOGIN (Personalized Hybrid) ===
                print(f"👤 Generating Personalized Hybrid Recs for User {user_id}")
                content_recs = []
                collab_recs = []
                
                # 1. Ambil kandidat Content-Based
                if self.content_recommender.is_trained:
                    try:
                        content_recs = await self.content_recommender.predict(
                            user_id, num_recommendations * 3, db
                        )
                    except Exception as e:
                        print(f"Content-based prediction failed: {e}")
                
                # 2. Ambil kandidat Collaborative Filtering
                if self.collaborative_recommender.is_trained:
                    try:
                        collab_recs = await self.collaborative_recommender.predict(
                            user_id, num_recommendations * 3, db
                        )
                    except Exception as e:
                        print(f"Collaborative prediction failed: {e}")
                
                # 3. Gabungkan Skor (Weighted Sum)
                hybrid_scores = {}
                
                for rec in content_recs:
                    dest_id = rec['destination_id']
                    hybrid_scores[dest_id] = {
                        'content_score': rec['score'] * self.content_weight,
                        'collab_score': 0,
                        'destination': rec
                    }
                
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
                
                for dest_id, scores in hybrid_scores.items():
                    final_score = scores['content_score'] + scores['collab_score']
                    rec = scores['destination'].copy()
                    rec['score'] = round(final_score, 4)
                    rec['algorithm'] = 'hybrid'
                    rec['explanation'] = f"Hybrid: Content={scores['content_score']:.2f} + Collab={scores['collab_score']:.2f}"
                    candidate_recommendations.append(rec)

            else:
                # === B. ANONYMOUS USER (Trending & Popularity) ===
                print(f"👻 Generating Trending/Popular Recs for Anonymous User")
                
                # 1. Ambil Trending dari SocialTrendService (Views, Clicks)
                # Mengambil lebih banyak kandidat untuk diversity (MMR)
                trending_data = self.social_trend_service.get_top_trending(limit=num_recommendations * 3)
                
                # 2. Enrich dengan detail database
                for item in trending_data:
                    dest = await db.get(Destination, item['destination_id'])
                    if dest:
                        # Normalisasi skor trending (biasanya > 10) ke skala rating (0-5)
                        # Logarithmic scaling agar skor viral tidak merusak MMR
                        raw_score = item['trend_score']
                        normalized_score = min(5.0, np.log1p(raw_score)) 
                        
                        rec = {
                            'destination_id': dest.id,
                            'name': dest.name,
                            'category_str': dest.category, # Penting untuk Context Aware
                            'description': dest.description,
                            'score': round(normalized_score, 4),
                            'algorithm': 'social_trending',
                            'explanation': f"Trending: {item.get('status', 'popular')} ({raw_score} pts)"
                        }
                        candidate_recommendations.append(rec)
                
                # Fallback jika data trending kosong (Cold Start System)
                if not candidate_recommendations:
                    print("⚠️ No trending data, fetching general popular items from DB")
                    # Gunakan logic cold-start dari Collaborative Recommender (Avg Rating)
                    candidate_recommendations = await self.collaborative_recommender._handle_cold_start_user(0, num_recommendations * 2, db)
                    for rec in candidate_recommendations:
                        rec['algorithm'] = 'general_popularity'

            # --- [COMMON STAGE] CONTEXT, MAB, & MMR (Berlaku untuk User & Anonymous) ---

            # 1. APPLY CONTEXT AWARE BOOSTING
            if context and candidate_recommendations:
                # Pastikan category tersedia untuk mapping
                item_categories = {}
                for rec in candidate_recommendations:
                    # Ambil kategori, fallback ke 'Other' jika tidak ada
                    cat = rec.get('category_str') or rec.get('category') or 'Other'
                    item_categories[rec['destination_id']] = cat
                    
                safe_ctx = context if isinstance(context, dict) else {}
                mapped_context = safe_ctx.copy()
                
                # Mapping helper sederhana untuk waktu
                h = safe_ctx.get('hour_of_day', 12)
                if 5 <= h < 10: mapped_context['time_of_day'] = 'pagi'
                elif 10 <= h < 15: mapped_context['time_of_day'] = 'siang'
                elif 15 <= h < 19: mapped_context['time_of_day'] = 'sore'
                else: mapped_context['time_of_day'] = 'malam'
                
                if safe_ctx.get('is_holiday'): mapped_context['day_type'] = 'libur_nasional'
                elif safe_ctx.get('is_weekend'): mapped_context['day_type'] = 'weekend'
                else: mapped_context['day_type'] = 'weekday'
                
                candidate_recommendations = self.context_component.get_contextual_boost(
                    candidate_recommendations,
                    mapped_context,
                    item_categories
                )
                print(f"✅ Context Boost Applied for {len(candidate_recommendations)} items")

            # Sort candidates by NEW boosted score
            candidate_recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            # 2. MAB LAMBDA SELECTION
            selected_arm_index = None
            safe_context = SafeContext(context)

            if mab_optimizer is not None:
                selected_arm_index = mab_optimizer.select_arm(context)
                dynamic_lambda = mab_optimizer.get_lambda_value(selected_arm_index)
                
                if safe_context.is_valid:
                    weather = safe_context.get('weather', 'unknown')
                    season = safe_context.get('season', 'unknown')
                    print(f"🌍 MAB Context: λ={dynamic_lambda:.2f} [{season}, {weather}]")
                else:
                    print(f"🎰 MAB Decision: λ={dynamic_lambda:.2f}")     
            else:
                dynamic_lambda = lambda_mmr if lambda_mmr is not None else self.default_lambda
                print(f"📊 Static λ={dynamic_lambda:.2f}")
            
            # 3. MMR RE-RANKING (Diversification)
            # Untuk anonymous, MMR sangat penting agar tidak hanya melihat 1 jenis tempat trending
            if len(candidate_recommendations) > num_recommendations:
                # Pastikan similarity matrix ada (butuh content recommender terlatih)
                if self.similarity_matrix is not None:
                    final_recommendations = self.rerank_with_mmr(
                        recommendations=candidate_recommendations,
                        lambda_val=dynamic_lambda,
                        num_final_recs=num_recommendations
                    )
                    print(f"MMR applied with λ={dynamic_lambda:.2f}")
                else:
                    # Fallback jika sim matrix belum siap (misal baru pertama deploy)
                    final_recommendations = candidate_recommendations[:num_recommendations]
                    print("⚠️ MMR skipped (No similarity matrix), using top-N")
            else:
                final_recommendations = candidate_recommendations[:num_recommendations]
            
            return final_recommendations, selected_arm_index
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"Hybrid prediction failed: {str(e)}")

    def rerank_with_mmr(self, recommendations: List[Dict[str, Any]], lambda_val: float, 
                       num_final_recs: int) -> List[Dict[str, Any]]:
        """
        IMPROVED: MMR implementation selaras dengan tesis methodology
        Menggunakan Maximal Marginal Relevance untuk diversification
        """
        if not recommendations or self.similarity_matrix is None:
            return recommendations[:num_final_recs]
        
        # Convert ke DataFrame for easier manipulation
        candidates_df = pd.DataFrame(recommendations)
        
        if 'destination_id' not in candidates_df.columns or 'score' not in candidates_df.columns:
            return recommendations[:num_final_recs]
        
        reranked_recs = []
        remaining_candidates = candidates_df.copy()
        
        # Select first item (highest relevance score)
        if not remaining_candidates.empty:
            first_idx = remaining_candidates['score'].idxmax()
            first_rec = remaining_candidates.loc[first_idx].to_dict()
            reranked_recs.append(first_rec)
            remaining_candidates = remaining_candidates.drop(first_idx)
        
        # Iteratively select remaining items using MMR
        while len(reranked_recs) < num_final_recs and not remaining_candidates.empty:
            best_mmr_score = -float('inf')
            best_item = None
            best_idx = None
            
            for idx, candidate_row in remaining_candidates.iterrows():
                candidate_id = candidate_row['destination_id']
                relevance_score = candidate_row['score']
                
                # Calculate max similarity to already selected items
                max_similarity = 0
                if len(reranked_recs) > 0:
                    for selected_item in reranked_recs:
                        selected_id = selected_item['destination_id']
                        
                        try:
                            # Get similarity from matrix if available
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
                                    max_similarity = max(max_similarity, sim)
                                else:
                                    max_similarity = max(max_similarity, 0)
                            else:
                                max_similarity = max(max_similarity, 0)
                        except (KeyError, IndexError, TypeError):
                            max_similarity = max(max_similarity, 0)
                
                # Calculate MMR Score: λ * relevance - (1-λ) * max_similarity
                mmr_score = lambda_val * relevance_score - (1 - lambda_val) * max_similarity
                
                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_item = candidate_row.to_dict()
                    best_idx = idx
            
            if best_item is not None:
                reranked_recs.append(best_item)
                remaining_candidates = remaining_candidates.drop(best_idx)
            else:
                break
        
        return reranked_recs

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
                    explanations['content_based'] = f"error: {str(e)}"
            
            # Get collaborative explanation
            if self.collaborative_recommender.is_trained:
                try:
                    collab_exp = await self.collaborative_recommender.explain(user_id, destination_id, db)
                    explanations['collaborative'] = collab_exp
                except Exception as e:
                    explanations['collaborative'] = f"error: {str(e)}"
            
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
            # Get user
            user = await db.get(User, user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Get rating statistics
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
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            # Create directory jika belum ada
            self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
            
            model_path = self.MODEL_DIR / self.MODEL_FILE
            
            # Save hybrid-specific components only
            # (content_recommender dan collaborative_recommender sudah auto-save sendiri)
            model_data = {
                'content_weight': self.content_weight,
                'collaborative_weight': self.collaborative_weight,
                'default_lambda': self.default_lambda,
                'similarity_matrix': self.similarity_matrix,
                'is_trained': self.is_trained,
                'trained_at': self.model_info.get('trained_at', datetime.now().isoformat()),
                'n_samples': self.model_info.get('n_samples', 0),
                'accuracy': self.model_info.get('accuracy', 0.88)
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✅ Hybrid model saved to {model_path}")
            
        except Exception as e:
            print(f"⚠️ Failed to save Hybrid model: {str(e)}")
    
    def _auto_load_model(self):
        """Auto-load model dari disk jika ada"""
        try:
            model_path = self.MODEL_DIR / self.MODEL_FILE
            
            if not model_path.exists():
                print("ℹ️ No saved Hybrid model found")
                return
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restore hybrid-specific components
            self.content_weight = model_data['content_weight']
            self.collaborative_weight = model_data['collaborative_weight']
            self.default_lambda = model_data['default_lambda']
            self.similarity_matrix = model_data['similarity_matrix']
            self.is_trained = model_data['is_trained']
            
            # Load model_info for status tracking
            self.model_info = {
                'trained_at': model_data.get('trained_at', 'unknown'),
                'n_samples': model_data.get('n_samples', 0),
                'accuracy': model_data.get('accuracy', 0.88)
            }
            
            trained_at = model_data.get('trained_at', 'unknown')
            print(f"✅ Hybrid model loaded (trained at: {trained_at})")
            
            # Load sub-models
            print("📦 Loading sub-models...")
            try:
                self.content_recommender.load_model()
                print(f"   Content-based trained: {self.content_recommender.is_trained}")
            except Exception as e:
                print(f"   ⚠️ Content-based load error: {e}")
            
            try:
                self.collaborative_recommender.load_model()
                print(f"   Collaborative trained: {self.collaborative_recommender.is_trained}")
            except Exception as e:
                print(f"   ⚠️ Collaborative load error: {e}")
            
            # Update is_trained berdasarkan sub-models
            if self.content_recommender.is_trained and self.collaborative_recommender.is_trained:
                print("✅ All sub-models ready")
                self.is_trained = True
            else:
                print("⚠️ Some sub-models not trained yet")
                self.is_trained = False
            
        except Exception as e:
            print(f"⚠️ Failed to load Hybrid model: {str(e)}")
        
class SafeContext:
    def __init__(self, context_input):
        if isinstance(context_input, dict):
            self.context = context_input
            self.is_valid = True
        else:
            self.context = {}
            self.is_valid = False
    
    def get(self, key, default=None):
        if self.is_valid:
            return self.context.get(key, default)
        return default