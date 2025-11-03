from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous users
    session_id = Column(String, nullable=True)  # For anonymous tracking
    interaction_type = Column(String, nullable=False)  # 'click', 'view', 'favorite', 'share'
    entity_type = Column(String, nullable=False)  # 'destination', 'activity', 'itinerary'
    entity_id = Column(Integer, nullable=False)  # ID of the entity
    duration = Column(Float, nullable=True)  # Time spent (in seconds) for 'view' interactions
    extra_data = Column(Text, nullable=True)  # JSON string for additional data (renamed from 'metadata' to avoid SQLAlchemy conflict)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="interactions")
