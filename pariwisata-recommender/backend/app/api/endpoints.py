from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.db import get_db
from app.models.user import User
from app.models.destination import Destination
from app.models.category import Category
from app.models.rating import Rating
from app.services.ml_service import simple_recommendation

router = APIRouter()

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
            "location": d.location,
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

@router.get("/recommendation/{user_id}")
async def get_recommendation(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get recommendations for user"""
    # Ambil user
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ambil semua destinasi dengan categories
    result = await db.execute(
        select(Destination).options(selectinload(Destination.categories))
    )
    destinations = result.scalars().all()
    
    # Generate rekomendasi
    recs = simple_recommendation(user, destinations)
    
    return [
        {
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "location": d.location,
            "categories": [c.name for c in d.categories]
        }
        for d in recs
    ]

@router.post("/rating")
async def add_rating(user_id: int, destination_id: int, rating: float, db: AsyncSession = Depends(get_db)):
    """Add user rating for destination"""
    # Check if user and destination exist
    user = await db.get(User, user_id)
    destination = await db.get(Destination, destination_id)
    
    if not user or not destination:
        raise HTTPException(status_code=404, detail="User or destination not found")
    
    # Create rating
    new_rating = Rating(
        user_id=user_id,
        destination_id=destination_id,
        rating=rating
    )
    db.add(new_rating)
    await db.commit()
    await db.refresh(new_rating)
    
    return {"message": "Rating added successfully", "rating_id": new_rating.id}