from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Pariwisata API",
    description="Sistem Rekomendasi Pariwisata Adaptif",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api")