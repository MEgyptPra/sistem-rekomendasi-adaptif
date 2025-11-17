import os
from typing import List, Dict, Any, Optional, Literal, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.content_based_recommender import ContentBasedRecommender
from app.services.collaborative_recommender import CollaborativeRecommender
from app.services.hybrid_recommender import HybridRecommender
from app.services.mab_optimizer import MABOptimizer

# Auto-select between production (real API) and simulation
USE_PRODUCTION_API = bool(os.getenv("OPENWEATHER_API_KEY")) or \
                     bool(os.getenv("GOOGLE_MAPS_API_KEY")) or \
                     bool(os.getenv("TOMTOM_API_KEY"))

if USE_PRODUCTION_API:
    from app.services.real_time_data_production import RealTimeContextService
    print("🌍 Using PRODUCTION Real-Time Data Service (Real APIs)")
else:
    from app.services.real_time_data import RealTimeContextService
    print("🎲 Using SIMULATION Real-Time Data Service")

class MLService:
    """Central service untuk managing semua ML recommendation algorithms"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("🚀 Initializing ML Service...")
        print("="*60)
        
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeRecommender()
        self.hybrid_recommender = HybridRecommender()
        
        # Initialize MAB Optimizer dengan contextual capabilities
        self.mab_optimizer = MABOptimizer(
            n_arms=11, 
            exploration_param=2.0,
            persistence_file="data/contextual_mab_state.json"  # Contextual state file
        )
        
        # Initialize Real-Time Context Service
        self.context_service = RealTimeContextService()
        
        # Update training status dari auto-loaded models
        self._training_status = {
            'content_based': self.content_recommender.is_trained,
            'collaborative': self.collaborative_recommender.is_trained,
            'hybrid': self.hybrid_recommender.is_trained
        }
        
        # Print status summary
        print("\n📊 Model Status:")
        print(f"   Content-Based: {'✅ LOADED' if self._training_status['content_based'] else '❌ NOT TRAINED'}")
        print(f"   Collaborative: {'✅ LOADED' if self._training_status['collaborative'] else '❌ NOT TRAINED'}")
        print(f"   Hybrid:        {'✅ LOADED' if self._training_status['hybrid'] else '❌ NOT TRAINED'}")
        print("="*60 + "\n")
    
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
    ) -> Tuple[List[Dict[str, Any]], Optional[int], Optional[Dict[str, Any]]]:
        """
        Get recommendations menggunakan algorithm yang dipilih dengan context awareness
        
        Returns:
            Tuple: (recommendations, arm_index, context) where context and arm_index are None for non-hybrid algorithms
        """
        
        if algorithm == 'content_based':
            if not self.content_recommender.is_trained:
                raise ValueError("Content-based model belum di-train")
            recommendations = await self.content_recommender.predict(user_id, num_recommendations, db)
            return recommendations, None, None
        
        elif algorithm == 'collaborative':
            if not self.collaborative_recommender.is_trained:
                raise ValueError("Collaborative model belum di-train")
            recommendations = await self.collaborative_recommender.predict(user_id, num_recommendations, db)
            return recommendations, None, None
        
        elif algorithm == 'hybrid':
            if not self.hybrid_recommender.is_trained:
                raise ValueError("Hybrid model belum di-train")
            
            # 1. Get current context from real-time service
            current_context = self.context_service.get_current_context()
            
            # 2. Use Contextual MAB to select optimal lambda for this context
            recommendations, arm_index = await self.hybrid_recommender.predict(
                user_id, 
                num_recommendations, 
                db, 
                mab_optimizer=self.mab_optimizer,
                context=current_context
            )
            
            # 3. Log contextual MAB decision for monitoring
            lambda_value = self.mab_optimizer.get_lambda_value(arm_index) if arm_index is not None else 0.7
            print(f"🎯 Contextual MAB: selected λ={lambda_value:.2f} (arm {arm_index}) "
                  f"for user {user_id} in context: {current_context}")
            
            return recommendations, arm_index, current_context
        
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
            "training_status": self._training_status,
            "mab_optimizer": {
                "total_contexts": len(self.mab_optimizer.context_data),
                "exploration_param": self.mab_optimizer.c,
                "persistence_file": self.mab_optimizer.persistence_file
            }
        }
    
    def update_recommendation_feedback(self, arm_index: int, reward: float, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Update Contextual MAB dengan feedback dari user
        
        Args:
            arm_index (int): Index arm yang digunakan untuk rekomendasi
            reward (float): Reward value (0-1, dimana 1 = sangat baik, 0 = sangat buruk)
            context (Dict): Konteks saat rekomendasi diberikan
            
        Returns:
            Dict: Informasi update
        """
        if arm_index is not None and 0 <= arm_index < self.mab_optimizer.n_arms:
            lambda_value = self.mab_optimizer.get_lambda_value(arm_index)
            self.mab_optimizer.update_reward(arm_index, reward, context)
            
            return {
                "status": "success",
                "arm_index": arm_index,
                "lambda_value": lambda_value,
                "reward": reward,
                "context": context,
                "message": f"Contextual feedback updated for λ={lambda_value:.2f} in given context"
            }
        else:
            return {
                "status": "error",
                "message": "Invalid arm_index"
            }
    
    def get_mab_statistics(self) -> Dict[str, Any]:
        """Get detailed MAB statistics"""
        return self.mab_optimizer.get_statistics()
    
    def reset_mab(self) -> Dict[str, Any]:
        """Reset MAB state (for testing/development)"""
        self.mab_optimizer.reset()
        return {"status": "success", "message": "MAB state has been reset"}

# Global instance
ml_service = MLService()