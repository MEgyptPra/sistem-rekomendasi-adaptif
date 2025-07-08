from typing import List
from app.models.user import User
from app.models.destination import Destination

def simple_recommendation(user: User, destinations: List[Destination]) -> List[Destination]:
    """
    Simple content-based recommendation based on user preferences
    """
    if not user.preferences:
        return destinations[:5]  # Return first 5 if no preferences
    
    prefs = [p.strip().lower() for p in user.preferences.split(",")]
    result = []
    
    for destination in destinations:
        # Check if any destination category matches user preferences
        destination_categories = [c.name.lower() for c in destination.categories]
        if any(pref in destination_categories for pref in prefs):
            result.append(destination)
    
    # If no matches, return popular destinations (first 5)
    if not result:
        return destinations[:5]
    
    return result[:10]  # Return max 10 recommendations

def collaborative_filtering_recommendation(user_id: int, destinations: List[Destination]) -> List[Destination]:
    """
    Placeholder for collaborative filtering - will be implemented in Tahap 2
    """
    return destinations[:5]

def hybrid_recommendation(user: User, destinations: List[Destination]) -> List[Destination]:
    """
    Placeholder for hybrid recommendation - will be implemented in Tahap 2
    """
    return simple_recommendation(user, destinations)