import geopandas as gpd
import rasterio
import numpy as np
from rasterstats import zonal_stats

# Load grid dataset (small dataset)
grid = gpd.read_file("datasets/chennai_grid_with_features.gpkg")

print("Grid loaded:", len(grid))

# Load DEM
dem_path = "datasets/dem/chennai_dem.tif"

with rasterio.open(dem_path) as src:
    dem = src.read(1)
    transform = src.transform

print("DEM loaded")

# Compute slope
gy, gx = np.gradient(dem)
slope = np.sqrt(gx**2 + gy**2)

print("Slope calculated")

# Extract slope per grid
stats = zonal_stats(
    grid,
    slope,
    affine=transform,
    stats=["mean"],
    nodata=0
)

grid["slope_mean"] = [s["mean"] for s in stats]

print("Slope added")

# Save grid dataset
grid.to_file("datasets/grid_with_slope.gpkg", driver="GPKG")

print("Saved grid_with_slope.gpkg")