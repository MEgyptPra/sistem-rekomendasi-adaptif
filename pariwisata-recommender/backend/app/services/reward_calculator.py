"""
Reward Calculator for Multi-Armed Bandit (MAB) Updates
Implements composite reward formula from thesis (BAB III.4.4):
Reward = 0.5*NDCG + 0.3*Diversity + 0.2*Novelty
"""

import numpy as np
from typing import Dict, List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.rating import Rating
from app.models.user_interaction import UserInteraction


class RewardCalculator:
    """
    Calculate composite reward for MAB updates based on:
    - Accuracy (NDCG): 50%
    - Diversity (ILD): 30%
    - Novelty (Long-tail promotion): 20%
    """
    
    # Reward weights sesuai tesis
    WEIGHTS = {
        'ndcg': 0.5,      # Accuracy/Relevance
        'diversity': 0.3,  # Category diversity
        'novelty': 0.2     # Long-tail promotion
    }
    
    def __init__(self):
        pass
    
    def calculate_reward(self, ndcg: float, diversity: float, novelty: float) -> float:
        """
        Calculate composite reward from individual metrics.
        
        Args:
            ndcg: Normalized Discounted Cumulative Gain [0,1]
            diversity: Intra-List Diversity [0,1]
            novelty: Average item novelty score (will be normalized by /3.0)
        
        Returns:
            Composite reward in [0,1]
        """
        # Clamp NDCG to [0,1]
        ndcg = max(0.0, min(1.0, ndcg))
        
        # Clamp diversity to [0,1]
        diversity = max(0.0, min(1.0, diversity))
        
        # Normalize novelty (assuming max novelty ~3.0)
        novelty_normalized = max(0.0, min(1.0, novelty / 3.0))
        
        # Composite reward
        reward = (
            self.WEIGHTS['ndcg'] * ndcg +
            self.WEIGHTS['diversity'] * diversity +
            self.WEIGHTS['novelty'] * novelty_normalized
        )
        
        return float(reward)
    
    async def calculate_ndcg_from_interactions(
        self, 
        user_id: int, 
        recommended_ids: List[int], 
        db: AsyncSession,
        k: int = 10
    ) -> float:
        """
        Calculate NDCG based on user interactions with recommendations.
        
        Uses implicit feedback:
        - Click/View = 1 point
        - Rating >= 4 = 3 points
        - Rating 3 = 2 points
        - Rating < 3 = 0 points
        
        Args:
            user_id: User ID
            recommended_ids: List of recommended destination IDs
            db: Database session
            k: Number of items to consider
        
        Returns:
            NDCG score [0,1]
        """
        if not recommended_ids:
            return 0.0
        
        # Get user ratings for recommended items
        rating_query = select(Rating).where(
            Rating.user_id == user_id,
            Rating.destination_id.in_(recommended_ids)
        )
        rating_result = await db.execute(rating_query)
        ratings = rating_result.scalars().all()
        
        rating_map = {r.destination_id: r.rating for r in ratings}
        
        # Get user interactions (clicks, views)
        interaction_query = select(UserInteraction).where(
            UserInteraction.user_id == user_id,
            UserInteraction.entity_type == 'destination',
            UserInteraction.entity_id.in_(recommended_ids)
        )
        interaction_result = await db.execute(interaction_query)
        interactions = interaction_result.scalars().all()
        
        interaction_map = {}
        for inter in interactions:
            if inter.entity_id not in interaction_map:
                interaction_map[inter.entity_id] = 0
            interaction_map[inter.entity_id] += 1
        
        # Calculate relevance scores (ground truth)
        relevance_scores = []
        for dest_id in recommended_ids[:k]:
            score = 0.0
            
            # Rating-based relevance
            if dest_id in rating_map:
                rating_val = rating_map[dest_id]
                if rating_val >= 4.0:
                    score = 3.0  # Highly relevant
                elif rating_val >= 3.0:
                    score = 2.0  # Moderately relevant
                else:
                    score = 0.0  # Not relevant
            
            # Interaction-based relevance (if no rating)
            elif dest_id in interaction_map:
                score = min(1.0, interaction_map[dest_id] * 0.5)  # Click = 0.5, multiple = more
            
            relevance_scores.append(score)
        
        # Calculate DCG
        dcg = 0.0
        for i, rel in enumerate(relevance_scores):
            dcg += rel / np.log2(i + 2)  # i+2 because positions start at 1
        
        # Calculate IDCG (ideal DCG - sorted by relevance)
        ideal_relevance = sorted(relevance_scores, reverse=True)
        idcg = 0.0
        for i, rel in enumerate(ideal_relevance):
            idcg += rel / np.log2(i + 2)
        
        # NDCG
        if idcg == 0:
            return 0.0
        
        ndcg = dcg / idcg
        return min(1.0, ndcg)
    
    def calculate_diversity_from_categories(
        self, 
        recommended_items: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate category diversity using Simpson's Diversity Index.
        
        Args:
            recommended_items: List of dicts with 'category' or 'category_str' field
        
        Returns:
            Diversity score [0,1]
        """
        if not recommended_items:
            return 0.0
        
        # Extract categories
        categories = []
        for item in recommended_items:
            cat = item.get('category_str') or item.get('category') or 'Other'
            categories.append(cat)
        
        # Count category occurrences
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Simpson's Diversity Index: 1 - Σ(pi^2)
        n = len(categories)
        if n <= 1:
            return 0.0
        
        simpson_sum = sum((count / n) ** 2 for count in category_counts.values())
        diversity = 1 - simpson_sum
        
        return float(diversity)
    
    def calculate_novelty_from_popularity(
        self, 
        recommended_items: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate average novelty score.
        Novelty = -log2(popularity)
        
        Args:
            recommended_items: List of dicts with 'popularity_score' or 'interaction_count'
        
        Returns:
            Average novelty score (typically [0,3])
        """
        if not recommended_items:
            return 0.0
        
        novelty_scores = []
        
        for item in recommended_items:
            # Get popularity indicator
            popularity = item.get('popularity_score', 0) or item.get('interaction_count', 0)
            
            # Avoid log(0)
            if popularity <= 0:
                popularity = 0.1  # Small non-zero value for unpopular items
            
            # Novelty = -log2(normalized_popularity)
            # Assume max popularity ~1000 for normalization
            normalized_pop = min(1.0, popularity / 1000.0)
            novelty = -np.log2(normalized_pop) if normalized_pop > 0 else 3.0
            
            novelty_scores.append(novelty)
        
        avg_novelty = np.mean(novelty_scores) if novelty_scores else 0.0
        return float(avg_novelty)
    
    async def calculate_reward_from_recommendations(
        self,
        user_id: int,
        recommended_items: List[Dict[str, Any]],
        db: AsyncSession
    ) -> float:
        """
        All-in-one method to calculate composite reward from recommendations.
        
        Args:
            user_id: User ID
            recommended_items: List of recommendation dicts with 'destination_id', 'category', etc.
            db: Database session
        
        Returns:
            Composite reward [0,1]
        """
        # Extract destination IDs
        dest_ids = [item['destination_id'] for item in recommended_items if 'destination_id' in item]
        
        # Calculate individual metrics
        ndcg = await self.calculate_ndcg_from_interactions(user_id, dest_ids, db)
        diversity = self.calculate_diversity_from_categories(recommended_items)
        novelty = self.calculate_novelty_from_popularity(recommended_items)
        
        # Calculate composite reward
        reward = self.calculate_reward(ndcg, diversity, novelty)
        
        return reward


# Global instance
reward_calculator = RewardCalculator()
