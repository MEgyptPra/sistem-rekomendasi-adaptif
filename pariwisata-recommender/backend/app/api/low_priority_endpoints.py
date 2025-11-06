"""
LOW PRIORITY API ENDPOINTS
- Search functionality (destinations, activities)
- Related items recommendations
- User preferences management
- Advanced filtering
- Social features (favorites, likes)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, or_, and_, desc
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.db import get_db
from app.models.user import User
from app.models.destinations import Destination
from app.models.activity import Activity
from app.models.category import Category
from app.models.destination_review import DestinationReview
from app.models.activity_review import ActivityReview
from app.models.user_interaction import UserInteraction
from app.api.medium_priority_endpoints import get_current_user, require_auth

router = APIRouter()

# ============== PYDANTIC SCHEMAS ==============

class SearchResult(BaseModel):
    type: str  # 'destination' or 'activity'
    id: int
    name: str
    description: Optional[str]
    image: str
    category: Optional[str]
    rating: float
    reviewCount: int
    
class UserPreferencesUpdate(BaseModel):
    preferences: str  # Comma-separated categories: "alam,kuliner,budaya"

class FavoriteCreate(BaseModel):
    entity_type: str  # 'destination' or 'activity'
    entity_id: int

# ============== SEARCH ENDPOINTS ==============

@router.get("/search")
async def search_all(
    q: str = Query(..., min_length=2, description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type: 'destination' or 'activity'"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Universal search across destinations and activities
    Searches in name and description
    """
    results = []
    
    try:
        # Search destinations if not filtered to activities only
        if not type or type == 'destination':
            dest_query = select(Destination).where(
                or_(
                    Destination.name.ilike(f"%{q}%"),
                    Destination.description.ilike(f"%{q}%")
                )
            )
            
            dest_result = await db.execute(dest_query.limit(limit))
            destinations = dest_result.scalars().all()
            
            for dest in destinations:
                # Get review stats
                review_stats = await db.execute(
                    select(
                        func.count(DestinationReview.id),
                        func.avg(DestinationReview.rating)
                    ).where(DestinationReview.destination_id == dest.id)
                )
                count, avg_rating = review_stats.one()
                
                # Get category (first one)
                cat_result = await db.execute(
                    select(Category)
                    .join(Destination.categories)
                    .where(Destination.id == dest.id)
                    .limit(1)
                )
                category_obj = cat_result.scalar_one_or_none()
                
                results.append({
                    "type": "destination",
                    "id": dest.id,
                    "name": dest.name,
                    "description": dest.description,
                    "image": f"/assets/images/{dest.name.lower().replace(' ', '-')}.jpg",
                    "category": category_obj.name if category_obj else "Umum",
                    "rating": round(float(avg_rating or 0), 1),
                    "reviewCount": count or 0
                })
        
        # Search activities if not filtered to destinations only
        if not type or type == 'activity':
            activity_query = select(Activity).where(
                or_(
                    Activity.name.ilike(f"%{q}%"),
                    Activity.description.ilike(f"%{q}%")
                )
            )
            
            if category:
                activity_query = activity_query.where(Activity.category.ilike(f"%{category}%"))
            
            activity_result = await db.execute(activity_query.limit(limit))
            activities = activity_result.scalars().all()
            
            for activity in activities:
                # Get review stats
                review_stats = await db.execute(
                    select(
                        func.count(ActivityReview.id),
                        func.avg(ActivityReview.rating)
                    ).where(ActivityReview.activity_id == activity.id)
                )
                count, avg_rating = review_stats.one()
                
                results.append({
                    "type": "activity",
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "image": activity.image_url or "/assets/images/default.jpg",
                    "category": activity.category,
                    "rating": round(float(avg_rating or 0), 1),
                    "reviewCount": count or 0
                })
        
        return {
            "query": q,
            "results": results[:limit],
            "total": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/destinations")
async def search_destinations(
    q: str = Query(..., min_length=2),
    category: Optional[str] = None,
    region: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Advanced search for destinations with filters
    """
    try:
        query = select(Destination).where(
            or_(
                Destination.name.ilike(f"%{q}%"),
                Destination.description.ilike(f"%{q}%"),
                Destination.address.ilike(f"%{q}%")
            )
        )
        
        if region:
            query = query.where(Destination.address.ilike(f"%{region}%"))
        
        result = await db.execute(query.limit(limit))
        destinations = result.scalars().all()
        
        # Filter by rating if specified
        filtered_destinations = []
        for dest in destinations:
            review_stats = await db.execute(
                select(func.avg(DestinationReview.rating))
                .where(DestinationReview.destination_id == dest.id)
            )
            avg_rating = review_stats.scalar() or 0
            
            if not min_rating or avg_rating >= min_rating:
                filtered_destinations.append({
                    "id": dest.id,
                    "name": dest.name,
                    "description": dest.description,
                    "address": dest.address,
                    "rating": round(float(avg_rating), 1)
                })
        
        return {
            "query": q,
            "destinations": filtered_destinations,
            "total": len(filtered_destinations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/activities")
async def search_activities(
    q: str = Query(..., min_length=2),
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Advanced search for activities with filters
    """
    try:
        query = select(Activity).where(
            or_(
                Activity.name.ilike(f"%{q}%"),
                Activity.description.ilike(f"%{q}%")
            )
        )
        
        if category:
            query = query.where(Activity.category.ilike(f"%{category}%"))
        
        result = await db.execute(query.limit(limit))
        activities = result.scalars().all()
        
        # Note: Price filtering would require parsing price_range string
        # For now, return all matching activities
        
        activities_list = []
        for activity in activities:
            review_stats = await db.execute(
                select(
                    func.count(ActivityReview.id),
                    func.avg(ActivityReview.rating)
                ).where(ActivityReview.activity_id == activity.id)
            )
            count, avg_rating = review_stats.one()
            
            activities_list.append({
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "category": activity.category,
                "duration": activity.duration,
                "price_range": activity.price_range,
                "rating": round(float(avg_rating or 0), 1),
                "reviewCount": count or 0
            })
        
        return {
            "query": q,
            "activities": activities_list,
            "total": len(activities_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# ============== RELATED ITEMS ENDPOINTS ==============

@router.get("/destinations/{destination_id}/related")
async def get_related_destinations(
    destination_id: int,
    limit: int = Query(6, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """
    Get related destinations based on categories and location
    """
    try:
        # Get the destination
        result = await db.execute(
            select(Destination)
            .options(selectinload(Destination.categories))
            .where(Destination.id == destination_id)
        )
        destination = result.scalar_one_or_none()
        
        if not destination:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        # Get destinations with same categories
        category_ids = [cat.id for cat in destination.categories]
        
        if category_ids:
            # Find destinations sharing categories
            related_query = select(Destination).join(Destination.categories).where(
                and_(
                    Category.id.in_(category_ids),
                    Destination.id != destination_id
                )
            ).distinct().limit(limit)
        else:
            # Fallback: get random popular destinations
            related_query = select(Destination).where(
                Destination.id != destination_id
            ).limit(limit)
        
        related_result = await db.execute(related_query)
        related_destinations = related_result.scalars().all()
        
        # Format response
        related_list = []
        for dest in related_destinations:
            review_stats = await db.execute(
                select(
                    func.count(DestinationReview.id),
                    func.avg(DestinationReview.rating)
                ).where(DestinationReview.destination_id == dest.id)
            )
            count, avg_rating = review_stats.one()
            
            related_list.append({
                "id": dest.id,
                "name": dest.name,
                "description": dest.description,
                "image": f"/assets/images/{dest.name.lower().replace(' ', '-')}.jpg",
                "rating": round(float(avg_rating or 0), 1),
                "reviewCount": count or 0
            })
        
        return {
            "destination_id": destination_id,
            "related": related_list,
            "total": len(related_list)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch related destinations: {str(e)}")


@router.get("/activities/{activity_id}/related")
async def get_related_activities(
    activity_id: int,
    limit: int = Query(6, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """
    Get related activities based on category
    """
    try:
        # Get the activity
        result = await db.execute(
            select(Activity).where(Activity.id == activity_id)
        )
        activity = result.scalar_one_or_none()
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Find activities with same category
        related_query = select(Activity).where(
            and_(
                Activity.category == activity.category,
                Activity.id != activity_id
            )
        ).limit(limit)
        
        related_result = await db.execute(related_query)
        related_activities = related_result.scalars().all()
        
        # Format response
        related_list = []
        for act in related_activities:
            review_stats = await db.execute(
                select(
                    func.count(ActivityReview.id),
                    func.avg(ActivityReview.rating)
                ).where(ActivityReview.activity_id == act.id)
            )
            count, avg_rating = review_stats.one()
            
            related_list.append({
                "id": act.id,
                "name": act.name,
                "description": act.description,
                "category": act.category,
                "duration": act.duration,
                "price_range": act.price_range,
                "rating": round(float(avg_rating or 0), 1),
                "reviewCount": count or 0
            })
        
        return {
            "activity_id": activity_id,
            "related": related_list,
            "total": len(related_list)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch related activities: {str(e)}")


# ============== USER PREFERENCES ENDPOINTS ==============

@router.get("/users/{user_id}/preferences")
async def get_user_preferences(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user preferences
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        preferences_list = user.preferences.split(",") if user.preferences else []
        
        return {
            "user_id": user_id,
            "preferences": preferences_list,
            "preferences_string": user.preferences or ""
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch preferences: {str(e)}")


@router.put("/users/{user_id}/preferences")
async def update_user_preferences(
    user_id: int,
    preferences_data: UserPreferencesUpdate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user preferences
    Requires authentication and user must be the owner
    """
    try:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this user's preferences")
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.preferences = preferences_data.preferences
        await db.commit()
        
        preferences_list = user.preferences.split(",") if user.preferences else []
        
        return {
            "message": "Preferences updated successfully",
            "user_id": user_id,
            "preferences": preferences_list
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update preferences: {str(e)}")


@router.get("/users/{user_id}/recommendations")
async def get_personalized_recommendations_for_user(
    user_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized recommendations based on user preferences and interactions
    """
    try:
        # Get user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        recommendations = []
        
        # Get user preferences
        preferred_categories = user.preferences.split(",") if user.preferences else []
        
        if preferred_categories:
            # Get destinations matching preferences
            for category in preferred_categories[:3]:  # Limit to top 3 preferences
                dest_query = select(Destination).join(Destination.categories).where(
                    Category.name.ilike(f"%{category.strip()}%")
                ).limit(5)
                
                dest_result = await db.execute(dest_query)
                destinations = dest_result.scalars().all()
                
                for dest in destinations:
                    if len(recommendations) >= limit:
                        break
                    
                    review_stats = await db.execute(
                        select(
                            func.count(DestinationReview.id),
                            func.avg(DestinationReview.rating)
                        ).where(DestinationReview.destination_id == dest.id)
                    )
                    count, avg_rating = review_stats.one()
                    
                    recommendations.append({
                        "type": "destination",
                        "id": dest.id,
                        "name": dest.name,
                        "description": dest.description,
                        "category": category.strip(),
                        "rating": round(float(avg_rating or 0), 1),
                        "reviewCount": count or 0,
                        "reason": f"Based on your interest in {category.strip()}"
                    })
        
        # Fill remaining slots with popular destinations
        if len(recommendations) < limit:
            popular_query = select(Destination).limit(limit - len(recommendations))
            popular_result = await db.execute(popular_query)
            popular_destinations = popular_result.scalars().all()
            
            for dest in popular_destinations:
                review_stats = await db.execute(
                    select(
                        func.count(DestinationReview.id),
                        func.avg(DestinationReview.rating)
                    ).where(DestinationReview.destination_id == dest.id)
                )
                count, avg_rating = review_stats.one()
                
                recommendations.append({
                    "type": "destination",
                    "id": dest.id,
                    "name": dest.name,
                    "description": dest.description,
                    "rating": round(float(avg_rating or 0), 1),
                    "reviewCount": count or 0,
                    "reason": "Popular destination"
                })
        
        return {
            "user_id": user_id,
            "recommendations": recommendations[:limit],
            "total": len(recommendations[:limit])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")


# ============== FAVORITES ENDPOINTS ==============

@router.post("/favorites")
async def add_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a destination or activity to favorites
    """
    try:
        # Check if already favorited
        existing = await db.execute(
            select(UserInteraction).where(
                and_(
                    UserInteraction.user_id == current_user.id,
                    UserInteraction.interaction_type == 'favorite',
                    UserInteraction.entity_type == favorite_data.entity_type,
                    UserInteraction.entity_id == favorite_data.entity_id
                )
            )
        )
        
        if existing.scalar_one_or_none():
            return {"message": "Already in favorites", "action": "none"}
        
        # Create favorite interaction
        new_favorite = UserInteraction(
            user_id=current_user.id,
            interaction_type='favorite',
            entity_type=favorite_data.entity_type,
            entity_id=favorite_data.entity_id
        )
        
        db.add(new_favorite)
        await db.commit()
        
        # 🚀 AUTO LEARNING: Track favorite (only for destinations)
        if favorite_data.entity_type == 'destination':
            from app.middleware.learning_middleware import track_favorite_added
            import asyncio
            asyncio.create_task(
                track_favorite_added(favorite_data.entity_id, current_user.id, db)
            )
        
        return {
            "message": "Added to favorites",
            "action": "added",
            "favorite_id": new_favorite.id
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add favorite: {str(e)}")


@router.delete("/favorites/{entity_type}/{entity_id}")
async def remove_favorite(
    entity_type: str,
    entity_id: int,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove from favorites
    """
    try:
        result = await db.execute(
            select(UserInteraction).where(
                and_(
                    UserInteraction.user_id == current_user.id,
                    UserInteraction.interaction_type == 'favorite',
                    UserInteraction.entity_type == entity_type,
                    UserInteraction.entity_id == entity_id
                )
            )
        )
        favorite = result.scalar_one_or_none()
        
        if not favorite:
            raise HTTPException(status_code=404, detail="Favorite not found")
        
        await db.delete(favorite)
        await db.commit()
        
        return {"message": "Removed from favorites"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to remove favorite: {str(e)}")


@router.get("/users/{user_id}/favorites")
async def get_user_favorites(
    user_id: int,
    entity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's favorite destinations and activities
    """
    try:
        query = select(UserInteraction).where(
            and_(
                UserInteraction.user_id == user_id,
                UserInteraction.interaction_type == 'favorite'
            )
        )
        
        if entity_type:
            query = query.where(UserInteraction.entity_type == entity_type)
        
        query = query.order_by(UserInteraction.created_at.desc())
        
        result = await db.execute(query)
        favorites = result.scalars().all()
        
        favorites_list = []
        for fav in favorites:
            item = {
                "entity_type": fav.entity_type,
                "entity_id": fav.entity_id,
                "added_at": fav.created_at
            }
            
            # Get entity details
            if fav.entity_type == 'destination':
                dest_result = await db.execute(
                    select(Destination).where(Destination.id == fav.entity_id)
                )
                dest = dest_result.scalar_one_or_none()
                if dest:
                    item["name"] = dest.name
                    item["description"] = dest.description
            elif fav.entity_type == 'activity':
                act_result = await db.execute(
                    select(Activity).where(Activity.id == fav.entity_id)
                )
                act = act_result.scalar_one_or_none()
                if act:
                    item["name"] = act.name
                    item["description"] = act.description
                    item["category"] = act.category
            
            favorites_list.append(item)
        
        return {
            "user_id": user_id,
            "favorites": favorites_list,
            "total": len(favorites_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch favorites: {str(e)}")


# ============== STATISTICS ENDPOINTS ==============

@router.get("/stats/popular")
async def get_popular_items(
    type: Optional[str] = Query(None, description="'destination' or 'activity'"),
    period: str = Query("all", description="'week', 'month', 'all'"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get most popular destinations/activities based on views and clicks
    """
    try:
        results = []
        
        # Get popular destinations
        if not type or type == 'destination':
            dest_stats = await db.execute(
                select(
                    UserInteraction.entity_id,
                    func.count(UserInteraction.id).label('interaction_count')
                ).where(
                    and_(
                        UserInteraction.entity_type == 'destination',
                        UserInteraction.interaction_type.in_(['click', 'view'])
                    )
                ).group_by(UserInteraction.entity_id)
                .order_by(desc('interaction_count'))
                .limit(limit)
            )
            
            for entity_id, count in dest_stats:
                dest_result = await db.execute(
                    select(Destination).where(Destination.id == entity_id)
                )
                dest = dest_result.scalar_one_or_none()
                if dest:
                    results.append({
                        "type": "destination",
                        "id": dest.id,
                        "name": dest.name,
                        "interaction_count": count
                    })
        
        # Get popular activities
        if not type or type == 'activity':
            act_stats = await db.execute(
                select(
                    UserInteraction.entity_id,
                    func.count(UserInteraction.id).label('interaction_count')
                ).where(
                    and_(
                        UserInteraction.entity_type == 'activity',
                        UserInteraction.interaction_type.in_(['click', 'view'])
                    )
                ).group_by(UserInteraction.entity_id)
                .order_by(desc('interaction_count'))
                .limit(limit)
            )
            
            for entity_id, count in act_stats:
                act_result = await db.execute(
                    select(Activity).where(Activity.id == entity_id)
                )
                act = act_result.scalar_one_or_none()
                if act:
                    results.append({
                        "type": "activity",
                        "id": act.id,
                        "name": act.name,
                        "category": act.category,
                        "interaction_count": count
                    })
        
        # Sort by interaction count
        results.sort(key=lambda x: x['interaction_count'], reverse=True)
        
        return {
            "popular_items": results[:limit],
            "total": len(results[:limit])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch popular items: {str(e)}")
