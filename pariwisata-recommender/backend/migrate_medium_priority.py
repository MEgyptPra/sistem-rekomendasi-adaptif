"""
Database Migration Script - MEDIUM PRIORITY
Creates tables for Itinerary, ItineraryDay, ItineraryItem
Also adds password_hash column to users table
"""

import asyncio
import sys
from sqlalchemy import text

# Import engine dan Base
from app.core.db import engine
from app.models import Base

# Import all models
from app.models.user import User
from app.models.itinerary import Itinerary, ItineraryDay, ItineraryItem


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


async def check_column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table"""
    async with engine.begin() as conn:
        result = await conn.execute(
            text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table_name}'
                    AND column_name = '{column_name}'
                );
            """)
        )
        exists = result.scalar()
        return exists


async def add_password_column():
    """Add password_hash column to users table if it doesn't exist"""
    print("\n🔐 Checking users table for password_hash column...")
    
    exists = await check_column_exists('users', 'password_hash')
    
    if exists:
        print("   ✅ Column 'password_hash' already exists in users table")
        return False
    else:
        print("   ⚠️  Column 'password_hash' does not exist")
        print("   📝 Adding password_hash column to users table...")
        
        async with engine.begin() as conn:
            await conn.execute(
                text("ALTER TABLE users ADD COLUMN password_hash VARCHAR;")
            )
        
        print("   ✅ Column 'password_hash' added successfully")
        return True


async def create_tables():
    """Create all tables defined in models"""
    
    print("=" * 60)
    print("  DATABASE MIGRATION TOOL - MEDIUM PRIORITY")
    print("  Adding Itinerary Management tables")
    print("=" * 60)
    print()
    
    print("🔍 Checking existing tables...")
    
    # Check which new tables already exist
    tables_to_create = {
        'itineraries': Itinerary,
        'itinerary_days': ItineraryDay,
        'itinerary_items': ItineraryItem
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
    
    # Check for password_hash column
    password_column_added = await add_password_column()
    
    if not new_tables and not password_column_added:
        print("\n✅ All tables and columns already exist! No migration needed.")
        return
    
    if new_tables:
        print(f"\n📝 Will create {len(new_tables)} new table(s):")
        for table_name in new_tables:
            print(f"   - {table_name}")
    
    # Confirm before proceeding
    print("\n⚠️  This will create new tables/columns in the database.")
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
        
        if new_tables:
            print("\n📋 Created tables:")
            for table_name in new_tables:
                print(f"   ✅ {table_name}")
        
        if existing_tables:
            print("\n📋 Existing tables (skipped):")
            for table_name in existing_tables:
                print(f"   ⏭️  {table_name}")
        
        if password_column_added:
            print("\n📋 Modified tables:")
            print("   ✅ users (added password_hash column)")
        
        print("\n🎉 Database is ready!")
        print("\n📝 Next steps:")
        print("   1. Install dependencies: pip install passlib[bcrypt] python-jose[cryptography] python-multipart email-validator")
        print("   2. Restart backend server")
        print("   3. Test API: http://localhost:8000/docs")
        print("   4. Try authentication endpoints: /api/auth/register, /api/auth/login")
        print("   5. Try itinerary endpoints: /api/itineraries")
        
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
