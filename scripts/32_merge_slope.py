import geopandas as gpd

# Load datasets
grid = gpd.read_file("datasets/grid_with_slope.gpkg")
data = gpd.read_file("datasets/spatial_dataset_with_water.gpkg")

print("Grid rows:", len(grid))
print("Dataset rows:", len(data))

# Keep only needed columns
grid = grid[["grid_id", "slope_mean"]]

# Merge slope feature
data = data.merge(grid, on="grid_id", how="left")

# Save updated dataset
data.to_file("datasets/final_spatial_dataset.gpkg", driver="GPKG")

print("Slope merged successfully!")