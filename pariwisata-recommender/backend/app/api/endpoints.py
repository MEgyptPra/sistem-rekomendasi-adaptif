from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any, Optional, Literal

from app.core.db import get_db
from app.models.user import User
from app.models.destinations import Destination
from app.models.category import Category
from app.models.rating import Rating
from app.services.ml_service import ml_service

router = APIRouter()

# ============== ML TRAINING ENDPOINTS ==============

@router.post("/ml/train")
async def train_ml_models(db: AsyncSession = Depends(get_db)):
    """Train all ML recommendation models"""
    try:
        results = await ml_service.train_all_models(db)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get("/ml/status")
async def get_ml_status():
    """Get status of all ML models"""
    return ml_service.get_models_status()

# ============== RECOMMENDATION ENDPOINTS ==============

@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: int,
    algorithm: Literal['content_based', 'collaborative', 'hybrid'] = Query('hybrid'),
    num_recommendations: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized recommendations for user"""
    try:
        recommendations = await ml_service.get_recommendations(
            user_id=user_id,
            algorithm=algorithm,
            num_recommendations=num_recommendations,
            db=db
        )
        
        return {
            "user_id": user_id,
            "algorithm": algorithm,
            "recommendations": recommendations,
            "count": len(recommendations)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

@router.get("/recommendations/{user_id}/explain/{destination_id}")
async def explain_recommendation(
    user_id: int,
    destination_id: int,
    algorithm: Literal['content_based', 'collaborative', 'hybrid'] = Query('hybrid'),
    db: AsyncSession = Depends(get_db)
):
    """Explain why this destination was recommended"""
    try:
        explanation = await ml_service.explain_recommendation(
            user_id=user_id,
            destination_id=destination_id,
            algorithm=algorithm,
            db=db
        )
        
        return {
            "user_id": user_id,
            "destination_id": destination_id,
            "algorithm": algorithm,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")

@router.get("/user/{user_id}/profile")
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get comprehensive user profile"""
    try:
        profile = await ml_service.get_user_profile(user_id, db)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get profile failed: {str(e)}")

# ============== DATA ENDPOINTS ==============

@router.get("/destinations")
async def get_destinations(db: AsyncSession = Depends(get_db)):
    """Get all destinations with categories"""
    result = await db.execute(
        select(Destination).options(selectinload(Destination.categories))
    )
    destinations = result.scalars().all()
    
    return [
        {
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "location": d.address,
            "latitude": d.lat,
            "longitude": d.lon,
            "categories": [{"id": c.id, "name": c.name} for c in d.categories]
        }
        for d in destinations
    ]

@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all categories"""
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return [{"id": c.id, "name": c.name, "description": c.description} for c in categories]

@router.post("/rating")
async def add_rating(
    user_id: int,
    destination_id: int,
    rating: float = Query(..., ge=1.0, le=5.0),
    db: AsyncSession = Depends(get_db)
):
    """Add user rating for destination"""
    # Check if user and destination exist
    user = await db.get(User, user_id)
    destination = await db.get(Destination, destination_id)
    
    if not user or not destination:
        raise HTTPException(status_code=404, detail="User or destination not found")
    
    # Check if rating already exists
    existing_rating = await db.execute(
        select(Rating).where(
            Rating.user_id == user_id,
            Rating.destination_id == destination_id
        )
    )
    existing = existing_rating.scalar_one_or_none()
    
    if existing:
        # Update existing rating
        existing.rating = rating
        await db.commit()
        return {"message": "Rating updated successfully", "rating_id": existing.id}
    else:
        # Create new rating
        new_rating = Rating(
            user_id=user_id,
            destination_id=destination_id,
            rating=rating
        )
        db.add(new_rating)
        await db.commit()
        await db.refresh(new_rating)
        return {"message": "Rating added successfully", "rating_id": new_rating.id}

@router.get("/user/{user_id}/ratings")
async def get_user_ratings(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all ratings by user"""
    result = await db.execute(
        select(Rating).where(Rating.user_id == user_id)
    )
    ratings = result.scalars().all()
    
    ratings_data = []
    for rating in ratings:
        destination = await db.get(Destination, rating.destination_id)
        ratings_data.append({
            "rating_id": rating.id,
            "destination_id": rating.destination_id,
            "destination_name": destination.name if destination else "Unknown",
            "rating": rating.rating,
            "created_at": rating.created_at
        })
    
    return ratings_data

# ============== ANALYTICS ENDPOINTS ==============

@router.get("/analytics/destinations")
async def get_destination_analytics(db: AsyncSession = Depends(get_db)):
    """Get destination analytics"""
    from sqlalchemy import func
    
    # Rating statistics per destination
    result = await db.execute(
        select(
            Destination.id,
            Destination.name,
            func.count(Rating.id).label('rating_count'),
            func.avg(Rating.rating).label('avg_rating'),
            func.min(Rating.rating).label('min_rating'),
            func.max(Rating.rating).label('max_rating')
        )
        .outerjoin(Rating)
        .group_by(Destination.id, Destination.name)
        .order_by(func.avg(Rating.rating).desc())
    )
    
    analytics = []
    for row in result:
        analytics.append({
            "destination_id": row.id,
            "destination_name": row.name,
            "rating_count": row.rating_count or 0,
            "average_rating": round(float(row.avg_rating), 2) if row.avg_rating else 0,
            "min_rating": float(row.min_rating) if row.min_rating else 0,
            "max_rating": float(row.max_rating) if row.max_rating else 0
        })
    
    return analytics

@router.get("/analytics/users")
async def get_user_analytics(db: AsyncSession = Depends(get_db)):
    """Get user analytics"""
    from sqlalchemy import func
    
    result = await db.execute(
        select(
            User.id,
            User.name,
            func.count(Rating.id).label('rating_count'),
            func.avg(Rating.rating).label('avg_rating')
        )
        .outerjoin(Rating)
        .group_by(User.id, User.name)
        .order_by(func.count(Rating.id).desc())
    )
    
    analytics = []
    for row in result:
        analytics.append({
            "user_id": row.id,
            "user_name": row.name,
            "rating_count": row.rating_count or 0,
            "average_rating": round(float(row.avg_rating), 2) if row.avg_rating else 0
        })
    
    return analytics