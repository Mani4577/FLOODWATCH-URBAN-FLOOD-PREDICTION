import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import os

# -------------------------------
# 1️⃣ Load grid
# -------------------------------

grid_path = "datasets/chennai_grid_500m.shp"
grid = gpd.read_file(grid_path)

print("Grid CRS:", grid.crs)

# -------------------------------
# 2️⃣ Load DEM
# -------------------------------

dem_path = "datasets/dem/chennai_dem.tif"
dem = rasterio.open(dem_path)

print("DEM CRS:", dem.crs)

# -------------------------------
# 3️⃣ Reproject grid to DEM CRS
# -------------------------------

if grid.crs != dem.crs:
    grid = grid.to_crs(dem.crs)

# -------------------------------
# 4️⃣ Compute elevation statistics
# -------------------------------

stats = zonal_stats(
    grid,
    dem_path,
    stats=["mean", "min", "max"],
    nodata=dem.nodata
)

# Add stats to grid
grid["elev_mean"] = [s["mean"] for s in stats]
grid["elev_min"] = [s["min"] for s in stats]
grid["elev_max"] = [s["max"] for s in stats]

grid["elev_range"] = grid["elev_max"] - grid["elev_min"]

print("Elevation features added.")

# -------------------------------
# 5️⃣ Save updated grid
# -------------------------------

output_path = "datasets/chennai_grid_with_elevation.shp"
grid.to_file(output_path)

print("Elevation extraction completed successfully!")