"""
Script to seed sample tourism data for testing
"""
import asyncio
import json
from datetime import datetime
from sqlalchemy import select
from app.core.db import get_db
from app.models.destinations import Destination
from app.models.activity import Activity
from app.models.user import User
from app.models.user_interaction import UserInteraction
from app.models.rating import Rating

# Sample destinations data (simplified to match model)
SAMPLE_DESTINATIONS = [
    {
        "name": "Candi Borobudur",
        "description": "Candi Buddha terbesar di dunia, warisan UNESCO yang terletak di Magelang, Jawa Tengah. Dibangun pada abad ke-9 dengan 504 arca Buddha dan 2672 panel relief.",
        "lat": -7.6079,
        "lon": 110.2038,
        "address": "Borobudur, Magelang, Jawa Tengah"
    },
    {
        "name": "Pantai Kuta",
        "description": "Pantai legendaris di Bali dengan pasir putih dan sunset yang menakjubkan. Surga peselancar dan tempat favorit wisatawan.",
        "lat": -8.7184,
        "lon": 115.1686,
        "address": "Kuta, Badung, Bali"
    },
    {
        "name": "Gunung Bromo",
        "description": "Gunung berapi aktif dengan pemandangan sunrise spektakuler di Taman Nasional Bromo Tengger Semeru, Jawa Timur.",
        "lat": -7.9425,
        "lon": 112.9531,
        "address": "Probolinggo, Jawa Timur"
    },
    {
        "name": "Taman Mini Indonesia Indah",
        "description": "Miniatur kebudayaan Indonesia dengan rumah adat dari 34 provinsi, museum, dan taman rekreasi di Jakarta.",
        "lat": -6.3025,
        "lon": 106.8952,
        "address": "Jakarta Timur, DKI Jakarta"
    },
    {
        "name": "Raja Ampat",
        "description": "Surga diving terbaik di dunia dengan keanekaragaman hayati laut tertinggi. Kepulauan eksotis di Papua Barat.",
        "lat": -0.2354,
        "lon": 130.5203,
        "address": "Raja Ampat, Papua Barat"
    },
    {
        "name": "Kawah Ijen",
        "description": "Kawah vulkanik dengan blue fire phenomenon dan danau kawah berwarna hijau tosca di Banyuwangi, Jawa Timur.",
        "lat": -8.0583,
        "lon": 114.2425,
        "address": "Banyuwangi, Jawa Timur"
    },
    {
        "name": "Ubud",
        "description": "Pusat seni dan budaya Bali dengan sawah terasering, monkey forest, dan galeri seni tradisional.",
        "lat": -8.5069,
        "lon": 115.2625,
        "address": "Ubud, Gianyar, Bali"
    },
    {
        "name": "Danau Toba",
        "description": "Danau vulkanik terbesar di Asia Tenggara dengan Pulau Samosir di tengahnya. Keindahan alam dan budaya Batak.",
        "lat": 2.6845,
        "lon": 98.8756,
        "address": "Sumatera Utara"
    },
    {
        "name": "Tanah Lot",
        "description": "Pura Hindu di atas batu karang dengan pemandangan sunset yang ikonik di Bali.",
        "lat": -8.6212,
        "lon": 115.0868,
        "address": "Tabanan, Bali"
    },
    {
        "name": "Labuan Bajo",
        "description": "Gerbang menuju Taman Nasional Komodo, pulau dengan komodo asli dan snorkeling spot terbaik.",
        "lat": -8.4967,
        "lon": 119.8881,
        "address": "Manggarai Barat, NTT"
    }
]

