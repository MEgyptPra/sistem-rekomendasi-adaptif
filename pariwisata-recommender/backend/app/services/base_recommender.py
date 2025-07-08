from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models.user import User
from app.models.destinations import Destination

class BaseRecommender(ABC):
    """Base class untuk semua recommendation algorithms"""
    
    def __init__(self):
        self.model_name = self.__class__.__name__
        self.is_trained = False
    
    @abstractmethod
    async def train(self, **kwargs):
        """Train the recommendation model"""
        pass
    
    @abstractmethod
    async def predict(self, user_id: int, num_recommendations: int = 10) -> List[Dict[str, Any]]:
        """Generate recommendations for a user"""
        pass
    
    @abstractmethod
    async def explain(self, user_id: int, destination_id: int) -> Dict[str, Any]:
        """Explain why this destination was recommended"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "name": self.model_name,
            "is_trained": self.is_trained,
            "description": self.__doc__
        }