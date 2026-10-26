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
# Load DEM
# -------------------------
dem_path = "datasets/dem/chennai_dem.tif"

with rasterio.open(dem_path) as src:
    dem_crs = src.crs

print("DEM CRS:", dem_crs)

# -------------------------
# Reproject grid to DEM CRS
# -------------------------
grid = grid.to_crs(dem_crs)

print("Grid reprojected")

# -------------------------
# Compute elevation mean
# -------------------------
stats = zonal_stats(
    grid,
    dem_path,
    stats=["mean"]
)

grid["elev_mean_dem"] = [s["mean"] for s in stats]

# -------------------------
# Save result
# -------------------------
grid.to_file("datasets/grid_with_dem_stats.gpkg", driver="GPKG")

print("DEM statistics added successfully!")