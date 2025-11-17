"""
Script untuk cek isi database destinations
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def check_database():
    try:
        from app.core.db import get_db
        from app.models.destinations import Destination
        from sqlalchemy import select, func
        
        print("🔍 Checking database for destinations...")
        
        async for db in get_db():
            try:
                # Count destinations
                count_result = await db.execute(select(func.count(Destination.id)))
                total = count_result.scalar()
                print(f"📊 Total destinations in database: {total}")
                
                if total > 0:
                    # Get first 10 destinations
                    result = await db.execute(
                        select(Destination).limit(10)
                    )
                    destinations = result.scalars().all()
                    
                    print(f"\n✅ Found {len(destinations)} destinations (showing first 10):")
                    print("-" * 80)
                    for dest in destinations:
                        print(f"ID: {dest.id:4d} | Name: {dest.name:40s} | Address: {dest.address or 'No address'}")
                    print("-" * 80)
                else:
                    print("\n⚠️  Database is EMPTY! No destinations found.")
                    print("\n💡 Solution: Run seed script to populate database:")
                    print("   cd backend")
                    print("   python seed_activities.py")
                
            except Exception as e:
                print(f"❌ Error querying database: {e}")
                import traceback
                traceback.print_exc()
            finally:
                await db.close()
                break
                
    except ImportError as e:
        print(f"❌ Cannot import database modules: {e}")
        print("\n💡 Make sure you're in the backend directory:")
        print("   cd backend")
        print("   python check_database_destinations.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_database())
