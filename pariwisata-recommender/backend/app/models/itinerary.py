from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default='upcoming')  # 'upcoming', 'ongoing', 'completed', 'cancelled'
    total_budget = Column(Integer, nullable=True)  # Total budget dalam Rupiah
    accommodation = Column(Text, nullable=True)  # JSON string untuk info penginapan
    transportation = Column(Text, nullable=True)  # JSON string untuk info transportasi
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="itineraries")
    days = relationship("ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan")


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day_number = Column(Integer, nullable=False)  # Day 1, 2, 3, etc.
    date = Column(Date, nullable=False)
    title = Column(String, nullable=True)  # e.g., "Exploring Sumedang City"
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="days")
    items = relationship("ItineraryItem", back_populates="day", cascade="all, delete-orphan")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"), nullable=False)
    time = Column(String, nullable=True)  # e.g., "09:00"
    activity_type = Column(String, nullable=False)  # 'destination', 'activity', 'meal', 'rest', 'transport'
    entity_id = Column(Integer, nullable=True)  # ID of destination or activity
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    duration = Column(String, nullable=True)  # e.g., "2 hours"
    cost = Column(Integer, nullable=True)  # Cost in Rupiah
    notes = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)  # Order within the day
    
    # Relationships
    day = relationship("ItineraryDay", back_populates="items")
