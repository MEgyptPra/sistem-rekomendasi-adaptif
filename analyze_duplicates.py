"""
Analyze why we can't create all 28,547 users
"""
import pandas as pd
from pathlib import Path

excel_path = Path(__file__).parent / 'notebooks' / 'data' / 'sumedang reviews.xlsx'
df = pd.read_excel(excel_path)

print(f"Total rows: {len(df):,}")
print(f"Unique users: {df['user'].nunique():,}\n")

# Generate emails like the import script does
df['email'] = df['user'].apply(lambda x: f"{str(x).strip()[:100].replace(' ', '_').lower()}@gmaps.sumedang.com"[:255])

print(f"Unique emails after cleaning: {df['email'].nunique():,}")
print(f"Email duplicates: {len(df) - df['email'].nunique():,}\n")

# Show some duplicate examples
duplicate_emails = df[df.duplicated('email', keep=False)].groupby('email')['user'].apply(list)
print(f"Examples of different names → same email:\n")
for email, names in list(duplicate_emails.items())[:10]:
    unique_names = list(set(names))
    if len(unique_names) > 1:
        print(f"  {email}")
        for name in unique_names[:5]:
            print(f"    - '{name}'")
        print()
