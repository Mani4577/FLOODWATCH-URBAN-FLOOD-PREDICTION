import geopandas as gpd

# Load datasets
grid = gpd.read_file("datasets/grid_with_dem_stats.gpkg")
data = gpd.read_file("datasets/spatial_rainfall_dataset.gpkg")

print("Grid rows:", len(grid))
print("Dataset rows:", len(data))

# Keep only needed columns
grid = grid[["grid_id", "elev_mean_dem"]]

# Merge DEM feature
data = data.merge(grid, on="grid_id", how="left")

# Create elevation difference feature
data["elev_diff"] = data["elev_mean_dem"] - data["elev_mean"]

# Save updated dataset
data.to_file("datasets/spatial_dataset_with_dem.gpkg", driver="GPKG")

print("DEM features merged successfully!")