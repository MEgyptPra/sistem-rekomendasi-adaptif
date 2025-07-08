# Database Models Update - Documentation

## Overview

This document describes the updated database models that now match the actual database schema. The models have been updated to support proper relationships and prepare for recommendation algorithms in Stage 2.

## Model Changes Summary

### New Models Added

1. **Category** (`categories` table)
   - `id`: Primary key
   - `name`: Category name (unique)
   - Relationships: Many-to-many with destinations

2. **Rating** (`ratings` table)
   - `id`: Primary key
   - `user_id`: Foreign key to users table
   - `destination_id`: Foreign key to destinations table
   - `rating`: Float value (typically 1-5 scale)
   - `created_at`: Timestamp

3. **Review** (`reviews` table)
   - `id`: Primary key
   - `user_id`: Foreign key to users table
   - `destination_id`: Foreign key to destinations table
   - `content`: Text content of review
   - `created_at`: Timestamp

4. **DestinationCategory** (association table `destination_categories`)
   - `destination_id`: Foreign key to destinations
   - `category_id`: Foreign key to categories
   - Used for many-to-many relationship

### Updated Models

1. **Destination** (formerly Tourism)
   - Table name changed from `tourism` to `destinations`
   - Removed `category` string field
   - Added relationships:
     - `categories`: Many-to-many with Category model
     - `ratings`: One-to-many with Rating model
     - `reviews`: One-to-many with Review model
   - Added backward compatibility `category` property

2. **User** 
   - Added relationships:
     - `ratings`: One-to-many with Rating model
     - `reviews`: One-to-many with Review model

## Backward Compatibility

To ensure existing API code continues to work:

1. **Tourism Model**: Still available as an alias to Destination
   ```python
   from app.models.tourism import Tourism  # Works as before
   ```

2. **Category Property**: Destination model has a `category` property that returns the first category name
   ```python
   destination = Destination()
   category_name = destination.category  # Returns first category name or ""
   ```

## Database Schema

The updated schema matches these table structures:

```sql
-- categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

-- destinations table (was tourism)
CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    lat FLOAT,
    lon FLOAT,
    density INTEGER DEFAULT 0
);

-- users table (unchanged structure)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    preferences VARCHAR
);

-- ratings table
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    destination_id INTEGER REFERENCES destinations(id),
    rating FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    destination_id INTEGER REFERENCES destinations(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- destination_categories table (many-to-many)
CREATE TABLE destination_categories (
    destination_id INTEGER REFERENCES destinations(id),
    category_id INTEGER REFERENCES categories(id),
    PRIMARY KEY (destination_id, category_id)
);
```

## Usage Examples

### Using the New Models

```python
from app.models import User, Destination, Category, Rating, Review

# Create relationships
user = User(name="John Doe", preferences="alam,kuliner")
category = Category(name="alam")
destination = Destination(name="Pantai Kuta", lat=-8.718, lon=115.169)

# Add category to destination
destination.categories.append(category)

# Add rating
rating = Rating(user=user, destination=destination, rating=4.5)

# Add review
review = Review(user=user, destination=destination, content="Beautiful beach!")
```

### Backward Compatibility Usage

```python
# This still works for existing API code
from app.models.tourism import Tourism

destinations = session.query(Tourism).all()
for dest in destinations:
    print(f"{dest.name}: {dest.category}")  # Uses the property
```

## Migration Notes

1. **Table Creation**: Run `create_tables.py` to create all new tables
2. **Data Migration**: You may need to migrate existing data from `tourism` table to `destinations` table
3. **Category Migration**: Convert existing string categories to proper Category records and relationships

## Preparation for Stage 2

These models provide the foundation for recommendation algorithms:

1. **Collaborative Filtering**: Uses Rating model for user-item ratings
2. **Content-Based Filtering**: Uses Category relationships and destination features
3. **Hybrid Approaches**: Combines both rating data and content features

The proper relationships enable efficient queries for:
- User rating patterns
- Destination categories and features
- User preferences and history
- Review sentiment analysis