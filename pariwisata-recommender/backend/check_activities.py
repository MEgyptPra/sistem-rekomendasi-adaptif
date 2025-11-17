import asyncio
from sqlalchemy import text
from app.core.db import AsyncSessionLocal

async def check_activities():
    """Check if activities table exists and show sample data"""
    async with AsyncSessionLocal() as session:
        try:
            # Check if table exists
            result = await session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%activit%'
            """))
            tables = result.fetchall()
            print(f"📊 Tables with 'activit' in name: {[t[0] for t in tables]}")
            
            # Try to query activities table
            try:
                result = await session.execute(text("SELECT * FROM activities LIMIT 5"))
                activities = result.fetchall()
                print(f"\n✅ Found {len(activities)} activities (showing first 5)")
                for act in activities:
                    print(f"   {dict(act._mapping)}")
            except Exception as e:
                print(f"\n❌ Error querying activities: {e}")
                
        except Exception as e:
            print(f"❌ Database error: {e}")

if __name__ == "__main__":
    asyncio.run(check_activities())
