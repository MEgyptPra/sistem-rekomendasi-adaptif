from typing import List, Dict, Any, Optional, Literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.content_based_recommender import ContentBasedRecommender
from app.services.collaborative_recommender import CollaborativeRecommender
from app.services.hybrid_recommender import HybridRecommender

class MLService:
    """Central service untuk managing semua ML recommendation algorithms"""
    
    def __init__(self):
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeRecommender()
        self.hybrid_recommender = HybridRecommender()
        self._training_status = {
            'content_based': False,
            'collaborative': False,
            'hybrid': False
        }
    
    async def train_all_models(self, db: AsyncSession) -> Dict[str, Any]:
        """Train semua recommendation models"""
        results = {}
        
        # Train content-based
        try:
            content_result = await self.content_recommender.train(db)
            results['content_based'] = content_result
            self._training_status['content_based'] = True
        except Exception as e:
            results['content_based'] = {"status": "failed", "error": str(e)}
            self._training_status['content_based'] = False
        
        # Train collaborative
        try:
            collab_result = await self.collaborative_recommender.train(db)
            results['collaborative'] = collab_result
            self._training_status['collaborative'] = True
        except Exception as e:
            results['collaborative'] = {"status": "failed", "error": str(e)}
            self._training_status['collaborative'] = False
        
        # Train hybrid
        try:
            hybrid_result = await self.hybrid_recommender.train(db)
            results['hybrid'] = hybrid_result
            self._training_status['hybrid'] = True
        except Exception as e:
            results['hybrid'] = {"status": "failed", "error": str(e)}
            self._training_status['hybrid'] = False
        
        return {
            "training_results": results,
            "training_status": self._training_status,
            "overall_status": "success" if any(self._training_status.values()) else "failed"
        }
    
    async def get_recommendations(
        self, 
        user_id: int, 
        algorithm: Literal['content_based', 'collaborative', 'hybrid'] = 'hybrid',
        num_recommendations: int = 10,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get recommendations menggunakan algorithm yang dipilih"""
        
        if algorithm == 'content_based':
            if not self.content_recommender.is_trained:
                raise ValueError("Content-based model belum di-train")
            return await self.content_recommender.predict(user_id, num_recommendations, db)
        
        elif algorithm == 'collaborative':
            if not self.collaborative_recommender.is_trained:
                raise ValueError("Collaborative model belum di-train")
            return await self.collaborative_recommender.predict(user_id, num_recommendations, db)
        
        elif algorithm == 'hybrid':
            if not self.hybrid_recommender.is_trained:
                raise ValueError("Hybrid model belum di-train")
            return await self.hybrid_recommender.predict(user_id, num_recommendations, db)
        
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    async def explain_recommendation(
        self,
        user_id: int,
        destination_id: int,
        algorithm: Literal['content_based', 'collaborative', 'hybrid'] = 'hybrid',
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Explain mengapa destination direkomendasikan"""
        
        if algorithm == 'content_based':
            return await self.content_recommender.explain(user_id, destination_id, db)
        elif algorithm == 'collaborative':
            return await self.collaborative_recommender.explain(user_id, destination_id, db)
        elif algorithm == 'hybrid':
            return await self.hybrid_recommender.explain(user_id, destination_id, db)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    async def get_user_profile(self, user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get user profile dan recommendation readiness"""
        return await self.hybrid_recommender.get_user_profile(user_id, db)
    
    def get_models_status(self) -> Dict[str, Any]:
        """Get status semua models"""
        return {
            "models": {
                "content_based": {
                    "is_trained": self.content_recommender.is_trained,
                    "description": "Content-Based Filtering using TF-IDF and categories"
                },
                "collaborative": {
                    "is_trained": self.collaborative_recommender.is_trained,
                    "description": "Collaborative Filtering using Matrix Factorization (NMF)"
                },
                "hybrid": {
                    "is_trained": self.hybrid_recommender.is_trained,
                    "description": "Hybrid system combining content-based and collaborative"
                }
            },
            "training_status": self._training_status
        }

# Global instance
ml_service = MLService()