"""
Fix PostgreSQL sequence for users table
This fixes the "duplicate key value violates unique constraint" error
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pariwisata_db")

async def fix_sequence():
    # Convert SQLAlchemy URL to asyncpg format
    db_url = DATABASE_URL.replace("postgresql://", "").replace("postgresql+asyncpg://", "")
    
    # Parse connection string
    if "@" in db_url:
        auth, rest = db_url.split("@")
        user, password = auth.split(":")
        host_port, database = rest.split("/")
        if ":" in host_port:
            host, port = host_port.split(":")
        else:
            host = host_port
            port = "5432"
    else:
        print("⚠️  Using default connection parameters")
        user = "postgres"
        password = "postgres"
        host = "localhost"
        port = "5432"
        database = "pariwisata_db"
    
    print(f"🔌 Connecting to database: {host}:{port}/{database}")
    
    try:
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        
        print("✅ Connected to database")
        
        # Get current max ID from users table
        max_id = await conn.fetchval("SELECT MAX(id) FROM users")
        print(f"📊 Current max user ID: {max_id}")
        
        if max_id is None:
            max_id = 0
            print("⚠️  No users found in table, starting from 1")
        
        # Fix the sequence
        next_id = max_id + 1
        await conn.execute(f"SELECT setval('users_id_seq', {next_id}, false)")
        
        print(f"✅ Updated users_id_seq to {next_id}")
        print(f"✅ Next user will get ID: {next_id}")
        
        # Verify
        current_seq = await conn.fetchval("SELECT last_value FROM users_id_seq")
        print(f"✅ Verified sequence value: {current_seq}")
        
        await conn.close()
        print("\n✅ Sequence fixed successfully!")
        print("👉 You can now register new users without errors")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(fix_sequence())
