from sqlalchemy import Column, Integer, String, Float
from . import Base

class Tourism(Base):
    __tablename__ = "tourism"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False) # contoh: "alam", "indoor"
    lat = Column(Float)
    lon = Column(Float)
    density = Column(Integer, default=0)  # 0: sepi, 1: sedang, 2: ramai