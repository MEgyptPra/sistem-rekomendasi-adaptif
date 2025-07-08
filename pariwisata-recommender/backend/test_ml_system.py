import asyncio
import json
from sqlalchemy.future import select
from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.destinations import Destination
from app.models.category import Category
from app.models.rating import Rating
from app.services.ml_service import ml_service

async def test_ml_system():
    """Test complete ML recommendation system"""
    async with AsyncSessionLocal() as session:
        print("🧪 Testing ML Recommendation System...")
        
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
            print(f"Testing recommendations for User ID: {user.id}")
            
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
                            print(f"{i}. {rec['name']} (Score: {rec['score']}) - {rec['explanation']}")
                    else:
                        print("No recommendations generated")
                        
                except Exception as e:
                    print(f"Error with {algorithm}: {e}")
        
        # 4. Test user profile
        if user:
            print(f"\n👤 User Profile for ID {user.id}:")
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

if __name__ == "__main__":
    asyncio.run(test_ml_system())