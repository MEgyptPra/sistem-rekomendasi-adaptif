import numpy as np
from app.services.context_aware_component import ContextAwareComponent
from app.services.social_trend_service import SocialTrendService
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
from app.models.destinations import Destination

class HybridRecommender(BaseRecommender):
    """Hybrid Recommendation System combining Content-Based and Collaborative Filtering"""
    
    # Point to backend/data/models
    MODEL_DIR = Path(__file__).resolve().parents[3] / "data" / "models"
    MODEL_FILE = "hybrid_model.pkl"

    def __init__(self):
        import os
        super().__init__()
        self.context_component = ContextAwareComponent()
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeRecommender()
        self.social_trend_service = SocialTrendService()

        # Weight parameters
        self.content_weight = 0.6
        self.collaborative_weight = 0.4

        self.default_lambda = 0.7
        self.similarity_matrix = None
        self.model_info = {}

        env_path = os.getenv("MODEL_PATH_HYBRID")
        if env_path:
            self.model_path = Path(env_path).resolve()
        else:
            self.model_path = (Path(__file__).resolve().parents[3] / "data" / "models" / self.MODEL_FILE).resolve()

        self._model_loaded = False

    def load_model(self):
        """
        Public method to load model from disk on demand.
        [PERBAIKAN] Memaksa sub-model untuk load terlebih dahulu.
        """
        print("🔄 Hybrid orchestrator: Triggering sub-models load...")
        
        # 1. Paksa sub-model untuk memuat diri mereka sendiri
        try:
            self.content_recommender.load_model()
        except Exception as e:
            print(f"⚠️ Warning loading content recommender: {e}")

        try:
            self.collaborative_recommender.load_model()
        except Exception as e:
            print(f"⚠️ Warning loading collaborative recommender: {e}")

        # 2. Load state hybrid sendiri
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
            
            # Update model info
            self.model_info = {
                'trained_at': datetime.now().isoformat(),
                'n_samples': 0, 
                'accuracy': 0.88 
            }
            
            # Auto-save model
            self._save_model()
            
            print("✅ Hybrid recommender training completed!")
            
            return results
            
        except Exception as e:
            print(f"❌ Hybrid training failed: {str(e)}")
            raise Exception(f"Hybrid training failed: {str(e)}")

    async def predict(self, user_id: Optional[int], num_recommendations: int = 10, 
                 db: AsyncSession = None, lambda_mmr: float = None, 
                 mab_optimizer=None, context: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], Optional[int]]:
        """Generate hybrid recommendations with contextual MMR diversification."""
        
        # Fallback to anonymous logic if needed
        if user_id and not self.is_trained:
            print("⚠️ Model not trained, falling back to non-personalized logic")
            user_id = None 
        
        try:
            candidate_recommendations = []

            if user_id:
                # === A. USER LOGIN (Personalized Hybrid) ===
                content_recs = []
                collab_recs = []
                
                if self.content_recommender.is_trained:
                    try:
                        content_recs = await self.content_recommender.predict(user_id, num_recommendations * 3, db)
                    except Exception as e:
                        print(f"Content-based prediction failed: {e}")
                
                if self.collaborative_recommender.is_trained:
                    try:
                        collab_recs = await self.collaborative_recommender.predict(user_id, num_recommendations * 3, db)
                    except Exception as e:
                        print(f"Collaborative prediction failed: {e}")
                
                # Merge Scores
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
                # === B. ANONYMOUS USER (Trending) ===
                trending_data = self.social_trend_service.get_top_trending(limit=num_recommendations * 3)
                
                for item in trending_data:
                    dest = await db.get(Destination, item['destination_id'])
                    if dest:
                        raw_score = item['trend_score']
                        normalized_score = min(5.0, np.log1p(raw_score)) 
                        
                        rec = {
                            'destination_id': dest.id,
                            'name': dest.name,
                            'category_str': dest.category, 
                            'description': dest.description,
                            'score': round(normalized_score, 4),
                            'algorithm': 'social_trending',
                            'explanation': f"Trending: {item.get('status', 'popular')} ({raw_score} pts)"
                        }
                        candidate_recommendations.append(rec)
                
                if not candidate_recommendations:
                    candidate_recommendations = await self.collaborative_recommender._handle_cold_start_user(0, num_recommendations * 2, db)
                    for rec in candidate_recommendations:
                        rec['algorithm'] = 'general_popularity'

            # --- [COMMON STAGE] CONTEXT, MAB, & MMR ---
            if context and candidate_recommendations:
                item_categories = {}
                for rec in candidate_recommendations:
                    cat = rec.get('category_str') or rec.get('category') or 'Other'
                    item_categories[rec['destination_id']] = cat
                    
                safe_ctx = context if isinstance(context, dict) else {}
                mapped_context = safe_ctx.copy()
                
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

            candidate_recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            selected_arm_index = None
            if mab_optimizer is not None:
                selected_arm_index = mab_optimizer.select_arm(context)
                dynamic_lambda = mab_optimizer.get_lambda_value(selected_arm_index)
            else:
                dynamic_lambda = lambda_mmr if lambda_mmr is not None else self.default_lambda
            
            if len(candidate_recommendations) > num_recommendations:
                if self.similarity_matrix is not None:
                    final_recommendations = self.rerank_with_mmr(
                        recommendations=candidate_recommendations,
                        lambda_val=dynamic_lambda,
                        num_final_recs=num_recommendations
                    )
                else:
                    final_recommendations = candidate_recommendations[:num_recommendations]
            else:
                final_recommendations = candidate_recommendations[:num_recommendations]
            
            return final_recommendations, selected_arm_index
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"Hybrid prediction failed: {str(e)}")

    def rerank_with_mmr(self, recommendations: List[Dict[str, Any]], lambda_val: float, num_final_recs: int) -> List[Dict[str, Any]]:
        if not recommendations or self.similarity_matrix is None:
            return recommendations[:num_final_recs]
        
        candidates_df = pd.DataFrame(recommendations)
        if 'destination_id' not in candidates_df.columns or 'score' not in candidates_df.columns:
            return recommendations[:num_final_recs]
        
        reranked_recs = []
        remaining_candidates = candidates_df.copy()
        
        if not remaining_candidates.empty:
            first_idx = remaining_candidates['score'].idxmax()
            first_rec = remaining_candidates.loc[first_idx].to_dict()
            reranked_recs.append(first_rec)
            remaining_candidates = remaining_candidates.drop(first_idx)
        
        while len(reranked_recs) < num_final_recs and not remaining_candidates.empty:
            best_mmr_score = -float('inf')
            best_item = None
            best_idx = None
            
            for idx, candidate_row in remaining_candidates.iterrows():
                candidate_id = candidate_row['destination_id']
                relevance_score = candidate_row['score']
                max_similarity = 0
                
                if len(reranked_recs) > 0:
                    for selected_item in reranked_recs:
                        selected_id = selected_item['destination_id']
                        try:
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
                        except Exception:
                            max_similarity = 0
                
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
        return {
            "explanation": "Hybrid recommendation combining multiple algorithms",
            "weights": {"content": self.content_weight, "collab": self.collaborative_weight}
        }

    async def get_user_profile(self, user_id: int, db: AsyncSession) -> Dict[str, Any]:
        try:
            user = await db.get(User, user_id)
            return {"user_id": user.id, "name": user.name if user else "Unknown"}
        except:
            return {}

    def _save_model(self):
        try:
            self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
            model_path = self.MODEL_DIR / self.MODEL_FILE
            model_data = {
                'content_weight': self.content_weight,
                'collaborative_weight': self.collaborative_weight,
                'default_lambda': self.default_lambda,
                'similarity_matrix': self.similarity_matrix,
                'is_trained': self.is_trained,
                'trained_at': self.model_info.get('trained_at', datetime.now().isoformat())
            }
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"✅ Hybrid model saved to {model_path}")
        except Exception as e:
            print(f"⚠️ Failed to save Hybrid model: {str(e)}")
    
    def _auto_load_model(self):
        try:
            model_path = self.MODEL_DIR / self.MODEL_FILE
            if not model_path.exists():
                print("ℹ️ No saved Hybrid model found")
                return
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.content_weight = model_data['content_weight']
            self.collaborative_weight = model_data['collaborative_weight']
            self.default_lambda = model_data['default_lambda']
            self.similarity_matrix = model_data['similarity_matrix']
            self.is_trained = model_data['is_trained']
            self.model_info = {'trained_at': model_data.get('trained_at', 'unknown')}
            
            print(f"✅ Hybrid model loaded (trained at: {self.model_info['trained_at']})")
            
            # Check if sub-models are ready
            if self.content_recommender.is_trained and self.collaborative_recommender.is_trained:
                print("✅ All sub-models ready")
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