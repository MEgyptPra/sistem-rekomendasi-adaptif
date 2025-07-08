from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preferences = Column(String, nullable=True)  # contoh: "alam,kuliner"
    
    # Relationships
    ratings = relationship("Rating", back_populates="user")
    reviews = relationship("Review", back_populates="user")