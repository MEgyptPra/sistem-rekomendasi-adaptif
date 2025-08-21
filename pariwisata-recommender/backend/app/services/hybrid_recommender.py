import numpy as np
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
            
            return results
            
        except Exception as e:
            raise Exception(f"Hybrid training failed: {str(e)}")
    
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
                        user_id, num_recommendations * 2, db  # Get more for better mixing
                    )
                except Exception as e:
                    print(f"Content-based prediction failed: {e}")
            
            # Get collaborative recommendations
            if self.collaborative_recommender.is_trained:
                try:
                    collab_recs = await self.collaborative_recommender.predict(
                        user_id, num_recommendations * 2, db  # Get more for better mixing
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
            final_recommendations = []
            for dest_id, scores in hybrid_scores.items():
                final_score = scores['content_score'] + scores['collab_score']
                rec = scores['destination'].copy()
                rec['score'] = round(final_score, 4)
                rec['algorithm'] = 'hybrid'
                rec['explanation'] = f"Hybrid: Content({scores['content_score']:.3f}) + Collaborative({scores['collab_score']:.3f})"
                final_recommendations.append(rec)
            
            # Sort by final score and return top N
            final_recommendations.sort(key=lambda x: x['score'], reverse=True)
            return final_recommendations[:num_recommendations]
            
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