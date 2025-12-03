"""
Add password_hash column to users table
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.core.db import engine

async def add_password_hash_column():
    """Add password_hash column to users table if it doesn't exist"""
    async with engine.begin() as conn:
        # Check if column exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='password_hash'
        """))
        
        existing = result.fetchone()
        
        if existing:
            print("✅ Column 'password_hash' already exists in users table")
        else:
            print("🔄 Adding 'password_hash' column to users table...")
            await conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN password_hash VARCHAR(255) NULL
            """))
            print("✅ Column 'password_hash' added successfully!")
            print("   - Users from GMaps: password_hash = NULL (cannot login)")
            print("   - New registered users: password_hash = hashed password")

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION: Add password_hash column")
    print("=" * 60)
    asyncio.run(add_password_hash_column())
    print("\n✅ Migration completed!")
