# Endpoint: POST /admin/test-api

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import httpx

admin_router = APIRouter()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# Dependency for protected routes
async def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email != admin_user["email"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

@admin_router.post("/test-api")
async def test_api_endpoint(request: Request, current_admin: dict = Depends(get_current_admin)):
    """
    Proxy request to any backend endpoint for testing purposes.
    Body: {
      "method": "GET"|"POST"|"PUT"|"DELETE",
      "url": "/admin/endpoint",
      "params": {...},
      "body": {...}
    }
    """
    data = await request.json()
    method = data.get("method", "GET").upper()
    url = data.get("url")
    params = data.get("params", {})
    body = data.get("body", {})
    # Only allow internal endpoints for security
    if not url or not url.startswith("/admin/"):
        return {"error": "Invalid or forbidden endpoint."}
    backend_url = f"http://localhost:8000{url}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(method, backend_url, params=params, json=body)
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": resp.json() if resp.headers.get("content-type","").startswith("application/json") else resp.text
            }
        except Exception as e:
            return {"error": str(e)}
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import os
import sys

# Add app to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.db import get_db
    from app.models.user import User
    from app.models.destinations import Destination
    from app.models.rating import Rating
    DB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Database modules not available: {e}")
    # Fallback if app modules not available
    get_db = None
    User = None
    Destination = None
    Rating = None
    DB_AVAILABLE = False

# Configuration
SECRET_KEY = "your-secret-key-for-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock admin user for demonstration
admin_user = {
    "email": "admin@example.com",
    "password": "admin123",  # In production, use hashed passwords
    "name": "Admin User",
    "role": "admin"
}

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class AdminLoginForm(BaseModel):
    email: str
    password: str

