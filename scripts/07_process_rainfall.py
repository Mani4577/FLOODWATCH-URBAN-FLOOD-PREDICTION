import pandas as pd

# -------------------------------
# 1️⃣ Load rainfall CSV
# -------------------------------

path = "datasets/rainfall/e5c275eb-a4f2-4412-9677-73654e8f5f4d.csv"
df = pd.read_csv(path)

print("Original rows:", len(df))

# -------------------------------
# 2️⃣ Remove duplicates
# -------------------------------

df = df.drop_duplicates()

print("After removing duplicates:", len(df))

# -------------------------------
# 3️⃣ Convert Date
# -------------------------------

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# -------------------------------
# 4️⃣ Convert rainfall to numeric
# -------------------------------

df["Rainfall"] = pd.to_numeric(df["Rainfall"], errors="coerce")

# -------------------------------
# 5️⃣ Daily aggregation (city-level)
# -------------------------------

daily = df.groupby("Date")["Rainfall"].agg([
    "mean",
    "max",
    "sum"
]).reset_index()

daily.rename(columns={
    "mean": "rain_mean",
    "max": "rain_max",
    "sum": "rain_total"
}, inplace=True)

# -------------------------------
# 6️⃣ 3-day cumulative rainfall
# -------------------------------

daily = daily.sort_values("Date")
daily["rain_3day"] = daily["rain_total"].rolling(3).sum()

# -------------------------------
# 7️⃣ Save processed rainfall
# -------------------------------

output_path = "datasets/rainfall/processed_rainfall.csv"
daily.to_csv(output_path, index=False)

print("Rainfall processed successfully!")
print(daily.head())