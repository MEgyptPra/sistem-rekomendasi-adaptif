"""
Migration script: create realtime_api_config table
"""
from app.core.db import Base
from app.models.realtime_api_config import RealtimeAPIConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:rekompari@localhost:5432/pariwisata")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def migrate():
    print("Creating realtime_api_config table...")
    Base.metadata.create_all(bind=engine, tables=[RealtimeAPIConfig.__table__])
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
