from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.user import User
from app.models.tourism import Tourism
from app.services.ml_service import simple_recommendation
from sqlalchemy.future import select

router = APIRouter()

@router.get("/recommendation")
async def get_recommendation(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    # Ambil user
    user = await db.get(User, user_id)
    # Ambil semua destinasi
    result = await db.execute(select(Tourism))
    destinations = result.scalars().all()
    # Dummy rekomendasi
    recs = simple_recommendation(user, destinations)
    # Keluarkan data sederhana
    return [{"id": d.id, "name": d.name, "category": d.category} for d in recs]