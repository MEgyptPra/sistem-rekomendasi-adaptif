"""
Script to clear all sample data from database
"""
import asyncio
from sqlalchemy import text
from app.core.db import get_db

async def clear_data():
    """Clear all data from tables"""
    print("\n" + "="*60)
    print("🧹 CLEARING DATABASE")
    print("="*60 + "\n")
    
    async for db in get_db():
        try:
            # Disable foreign key checks and truncate tables
            print("🗑️  Truncating tables...")
            await db.execute(text("TRUNCATE TABLE user_interactions, ratings, users, activities, destinations RESTART IDENTITY CASCADE;"))
            await db.commit()
            
            print("✅ Database cleared successfully!\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            await db.rollback()
        finally:
            break

if __name__ == "__main__":
    asyncio.run(clear_data())
