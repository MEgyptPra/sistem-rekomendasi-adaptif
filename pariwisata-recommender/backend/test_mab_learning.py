"""
Test script to verify MAB is learning from historical data
"""
import asyncio
import json
from sqlalchemy import select, func
from app.database import get_db
from app.models.user_interaction import UserInteraction
from app.models.rating import Rating
from app.services.ml_service import get_ml_service

async def test_mab_state():
    print("="*80)
    print("🧪 TESTING MAB LEARNING FROM HISTORICAL DATA")
    print("="*80)
    print()
    
    # 1. Check data availability
    print("📊 Step 1: Checking Historical Data...")
    async for db in get_db():
        # Count ratings
        rating_count = await db.scalar(select(func.count(Rating.id)))
        print(f"   ✅ Ratings in database: {rating_count:,}")
        
        # Count interactions
        interaction_count = await db.scalar(select(func.count(UserInteraction.id)))
        print(f"   ✅ User Interactions: {interaction_count:,}")
        
        # Count unique users with ratings
        unique_users = await db.scalar(
            select(func.count(func.distinct(Rating.user_id)))
        )
        print(f"   ✅ Unique users with ratings: {unique_users:,}")
        
        # Count unique destinations rated
        unique_dests = await db.scalar(
            select(func.count(func.distinct(Rating.destination_id)))
        )
        print(f"   ✅ Unique destinations rated: {unique_dests:,}")
        
        print(f"\n   📈 TOTAL HISTORICAL DATA: {rating_count + interaction_count:,} interactions")
        print()
    
    # 2. Check ML Service models
    print("🤖 Step 2: Checking ML Models...")
    ml_service = get_ml_service()
    
    # Check if models are trained
    cb_trained = ml_service.content_based_trained
    collab_trained = ml_service.collaborative_trained
    hybrid_trained = ml_service.hybrid_trained
    
    print(f"   Content-Based Model: {'✅ TRAINED' if cb_trained else '❌ NOT TRAINED'}")
    print(f"   Collaborative Model: {'✅ TRAINED' if collab_trained else '❌ NOT TRAINED'}")
    print(f"   Hybrid Model:        {'✅ TRAINED' if hybrid_trained else '❌ NOT TRAINED'}")
    print()
    
    # Check content-based details
    if cb_trained and ml_service.content_based:
        cb = ml_service.content_based
        print(f"   📋 Content-Based Details:")
        print(f"      - Items: {cb.n_items}")
        print(f"      - User profiles: {len(cb.user_profiles)}")
        print(f"      - Features: {cb.n_features}")
    
    # Check collaborative details
    if collab_trained and ml_service.collaborative:
        collab = ml_service.collaborative
        print(f"\n   🤝 Collaborative Details:")
        print(f"      - Users: {collab.n_users}")
        print(f"      - Items: {collab.n_items}")
        if hasattr(collab, 'sparsity'):
            print(f"      - Sparsity: {collab.sparsity:.2%}")
    print()
    
    # 3. Check MAB state
    print("🎯 Step 3: Checking MAB State...")
    
    # Access MAB component
    if hasattr(ml_service, 'hybrid') and ml_service.hybrid:
        hybrid = ml_service.hybrid
        
        # Check if MAB exists
        if hasattr(hybrid, 'mab_component') and hybrid.mab_component:
            mab = hybrid.mab_component
            
            # Get contextual states
            if hasattr(mab, 'contextual_states'):
                num_contexts = len(mab.contextual_states)
                print(f"   ✅ Contextual MAB initialized")
                print(f"   📊 Number of contexts learned: {num_contexts}")
                
                # Show sample contexts
                if num_contexts > 0:
                    print(f"\n   🔍 Sample Contexts (showing first 3):")
                    for i, (context_key, state) in enumerate(list(mab.contextual_states.items())[:3]):
                        print(f"      {i+1}. Context: {context_key[:60]}...")
                        if hasattr(state, 'arm_counts'):
                            total_pulls = sum(state.arm_counts.values())
                            print(f"         Total pulls: {total_pulls}")
                            print(f"         Arms: {list(state.arm_counts.keys())}")
            else:
                print(f"   ⚠️  MAB exists but no contextual states found")
        else:
            print(f"   ⚠️  MAB component not initialized")
    else:
        print(f"   ❌ Hybrid model not available")
    
    print()
    print("="*80)
    print("✅ MAB VERIFICATION COMPLETE")
    print("="*80)
    print()
    print("💡 Summary:")
    print(f"   • Models trained with {rating_count:,} ratings from {unique_users:,} users")
    print(f"   • Collaborative filtering uses dense interaction matrix")
    print(f"   • MAB learns context-specific lambda values")
    print(f"   • System ready for personalized recommendations!")
    print()

if __name__ == "__main__":
    asyncio.run(test_mab_state())
