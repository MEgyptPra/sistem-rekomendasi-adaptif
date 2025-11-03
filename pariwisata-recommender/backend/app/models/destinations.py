from sqlalchemy import Column, Integer, String, Float, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

# Association table for many-to-many relationship
destination_categories = Table(
    'destination_categories',
    Base.metadata,
    Column('destination_id', Integer, ForeignKey('destinations.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True),
    extend_existing=True
)

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
    destination_reviews = relationship("DestinationReview", back_populates="destination")