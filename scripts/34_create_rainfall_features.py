import pandas as pd

# Load rainfall dataset
df = pd.read_csv("datasets/rainfall/e5c275eb-a4f2-4412-9677-73654e8f5f4d.csv")

print("Rows:", len(df))

# Convert date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Sort by date
df = df.sort_values("Date")

# Rolling rainfall windows
df["rain_3day"] = df["Rainfall"].rolling(3).sum()
df["rain_7day"] = df["Rainfall"].rolling(7).sum()

# Rainfall intensity
df["rain_intensity"] = df["Rainfall"] / (df["rain_3day"] + 1)

# Remove NaN rows
df = df.dropna()

# Save features
df.to_csv("datasets/rainfall_features.csv", index=False)

print("Rainfall features created successfully")