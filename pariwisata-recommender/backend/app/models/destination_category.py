from sqlalchemy import Column, Integer, ForeignKey, Table
from . import Base

# Association table untuk many-to-many relationship
destination_categories = Table(
    'destination_categories',
    Base.metadata,
    Column('destination_id', Integer, ForeignKey('destinations.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)