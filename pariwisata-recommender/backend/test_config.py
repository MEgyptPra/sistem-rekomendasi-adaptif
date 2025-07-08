#!/usr/bin/env python3
"""
Test configuration for ML recommendation system
Uses SQLite database for simple testing without requiring PostgreSQL
"""

import asyncio
import random
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///test_pariwisata.db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

async def create_test_tables():
    """Create all tables for testing"""
    from app.models import Base
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_test_data():
    """Seed test data untuk testing ML algorithms"""
    async with TestAsyncSessionLocal() as session:
        print("🌱 Seeding test data...")
        
        # Import models after engine is ready
        from app.models.user import User
        from app.models.destinations import Destination
        from app.models.category import Category
        from app.models.rating import Rating
        from sqlalchemy.future import select
        
        # Check if data already exists
        existing_users = await session.execute(select(User))
        if len(existing_users.scalars().all()) > 0:
            print("❌ Data already exists. Skipping seeding.")
            return
        
        # Create test categories
        test_categories = [
            Category(name="Alam", description="Destinasi alam dan outdoor"),
            Category(name="Kuliner", description="Tempat makan dan kuliner khas"),
            Category(name="Budaya", description="Situs budaya dan sejarah"),
            Category(name="Pantai", description="Destinasi pantai dan air"),
            Category(name="Petualangan", description="Aktivitas petualangan"),
            Category(name="Museum", description="Museum dan galeri"),
            Category(name="Relaksasi", description="Tempat untuk relaksasi"),
        ]
        
        for category in test_categories:
            session.add(category)
        await session.commit()
        
        # Get categories for relationships
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        category_map = {cat.name: cat for cat in categories}
        
        # Create test destinations
        test_destinations = [
            {
                "name": "Gunung Bromo",
                "description": "Gunung berapi aktif dengan pemandangan sunrise yang menakjubkan",
                "lat": -7.9425,
                "lon": 112.9530,
                "address": "Jawa Timur",
                "categories": ["Alam", "Petualangan"]
            },
            {
                "name": "Borobudur",
                "description": "Candi Buddha terbesar di dunia dengan arsitektur yang memukau",
                "lat": -7.6079,
                "lon": 110.2038,
                "address": "Yogyakarta",
                "categories": ["Budaya", "Museum"]
            },
            {
                "name": "Pantai Kuta",
                "description": "Pantai terkenal dengan ombak yang bagus untuk surfing",
                "lat": -8.7184,
                "lon": 115.1686,
                "address": "Bali",
                "categories": ["Pantai", "Relaksasi"]
            },
            {
                "name": "Gudeg Yu Djum",
                "description": "Restoran gudeg tradisional Yogyakarta yang terkenal",
                "lat": -7.7956,
                "lon": 110.3695,
                "address": "Yogyakarta",
                "categories": ["Kuliner"]
            },
            {
                "name": "Taman Nasional Komodo",
                "description": "Habitat asli komodo dengan pemandangan alam yang eksotis",
                "lat": -8.5500,
                "lon": 119.4833,
                "address": "Nusa Tenggara Timur",
                "categories": ["Alam", "Petualangan"]
            },
            {
                "name": "Ubud Monkey Forest",
                "description": "Hutan suci dengan monyet dan temple tradisional Bali",
                "lat": -8.5205,
                "lon": 115.2580,
                "address": "Bali",
                "categories": ["Alam", "Budaya"]
            },
            {
                "name": "Malioboro Street",
                "description": "Jalan utama Yogyakarta dengan kuliner dan oleh-oleh",
                "lat": -7.7924,
                "lon": 110.3652,
                "address": "Yogyakarta",
                "categories": ["Kuliner", "Budaya"]
            },
            {
                "name": "Raja Ampat",
                "description": "Surga diving dengan keanekaragaman hayati laut terbaik dunia",
                "lat": -0.2317,
                "lon": 130.5169,
                "address": "Papua Barat",
                "categories": ["Alam", "Petualangan"]
            }
        ]
        
        destinations = []
        for dest_data in test_destinations:
            dest = Destination(
                name=dest_data["name"],
                description=dest_data["description"],
                lat=dest_data["lat"],
                lon=dest_data["lon"],
                address=dest_data["address"]
            )
            # Add categories
            for cat_name in dest_data["categories"]:
                if cat_name in category_map:
                    dest.categories.append(category_map[cat_name])
            
            session.add(dest)
            destinations.append(dest)
        
        await session.commit()
        
        # Create test users
        test_users = [
            User(name="Alice Johnson", preferences="Alam,Petualangan", email="alice@test.com"),
            User(name="Bob Smith", preferences="Kuliner,Budaya", email="bob@test.com"),
            User(name="Carol Davis", preferences="Pantai,Relaksasi", email="carol@test.com"),
            User(name="David Wilson", preferences="Alam,Petualangan", email="david@test.com"),
            User(name="Eva Brown", preferences="Budaya,Museum", email="eva@test.com"),
        ]
        
        for user in test_users:
            session.add(user)
        await session.commit()
        
        # Get users and destinations for ratings
        users_result = await session.execute(select(User))
        users = users_result.scalars().all()
        
        dest_result = await session.execute(select(Destination))
        destinations = dest_result.scalars().all()
        
        # Create realistic ratings based on user preferences
        ratings_data = []
        preference_mapping = {
            "Alice Johnson": {"Alam": 5, "Petualangan": 5, "Pantai": 4, "Budaya": 3, "Kuliner": 3},
            "Bob Smith": {"Kuliner": 5, "Budaya": 5, "Museum": 4, "Alam": 3, "Pantai": 2},
            "Carol Davis": {"Pantai": 5, "Relaksasi": 5, "Alam": 4, "Kuliner": 4, "Budaya": 3},
            "David Wilson": {"Alam": 5, "Petualangan": 5, "Budaya": 4, "Pantai": 3, "Kuliner": 3},
            "Eva Brown": {"Budaya": 5, "Museum": 5, "Kuliner": 4, "Alam": 3, "Pantai": 2}
        }
        
        for user in users:
            user_prefs = preference_mapping.get(user.name, {})
            for dest in destinations:
                # Calculate rating based on destination categories and user preferences
                dest_categories = [cat.name for cat in dest.categories]
                base_rating = 3.0  # neutral
                
                for cat in dest_categories:
                    if cat in user_prefs:
                        base_rating = max(base_rating, user_prefs[cat])
                
                # Add some randomness (70% chance to rate, with slight variation)
                if random.random() < 0.7:
                    rating_value = base_rating + random.uniform(-0.5, 0.5)
                    rating_value = max(1.0, min(5.0, rating_value))  # Clamp to 1-5 range
                    
                    rating = Rating(
                        user_id=user.id,
                        destination_id=dest.id,
                        rating=round(rating_value, 1)
                    )
                    session.add(rating)
        
        await session.commit()
        
        # Print statistics
        users_count = len(users)
        dest_count = len(destinations)
        
        ratings_result = await session.execute(select(Rating))
        ratings_count = len(ratings_result.scalars().all())
        
        print(f"✅ Test data seeded successfully:")
        print(f"   - Users: {users_count}")
        print(f"   - Categories: {len(categories)}")
        print(f"   - Destinations: {dest_count}")
        print(f"   - Ratings: {ratings_count}")

