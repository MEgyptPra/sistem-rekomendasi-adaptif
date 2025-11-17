"""
Script untuk train models SEKALI SAJA
Setelah ini, models akan auto-load setiap server restart
"""
import asyncio
from app.core.db import get_db
from app.services.ml_service import MLService

async def train_models():
    print("\n" + "="*60)
    print("🎯 TRAINING ALL ML MODELS")
    print("="*60 + "\n")
    
    # Initialize ML Service
    ml_service = MLService()
    
    # Get database session
    async for db in get_db():
        try:
            # Train all models
            print("🚀 Starting training process...")
            results = await ml_service.train_all_models(db)
            
            print("\n" + "="*60)
            print("📊 TRAINING RESULTS")
            print("="*60)
            print(f"\n{results}\n")
            
            # Check training status
            if results['overall_status'] == 'success':
                print("✅ SUCCESS! Models trained and saved to disk")
                print("\n💡 Next time you start the server:")
                print("   - Models will AUTO-LOAD from disk")
                print("   - No need to train again")
                print("   - Ready to use immediately!\n")
            else:
                print("❌ Training failed. Check errors above.")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
        finally:
            break

if __name__ == "__main__":
    asyncio.run(train_models())
