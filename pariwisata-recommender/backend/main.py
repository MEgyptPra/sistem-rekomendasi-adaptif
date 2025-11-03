from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from admin_routes import admin_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Pariwisata Admin API",
    description="API untuk Admin Dashboard Sistem Rekomendasi Pariwisata",
    version="1.0.0"
)

# Configure CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:5173",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include admin routes
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"message": "Pariwisata API is running", "status": "ok"}
