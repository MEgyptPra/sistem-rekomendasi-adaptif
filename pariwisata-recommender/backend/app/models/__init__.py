from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import association table first
from .destination_category import destination_categories

# Import semua model agar register ke Base.metadata
from .category import Category
from .destinations import Destination
from .rating import Rating
from .review import Review
from .user import User
from .activity import Activity
from .activity_review import ActivityReview
from .destination_review import DestinationReview
from .user_interaction import UserInteraction
from .itinerary import Itinerary, ItineraryDay, ItineraryItem
