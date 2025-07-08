from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    
    # Relationship dengan destinations melalui destination_categories
    destinations = relationship(
        "Destination", 
        secondary="destination_categories", 
        back_populates="categories"
    )
    