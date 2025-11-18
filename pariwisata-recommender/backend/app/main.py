from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..admin_routes import admin_router
from ..model_routes import model_router
from app.api.endpoints import router as ml_router
from app.api.frontend_endpoints import router as frontend_router
from app.api.medium_priority_endpoints import router as medium_router
from app.api.low_priority_endpoints import router as low_router
from app.api.itineraries import router as itinerary_router
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()


app = FastAPI(
    title="Pariwisata Recommendation API",
    description="API untuk Sistem Rekomendasi Pariwisata Adaptif dengan Incremental Learning",
    version="2.0.0"
)

# TODO: Enable scheduler when database module is fixed
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     from app.scheduler.learning_scheduler import start_scheduler, stop_scheduler
#     print("� Starting Incremental Learning Scheduler...")
#     start_scheduler()
#     yield
#     print("🛑 Stopping Incremental Learning Scheduler...")
#     stop_scheduler()

# Configure CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Admin dashboard & future frontend
        "http://localhost:5173",  # Frontend (Vite dev server)
        "http://localhost:8000"   # API itself (for docs)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(admin_router)  # Admin dashboard routes
app.include_router(model_router)  # Model management routes
app.include_router(frontend_router, prefix="/api", tags=["Frontend"])  # High priority frontend routes
app.include_router(ml_router, prefix="/api", tags=["ML & Recommendations"])  # ML endpoints
app.include_router(medium_router, prefix="/api", tags=["User & Auth"])  # Medium priority (auth, etc)
app.include_router(low_router, prefix="/api", tags=["Utilities"])  # Low priority utilities
app.include_router(itinerary_router, prefix="/api", tags=["Itineraries"])  # Itinerary routes

@app.get("/")
def read_root():
    return {"message": "Pariwisata API is running", "status": "ok", "version": "1.0.0"}
