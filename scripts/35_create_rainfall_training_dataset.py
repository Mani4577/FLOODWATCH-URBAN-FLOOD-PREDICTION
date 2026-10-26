import geopandas as gpd
import pandas as pd

# Load dataset
gdf = gpd.read_file("datasets/final_spatial_dataset.gpkg")

print("Original rows:", len(gdf))

# Keep only ONE record per grid
grid = gdf.drop_duplicates(subset="grid_id")

print("Unique grids:", len(grid))

# Load rainfall features
rain = pd.read_csv("datasets/rainfall_features.csv")

print("Rainfall records:", len(rain))

# Reduce rainfall samples (important for memory)
rain = rain.sample(200)

samples = []

for _, r in rain.iterrows():

    temp = grid.copy()

    temp["rain_today"] = r["Rainfall"]
    temp["rain_3day"] = r["rain_3day"]
    temp["rain_7day"] = r["rain_7day"]
    temp["rain_intensity"] = r["rain_intensity"]

    samples.append(temp)

dataset = pd.concat(samples)

print("Final dataset rows:", len(dataset))

dataset.to_file("datasets/rainfall_training_dataset.gpkg", driver="GPKG")

print("Rainfall training dataset created successfully")