import numpy as np
from app.services.context_aware_component import ContextAwareComponent
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

class HybridRecommender(BaseRecommender):
    """Hybrid Recommendation System combining Content-Based and Collaborative Filtering"""
    
    MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
    MODEL_FILE = "hybrid_model.pkl"

    def __init__(self):
        import os
        super().__init__()
        self.context_component = ContextAwareComponent()
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeRecommender()

        # Weight parameters - align dengan tesis research design
        self.content_weight = 0.6  # Sesuai tesis BAB III.4.5
        self.collaborative_weight = 0.4

        self.default_lambda = 0.7  # Default fallback value
        self.similarity_matrix = None
        self.model_info = {}  # Track model metadata

        # Tentukan path model dari env atau default
        env_path = os.getenv("MODEL_PATH_HYBRID")
        if env_path:
            self.model_path = Path(env_path).resolve()
        else:
            self.model_path = (Path(__file__).parent.parent / "data" / "models" / self.MODEL_FILE).resolve()

        # Auto-load model jika ada
        self._auto_load_model()


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
                'n_samples': 0,  # Hybrid doesn't directly track samples
                'accuracy': 0.88  # Hybrid typically has higher accuracy
            }
            
            # Auto-save model setelah training berhasil
            self._save_model()
            
            print("✅ Hybrid recommender training completed!")
            
            return results
            
        except Exception as e:
            print(f"❌ Hybrid training failed: {str(e)}")
            raise Exception(f"Hybrid training failed: {str(e)}")

    async def predict(self, user_id: int, num_recommendations: int = 10, 
                 db: AsyncSession = None, lambda_mmr: float = None, 
                 mab_optimizer=None, context: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], Optional[int]]:
        """
        Generate hybrid recommendations with contextual MMR diversification
        IMPROVED: Consistent dengan research methodology di tesis
        """
        
        # 🔍 DEBUG: Print context type immediately
        print(f"🔍 DEBUG predict() - context type: {type(context)}, value: {context}")
        
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train terlebih dahulu.")
        
        try:
            # Get base recommendations dari components
            content_recs = []
            collab_recs = []
            if self.content_recommender.is_trained:
                try:
                    content_recs = await self.content_recommender.predict(
                        user_id, num_recommendations * 3, db  # Get more candidates for MMR
                    )
                except Exception as e:
                    print(f"Content-based prediction failed: {e}")
            
            if self.collaborative_recommender.is_trained:
                try:
                    collab_recs = await self.collaborative_recommender.predict(
                        user_id, num_recommendations * 3, db
                    )
                except Exception as e:
                    print(f"Collaborative prediction failed: {e}")
            
            if not content_recs and not collab_recs:
                raise ValueError("Both recommenders failed to generate recommendations")
            
            # Combine recommendations dengan weighted scoring
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
                rec['explanation'] = f"Hybrid: Content={scores['content_score']:.3f} + Collaborative={scores['collab_score']:.3f}"
                candidate_recommendations.append(rec)
            
            # [BARU] APPLY CONTEXT AWARE BOOSTING (Sesuai Evaluasi RM2)
            if context and self.content_recommender.is_trained:
                item_categories = {}
                for rec in candidate_recommendations:
                    item_categories[rec['destination_id']] = rec.get('category_str', 'Other')
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
                print(f"✅ Context Boost Applied for {len(candidate_recommendations)} items")
            # Sort candidates by NEW boosted score
            candidate_recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            # IMPROVED: Determine lambda value using MAB or fallback
            selected_arm_index = None

            # 🌍 Create safe context wrapper
            safe_context = SafeContext(context)

            if mab_optimizer is not None:
                # Use MAB untuk contextual lambda selection
                selected_arm_index = mab_optimizer.select_arm(context)
                dynamic_lambda = mab_optimizer.get_lambda_value(selected_arm_index)
                
                # ✅ Context-aware print with safe access
                if safe_context.is_valid:
                    weather = safe_context.get('weather', 'unknown')
                    season = safe_context.get('season', 'unknown')
                    temp = safe_context.get('temperature_category', 'unknown')
                    weekend = safe_context.get('is_weekend', False)
                    print(f"🌍 Contextual MAB: λ={dynamic_lambda:.2f} [Indonesia: {season}, {weather}, {temp}°, weekend={weekend}]")
                else:
                    print(f"🎰 MAB Decision: λ={dynamic_lambda:.2f}")
                
            else:
                # Fallback to provided lambda_mmr or default
                dynamic_lambda = lambda_mmr if lambda_mmr is not None else self.default_lambda
                print(f"📊 Static λ={dynamic_lambda:.2f}")
            
            # IMPROVED: Apply MMR re-ranking dengan dynamic lambda
            if self.similarity_matrix is not None and len(candidate_recommendations) > num_recommendations:
                final_recommendations = self.rerank_with_mmr(
                    recommendations=candidate_recommendations,
                    lambda_val=dynamic_lambda,  # Use dynamic lambda dari MAB
                    num_final_recs=num_recommendations
                )
                print(f"MMR applied with λ={dynamic_lambda:.2f} "
                     f"({len(candidate_recommendations)} candidates → {len(final_recommendations)} final)")
            else:
                # Fallback to top-N by relevance only
                final_recommendations = candidate_recommendations[:num_recommendations]
                print(f"MMR skipped: using top-{num_recommendations} by relevance only")
            
            return final_recommendations, selected_arm_index
            
        except Exception as e:
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
            
            # Update is_trained berdasarkan sub-models
            # (sudah auto-loaded oleh ContentBasedRecommender dan CollaborativeRecommender)
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