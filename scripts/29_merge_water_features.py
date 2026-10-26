import geopandas as gpd

# Load datasets
grid = gpd.read_file("datasets/grid_with_water_features.gpkg")
data = gpd.read_file("datasets/spatial_rainfall_dataset.gpkg")

print("Grid rows:", len(grid))
print("Dataset rows:", len(data))

# Keep only needed columns
grid = grid[["grid_id", "dist_to_water", "drain_density"]]

# Merge
data = data.merge(grid, on="grid_id", how="left")

# Save updated dataset
data.to_file("datasets/spatial_dataset_with_water.gpkg", driver="GPKG")

print("Water features merged successfully!")