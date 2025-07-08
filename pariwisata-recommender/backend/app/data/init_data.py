# Script untuk populate initial data untuk testing algoritma
from app.models import Category, Destination, User, Rating, Review

SAMPLE_CATEGORIES = [
    {"name": "Alam", "description": "Destinasi wisata alam"},
    {"name": "Budaya", "description": "Destinasi wisata budaya"},
    {"name": "Kuliner", "description": "Destinasi wisata kuliner"},
    {"name": "Religi", "description": "Destinasi wisata religi"},
]

# Sample data untuk testing collaborative filtering
SAMPLE_RATINGS = [
    {"user_id": 1, "destination_id": 1, "rating": 4.5},
    {"user_id": 1, "destination_id": 2, "rating": 3.0},
    # ... lebih banyak sample data
]