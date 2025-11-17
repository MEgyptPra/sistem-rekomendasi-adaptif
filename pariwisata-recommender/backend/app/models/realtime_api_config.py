from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.db import Base

class RealtimeAPIConfig(Base):
    __tablename__ = "realtime_api_config"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String(32), nullable=False, unique=True)  # e.g. weather, traffic, social_trend, calendar
    api_key = Column(Text, nullable=True)
    api_url = Column(Text, nullable=True)
    status = Column(String(16), default="active")  # active, inactive, error
    last_checked = Column(DateTime, default=func.now())
    notes = Column(Text, nullable=True)
