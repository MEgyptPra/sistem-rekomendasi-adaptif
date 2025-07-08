from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from . import Base

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    density = Column(Integer, default=0)  # 0: sepi, 1: sedang, 2: ramai
    
    # Relationships
    categories = relationship("Category", secondary="destination_categories", back_populates="destinations")
    ratings = relationship("Rating", back_populates="destination")
    reviews = relationship("Review", back_populates="destination")
    
    @property
    def category(self):
        """Backward compatibility property for single category access.
        Returns the first category name if available, otherwise empty string.
        """
        if self.categories:
            return self.categories[0].name
        return ""