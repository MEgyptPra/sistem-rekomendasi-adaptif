from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import semua model agar register ke Base.metadata
from .tourism import Tourism
from .user import User