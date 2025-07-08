import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.base_recommender import BaseRecommender
from app.models.user import User
from app.models.destinations import Destination
from app.models.rating import Rating

class CollaborativeRecommender(BaseRecommender):
    """Collaborative Filtering menggunakan Matrix Factorization (NMF)"""
    
    def __init__(self):
        super().__init__()
        self.nmf_model = NMF(n_components=50, random_state=42, max_iter=500)
        self.user_item_matrix = None
        self.user_factors = None
        self.item_factors = None
        self.user_encoder = {}
        self.item_encoder = {}
        self.user_decoder = {}
        self.item_decoder = {}
        self.user_similarities = None
    
    async def train(self, db: AsyncSession):
        """Train collaborative filtering model using user ratings"""
        try:
            # Load ratings data
            result = await db.execute(select(Rating))
            ratings = result.scalars().all()
            
            if len(ratings) < 10:
                raise ValueError("Not enough ratings for collaborative filtering (minimum 10 required)")
            
            # Convert ke DataFrame
            ratings_data = []
            for rating in ratings:
                ratings_data.append({
                    'user_id': rating.user_id,
                    'destination_id': rating.destination_id,
                    'rating': rating.rating
                })
            
            ratings_df = pd.DataFrame(ratings_data)
            
            # Create user-item matrix
            self.user_item_matrix = ratings_df.pivot(
                index='user_id', 
                columns='destination_id', 
                values='rating'
            ).fillna(0)
            
            # Create encoders/decoders
            unique_users = self.user_item_matrix.index.tolist()
            unique_items = self.user_item_matrix.columns.tolist()
            
            self.user_encoder = {user_id: idx for idx, user_id in enumerate(unique_users)}
            self.item_encoder = {item_id: idx for idx, item_id in enumerate(unique_items)}
            self.user_decoder = {idx: user_id for user_id, idx in self.user_encoder.items()}
            self.item_decoder = {idx: item_id for item_id, idx in self.item_encoder.items()}
            
            # Train NMF model
            matrix_values = self.user_item_matrix.values
            self.user_factors = self.nmf_model.fit_transform(matrix_values)
            self.item_factors = self.nmf_model.components_.T
            
            # Calculate user-user similarities
            self.user_similarities = cosine_similarity(self.user_factors)
            
            self.is_trained = True
            return {
                "status": "success", 
                "users_count": len(unique_users),
                "items_count": len(unique_items),
                "ratings_count": len(ratings)
            }
            
        except Exception as e:
            raise Exception(f"Collaborative training failed: {str(e)}")
    
    async def predict(self, user_id: int, num_recommendations: int = 10, db: AsyncSession = None) -> List[Dict[str, Any]]:
        """Generate collaborative filtering recommendations"""
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        try:
            # Check if user exists in training data
            if user_id not in self.user_encoder:
                return await self._handle_cold_start_user(user_id, num_recommendations, db)
            
            user_idx = self.user_encoder[user_id]
            
            # Predict ratings untuk semua items
            predicted_ratings = np.dot(self.user_factors[user_idx], self.item_factors.T)
            
            # Get items user belum rate
            user_ratings = self.user_item_matrix.iloc[user_idx]
            unrated_items = user_ratings[user_ratings == 0].index.tolist()
            
            # Score untuk unrated items
            item_scores = []
            for item_id in unrated_items:
                if item_id in self.item_encoder:
                    item_idx = self.item_encoder[item_id]
                    score = predicted_ratings[item_idx]
                    item_scores.append({
                        'destination_id': item_id,
                        'score': score
                    })
            
            # Sort by score
            item_scores.sort(key=lambda x: x['score'], reverse=True)
            top_items = item_scores[:num_recommendations]
            
            # Enrich dengan destination details
            recommendations = []
            for item in top_items:
                dest = await db.get(Destination, item['destination_id'])
                if dest:
                    recommendations.append({
                        'destination_id': dest.id,
                        'name': dest.name,
                        'description': dest.description,
                        'score': round(float(item['score']), 4),
                        'explanation': "Based on similar users' preferences",
                        'algorithm': 'collaborative_filtering'
                    })
            
            return recommendations
            
        except Exception as e:
            raise Exception(f"Collaborative prediction failed: {str(e)}")
    
    async def explain(self, user_id: int, destination_id: int, db: AsyncSession = None) -> Dict[str, Any]:
        """Explain collaborative filtering recommendation"""
        try:
            if user_id not in self.user_encoder or destination_id not in self.item_encoder:
                return {
                    "explanation": "Based on popular destinations",
                    "details": "User or destination not in training data"
                }
            
            user_idx = self.user_encoder[user_id]
            
            # Find similar users
            user_similarities_scores = self.user_similarities[user_idx]
            similar_users_idx = np.argsort(user_similarities_scores)[::-1][1:6]  # Top 5 similar users
            
            similar_users_ids = [self.user_decoder[idx] for idx in similar_users_idx]
            similarity_scores = [user_similarities_scores[idx] for idx in similar_users_idx]
            
            return {
                "explanation": f"Recommended based on {len(similar_users_ids)} similar users",
                "details": {
                    "similar_users": [
                        {"user_id": uid, "similarity": round(float(score), 4)}
                        for uid, score in zip(similar_users_ids, similarity_scores)
                    ],
                    "algorithm": "collaborative_filtering_nmf"
                }
            }
            
        except Exception as e:
            raise Exception(f"Collaborative explanation failed: {str(e)}")
    
    async def _handle_cold_start_user(self, user_id: int, num_recommendations: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """Handle new users (cold start problem)"""
        # Return most popular destinations based on average ratings
        result = await db.execute(
            select(Rating.destination_id, db.func.avg(Rating.rating).label('avg_rating'))
            .group_by(Rating.destination_id)
            .order_by(db.func.avg(Rating.rating).desc())
            .limit(num_recommendations)
        )
        
        popular_destinations = result.all()
        
        recommendations = []
        for dest_rating in popular_destinations:
            dest = await db.get(Destination, dest_rating.destination_id)
            if dest:
                recommendations.append({
                    'destination_id': dest.id,
                    'name': dest.name,
                    'description': dest.description,
                    'score': round(float(dest_rating.avg_rating), 4),
                    'explanation': "Popular destination (new user)",
                    'algorithm': 'collaborative_cold_start'
                })
        
        return recommendations