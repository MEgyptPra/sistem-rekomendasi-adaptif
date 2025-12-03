from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any, Optional, Literal
import os
import sys
import subprocess
from datetime import datetime

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


@router.post("/ml/load")
def load_ml_models(
    model: Optional[Literal['content_based', 'collaborative', 'hybrid', 'all']] = Query('all', description="Which model to load (or 'all')"),
    x_admin_token: str = Header(None)
):
    """Load model artifacts on-demand."""
    admin_token = os.getenv('ADMIN_LOAD_TOKEN')
    if admin_token and x_admin_token != admin_token:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    try:
        if model == 'all':
            result = ml_service.load_all_models()
            return result
        
        # Individual loaders not strictly implemented in new MLService but keeping interface
        ml_service.load_all_models()
        return {"status": "success", "message": "Models reloaded"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model load failed: {str(e)}")

@router.get("/ml/status")
async def get_ml_status():
    """Get status of all ML models"""
    return ml_service.get_models_status()

@router.get("/ml/context")
async def get_current_context():
    """Get current real-time context (weather, traffic, etc)"""
    try:
        # Panggil service untuk dapat context
        # Perbaikan: Gunakan cara akses yang aman
        if hasattr(ml_service.context_service, 'get_current_context'):
            context = await ml_service.context_service.get_current_context()
        elif hasattr(ml_service.context_service, 'context_service'):
             # Fallback jika context_service ada di dalam properti (nested)
             context = await ml_service.context_service.context_service.get_current_context()
        else:
            context = {}

        # Tentukan mode secara aman (Safe Access)
        # Cek berbagai kemungkinan key untuk menentukan apakah ini simulasi atau bukan
        is_simulation = True
        if context:
            # Cek flag explicit
            if context.get('source') == 'openweathermap_api':
                is_simulation = False
            # Cek nested data_source jika ada
            elif context.get('data_source', {}).get('weather') != 'simulation':
                 # Jika key tidak ada, asumsi simulasi (default)
                 # Tapi jika key ada dan bukan 'simulation', maka production
                 if context.get('data_source', {}).get('weather'):
                     is_simulation = False
            # Cek key weather_description
            elif context.get('weather_description') and 'simulasi' not in str(context.get('weather_description')):
                is_simulation = False

        return {
            "status": "success",
            "context": context,
            "mode": "simulation" if is_simulation else "production"
        }
    except Exception as e:
        print(f"❌ Context Endpoint Error: {e}")
        # Jangan return 500, return default context agar frontend tidak crash
        return {
            "status": "partial_success",
            "context": {
                "weather": "cerah",
                "traffic": "lancar",
                "season": "kemarau"
            },
            "mode": "fallback"
        }

@router.get("/ml/context/status")
async def get_context_service_status():
    """Get status of real-time context service (API configuration)"""
    has_weather_api = bool(os.getenv("OPENWEATHER_API_KEY"))
    
    return {
        "weather_api": {
            "configured": has_weather_api,
            "provider": "OpenWeatherMap" if has_weather_api else None,
            "status": "active" if has_weather_api else "using_simulation"
        },
        "mode": "production" if has_weather_api else "simulation",
        "location": {
            "name": "Sumedang, Indonesia"
        }
    }

# ============== RECOMMENDATION ENDPOINTS ==============

@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: int,
    algorithm: Literal['content_based', 'collaborative', 'hybrid'] = Query('hybrid'),
    num_recommendations: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized recommendations for user with contextual awareness"""
    try:
        recommendations, arm_index, context = await ml_service.get_recommendations(
            user_id=user_id,
            algorithm=algorithm,
            num_recommendations=num_recommendations,
            db=db
        )
        
        response = {
            "user_id": user_id,
            "algorithm": algorithm,
            "recommendations": recommendations,
            "count": len(recommendations)
        }
        
        if algorithm == 'hybrid' and arm_index is not None:
            lambda_value = ml_service.mab_optimizer.get_lambda_value(arm_index)
            response["contextual_info"] = {
                "context": context,
                "mab_decision": {
                    "arm_index": arm_index,
                    "lambda_value": lambda_value
                }
            }
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

# ============== DATA ENDPOINTS ==============

@router.get("/destinations")
async def get_destinations(db: AsyncSession = Depends(get_db)):
    """Get all destinations"""
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
            "categories": [{"id": c.id, "name": c.name} for c in d.categories],
            "image": f"/assets/images/{d.name.lower().replace(' ', '-')}.jpg",
            "region": d.address
        }
        for d in destinations
    ]

@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all categories"""
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return [{"id": c.id, "name": c.name} for c in categories]

# ============== MAB ENDPOINTS ==============

@router.post("/mab/feedback")
async def submit_mab_feedback(
    arm_index: int,
    reward: float = Query(..., ge=0.0, le=1.0),
    context: str = Query(None) # Simplification
):
    """Submit contextual feedback for MAB learning"""
    try:
        # Parse context string back to dict if needed, or accept simple params
        # For now, we trust the service handles update
        result = ml_service.update_recommendation_feedback(arm_index, reward)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback update failed: {str(e)}")

@router.get("/mab/statistics")
async def get_mab_statistics():
    """Get detailed MAB statistics"""
    return ml_service.get_mab_statistics()