import pandas as pd

df = pd.read_csv('data/ratings_proper.csv')

print("=== HASIL PREPROCESSING TERBARU ===")
print(f"Total ratings: {len(df)}")
print(f"Total users: {df['user_id'].nunique()}")
print(f"Total destinations: {df['destination_id'].nunique()}")
print(f"Destination retention: {df['destination_id'].nunique()/231*100:.2f}%")

item_counts = df.groupby('destination_id').size()
print(f"\nMin ratings/dest: {item_counts.min()}")
print(f"Mean ratings/dest: {item_counts.mean():.2f}")
print(f"Median ratings/dest: {item_counts.median():.0f}")
print(f"Max ratings/dest: {item_counts.max()}")

longtail = (item_counts <= 10).sum()
print(f"\nLong-tail items (<=10 ratings): {longtail} ({longtail/len(item_counts)*100:.1f}%)")

# Check columns
print(f"\nColumns in dataset: {df.columns.tolist()}")
