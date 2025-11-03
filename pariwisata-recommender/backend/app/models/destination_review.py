from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class DestinationReview(Base):
    __tablename__ = "destination_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    name = Column(String, nullable=False)  # Nama reviewer
    rating = Column(Float, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="destination_reviews")
    destination = relationship("Destination", back_populates="destination_reviews")
