from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class ActivityReview(Base):
    __tablename__ = "activity_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    name = Column(String, nullable=False)  # Nama reviewer (bisa beda dengan user.name)
    rating = Column(Float, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="activity_reviews")
    activity = relationship("Activity", back_populates="reviews")
