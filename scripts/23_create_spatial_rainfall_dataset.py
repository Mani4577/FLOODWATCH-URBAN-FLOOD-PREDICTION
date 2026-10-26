import geopandas as gpd
import pandas as pd

# -----------------------------
# Load grid with station info
# -----------------------------
grid = gpd.read_file("datasets/grid_with_station.gpkg")

print("Grid loaded:", len(grid))

# -----------------------------
# Load rainfall dataset
# -----------------------------
rain = pd.read_csv("datasets/rainfall/e5c275eb-a4f2-4412-9677-73654e8f5f4d.csv")

# Convert date
rain["Date"] = pd.to_datetime(rain["Date"], dayfirst=True)

print("Rainfall rows:", len(rain))

# -----------------------------
# Compute rainfall features
# -----------------------------
rain = rain.sort_values("Date")

rain["rain_3day"] = rain.groupby("Station")["Rainfall"].rolling(3).sum().reset_index(level=0, drop=True)
rain["rain_7day"] = rain.groupby("Station")["Rainfall"].rolling(7).sum().reset_index(level=0, drop=True)

# Remove NaNs
rain = rain.dropna()

print("After rolling windows:", len(rain))

# -----------------------------
# Merge rainfall with grid
# -----------------------------
dataset = grid.merge(
    rain,
    left_on="station",
    right_on="Station",
    how="left"
)

print("Merged rows:", len(dataset))

# Remove duplicate column
dataset = dataset.drop(columns=["Station"])

# Save dataset
dataset.to_file("datasets/spatial_rainfall_dataset.gpkg", driver="GPKG")

print("Spatial rainfall dataset created!")