# JWT token generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# Dependency for protected routes
async def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email != admin_user["email"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    return admin_user

from app.services.real_time_data_production import RealTimeContextService
admin_router = APIRouter(prefix="/admin", tags=["admin"])
# Endpoint: GET /admin/model/realtime-stats?source=...
@admin_router.get("/model/realtime-stats")
async def get_realtime_stats(source: str, current_admin: dict = Depends(get_current_admin)):
    """
    Get status and preview data for real-time source (weather, traffic_google, traffic_tomtom, calendar, social_trend)
    """
    service = RealTimeContextService()
    now = datetime.now()
    status = "OK"
    last_checked = now.isoformat()
    preview = None
    try:
        if source == "weather":
            data = await service._get_weather(service.DEFAULT_LAT, service.DEFAULT_LON)
            preview = {
                "condition": data.get("condition"),
                "temperature": data.get("temperature"),
                "humidity": data.get("humidity"),
                "description": data.get("description"),
                "source": data.get("source")
            }
        elif source == "traffic_google":
            data = await service._get_traffic(service.DEFAULT_LAT, service.DEFAULT_LON)
            preview = {
                "condition": data.get("condition"),
                "speed": data.get("speed"),
                "source": data.get("source")
            }
        elif source == "traffic_tomtom":
            data = await service._get_traffic(service.DEFAULT_LAT, service.DEFAULT_LON)
            preview = {
                "condition": data.get("condition"),
                "speed": data.get("speed"),
                "source": data.get("source")
            }
        elif source == "calendar":
            data = await service._get_calendar_info(now)
            preview = {
                "is_holiday": data.get("is_holiday"),
                "holiday_name": data.get("holiday_name"),
                "holiday_type": data.get("holiday_type"),
                "source": data.get("source")
            }
        elif source == "social_trend":
            data = service.trend_service.get_trending_status()
            preview = {
                "overall_trend": data.get("overall_trend"),
                "trending_destinations": data.get("trending_destinations", [])[:3],
                "viral_destinations": data.get("viral_destinations", [])[:3]
            }
        else:
            status = "Error"
            preview = None
    except Exception as e:
        status = "Error"
        preview = {"error": str(e)}
    return {
        "status": status,
        "last_checked": last_checked,
        "preview": preview
    }

# Login endpoint
@admin_router.post("/login", response_model=Token)
async def admin_login(form_data: AdminLoginForm):
    if form_data.email != admin_user["email"] or form_data.password != admin_user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin_user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Dashboard stats endpoint - USING DATABASE
@admin_router.get("/stats")
async def get_admin_stats(
    current_admin: dict = Depends(get_current_admin)
):
    """Get dashboard statistics from database"""
    
    # Check if database is available
    if not DB_AVAILABLE or get_db is None:
        print("⚠️ Database not available, using demo data")
        return {
            "totalUsers": 150,
            "totalDestinations": 45,
            "totalRatings": 523,
            "averageRating": 4.2,
            "dataSource": "demo"
        }
    
    try:
        # Import Activity model
        from app.models.activity import Activity
        
        # Get database session
        async for db in get_db():
            try:
                # Count users
                users_count = await db.execute(select(func.count(User.id)))
                total_users = users_count.scalar() or 0
                
                # Count destinations
                dest_count = await db.execute(select(func.count(Destination.id)))
                total_destinations = dest_count.scalar() or 0
                
                # Count activities
                activities_count = await db.execute(select(func.count(Activity.id)))
                total_activities = activities_count.scalar() or 0
                
                # Count ratings and calculate average
                ratings_count = await db.execute(select(func.count(Rating.id)))
                total_ratings = ratings_count.scalar() or 0
                
                avg_rating = await db.execute(select(func.avg(Rating.rating)))
                average_rating = float(avg_rating.scalar() or 0)
                
                return {
                    "totalUsers": total_users,
                    "totalDestinations": total_destinations,
                    "totalActivities": total_activities,
                    "totalRatings": total_ratings,
                    "averageRating": round(average_rating, 2),
                    "dataSource": "database"
                }
            except Exception as e:
                print(f"❌ Database query error: {e}")
                import traceback
                traceback.print_exc()
                break
            finally:
                await db.close()
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        import traceback
        traceback.print_exc()
    
    # Fallback to demo data
    return {
        "totalUsers": 150,
        "totalDestinations": 45,
        "totalRatings": 523,
        "averageRating": 4.2,
        "dataSource": "demo"
    }

# Activity stats endpoint
@admin_router.get("/activity-stats")
async def get_activity_stats(current_admin: dict = Depends(get_current_admin)):
    # In a real app, fetch actual stats from your database
    return [
        {"name": "Jan", "users": 400, "recommendations": 240},
        {"name": "Feb", "users": 300, "recommendations": 139},
        {"name": "Mar", "users": 200, "recommendations": 980},
        {"name": "Apr", "users": 278, "recommendations": 390},
        {"name": "May", "users": 189, "recommendations": 480},
        {"name": "Jun", "users": 239, "recommendations": 380},
        {"name": "Jul", "users": 349, "recommendations": 430},
    ]

# Get all users from database
@admin_router.get("/users")
async def get_users(
    current_admin: dict = Depends(get_current_admin)
):
    """Get all users from database"""
    
    # Check if database is available
    if not DB_AVAILABLE or get_db is None:
        print("⚠️ Database not available, using demo data")
        return [
            {"id": 1, "name": "Demo User 1", "email": "user1@example.com", "preferences": "beach,culture", "created_at": "2024-01-01T00:00:00", "is_active": True},
            {"id": 2, "name": "Demo User 2", "email": "user2@example.com", "preferences": "adventure", "created_at": "2024-01-02T00:00:00", "is_active": True},
        ]
    
    try:
        async for db in get_db():
            try:
                result = await db.execute(select(User))
                users = result.scalars().all()
                
                return [
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email or f"user{user.id}@example.com",
                        "preferences": user.preferences,
                        "created_at": user.created_at.isoformat() if user.created_at else None,
                        "is_active": True
                    }
                    for user in users
                ]
            except Exception as e:
                print(f"❌ Database query error fetching users: {e}")
                import traceback
                traceback.print_exc()
                break
            finally:
                await db.close()
    except Exception as e:
        print(f"❌ Database connection error: {e}")
    
    # Fallback to demo data
    return [
        {"id": 1, "name": "Demo User 1", "email": "user1@example.com", "preferences": "beach,culture", "created_at": "2024-01-01T00:00:00", "is_active": True},
        {"id": 2, "name": "Demo User 2", "email": "user2@example.com", "preferences": "adventure", "created_at": "2024-01-02T00:00:00", "is_active": True},
    ]

