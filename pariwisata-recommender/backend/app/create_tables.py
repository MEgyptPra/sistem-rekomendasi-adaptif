import asyncio
from app.core.db import engine
from app.models import Base

async def create_tables():
    """Create all tables based on models"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())