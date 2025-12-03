"""
RESET DATABASE - Hapus semua data dan import fresh dari GMaps
WARNING: Akan menghapus SEMUA data user, reviews, ratings, interactions!
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.core.db import get_db

async def reset_database():
    """Truncate all tables"""
    print("\n" + "="*80)
    print("[WARNING] RESETTING DATABASE - ALL DATA WILL BE DELETED!")
    print("="*80 + "\n")
    
    async for db in get_db():
        try:
            # Truncate tables in correct order (respect foreign keys)
            tables = [
                'user_interactions',
                'reviews',
                'ratings',
                'favorites',
                'users'
            ]
            
            for table in tables:
                print(f"[DELETE] Truncating {table}...")
                await db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
            
            await db.commit()
            print("\n[SUCCESS] Database reset complete!")
            print("="*80 + "\n")
            
        except Exception as e:
            print(f"\n[ERROR] {str(e)}\n")
            import traceback
            traceback.print_exc()
            await db.rollback()
        finally:
            break

if __name__ == "__main__":
    print("\n[WARNING] This will delete ALL user data, reviews, ratings, and interactions!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm == 'YES':
        asyncio.run(reset_database())
        print("\n[NEXT] Run: python scripts/import_all_gmaps_data.py\n")
    else:
        print("\n[CANCELLED] Database reset cancelled.\n")
