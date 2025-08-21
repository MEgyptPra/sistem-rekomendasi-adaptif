import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:rekompari@db:5432/pariwisata")