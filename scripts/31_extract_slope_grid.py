import geopandas as gpd
import rasterio
from rasterstats import zonal_stats

# -------------------------
# Load grid
# -------------------------
grid = gpd.read_file("datasets/chennai_grid_with_features.gpkg")

print("Grid loaded:", len(grid))
print("Grid CRS:", grid.crs)

# -------------------------
# Load slope raster
# -------------------------
slope_path = "datasets/dem/slope.tif"

with rasterio.open(slope_path) as src:
    raster_crs = src.crs

print("Slope CRS:", raster_crs)

# -------------------------
# Reproject grid to raster CRS
# -------------------------
grid = grid.to_crs(raster_crs)

print("Grid reprojected")

# -------------------------
# Extract slope statistics
# -------------------------
stats = zonal_stats(
    grid,
    slope_path,
    stats=["mean"]
)

grid["slope_mean"] = [s["mean"] for s in stats]

# -------------------------
# Save dataset
# -------------------------
grid.to_file("datasets/grid_with_slope.gpkg", driver="GPKG")

print("Slope added successfully!")