# Sample activities (match Activity model fields)
SAMPLE_ACTIVITIES = [
    {
        "name": "Sunrise Tour Borobudur",
        "description": "Nikmati sunrise dari puncak Candi Borobudur dengan pemandangan pegunungan Menoreh",
        "duration": "3 jam",
        "price_range": "Rp 250.000 - 400.000",
        "category": "tour"
    },
    {
        "name": "Surfing Lesson Kuta",
        "description": "Belajar surfing dengan instruktur profesional di Pantai Kuta",
        "duration": "2 jam",
        "price_range": "Rp 200.000 - 300.000",
        "category": "adventure"
    },
    {
        "name": "Bromo Sunrise Jeep Tour",
        "description": "Tour jeep ke viewpoint sunrise Gunung Bromo dan kawah aktif",
        "duration": "4 jam",
        "price_range": "Rp 400.000 - 500.000",
        "category": "adventure"
    },
    {
        "name": "Raja Ampat Diving",
        "description": "Eksplorasi bawah laut Raja Ampat dengan 3 diving spot terbaik",
        "duration": "6 jam",
        "price_range": "Rp 1.200.000 - 1.800.000",
        "category": "adventure"
    },
    {
        "name": "Ubud Art & Culture Tour",
        "description": "Kunjungi galeri seni, pasar tradisional, dan rice terrace di Ubud",
        "duration": "5 jam",
        "price_range": "Rp 350.000 - 450.000",
        "category": "culture"
    }
]

async def seed_data():
    """Seed sample data to database"""
    print("\n" + "="*60)
    print("🌱 SEEDING SAMPLE TOURISM DATA")
    print("="*60 + "\n")
    
    async for db in get_db():
        try:
            # Check if data already exists
            result = await db.execute(select(Destination))
            existing_dest = result.scalars().first()
            if existing_dest:
                print("⚠️  Data already exists. Skipping seed...")
                count_result = await db.execute(select(Destination))
                print(f"   Found {len(count_result.scalars().all())} destinations")
                return
            
            # Insert destinations
            print("📍 Adding destinations...")
            destinations = []
            for dest_data in SAMPLE_DESTINATIONS:
                dest = Destination(**dest_data)
                db.add(dest)
                destinations.append(dest)
            
            await db.flush()  # Get IDs
            print(f"   ✅ Added {len(destinations)} destinations")
            
            # Insert activities
            print("🎯 Adding activities...")
            for act_data in SAMPLE_ACTIVITIES:
                activity = Activity(**act_data)
                db.add(activity)
            
            await db.flush()
            print(f"   ✅ Added {len(SAMPLE_ACTIVITIES)} activities")
            
            # Create sample users
            print("👥 Adding sample users...")
            users = []
            for i in range(1, 6):
                user = User(
                    email=f"user{i}@example.com",
                    name=f"Sample User {i}",
                    preferences="nature,culture" if i % 2 == 0 else "beach,adventure"
                )
                db.add(user)
                users.append(user)
            
            await db.flush()
            print(f"   ✅ Added {len(users)} sample users")
            
            # Add some sample interactions
            print("💫 Adding sample interactions...")
            interaction_count = 0
            for user in users[:3]:  # First 3 users
                for dest in destinations[:5]:  # First 5 destinations
                    interaction = UserInteraction(
                        user_id=user.id,
                        entity_type="destination",
                        entity_id=dest.id,
                        interaction_type="view",
                        duration=120.0,  # 2 minutes
                        created_at=datetime.utcnow()
                    )
                    db.add(interaction)
                    interaction_count += 1
            
            print(f"   ✅ Added {interaction_count} sample interactions")
            
            # Add sample ratings (needed for collaborative filtering)
            print("⭐ Adding sample ratings...")
            rating_count = 0
            import random
            for user in users:  # All users
                # Each user rates 4-7 random destinations
                num_ratings = random.randint(4, 7)
                rated_destinations = random.sample(destinations, num_ratings)
                for dest in rated_destinations:
                    rating = Rating(
                        user_id=user.id,
                        destination_id=dest.id,
                        rating=random.uniform(3.5, 5.0)  # Random rating between 3.5 and 5.0
                    )
                    db.add(rating)
                    rating_count += 1
            
            print(f"   ✅ Added {rating_count} sample ratings")
            
            # Commit all changes
            await db.commit()
            
            print("\n" + "="*60)
            print("✅ SUCCESS! Sample data seeded")
            print("="*60)
            print(f"\n📊 Summary:")
            print(f"   - Destinations: {len(SAMPLE_DESTINATIONS)}")
            print(f"   - Activities: {len(SAMPLE_ACTIVITIES)}")
            print(f"   - Users: {len(users)}")
            print(f"   - Interactions: {interaction_count}")
            print(f"   - Ratings: {rating_count}")
            print(f"\n💡 Now you can train the models!\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            await db.rollback()
        finally:
            break

if __name__ == "__main__":
    asyncio.run(seed_data())