async def test_ml_system():
    """Test the complete ML recommendation system"""
    from app.services.ml_service import ml_service
    from app.models.user import User
    from app.models.destinations import Destination
    from app.models.rating import Rating
    from sqlalchemy.future import select
    import json
    
    async with TestAsyncSessionLocal() as session:
        print("\n🧪 Testing ML Recommendation System...")
        
        # 1. Check data availability
        print("\n📊 Checking data availability...")
        
        users = await session.execute(select(User))
        user_count = len(users.scalars().all())
        print(f"Users: {user_count}")
        
        destinations = await session.execute(select(Destination))
        dest_count = len(destinations.scalars().all())
        print(f"Destinations: {dest_count}")
        
        ratings = await session.execute(select(Rating))
        rating_count = len(ratings.scalars().all())
        print(f"Ratings: {rating_count}")
        
        if user_count == 0 or dest_count == 0:
            print("❌ No data found. Please run seed_test_data first.")
            return
        
        # 2. Train models
        print("\n🚀 Training ML models...")
        try:
            training_results = await ml_service.train_all_models(session)
            print("Training Results:")
            print(json.dumps(training_results, indent=2))
        except Exception as e:
            print(f"Training error: {e}")
            return
        
        # 3. Test recommendations
        print("\n🎯 Testing recommendations...")
        
        # Get first user for testing
        first_user = await session.execute(select(User).limit(1))
        user = first_user.scalar_one_or_none()
        
        if user:
            print(f"Testing recommendations for User: {user.name} (ID: {user.id})")
            
            # Test all algorithms
            algorithms = ['content_based', 'collaborative', 'hybrid']
            
            for algorithm in algorithms:
                try:
                    print(f"\n--- {algorithm.upper()} RECOMMENDATIONS ---")
                    recs = await ml_service.get_recommendations(
                        user_id=user.id,
                        algorithm=algorithm,
                        num_recommendations=5,
                        db=session
                    )
                    
                    if recs:
                        for i, rec in enumerate(recs, 1):
                            print(f"{i}. {rec['name']} (Score: {rec['score']:.3f}) - {rec['explanation']}")
                    else:
                        print("No recommendations generated")
                        
                except Exception as e:
                    print(f"Error with {algorithm}: {e}")
        
        # 4. Test user profile
        if user:
            print(f"\n👤 User Profile for {user.name} (ID {user.id}):")
            try:
                profile = await ml_service.get_user_profile(user.id, session)
                print(json.dumps(profile, indent=2, default=str))
            except Exception as e:
                print(f"Profile error: {e}")
        
        # 5. Models status
        print("\n📈 Models Status:")
        status = ml_service.get_models_status()
        print(json.dumps(status, indent=2))
        
        print("\n✅ ML System testing completed!")

async def main():
    """Main function to setup and test the ML system"""
    print("🔧 Setting up ML Recommendation System Test Environment...")
    
    # Install required dependency for SQLite
    import subprocess
    import sys
    
    try:
        import aiosqlite
    except ImportError:
        print("Installing aiosqlite for testing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiosqlite", "--no-cache-dir"])
        import aiosqlite
    
    # Create tables
    await create_test_tables()
    print("✅ Test tables created")
    
    # Seed data
    await seed_test_data()
    
    # Test ML system
    await test_ml_system()

if __name__ == "__main__":
    asyncio.run(main())