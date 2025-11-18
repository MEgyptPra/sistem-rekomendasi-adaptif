
print("[LOG] Importing FastAPI...")
from fastapi import FastAPI
print("[LOG] Importing CORS middleware...")
from fastapi.middleware.cors import CORSMiddleware
print("[LOG] Importing admin_router...")
from admin_routes import admin_router
print("[LOG] Importing model_router...")
from model_routes import model_router
print("[LOG] Importing ml_router...")
from app.api.endpoints import router as ml_router
print("[LOG] Importing frontend_router...")
from app.api.frontend_endpoints import router as frontend_router
print("[LOG] Importing medium_router...")
from app.api.medium_priority_endpoints import router as medium_router
print("[LOG] Importing low_router...")
from app.api.low_priority_endpoints import router as low_router
print("[LOG] Importing itinerary_router...")
from app.api.itineraries import router as itinerary_router
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import sys
try:
    print("[LOG] Importing FastAPI...")
    from fastapi import FastAPI
    print("[LOG] Importing CORS middleware...")
    from fastapi.middleware.cors import CORSMiddleware
    print("[LOG] Importing admin_router...")
    from admin_routes import admin_router
    print("[LOG] Importing model_router...")
    from model_routes import model_router
    print("[LOG] Importing ml_router...")
    from app.api.endpoints import router as ml_router
    print("[LOG] Importing frontend_router...")
    from app.api.frontend_endpoints import router as frontend_router
    print("[LOG] Importing medium_router...")
    from app.api.medium_priority_endpoints import router as medium_router
    print("[LOG] Importing low_router...")
    from app.api.low_priority_endpoints import router as low_router
    print("[LOG] Importing itinerary_router...")
    from app.api.itineraries import router as itinerary_router

    # Load environment variables
    load_dotenv()

    print("[LOG] Initializing FastAPI app...")
    app = FastAPI(
        title="Pariwisata Recommendation API",
        description="API untuk Sistem Rekomendasi Pariwisata Adaptif dengan Incremental Learning",
        version="2.0.0"
    )

    print("[LOG] Adding CORS middleware...")
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

    print("[LOG] Including routers...")
    app.include_router(admin_router)  # Admin dashboard routes
    print("[LOG] Included admin_router")
    app.include_router(model_router)  # Model management routes
    print("[LOG] Included model_router")
    app.include_router(frontend_router, prefix="/api", tags=["Frontend"])  # High priority frontend routes
    print("[LOG] Included frontend_router")
    app.include_router(ml_router, prefix="/api", tags=["ML & Recommendations"])  # ML endpoints
    print("[LOG] Included ml_router")
    app.include_router(medium_router, prefix="/api", tags=["User & Auth"])  # Medium priority (auth, etc)
    print("[LOG] Included medium_router")
    app.include_router(low_router, prefix="/api", tags=["Utilities"])  # Low priority utilities
    print("[LOG] Included low_router")
    app.include_router(itinerary_router, prefix="/api", tags=["Itineraries"])  # Itinerary routes
    print("[LOG] Included itinerary_router")

    @app.get("/")
    def read_root():
        return {"message": "Pariwisata API is running", "status": "ok", "version": "1.0.0"}

except Exception as e:
    print("[FATAL ERROR] Exception during import or app setup:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Load environment variables
load_dotenv()



print("[LOG] Initializing FastAPI app...")
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


print("[LOG] Adding CORS middleware...")
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


print("[LOG] Including routers...")
app.include_router(admin_router)  # Admin dashboard routes
print("[LOG] Included admin_router")
app.include_router(model_router)  # Model management routes
print("[LOG] Included model_router")
app.include_router(frontend_router, prefix="/api", tags=["Frontend"])  # High priority frontend routes
print("[LOG] Included frontend_router")
app.include_router(ml_router, prefix="/api", tags=["ML & Recommendations"])  # ML endpoints
print("[LOG] Included ml_router")
app.include_router(medium_router, prefix="/api", tags=["User & Auth"])  # Medium priority (auth, etc)
print("[LOG] Included medium_router")
app.include_router(low_router, prefix="/api", tags=["Utilities"])  # Low priority utilities
print("[LOG] Included low_router")
app.include_router(itinerary_router, prefix="/api", tags=["Itineraries"])  # Itinerary routes
print("[LOG] Included itinerary_router")

@app.get("/")
def read_root():
    return {"message": "Pariwisata API is running", "status": "ok", "version": "1.0.0"}
