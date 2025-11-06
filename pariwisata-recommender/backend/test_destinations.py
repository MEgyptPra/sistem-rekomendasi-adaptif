import asyncio
import traceback
from app.core.db import get_db
from app.models.destinations import Destination
from app.models.destination_review import DestinationReview
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

async def test_destinations():
    try:
        async for db in get_db():
            # Test 1: Simple query
            print("Test 1: Simple query...")
            result = await db.execute(select(Destination).limit(5))
            dests = result.scalars().all()
            print(f"✓ Found {len(dests)} destinations")
            
            # Test 2: Query with categories
            print("\nTest 2: Query with categories...")
            result = await db.execute(
                select(Destination).options(selectinload(Destination.categories)).limit(5)
            )
            dests = result.scalars().unique().all()
            print(f"✓ Found {len(dests)} destinations with categories")
            
            # Test 3: Query with review stats
            print("\nTest 3: Query with review stats...")
            for dest in dests[:2]:
                review_query = select(
                    func.count(DestinationReview.id).label('count'),
                    func.avg(DestinationReview.rating).label('avg_rating')
                ).where(DestinationReview.destination_id == dest.id)
                
                review_result = await db.execute(review_query)
                review_stats = review_result.one()
                print(f"  - {dest.name}: {review_stats.count} reviews, avg {review_stats.avg_rating}")
            
            print("\n✅ All tests passed!")
            break
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_destinations())
