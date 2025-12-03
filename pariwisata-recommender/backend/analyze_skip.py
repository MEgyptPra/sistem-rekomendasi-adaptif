"""
Analyze name mismatches between Excel and what was actually imported
"""
import pandas as pd

# Baca Excel
df = pd.read_excel('data/sumedang reviews.xlsx')

# Hitung statistik
total_rows = len(df)
users_created = 16005
reviews_imported = 20460
ratings_imported = 21642
skipped = 17055

print("="*80)
print("IMPORT STATISTICS ANALYSIS")
print("="*80)
print(f"\nTotal rows in Excel:     {total_rows:,}")
print(f"Ratings imported:        {ratings_imported:,}")
print(f"Reviews imported:        {reviews_imported:,}")
print(f"Skipped:                 {skipped:,}")
print(f"\nPercentage skipped:      {(skipped/total_rows)*100:.1f}%")
print(f"Percentage imported:     {(ratings_imported/total_rows)*100:.1f}%")

# Analisis per-user
print(f"\n\nUSER ANALYSIS:")
print(f"Unique users in Excel:   {df['user'].nunique():,}")
print(f"Users created in DB:     {users_created:,}")
print(f"Difference:              {df['user'].nunique() - users_created:,}")

# Check for NaN users
nan_users = df[df['user'].isna()]
print(f"\nRows with NaN username:  {len(nan_users):,}")

# Check for empty usernames
empty_users = df[df['user'].astype(str).str.strip() == '']
print(f"Rows with empty username: {len(empty_users):,}")

# Check potential issues
total_potential_skip = len(nan_users) + len(empty_users)
print(f"\nTotal potential user skip: {total_potential_skip:,}")
print(f"Actual skip:                {skipped:,}")
print(f"Difference (likely dest mismatch): {skipped - total_potential_skip:,}")
