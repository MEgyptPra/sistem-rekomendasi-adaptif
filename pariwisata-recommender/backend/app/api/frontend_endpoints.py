"""
HIGH PRIORITY API ENDPOINTS untuk Frontend
Endpoints untuk Destinations, Activities, Reviews, dan User Interactions
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.db import get_db
from app.models.user import User
from app.models.destinations import Destination
from app.models.activity import Activity
from app.models.destination_review import DestinationReview
from app.models.activity_review import ActivityReview
from app.models.user_interaction import UserInteraction
from app.models.category import Category

router = APIRouter()

# ============== PYDANTIC SCHEMAS ==============

class ReviewCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: str = Field(..., min_length=1)

class ReviewResponse(BaseModel):
    id: int
    name: str
    rating: float
    comment: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class InteractionCreate(BaseModel):
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    interaction_type: str  # 'click', 'view', 'favorite', 'share'
    entity_type: str  # 'destination', 'activity', 'itinerary'
    entity_id: int
    duration: Optional[float] = None
    extra_data: Optional[str] = None  # Renamed from 'metadata' to avoid SQLAlchemy conflict

# ============== DESTINATIONS ENDPOINTS ==============

@router.get("/destinations")
async def get_destinations_list(
    category: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of destinations with optional filters
    """
    try:
        query = select(Destination).options(selectinload(Destination.categories))
        
        # Apply filters
        if category:
            query = query.join(Destination.categories).where(Category.name.ilike(f"%{category}%"))
        
        if region:
            query = query.where(Destination.address.ilike(f"%{region}%"))
        
        # Add pagination
        query = query.offset(offset).limit(limit)
        
        result = await db.execute(query)
        destinations = result.scalars().unique().all()
        
        # Get review statistics for each destination
        destinations_data = []
        for dest in destinations:
            # Count reviews and calculate average rating
            review_query = select(
                func.count(DestinationReview.id).label('count'),
                func.avg(DestinationReview.rating).label('avg_rating')
            ).where(DestinationReview.destination_id == dest.id)
            
            review_result = await db.execute(review_query)
            review_stats = review_result.one()
            
            destinations_data.append({
                "id": dest.id,
                "name": dest.name,
                "description": dest.description,
                "image": f"/assets/images/{dest.name.lower().replace(' ', '-')}.jpg",  # Placeholder
                "region": dest.address or "Sumedang",
                "category": dest.categories[0].name if dest.categories else "Umum",
                "rating": round(float(review_stats.avg_rating or 0), 1),
                "reviewCount": review_stats.count or 0,
                "latitude": dest.lat,
                "longitude": dest.lon
            })
        
        return {
            "destinations": destinations_data,
            "total": len(destinations_data),
            "offset": offset,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch destinations: {str(e)}")


@router.get("/destinations/{destination_id}")
async def get_destination_detail(
    destination_id: int,
    user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information for a specific destination.
    Automatically tracks view for incremental learning.
    """
    try:
        # Fetch destination with categories
        query = select(Destination).options(
            selectinload(Destination.categories)
        ).where(Destination.id == destination_id)
        
        result = await db.execute(query)
        destination = result.scalar_one_or_none()
        
        if not destination:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        # 🚀 AUTO LEARNING: Track view (non-blocking)
        from app.middleware.learning_middleware import track_destination_view
        import asyncio
        asyncio.create_task(
            track_destination_view(destination_id, user_id, db)
        )
        
        # Get review statistics
        review_stats_query = select(
            func.count(DestinationReview.id).label('count'),
            func.avg(DestinationReview.rating).label('avg_rating')
        ).where(DestinationReview.destination_id == destination_id)
        
        review_stats = await db.execute(review_stats_query)
        stats = review_stats.one()
        
        # Get recent reviews (limit 10)
        reviews_query = select(DestinationReview).where(
            DestinationReview.destination_id == destination_id
        ).order_by(desc(DestinationReview.created_at)).limit(10)
        
        reviews_result = await db.execute(reviews_query)
        reviews = reviews_result.scalars().all()
        
        return {
            "id": destination.id,
            "name": destination.name,
            "description": destination.description,
            "category": destination.categories[0].name if destination.categories else "Umum",
            "region": destination.address or "Sumedang",
            "image": f"/assets/images/{destination.name.lower().replace(' ', '-')}-hero.jpg",
            "rating": round(float(stats.avg_rating or 0), 1),
            "reviewCount": stats.count or 0,
            "ticketPrice": "Gratis",  # Placeholder - bisa ditambahkan ke model
            "openingHours": "24 Jam",  # Placeholder
            "latitude": destination.lat,
            "longitude": destination.lon,
            "address": destination.address,
            "highlights": [
                "Pemandangan indah",
                "Spot foto instagramable",
                "Akses mudah",
                "Fasilitas lengkap"
            ],  # Placeholder - bisa dari database
            "facilities": [
                "Area parkir",
                "Toilet umum",
                "Warung makan",
                "Musala"
            ],  # Placeholder
            "bestTime": {
                "season": "Musim Kemarau (April - Oktober)",
                "avoid": "Hindari saat musim hujan untuk keamanan",
                "recommendation": "Datang pagi hari untuk cuaca yang lebih sejuk"
            },
            "tips": [
                "Gunakan alas kaki yang nyaman",
                "Bawa air minum yang cukup",
                "Gunakan sunscreen dan topi",
                "Jaga kebersihan lingkungan"
            ],
            "gallery": [
                f"/assets/images/{destination.name.lower().replace(' ', '-')}-{i}.jpg" 
                for i in range(1, 7)
            ],
            "nearbyAttractions": [],  # TODO: Implement nearby logic
            "reviews": [
                {
                    "id": review.id,
                    "name": review.name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "date": review.created_at.strftime("%d %B %Y"),
                    "avatar": f"/assets/images/avatar-{(review.id % 4) + 1}.jpg"
                }
                for review in reviews
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch destination: {str(e)}")


@router.post("/destinations/{destination_id}/reviews")
async def create_destination_review(
    destination_id: int,
    review: ReviewCreate,
    user_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a review for a destination
    """
    try:
        # Check if destination exists
        dest = await db.get(Destination, destination_id)
        if not dest:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        # Create review
        new_review = DestinationReview(
            user_id=user_id,
            destination_id=destination_id,
            name=review.name,
            rating=review.rating,
            comment=review.comment
        )
        
        db.add(new_review)
        await db.commit()
        await db.refresh(new_review)
        
        # 🚀 AUTO LEARNING: Track rating + review
        from app.middleware.learning_middleware import track_rating_added, track_review_added
        import asyncio
        asyncio.create_task(
            track_rating_added(destination_id, user_id, review.rating, db)
        )
        asyncio.create_task(
            track_review_added(destination_id, user_id, db)
        )
        
        return {
            "message": "Review submitted successfully",
            "review": {
                "id": new_review.id,
                "name": new_review.name,
                "rating": new_review.rating,
                "comment": new_review.comment,
                "created_at": new_review.created_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit review: {str(e)}")


@router.get("/destinations/{destination_id}/reviews")
async def get_destination_reviews(
    destination_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get reviews for a specific destination
    """
    try:
        # Check if destination exists
        dest = await db.get(Destination, destination_id)
        if not dest:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        # Get reviews
        query = select(DestinationReview).where(
            DestinationReview.destination_id == destination_id
        ).order_by(desc(DestinationReview.created_at)).offset(offset).limit(limit)
        
        result = await db.execute(query)
        reviews = result.scalars().all()
        
        # Get total count
        count_query = select(func.count(DestinationReview.id)).where(
            DestinationReview.destination_id == destination_id
        )
        count_result = await db.execute(count_query)
        total_count = count_result.scalar()
        
        return {
            "reviews": [
                {
                    "id": review.id,
                    "name": review.name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "date": review.created_at.strftime("%d %B %Y"),
                    "avatar": f"/assets/images/avatar-{(review.id % 4) + 1}.jpg"
                }
                for review in reviews
            ],
            "total": total_count,
            "offset": offset,
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")


# ============== ACTIVITIES ENDPOINTS ==============

@router.get("/activities")
async def get_activities_list(
    category: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of activities with optional filters
    """
    try:
        query = select(Activity)
        
        # Apply filter
        if category:
            query = query.where(Activity.category.ilike(f"%{category}%"))
        
        # Add pagination
        query = query.offset(offset).limit(limit)
        
        result = await db.execute(query)
        activities = result.scalars().all()
        
        # Get review statistics for each activity
        activities_data = []
        for activity in activities:
            review_query = select(
                func.count(ActivityReview.id).label('count'),
                func.avg(ActivityReview.rating).label('avg_rating')
            ).where(ActivityReview.activity_id == activity.id)
            
            review_result = await db.execute(review_query)
            review_stats = review_result.one()
            
            activities_data.append({
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "image": activity.image_url or f"/assets/images/activity-{activity.id}.jpg",
                "category": activity.category or "Umum",
                "rating": round(float(review_stats.avg_rating or 0), 1),
                "reviewCount": review_stats.count or 0,
                "duration": activity.duration,
                "price": activity.price_range
            })
        
        return {
            "activities": activities_data,
            "total": len(activities_data),
            "offset": offset,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activities: {str(e)}")


@router.get("/activities/{activity_id}")
async def get_activity_detail(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information for a specific activity
    """
    try:
        activity = await db.get(Activity, activity_id)
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Get review statistics
        review_stats_query = select(
            func.count(ActivityReview.id).label('count'),
            func.avg(ActivityReview.rating).label('avg_rating')
        ).where(ActivityReview.activity_id == activity_id)
        
        review_stats = await db.execute(review_stats_query)
        stats = review_stats.one()
        
        # Get recent reviews
        reviews_query = select(ActivityReview).where(
            ActivityReview.activity_id == activity_id
        ).order_by(desc(ActivityReview.created_at)).limit(10)
        
        reviews_result = await db.execute(reviews_query)
        reviews = reviews_result.scalars().all()
        
        return {
            "id": activity.id,
            "name": activity.name,
            "category": activity.category or "Umum",
            "description": activity.description,
            "image": activity.image_url or f"/assets/images/activity-{activity.id}-hero.jpg",
            "rating": round(float(stats.avg_rating or 0), 1),
            "reviewCount": stats.count or 0,
            "duration": activity.duration or "2-3 jam",
            "price": activity.price_range or "Rp 50.000 - 150.000",
            "highlights": [
                "Pengalaman unik",
                "Pemandu profesional",
                "Dokumentasi gratis",
                "Fasilitas lengkap"
            ],  # Placeholder
            "included": [
                "Pemandu wisata",
                "Snack & air mineral",
                "Dokumentasi foto",
                "Transportasi lokal"
            ],  # Placeholder
            "gallery": [
                f"/assets/images/activity-{activity.id}-{i}.jpg" 
                for i in range(1, 7)
            ],
            "reviews": [
                {
                    "id": review.id,
                    "name": review.name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "date": review.created_at.strftime("%d %B %Y"),
                    "avatar": f"/assets/images/avatar-{(review.id % 4) + 1}.jpg"
                }
                for review in reviews
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activity: {str(e)}")


@router.post("/activities/{activity_id}/reviews")
async def create_activity_review(
    activity_id: int,
    review: ReviewCreate,
    user_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a review for an activity
    """
    try:
        # Check if activity exists
        activity = await db.get(Activity, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Create review
        new_review = ActivityReview(
            user_id=user_id,
            activity_id=activity_id,
            name=review.name,
            rating=review.rating,
            comment=review.comment
        )
        
        db.add(new_review)
        await db.commit()
        await db.refresh(new_review)
        
        return {
            "message": "Review submitted successfully",
            "review": {
                "id": new_review.id,
                "name": new_review.name,
                "rating": new_review.rating,
                "comment": new_review.comment,
                "created_at": new_review.created_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit review: {str(e)}")


@router.get("/activities/{activity_id}/reviews")
async def get_activity_reviews(
    activity_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get reviews for a specific activity
    """
    try:
        # Check if activity exists
        activity = await db.get(Activity, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Get reviews
        query = select(ActivityReview).where(
            ActivityReview.activity_id == activity_id
        ).order_by(desc(ActivityReview.created_at)).offset(offset).limit(limit)
        
        result = await db.execute(query)
        reviews = result.scalars().all()
        
        # Get total count
        count_query = select(func.count(ActivityReview.id)).where(
            ActivityReview.activity_id == activity_id
        )
        count_result = await db.execute(count_query)
        total_count = count_result.scalar()
        
        return {
            "reviews": [
                {
                    "id": review.id,
                    "name": review.name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "date": review.created_at.strftime("%d %B %Y"),
                    "avatar": f"/assets/images/avatar-{(review.id % 4) + 1}.jpg"
                }
                for review in reviews
            ],
            "total": total_count,
            "offset": offset,
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")


# ============== PERSONALIZED RECOMMENDATIONS ==============

@router.get("/recommendations/personalized")
async def get_personalized_recommendations(
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    limit: int = Query(6, alias="num_recommendations"),
    algorithm: str = "auto",  # auto, incremental, hybrid, context_only
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized recommendations for Home page.
    
    HYBRID APPROACH [UPDATED]:
    - "auto": Chooses best algorithm (Personalized Hybrid for login, Trending Hybrid for anonymous)
    - "hybrid": Research-grade ML (MAB + Context + MMR) - now works for EVERYONE
    - "incremental": Real-time learning only (updates fast but less smart)
    """
    try:
        from app.services.incremental_learner import incremental_learner
        from app.services.ml_service import ml_service
        
        # AUTO MODE: Determine strategy
        if algorithm == "auto":
            model_status = ml_service.get_models_status()
            
            # Cek apakah model hybrid siap (sudah ditraining)
            is_hybrid_ready = model_status.get('training_status', {}).get('hybrid')
            
            if is_hybrid_ready:
                # [UPDATED] Gunakan Hybrid untuk SEMUA (User Login & Anonymous)
                algorithm = "hybrid"
                if user_id:
                    print(f"🎯 AUTO (logged-in): Using Personalized Hybrid MAB")
                else:
                    print(f"🌍 AUTO (anonymous): Using Trending Hybrid MAB")
            else:
                # Fallback jika model belum dilatih
                algorithm = "popular_fallback"
                print(f"⚠️ AUTO: Hybrid model not ready, using Popular fallback")

        # STRATEGY 1: INCREMENTAL LEARNING (Manual override)
        if algorithm == "incremental":
            trending = await incremental_learner.get_trending_destinations(
                limit=limit * 5,
                time_window_hours=168,
                db=db
            )
            algorithm_used = "incremental_learning"

        # STRATEGY 2: CONTEXT-ONLY (Legacy)
        elif algorithm == "context_only":
            # ... (kode lama dipertahankan untuk backward compatibility)
            try:
                ml_result = await ml_service.get_recommendations(
                    user_id=None,
                    algorithm="context_only",
                    num_recommendations=limit,
                    db=db
                )
                ml_recommendations = ml_result[0]
                trending = ml_recommendations
                algorithm_used = "context_only"
            except Exception as e:
                trending = []
                algorithm_used = "popular_fallback"

        # STRATEGY 3: HYBRID MAB (Research ML - THE CORE)
        # [PERBAIKAN UTAMA] Hapus 'and user_id is not None' agar Anonymous bisa masuk
        elif algorithm in ["hybrid", "mab"]: 
            try:
                ml_result = await ml_service.get_recommendations(
                    user_id=user_id, # Bisa None (untuk anonymous)
                    algorithm="hybrid",
                    num_recommendations=limit,
                    db=db
                )
                ml_recommendations = ml_result[0]
                trending = ml_recommendations
                
                # Cek apakah benar-benar personalized atau trending fallback
                if user_id:
                    algorithm_used = "hybrid_mab_personalized"
                else:
                    algorithm_used = "hybrid_mab_trending"
                    
                print(f"✅ Using Hybrid MAB ({algorithm_used})")
            except Exception as e:
                print(f"⚠️ Hybrid model failed: {e}")
                # Fallback ke incremental jika ML gagal
                trending = await incremental_learner.get_trending_destinations(limit=limit, db=db)
                algorithm_used = "incremental_fallback"

        else:
            # Default fallback
            trending = []
            algorithm_used = "popular_fallback"
        
        # --- (Bagian bawah sama: Fallback logic & Response Formatting) ---
        
        # If trending is empty or smaller than requested, fetch popular destinations from DB
        if not trending or len(trending) < limit:
            query = select(
                Destination.id,
                Destination.name,
                Destination.description,
                Destination.address,
                func.avg(DestinationReview.rating).label('avg_rating'),
                func.count(DestinationReview.id).label('review_count')
            ).outerjoin(DestinationReview).group_by(
                Destination.id,
                Destination.name,
                Destination.description,
                Destination.address
            ).order_by(
                desc('avg_rating'),
                desc('review_count')
            ).limit(max(limit, 50))
            
            result = await db.execute(query)
            destinations_data = result.all()

            # Convert to consistent format
            popular_list = [
                {
                    'destination_id': d.id,
                    'popularity_score': float(d.avg_rating or 0) * (d.review_count or 0),
                    'avg_rating': float(d.avg_rating or 0),
                    'interaction_count': d.review_count or 0
                }
                for d in destinations_data
            ]

            # Merge results
            existing_ids = set([int(x.get('destination_id', 0)) for x in (trending or [])])
            merged = list(trending or [])
            for p in popular_list:
                if int(p['destination_id']) not in existing_ids:
                    merged.append(p)
                    existing_ids.add(int(p['destination_id']))
                if len(merged) >= limit:
                    break
            trending = merged

        # Get full details for final response
        recommendations = []
        for item in trending[:limit]:
            # Handle beda format (objek vs dict)
            dest_id = item.get('destination_id') if isinstance(item, dict) else getattr(item, 'destination_id', None)
            
            if not dest_id: continue

            dest_query = select(Destination).where(Destination.id == dest_id)
            dest_result = await db.execute(dest_query)
            dest = dest_result.scalar_one_or_none()
            
            if not dest: continue
            
            # Get category
            cat_query = select(Category).join(
                Destination.categories
            ).where(Destination.id == dest.id).limit(1)
            cat_result = await db.execute(cat_query)
            category = cat_result.scalar_one_or_none()
            
            # Get Context/Algorithm info if available
            algo_info = item.get('algorithm', 'popular') if isinstance(item, dict) else 'popular'
            explanation = item.get('explanation', '') if isinstance(item, dict) else ''

            recommendations.append({
                "id": dest.id,
                "name": dest.name,
                "image": f"/assets/images/{dest.name.lower().replace(' ', '-')}.jpg",
                "description": dest.description or "Destinasi wisata menarik di Sumedang",
                "region": dest.address or "Sumedang",
                "category": category.name if category else "Alam",
                "rating": round(float(item.get('avg_rating', 0) if item.get('avg_rating') else 0), 1),
                "reviewCount": item.get('interaction_count', 0),
                "algorithm": algo_info,
                "explanation": explanation
            })
        
        # Build Context Info for Frontend Debugging
        context_info = None
        if 'ml_result' in locals() and isinstance(ml_result, tuple) and len(ml_result) > 2:
            context_info = ml_result[2]

        return {
            "recommendations": recommendations,
            "algorithm": algorithm_used,
            "message": f"Recommendations powered by {algorithm_used}",
            "info": {
                "mode": algorithm,
                "is_personalized": user_id is not None,
                "context_active": context_info is not None
            },
            "context": context_info
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


# ============== USER INTERACTIONS ==============

@router.post("/interactions/click")
async def track_click(
    interaction: InteractionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Track user click on destination/activity card
    """
    try:
        new_interaction = UserInteraction(
            user_id=interaction.user_id,
            session_id=interaction.session_id,
            interaction_type='click',
            entity_type=interaction.entity_type,
            entity_id=interaction.entity_id,
            extra_data=interaction.extra_data
        )
        
        db.add(new_interaction)
        await db.commit()
        
        return {
            "message": "Click tracked successfully",
            "interaction_id": new_interaction.id
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to track click: {str(e)}")


@router.post("/interactions/view")
async def track_view(
    interaction: InteractionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Track user page view with duration
    """
    try:
        new_interaction = UserInteraction(
            user_id=interaction.user_id,
            session_id=interaction.session_id,
            interaction_type='view',
            entity_type=interaction.entity_type,
            entity_id=interaction.entity_id,
            duration=interaction.duration,
            extra_data=interaction.extra_data
        )
        
        db.add(new_interaction)
        await db.commit()
        
        return {
            "message": "View tracked successfully",
            "interaction_id": new_interaction.id
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to track view: {str(e)}")


@router.get("/interactions/user/{user_id}")
async def get_user_interactions(
    user_id: int,
    interaction_type: Optional[str] = None,
    entity_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user interaction history
    """
    try:
        query = select(UserInteraction).where(UserInteraction.user_id == user_id)
        
        if interaction_type:
            query = query.where(UserInteraction.interaction_type == interaction_type)
        
        if entity_type:
            query = query.where(UserInteraction.entity_type == entity_type)
        
        query = query.order_by(desc(UserInteraction.created_at)).limit(limit)
        
        result = await db.execute(query)
        interactions = result.scalars().all()
        
        return {
            "interactions": [
                {
                    "id": inter.id,
                    "interaction_type": inter.interaction_type,
                    "entity_type": inter.entity_type,
                    "entity_id": inter.entity_id,
                    "duration": inter.duration,
                    "created_at": inter.created_at
                }
                for inter in interactions
            ],
            "total": len(interactions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch interactions: {str(e)}")