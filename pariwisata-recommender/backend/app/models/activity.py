from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # Kuliner, Budaya, Alam, etc.
    duration = Column(String, nullable=True)  # e.g., "2-3 jam"
    price_range = Column(String, nullable=True)  # e.g., "Rp 50.000 - 150.000"
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    reviews = relationship("ActivityReview", back_populates="activity")
