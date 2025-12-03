"""Quick script to check data counts in database"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select, func
from app.core.db import get_db
from app.models.rating import Rating
from app.models.user_interaction import UserInteraction
from app.models.review import Review
from app.models.destinations import Destination
from app.models.user import User

async def check_counts():
    async for db in get_db():
        # Count ratings
        result = await db.execute(select(func.count(Rating.id)))
        rating_count = result.scalar()
        
        # Count user interactions
        result = await db.execute(select(func.count(UserInteraction.id)))
        interaction_count = result.scalar()
        
        # Count reviews
        result = await db.execute(select(func.count(Review.id)))
        review_count = result.scalar()
        
        # Count destinations
        result = await db.execute(select(func.count(Destination.id)))
        destination_count = result.scalar()
        
        # Count users
        result = await db.execute(select(func.count(User.id)))
        user_count = result.scalar()
        
        print("="*50)
        print("📊 DATABASE DATA COUNTS")
        print("="*50)
        print(f"Users:              {user_count:,}")
        print(f"Destinations:       {destination_count:,}")
        print(f"Reviews:            {review_count:,}")
        print(f"Ratings:            {rating_count:,}")
        print(f"User Interactions:  {interaction_count:,}")
        print("="*50)
        print(f"TOTAL INTERACTIONS: {rating_count + interaction_count:,}")
        print("="*50)
        
        break

if __name__ == "__main__":
    asyncio.run(check_counts())
