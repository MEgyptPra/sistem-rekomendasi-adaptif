import asyncio
import random
from sqlalchemy.future import select
from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.destinations import Destination
from app.models.category import Category
from app.models.rating import Rating

async def seed_test_data():
    """Seed test data untuk testing ML algorithms"""
    async with AsyncSessionLocal() as session:
        print("🌱 Seeding test data...")
        
        # Check if data already exists
        existing_users = await session.execute(select(User))
        if len(existing_users.scalars().all()) > 0:
            print("❌ Data already exists. Skipping seeding.")
            return
        
        # Create test users
        test_users = [
            User(name="Alice Johnson", preferences="alam,petualangan,hiking", email="alice@test.com"),
            User(name="Bob Smith", preferences="kuliner,budaya,sejarah", email="bob@test.com"),
            User(name="Carol Davis", preferences="pantai,relaksasi,fotografi", email="carol@test.com"),
            User(name="David Wilson", preferences="alam,wildlife,petualangan", email="david@test.com"),
            User(name="Eva Brown", preferences="budaya,seni,museum", email="eva@test.com"),
        ]
        
        for user in test_users:
            session.add(user)
        
        await session.commit()
        print(f"✅ Created {len(test_users)} test users")
        
        # Create test categories
        test_categories = [
            Category(name="alam", description="Destinasi alam dan outdoor"),
            Category(name="kuliner", description="Destinasi kuliner dan gastronomi"),
            Category(name="budaya", description="Destinasi budaya dan sejarah"),
            Category(name="pantai", description="Destinasi pantai dan air"),
            Category(name="petualangan", description="Destinasi adventure dan extreme"),
            Category(name="relaksasi", description="Destinasi spa dan wellness"),
            Category(name="fotografi", description="Spot foto dan pemandangan"),
        ]
        
        for category in test_categories:
            session.add(category)
        
        await session.commit()
        print(f"✅ Created {len(test_categories)} categories")
        
        # Create test destinations
        test_destinations = [
            Destination(name="Gunung Bromo", description="Gunung berapi aktif dengan pemandangan sunrise spektakuler", lat=-7.942, lon=112.953, address="Jawa Timur"),
            Destination(name="Pantai Kuta", description="Pantai terkenal dengan ombak untuk surfing", lat=-8.718, lon=115.169, address="Bali"),
            Destination(name="Candi Borobudur", description="Candi Buddha terbesar di dunia", lat=-7.608, lon=110.204, address="Yogyakarta"),
            Destination(name="Danau Toba", description="Danau vulkanik terbesar di Indonesia", lat=2.686, lon=98.875, address="Sumatera Utara"),
            Destination(name="Raja Ampat", description="Surga diving dengan biodiversitas laut tertinggi", lat=-0.339, lon=130.826, address="Papua Barat"),
            Destination(name="Taman Nasional Komodo", description="Habitat asli komodo dan diving world-class", lat=-8.553, lon=119.489, address="NTT"),
            Destination(name="Kawah Ijen", description="Kawah dengan blue fire phenomenon", lat=-8.058, lon=114.242, address="Jawa Timur"),
            Destination(name="Ubud", description="Pusat seni dan budaya Bali", lat=-8.520, lon=115.264, address="Bali"),
        ]
        
        for destination in test_destinations:
            session.add(destination)
        
        await session.commit()
        print(f"✅ Created {len(test_destinations)} destinations")
        
        # Assign categories to destinations
        await session.refresh(test_categories[0])  # alam
        await session.refresh(test_categories[1])  # kuliner  
        await session.refresh(test_categories[2])  # budaya
        await session.refresh(test_categories[3])  # pantai
        await session.refresh(test_categories[4])  # petualangan
        await session.refresh(test_categories[5])  # relaksasi
        await session.refresh(test_categories[6])  # fotografi
        
        # Refresh destinations
        for dest in test_destinations:
            await session.refresh(dest)
        
        # Assign categories
        category_assignments = [
            (test_destinations[0], [test_categories[0], test_categories[4], test_categories[6]]),  # Bromo: alam, petualangan, fotografi
            (test_destinations[1], [test_categories[3], test_categories[5]]),  # Kuta: pantai, relaksasi
            (test_destinations[2], [test_categories[2], test_categories[6]]),  # Borobudur: budaya, fotografi
            (test_destinations[3], [test_categories[0], test_categories[5]]),  # Toba: alam, relaksasi
            (test_destinations[4], [test_categories[0], test_categories[4]]),  # Raja Ampat: alam, petualangan
            (test_destinations[5], [test_categories[0], test_categories[4]]),  # Komodo: alam, petualangan
            (test_destinations[6], [test_categories[0], test_categories[4], test_categories[6]]),  # Ijen: alam, petualangan, fotografi
            (test_destinations[7], [test_categories[2], test_categories[5]]),  # Ubud: budaya, relaksasi
        ]
        
        for destination, categories in category_assignments:
            for category in categories:
                destination.categories.append(category)
        
        await session.commit()
        print("✅ Assigned categories to destinations")
        
        # Create test ratings
        users_list = await session.execute(select(User))
        destinations_list = await session.execute(select(Destination))
        
        users = users_list.scalars().all()
        destinations = destinations_list.scalars().all()
        
        # Generate realistic ratings based on user preferences
        test_ratings = []
        
        for user in users:
            user_prefs = user.preferences.split(',') if user.preferences else []
            
            # Rate 60% of destinations
            num_ratings = int(len(destinations) * 0.6)
            selected_destinations = random.sample(destinations, num_ratings)
            
            for destination in selected_destinations:
                dest_categories = [cat.name for cat in destination.categories]
                
                # Higher rating if destination matches user preferences
                if any(pref.strip() in dest_categories for pref in user_prefs):
                    # User likes this type - rate 3.5-5.0
                    rating = random.uniform(3.5, 5.0)
                else:
                    # Neutral/mixed rating - 2.0-4.0
                    rating = random.uniform(2.0, 4.0)
                
                test_ratings.append(Rating(
                    user_id=user.id,
                    destination_id=destination.id,
                    rating=round(rating, 1)
                ))
        
        for rating in test_ratings:
            session.add(rating)
        
        await session.commit()
        print(f"✅ Created {len(test_ratings)} test ratings")
        
        print("🎉 Test data seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_test_data())