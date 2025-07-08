from sqlalchemy import Column, Integer, String, Float, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    
    # Relationships
    categories = relationship(
        "Category", 
        secondary="destination_categories", 
        back_populates="destinations"
    )
    ratings = relationship("Rating", back_populates="destination")
    reviews = relationship("Review", back_populates="destination")