# Get all destinations from database
@admin_router.get("/destinations")
async def get_destinations(
    current_admin: dict = Depends(get_current_admin)
):
    """Get all destinations from database"""
    
    # Check if database is available
    if not DB_AVAILABLE or get_db is None:
        print("⚠️ Database not available, using demo data")
        return [
            {"id": 1, "name": "Demo Destination 1", "address": "Jakarta", "description": "Beautiful place", "lat": -6.2088, "lon": 106.8456, "created_at": "2024-01-01T00:00:00"},
            {"id": 2, "name": "Demo Destination 2", "address": "Bali", "description": "Amazing beach", "lat": -8.3405, "lon": 115.0920, "created_at": "2024-01-02T00:00:00"},
        ]
    
    try:
        async for db in get_db():
            try:
                result = await db.execute(select(Destination))
                destinations = result.scalars().all()
                
                def safe_float(value, default=0):
                    """Convert to float, handling None and NaN"""
                    if value is None:
                        return default
                    try:
                        f = float(value)
                        # Check if NaN or infinite
                        if f != f or f == float('inf') or f == float('-inf'):
                            return default
                        return f
                    except (ValueError, TypeError):
                        return default
                
                return [
                    {
                        "id": dest.id,
                        "name": dest.name,
                        "location": dest.address or "Unknown",  # Use address as location
                        "address": dest.address,
                        "description": dest.description,
                        "lat": safe_float(dest.lat, 0),
                        "lon": safe_float(dest.lon, 0),
                        "image_url": None,  # Not in model, set to None
                        "price": 0,  # Not in model, set to default
                        "created_at": None  # Not in model
                    }
                    for dest in destinations
                ]
            except Exception as e:
                print(f"❌ Database query error fetching destinations: {e}")
                import traceback
                traceback.print_exc()
                break
            finally:
                await db.close()
    except Exception as e:
        print(f"❌ Database connection error: {e}")
    
    # Fallback to demo data
    return [
        {"id": 1, "name": "Demo Destination 1", "address": "Jakarta", "location": "Jakarta", "description": "Beautiful place", "lat": -6.2088, "lon": 106.8456, "created_at": "2024-01-01T00:00:00"},
        {"id": 2, "name": "Demo Destination 2", "address": "Bali", "location": "Bali", "description": "Amazing beach", "lat": -8.3405, "lon": 115.0920, "created_at": "2024-01-02T00:00:00"},
    ]

# Get analytics data
@admin_router.get("/analytics")
async def get_analytics(
    current_admin: dict = Depends(get_current_admin)
):
    """Get comprehensive analytics data"""
    # Reuse the stats endpoint
    return await get_admin_stats(current_admin)

# Get activities (if activities table exists)
@admin_router.get("/activities")
async def get_activities(
    current_admin: dict = Depends(get_current_admin)
):
    """Get all activities from database"""
    
    print("🔍 get_activities called")
    
    # Check if database is available
    if not DB_AVAILABLE or get_db is None:
        print("⚠️ Database not available, using demo data")
        return []
    
    print("✅ Database available, fetching activities...")
    
    try:
        # Import Activity model
        from app.models.activity import Activity
        
        async for db in get_db():
            try:
                result = await db.execute(select(Activity))
                activities = result.scalars().all()
                
                print(f"✅ Found {len(activities)} activities in database")
                
                activities_list = [
                    {
                        "id": act.id,
                        "name": act.name,
                        "description": act.description,
                        "category": act.category,
                        "duration": act.duration,
                        "price_range": act.price_range,
                        "image_url": act.image_url,
                        "created_at": act.created_at.isoformat() if act.created_at else None
                    }
                    for act in activities
                ]
                
                print(f"✅ Returning {len(activities_list)} activities")
                return activities_list
            except Exception as e:
                print(f"❌ Database query error fetching activities: {e}")
                import traceback
                traceback.print_exc()
                break
            finally:
                await db.close()
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        import traceback
        traceback.print_exc()
    
    # Fallback to empty array
    print("⚠️ Returning empty array")
    return []
