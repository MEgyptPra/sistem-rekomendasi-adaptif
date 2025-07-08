from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    preferences = Column(String, nullable=True)  # contoh: "alam,kuliner"
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    ratings = relationship("Rating", back_populates="user")
    reviews = relationship("Review", back_populates="user")