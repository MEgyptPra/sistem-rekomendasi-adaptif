from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import association table first to avoid circular imports
from .destination_category import destination_categories

# Import semua model agar register ke Base.metadata
from .user import User
from .category import Category
from .destination import Destination
from .rating import Rating
from .review import Review

# Import backward compatibility
from .tourism import Tourism