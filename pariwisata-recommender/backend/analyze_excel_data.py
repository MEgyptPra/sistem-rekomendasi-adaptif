"""
Script untuk menganalisis data Excel dan menghitung skip rate
"""
import pandas as pd

# Baca Excel
df = pd.read_excel('data/sumedang reviews.xlsx')

print(f'Total rows in Excel: {len(df):,}')
print(f'\nUnique places in Excel: {df["place"].nunique()}')
print(f'\nTop 15 most reviewed places:')
print(df['place'].value_counts().head(15))

# Baca destinations dari database
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/pariwisata_db')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) as count FROM destinations"))
    db_count = result.fetchone()[0]
    print(f'\n\nDestinations in database: {db_count}')
    
    result = conn.execute(text("SELECT name FROM destinations ORDER BY name"))
    db_destinations = [row[0] for row in result.fetchall()]

# Check berapa yang match
excel_places = set(df['place'].unique())
db_places = set(db_destinations)

matched = excel_places.intersection(db_places)
not_matched = excel_places - db_places

print(f'\n\n=== MATCHING ANALYSIS ===')
print(f'Places in Excel: {len(excel_places)}')
print(f'Places in DB: {len(db_places)}')
print(f'Matched: {len(matched)}')
print(f'Not matched: {len(not_matched)}')

# Hitung berapa banyak rows yang tidak match
not_matched_count = df[df['place'].isin(not_matched)].shape[0]
print(f'\nRows with unmatched places: {not_matched_count:,}')
print(f'Rows with matched places: {len(df) - not_matched_count:,}')

print(f'\n\nSample unmatched places (first 20):')
for i, place in enumerate(list(not_matched)[:20], 1):
    count = df[df['place'] == place].shape[0]
    print(f'  {i}. {place} ({count} reviews)')
