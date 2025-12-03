"""
MEDIUM PRIORITY API ENDPOINTS
- Itinerary Management (POST, GET itineraries)
- Authentication (Register, Login, Get Current User)
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date, timedelta
from pydantic import BaseModel, Field, EmailStr

from app.core.db import get_db
from app.core.auth import verify_password, get_password_hash, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User
from app.models.itinerary import Itinerary, ItineraryDay, ItineraryItem

router = APIRouter()

# ============== PYDANTIC SCHEMAS ==============

# Authentication Schemas
class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    preferences: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    preferences: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Itinerary Schemas
class ItineraryItemCreate(BaseModel):
    time: Optional[str] = None
    activity_type: str  # 'destination', 'activity', 'meal', 'rest', 'transport'
    entity_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[str] = None
    cost: Optional[int] = None
    notes: Optional[str] = None
    order: int

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

class ItineraryDayCreate(BaseModel):
    day_number: int
    date: date
    title: Optional[str] = None
    items: List[ItineraryItemCreate] = []

class ItineraryDayResponse(BaseModel):
    id: int
    day_number: int
    date: date
    title: Optional[str]
    items: List[ItineraryItemResponse]
    
    class Config:
        from_attributes = True

class ItineraryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: date
    end_date: date
    total_budget: Optional[int] = None
    accommodation: Optional[str] = None  # JSON string
    transportation: Optional[str] = None  # JSON string
    notes: Optional[str] = None
    days: List[ItineraryDayCreate] = []

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
    days: List[ItineraryDayResponse]
    
    class Config:
        from_attributes = True

# ============== AUTH HELPER ==============

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    return user

async def require_auth(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Require authentication (raises 401 if not authenticated)"""
    user = await get_current_user(authorization, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# ============== AUTHENTICATION ENDPOINTS ==============

@router.post("/auth/register", response_model=Token)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    try:
        # Check if email already exists
        result = await db.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            preferences=user_data.preferences
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(new_user.id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": new_user
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/auth/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password
    """
    try:
        # Find user by email
        result = await db.execute(select(User).where(User.email == credentials.email))
        user = result.scalar_one_or_none()
        
        if not user or not user.password_hash:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(require_auth)
):
    """
    Get current authenticated user info
    """
    return current_user


# ============== ITINERARY ENDPOINTS ==============

@router.post("/itineraries", response_model=ItineraryResponse)
async def create_itinerary(
    itinerary_data: ItineraryCreate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new itinerary
    Requires authentication
    """
    try:
        # Determine status based on start_date
        today = date.today()
        if itinerary_data.start_date > today:
            status = 'upcoming'
        elif itinerary_data.start_date <= today <= itinerary_data.end_date:
            status = 'ongoing'
        else:
            status = 'completed'
        
        # Create itinerary
        new_itinerary = Itinerary(
            user_id=current_user.id,
            title=itinerary_data.title,
            description=itinerary_data.description,
            start_date=itinerary_data.start_date,
            end_date=itinerary_data.end_date,
            status=status,
            total_budget=itinerary_data.total_budget,
            accommodation=itinerary_data.accommodation,
            transportation=itinerary_data.transportation,
            notes=itinerary_data.notes
        )
        
        db.add(new_itinerary)
        await db.flush()  # Get the itinerary ID
        
        # Create days and items
        for day_data in itinerary_data.days:
            new_day = ItineraryDay(
                itinerary_id=new_itinerary.id,
                day_number=day_data.day_number,
                date=day_data.date,
                title=day_data.title
            )
            db.add(new_day)
            await db.flush()  # Get the day ID
            
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
        complete_itinerary = result.scalar_one()
        
        return complete_itinerary
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create itinerary: {str(e)}")


@router.get("/itineraries", response_model=List[ItineraryResponse])
async def get_current_user_itineraries(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    """
    Get all itineraries for the current authenticated user
    Optional filter by status: 'upcoming', 'ongoing', 'completed', 'cancelled'
    """
    try:
        query = select(Itinerary).options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        ).where(Itinerary.user_id == current_user.id)
        
        if status:
            query = query.where(Itinerary.status == status)
        
        query = query.order_by(Itinerary.start_date.desc())
        
        result = await db.execute(query)
        itineraries = result.scalars().all()
        
        return itineraries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch itineraries: {str(e)}")


@router.get("/itineraries/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(
    itinerary_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get itinerary by ID
    Public endpoint (can be accessed without auth)
    """
    try:
        result = await db.execute(
            select(Itinerary)
            .options(
                selectinload(Itinerary.days).selectinload(ItineraryDay.items)
            )
            .where(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        return itinerary
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch itinerary: {str(e)}")


@router.get("/itineraries/user/{user_id}", response_model=List[ItineraryResponse])
async def get_user_itineraries(
    user_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all itineraries for a specific user
    Optional filter by status: 'upcoming', 'ongoing', 'completed', 'cancelled'
    """
    try:
        query = select(Itinerary).options(
            selectinload(Itinerary.days).selectinload(ItineraryDay.items)
        ).where(Itinerary.user_id == user_id)
        
        if status:
            query = query.where(Itinerary.status == status)
        
        query = query.order_by(Itinerary.start_date.desc())
        
        result = await db.execute(query)
        itineraries = result.scalars().all()
        
        return itineraries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user itineraries: {str(e)}")


@router.delete("/itineraries/{itinerary_id}")
async def delete_itinerary(
    itinerary_id: int,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an itinerary
    Only the owner can delete
    """
    try:
        result = await db.execute(
            select(Itinerary).where(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        # Check ownership
        if itinerary.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this itinerary")
        
        await db.delete(itinerary)
        await db.commit()
        
        return {"message": "Itinerary deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete itinerary: {str(e)}")


@router.get("/favorites")
async def get_current_user_favorites(
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Get favorites for the current authenticated user
    Returns empty list - favorites functionality to be implemented
    """
    # TODO: Implement actual favorites retrieval from database
    return []


@router.put("/itineraries/{itinerary_id}/status")
async def update_itinerary_status(
    itinerary_id: int,
    status: str,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Update itinerary status
    Valid statuses: 'upcoming', 'ongoing', 'completed', 'cancelled'
    """
    valid_statuses = ['upcoming', 'ongoing', 'completed', 'cancelled']
    
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    try:
        result = await db.execute(
            select(Itinerary).where(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        # Check ownership
        if itinerary.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this itinerary")
        
        itinerary.status = status
        await db.commit()
        
        return {"message": "Itinerary status updated successfully", "status": status}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update itinerary status: {str(e)}")
