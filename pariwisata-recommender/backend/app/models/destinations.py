from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from .destination_category import destination_categories

class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    lat = Column(Float)
    lon = Column(Float)
    address = Column(String, nullable=True)
    
    # Relationships
    categories = relationship("Category", secondary=destination_categories, back_populates="destinations")
    ratings = relationship("Rating", back_populates="destination")
    reviews = relationship("Review", back_populates="destination")