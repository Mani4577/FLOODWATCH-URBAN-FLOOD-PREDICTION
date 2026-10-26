import pandas as pd

df = pd.read_csv("datasets/rainfall/e5c275eb-a4f2-4412-9677-73654e8f5f4d.csv")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# daily mean rainfall across stations
daily = df.groupby("Date")["Rainfall"].mean().reset_index()

# rainfall features
daily["rain_3day"] = daily["Rainfall"].rolling(3).sum()
daily["rain_7day"] = daily["Rainfall"].rolling(7).sum()

print(daily.head())

daily.to_csv("datasets/rainfall_features.csv", index=False)

print("Rainfall features created!")