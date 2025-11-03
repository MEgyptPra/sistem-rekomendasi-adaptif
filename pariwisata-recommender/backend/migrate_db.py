"""
Database Migration Script
Creates all new tables for Activity, ActivityReview, DestinationReview, and UserInteraction models
"""

import asyncio
import sys
from sqlalchemy import text

# Import engine dan Base
from app.core.db import engine
from app.models import Base

# Import semua models agar terdaftar di Base.metadata
from app.models.user import User
from app.models.destinations import Destination
from app.models.category import Category
from app.models.rating import Rating
from app.models.review import Review
from app.models.activity import Activity
from app.models.activity_review import ActivityReview
from app.models.destination_review import DestinationReview
from app.models.user_interaction import UserInteraction


async def check_table_exists(table_name: str) -> bool:
    """Check if a table exists in the database"""
    async with engine.begin() as conn:
        result = await conn.execute(
            text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table_name}'
                );
            """)
        )
        exists = result.scalar()
        return exists


async def create_tables():
    """Create all tables defined in models"""
    
    print("🔍 Checking existing tables...")
    
    # Check which new tables already exist
    tables_to_create = {
        'activities': Activity,
        'activity_reviews': ActivityReview,
        'destination_reviews': DestinationReview,
        'user_interactions': UserInteraction
    }
    
    existing_tables = []
    new_tables = []
    
    for table_name, model in tables_to_create.items():
        exists = await check_table_exists(table_name)
        if exists:
            existing_tables.append(table_name)
            print(f"   ✅ Table '{table_name}' already exists")
        else:
            new_tables.append(table_name)
            print(f"   ⚠️  Table '{table_name}' does not exist")
    
    if not new_tables:
        print("\n✅ All tables already exist! No migration needed.")
        return
    
    print(f"\n📝 Will create {len(new_tables)} new table(s):")
    for table_name in new_tables:
        print(f"   - {table_name}")
    
    # Confirm before proceeding
    print("\n⚠️  This will create new tables in the database.")
    response = input("Continue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("❌ Migration cancelled.")
        return
    
    print("\n🚀 Creating tables...")
    
    try:
        # Create all tables (will skip existing ones)
        async with engine.begin() as conn:
            # SQLAlchemy will only create tables that don't exist
            await conn.run_sync(Base.metadata.create_all)
        
        print("\n✅ Migration completed successfully!")
        print("\n📋 Created tables:")
        for table_name in new_tables:
            print(f"   ✅ {table_name}")
        
        if existing_tables:
            print("\n📋 Existing tables (skipped):")
            for table_name in existing_tables:
                print(f"   ⏭️  {table_name}")
        
        print("\n🎉 Database is ready!")
        print("\n📝 Next steps:")
        print("   1. Run seed script: python seed_activities.py")
        print("   2. Start backend: python main.py")
        print("   3. Test API: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        print("\nPlease check:")
        print("   - Database connection in .env file")
        print("   - PostgreSQL server is running")
        print("   - Database exists and is accessible")
        sys.exit(1)


async def show_tables():
    """Show all tables in the database"""
    print("\n📊 Current database tables:")
    
    async with engine.begin() as conn:
        result = await conn.execute(
            text("""
                SELECT tablename 
                FROM pg_catalog.pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """)
        )
        tables = result.fetchall()
        
        if tables:
            for idx, (table_name,) in enumerate(tables, 1):
                print(f"   {idx}. {table_name}")
        else:
            print("   (no tables found)")


async def main():
    """Main migration function"""
    
    print("=" * 60)
    print("  DATABASE MIGRATION TOOL")
    print("  Adding new tables for HIGH PRIORITY API endpoints")
    print("=" * 60)
    print()
    
    try:
        # Show current tables
        await show_tables()
        print()
        
        # Run migration
        await create_tables()
        
        # Show tables after migration
        print()
        await show_tables()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        # Close engine
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
