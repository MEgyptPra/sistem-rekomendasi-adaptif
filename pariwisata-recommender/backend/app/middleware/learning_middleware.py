"""
Learning Middleware
Automatically triggers incremental learning on relevant events
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
import asyncio
from typing import Callable

from app.services.incremental_learner import incremental_learner


class IncrementalLearningMiddleware(BaseHTTPMiddleware):
    """
    Middleware that triggers incremental learning updates
    automatically based on user interactions.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Only process successful requests
        if response.status_code >= 200 and response.status_code < 300:
            # Background task untuk update (non-blocking)
            asyncio.create_task(
                self._process_learning_update(request, response)
            )
        
        return response
    
    async def _process_learning_update(self, request: Request, response: Response):
        """
        Process learning updates in background.
        Doesn't block the main response.
        """
        try:
            path = request.url.path
            method = request.method
            
            # Get user_id from request if available
            user_id = None
            if hasattr(request.state, 'user'):
                user_id = request.state.user.id
            
            # Detect interaction patterns
            
            # 1. View destination (GET /api/destinations/:id)
            if method == "GET" and "/api/destinations/" in path and path.count('/') == 3:
                dest_id = int(path.split('/')[-1])
                db = request.state.db if hasattr(request.state, 'db') else None
                if db:
                    await incremental_learner.update_from_interaction(
                        user_id=user_id,
                        destination_id=dest_id,
                        interaction_type='view',
                        db=db
                    )
            
            # 2. Add rating (POST /api/ratings)
            elif method == "POST" and "/api/ratings" in path:
                # Request body already consumed, would need custom handling
                # Better to explicitly call in the endpoint itself
                pass
            
            # 3. Add to favorites (POST /api/favorites)
            elif method == "POST" and "/api/favorites" in path:
                # Handle in endpoint
                pass
            
        except Exception as e:
            # Silent fail - don't break the application
            print(f"⚠️  Incremental learning update failed: {e}")


# Helper functions to be called explicitly in endpoints

async def track_destination_view(destination_id: int, user_id: int = None, db = None):
    """Call this in destination detail endpoint"""
    try:
        await incremental_learner.update_from_interaction(
            user_id=user_id,
            destination_id=destination_id,
            interaction_type='view',
            db=db
        )
    except Exception as e:
        print(f"⚠️  Failed to track view: {e}")


async def track_rating_added(destination_id: int, user_id: int, rating: float, db):
    """Call this after rating is saved"""
    try:
        await incremental_learner.update_from_rating(
            user_id=user_id,
            destination_id=destination_id,
            rating=rating,
            db=db
        )
    except Exception as e:
        print(f"⚠️  Failed to track rating: {e}")


async def track_favorite_added(destination_id: int, user_id: int, db):
    """Call this after favorite is added"""
    try:
        await incremental_learner.update_from_interaction(
            user_id=user_id,
            destination_id=destination_id,
            interaction_type='favorite',
            db=db
        )
    except Exception as e:
        print(f"⚠️  Failed to track favorite: {e}")


async def track_review_added(destination_id: int, user_id: int, db):
    """Call this after review is posted"""
    try:
        await incremental_learner.update_from_interaction(
            user_id=user_id,
            destination_id=destination_id,
            interaction_type='review',
            db=db
        )
    except Exception as e:
        print(f"⚠️  Failed to track review: {e}")
