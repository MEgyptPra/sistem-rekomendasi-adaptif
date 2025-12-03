"""
Database initialization script
Creates all tables and optionally seeds initial data
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import DATABASE_URL
from app.models import Base
from app.core.db import engine

# Import all models to ensure they're registered with Base.metadata
from app.models.category import Category
from app.models.destinations import Destination
from app.models.rating import Rating
from app.models.review import Review
from app.models.user import User
from app.models.activity import Activity
from app.models.activity_review import ActivityReview
from app.models.destination_review import DestinationReview
from app.models.user_interaction import UserInteraction
from app.models.itinerary import Itinerary, ItineraryDay, ItineraryItem
from app.models.realtime_api_config import RealtimeAPIConfig


async def init_database():
    """Initialize database by creating all tables"""
    print("🔧 Initializing database...")
    print(f"📍 Database URL: {DATABASE_URL}")
    
    async with engine.begin() as conn:
        print("🗑️  Dropping existing tables...")
        await conn.run_sync(Base.metadata.drop_all)
        
        print("🏗️  Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database initialized successfully!")
    print("\n📋 Created tables:")
    for table in Base.metadata.sorted_tables:
        print(f"   - {table.name}")


async def seed_initial_data():
    """Seed initial data for testing"""
    from app.core.db import AsyncSessionLocal
    
    print("\n🌱 Seeding initial data...")
    
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        from sqlalchemy import select
        result = await session.execute(select(Category))
        if result.scalars().first():
            print("⚠️  Data already exists, skipping seed...")
            return
        
        # Create categories
        categories = [
            Category(name="Alam", description="Destinasi wisata alam seperti pantai, gunung, dan taman"),
            Category(name="Budaya", description="Destinasi wisata budaya dan sejarah"),
            Category(name="Kuliner", description="Tempat wisata kuliner dan restoran"),
            Category(name="Religi", description="Tempat wisata religi dan spiritual"),
            Category(name="Hiburan", description="Taman hiburan dan rekreasi"),
        ]
        session.add_all(categories)
        
        # Create sample users
        sample_users = [
            User(
                name="Test User 1",
                email="test1@example.com",
                preferences="Alam,Budaya"
            ),
            User(
                name="Test User 2",
                email="test2@example.com",
                preferences="Kuliner,Hiburan"
            ),
        ]
        session.add_all(sample_users)
        
        await session.commit()
        print("✅ Initial data seeded successfully!")


async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize database")
    parser.add_argument("--seed", action="store_true", help="Seed initial data after creating tables")
    args = parser.parse_args()
    
    try:
        await init_database()
        
        if args.seed:
            await seed_initial_data()
        
        print("\n🎉 Database setup complete!")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
