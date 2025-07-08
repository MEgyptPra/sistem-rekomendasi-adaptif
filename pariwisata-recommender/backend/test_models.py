import asyncio
from sqlalchemy.future import select
from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.destination import Destination
from app.models.category import Category

async def test_models():
    """Test if models work correctly"""
    async with AsyncSessionLocal() as session:
        # Test select users
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Found {len(users)} users")
        
        # Test select destinations
        result = await session.execute(select(Destination))
        destinations = result.scalars().all()
        print(f"Found {len(destinations)} destinations")
        
        # Test select categories
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        print(f"Found {len(categories)} categories")
        
        print("All models working correctly!")

if __name__ == "__main__":
    asyncio.run(test_models())