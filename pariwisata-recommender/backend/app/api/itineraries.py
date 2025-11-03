from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

from ..core.db import get_db
from .medium_priority_endpoints import get_current_user
from ..models.itinerary import Itinerary, ItineraryDay, ItineraryItem
from ..models.user import User

router = APIRouter()

# Pydantic Schemas
class ItineraryItemCreate(BaseModel):
    time: Optional[str] = None
    activity_type: str
    entity_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[str] = None
    cost: Optional[int] = None
    notes: Optional[str] = None
    order: int

class ItineraryDayCreate(BaseModel):
    day_number: int
    date: date
    title: Optional[str] = None
    items: List[ItineraryItemCreate]

class ItineraryCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    total_budget: Optional[int] = None
    accommodation: Optional[str] = None
    transportation: Optional[str] = None
    notes: Optional[str] = None
    days: List[ItineraryDayCreate]

class ItineraryItemResponse(BaseModel):
    id: int
    time: Optional[str]
    activity_type: str
    entity_id: Optional[int]
    title: str
    description: Optional[str]
    location: Optional[str]
    duration: Optional[str]
    cost: Optional[int]
    notes: Optional[str]
    order: int

    class Config:
        from_attributes = True

class ItineraryDayResponse(BaseModel):
    id: int
    day_number: int
    date: date
    title: Optional[str]
    items: List[ItineraryItemResponse]

    class Config:
        from_attributes = True

class ItineraryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date
    status: str
    total_budget: Optional[int]
    accommodation: Optional[str]
    transportation: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    days: List[ItineraryDayResponse]

    class Config:
        from_attributes = True

class ItineraryListItem(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# === ENDPOINTS ===

@router.post("/", response_model=ItineraryResponse, status_code=status.HTTP_201_CREATED)
async def create_itinerary(
    itinerary_data: ItineraryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new itinerary for the authenticated user"""
    
    # Create itinerary
    new_itinerary = Itinerary(
        user_id=current_user.id,
        title=itinerary_data.title,
        description=itinerary_data.description,
        start_date=itinerary_data.start_date,
        end_date=itinerary_data.end_date,
        total_budget=itinerary_data.total_budget,
        accommodation=itinerary_data.accommodation,
        transportation=itinerary_data.transportation,
        notes=itinerary_data.notes,
        status='upcoming'
    )
    
    db.add(new_itinerary)
    await db.flush()
    
    # Create days and items
    for day_data in itinerary_data.days:
        new_day = ItineraryDay(
            itinerary_id=new_itinerary.id,
            day_number=day_data.day_number,
            date=day_data.date,
            title=day_data.title
        )
        db.add(new_day)
        await db.flush()
        
        # Create items for this day
        for item_data in day_data.items:
            new_item = ItineraryItem(
                day_id=new_day.id,
                time=item_data.time,
                activity_type=item_data.activity_type,
                entity_id=item_data.entity_id,
                title=item_data.title,
                description=item_data.description,
                location=item_data.location,
                duration=item_data.duration,
                cost=item_data.cost,
                notes=item_data.notes,
                order=item_data.order
            )
            db.add(new_item)
    
    await db.commit()
    
    # Fetch complete itinerary with relationships
    result = await db.execute(
        select(Itinerary)
        .options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        )
        .where(Itinerary.id == new_itinerary.id)
    )
    created_itinerary = result.scalar_one()
    
    return created_itinerary


@router.get("/", response_model=List[ItineraryListItem])
async def get_my_itineraries(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all itineraries for the authenticated user"""
    
    query = select(Itinerary).where(Itinerary.user_id == current_user.id)
    
    if status:
        query = query.where(Itinerary.status == status)
    
    query = query.order_by(Itinerary.start_date.desc())
    
    result = await db.execute(query)
    itineraries = result.scalars().all()
    
    return itineraries


@router.get("/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(
    itinerary_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific itinerary by ID"""
    
    result = await db.execute(
        select(Itinerary)
        .options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        )
        .where(Itinerary.id == itinerary_id)
        .where(Itinerary.user_id == current_user.id)
    )
    itinerary = result.scalar_one_or_none()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found"
        )
    
    return itinerary


@router.put("/{itinerary_id}", response_model=ItineraryResponse)
async def update_itinerary(
    itinerary_id: int,
    itinerary_data: ItineraryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing itinerary"""
    
    # Fetch itinerary
    result = await db.execute(
        select(Itinerary)
        .where(Itinerary.id == itinerary_id)
        .where(Itinerary.user_id == current_user.id)
    )
    itinerary = result.scalar_one_or_none()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found"
        )
    
    # Update itinerary fields
    itinerary.title = itinerary_data.title
    itinerary.description = itinerary_data.description
    itinerary.start_date = itinerary_data.start_date
    itinerary.end_date = itinerary_data.end_date
    itinerary.total_budget = itinerary_data.total_budget
    itinerary.accommodation = itinerary_data.accommodation
    itinerary.transportation = itinerary_data.transportation
    itinerary.notes = itinerary_data.notes
    
    # Delete old days and items (cascade will delete items)
    await db.execute(
        delete(ItineraryDay).where(ItineraryDay.itinerary_id == itinerary_id)
    )
    
    # Create new days and items
    for day_data in itinerary_data.days:
        new_day = ItineraryDay(
            itinerary_id=itinerary.id,
            day_number=day_data.day_number,
            date=day_data.date,
            title=day_data.title
        )
        db.add(new_day)
        await db.flush()
        
        for item_data in day_data.items:
            new_item = ItineraryItem(
                day_id=new_day.id,
                time=item_data.time,
                activity_type=item_data.activity_type,
                entity_id=item_data.entity_id,
                title=item_data.title,
                description=item_data.description,
                location=item_data.location,
                duration=item_data.duration,
                cost=item_data.cost,
                notes=item_data.notes,
                order=item_data.order
            )
            db.add(new_item)
    
    await db.commit()
    
    # Fetch updated itinerary
    result = await db.execute(
        select(Itinerary)
        .options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        )
        .where(Itinerary.id == itinerary_id)
    )
    updated_itinerary = result.scalar_one()
    
    return updated_itinerary


@router.delete("/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_itinerary(
    itinerary_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an itinerary"""
    
    result = await db.execute(
        select(Itinerary)
        .where(Itinerary.id == itinerary_id)
        .where(Itinerary.user_id == current_user.id)
    )
    itinerary = result.scalar_one_or_none()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found"
        )
    
    await db.delete(itinerary)
    await db.commit()
    
    return None


@router.patch("/{itinerary_id}/status", response_model=ItineraryResponse)
async def update_itinerary_status(
    itinerary_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update itinerary status (upcoming, ongoing, completed, cancelled)"""
    
    valid_statuses = ['upcoming', 'ongoing', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    result = await db.execute(
        select(Itinerary)
        .options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        )
        .where(Itinerary.id == itinerary_id)
        .where(Itinerary.user_id == current_user.id)
    )
    itinerary = result.scalar_one_or_none()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found"
        )
    
    itinerary.status = new_status
    await db.commit()
    await db.refresh(itinerary)
    
    return itinerary
