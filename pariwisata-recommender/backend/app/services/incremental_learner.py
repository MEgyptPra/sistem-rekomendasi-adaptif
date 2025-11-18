"""
Incremental Learning Service
Handles real-time updates without full model retraining
"""
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc
import json
import os

from app.models.rating import Rating
from app.models.user_interaction import UserInteraction
from app.models.destinations import Destination
from app.models.destination_review import DestinationReview


class IncrementalLearner:
    """
    Incremental learning without full model retraining.
    Updates scores and statistics in real-time.
    """
    
    def __init__(self):
        self.cache_dir = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Cache untuk mengurangi database queries
        self.destination_scores = {}
        self.trending_items = []
        self.last_cache_update = None
        self.cache_ttl = timedelta(hours=1)  # Cache valid untuk 1 jam
        
    async def update_destination_score(
        self, 
        destination_id: int, 
        interaction_type: str,
        rating_value: Optional[float] = None,
        db: AsyncSession = None
    ):
        """
        Update destination score incrementally based on new interaction.
        
        Args:
            destination_id: ID of destination
            interaction_type: 'view', 'click', 'rating', 'review'
            rating_value: Rating value if interaction_type is 'rating'
            db: Database session
        """
        # Weight untuk setiap jenis interaksi
        interaction_weights = {
            'view': 0.1,
            'click': 0.3,
            'favorite': 0.5,
            'review': 0.7,
            'rating': 1.0
        }
        
        weight = interaction_weights.get(interaction_type, 0.1)
        
        # Load current scores
        scores = self._load_scores()
        
        if destination_id not in scores:
            scores[destination_id] = {
                'total_score': 0,
                'interaction_count': 0,
                'avg_rating': 0,
                'rating_count': 0,
                'view_count': 0,
                'click_count': 0,
                'favorite_count': 0,
                'last_updated': datetime.now().isoformat()
            }
        
        dest_score = scores[destination_id]
        
        # Incremental update
        dest_score['interaction_count'] += 1
        dest_score['total_score'] += weight
        
        # Update specific counters
        if interaction_type == 'view':
            dest_score['view_count'] = dest_score.get('view_count', 0) + 1
        elif interaction_type == 'click':
            dest_score['click_count'] = dest_score.get('click_count', 0) + 1
        elif interaction_type == 'favorite':
            dest_score['favorite_count'] = dest_score.get('favorite_count', 0) + 1
        elif interaction_type == 'rating' and rating_value:
            # Incremental average rating calculation
            old_avg = dest_score['avg_rating']
            old_count = dest_score['rating_count']
            new_count = old_count + 1
            new_avg = (old_avg * old_count + rating_value) / new_count
            
            dest_score['avg_rating'] = new_avg
            dest_score['rating_count'] = new_count
        
        dest_score['last_updated'] = datetime.now().isoformat()
        
        # Calculate popularity score (weighted combination)
        dest_score['popularity_score'] = (
            dest_score['total_score'] + 
            (dest_score['avg_rating'] * 2) +  # Rating lebih penting
            (dest_score['rating_count'] * 0.5)
        )
        
        # Save updated scores
        self._save_scores(scores)
        
        # Invalidate cache
        self.last_cache_update = None
        
        return dest_score
    
    async def get_trending_destinations(
        self, 
        limit: int = 10,
        time_window_hours: int = 24,
        db: AsyncSession = None
    ) -> List[Dict]:
        """
        Get trending destinations based on recent interactions.
        Uses incremental data without retraining.
        """
        # Check cache
        if self._is_cache_valid():
            return self.trending_items[:limit]
        
        scores = self._load_scores()
        
        # Filter by recent activity
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        
        trending = []
        for dest_id, score_data in scores.items():
            last_updated = datetime.fromisoformat(score_data['last_updated'])
            if last_updated >= cutoff_time:
                trending.append({
                    'destination_id': int(dest_id),  # Convert string key back to int
                    'popularity_score': score_data.get('popularity_score', 0),
                    'avg_rating': score_data.get('avg_rating', 0),
                    'interaction_count': score_data.get('interaction_count', 0),
                    'view_count': score_data.get('view_count', 0),
                    'last_updated': score_data['last_updated']
                })
        
        # Sort by popularity score
        trending.sort(key=lambda x: x['popularity_score'], reverse=True)
        
        # Update cache
        self.trending_items = trending
        self.last_cache_update = datetime.now()
        
        return trending[:limit]
    
    async def get_personalized_boost(
        self,
        user_id: int,
        destination_id: int,
        db: AsyncSession
    ) -> float:
        """
        Calculate personalized boost factor based on user's history.
        Updates incrementally without retraining.
        """
        # Get user's recent interactions
        result = await db.execute(
            select(UserInteraction)
            .where(UserInteraction.user_id == user_id)
            .where(UserInteraction.entity_type == 'destination')
            .order_by(desc(UserInteraction.created_at))
            .limit(50)
        )
        interactions = result.scalars().all()
        
        if not interactions:
            return 0.0
        
        # Calculate boost based on category preference
        category_counts = {}
        for interaction in interactions:
            # You would need to join with destination to get category
            # For now, simplified
            pass
        
        # Simple boost: if user interacted with similar destinations
        similar_count = sum(1 for i in interactions if i.entity_id == destination_id)
        boost = min(similar_count * 0.1, 1.0)  # Max 1.0 boost
        
        return boost
    
    async def update_from_rating(
        self,
        user_id: int,
        destination_id: int,
        rating: float,
        db: AsyncSession
    ):
        """
        Update scores when user adds new rating.
        Real-time incremental update.
        """
        await self.update_destination_score(
            destination_id=destination_id,
            interaction_type='rating',
            rating_value=rating,
            db=db
        )
        
        print(f"✅ Incremental update: User {user_id} rated destination {destination_id} with {rating}")
    
    async def update_from_interaction(
        self,
        user_id: Optional[int],
        destination_id: int,
        interaction_type: str,
        db: AsyncSession
    ):
        """
        Update scores when user interacts (view, click, favorite).
        Real-time incremental update.
        """
        await self.update_destination_score(
            destination_id=destination_id,
            interaction_type=interaction_type,
            db=db
        )
        
        print(f"✅ Incremental update: Interaction '{interaction_type}' on destination {destination_id}")
    
    def _load_scores(self) -> Dict:
        """Load scores from cache file"""
        cache_file = os.path.join(self.cache_dir, "destination_scores.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_scores(self, scores: Dict):
        """Save scores to cache file"""
        cache_file = os.path.join(self.cache_dir, "destination_scores.json")
        # Convert int keys to str for JSON
        scores_str_keys = {str(k): v for k, v in scores.items()}
        with open(cache_file, 'w') as f:
            json.dump(scores_str_keys, f, indent=2)
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        if self.last_cache_update is None:
            return False
        return datetime.now() - self.last_cache_update < self.cache_ttl
    
    async def get_recommendations_with_incremental_boost(
        self,
        user_id: Optional[int],
        base_recommendations: List[Dict],
        db: AsyncSession
    ) -> List[Dict]:
        """
        Apply incremental learning boost to base recommendations.
        This combines ML model output with real-time learning.
        """
        scores = self._load_scores()
        
        for rec in base_recommendations:
            dest_id = rec.get('destination_id') or rec.get('id')
            
            # Get incremental score - convert to string for JSON lookup
            if str(dest_id) in scores:
                dest_score = scores[str(dest_id)]
                popularity_boost = dest_score.get('popularity_score', 0) / 100  # Normalize
                
                # Apply boost to recommendation score
                rec['original_score'] = rec.get('score', 0)
                rec['popularity_boost'] = popularity_boost
                rec['final_score'] = rec['original_score'] + popularity_boost
                rec['boosted'] = True
            else:
                rec['final_score'] = rec.get('score', 0)
                rec['boosted'] = False
        
        # Re-sort by final score
        base_recommendations.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        return base_recommendations
    
    async def schedule_cleanup(self):
        """
        Clean up old data from cache.
        Run periodically (e.g., daily cron job).
        """
        scores = self._load_scores()
        cutoff_time = datetime.now() - timedelta(days=30)
        
        cleaned = {}
        for dest_id, score_data in scores.items():
            last_updated = datetime.fromisoformat(score_data['last_updated'])
            if last_updated >= cutoff_time:
                cleaned[dest_id] = score_data
        
        self._save_scores(cleaned)
        print(f"🧹 Cleaned up old scores. {len(scores) - len(cleaned)} entries removed.")


# Global instance
incremental_learner = IncrementalLearner()
