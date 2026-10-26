import geopandas as gpd
from shapely.geometry import box
import numpy as np
import os

# -------------------------------
# 1️⃣ Load Chennai boundary
# -------------------------------

boundary_path = "datasets/boundary/chennai_boundary.shp"
boundary = gpd.read_file(boundary_path)

print("Original CRS:", boundary.crs)

# -------------------------------
# 2️⃣ Reproject to UTM (meters)
# Chennai is in UTM Zone 44N
# EPSG:32644
# -------------------------------

boundary = boundary.to_crs(epsg=32644)

print("Projected CRS:", boundary.crs)

# -------------------------------
# 3️⃣ Create 500m grid
# -------------------------------

xmin, ymin, xmax, ymax = boundary.total_bounds

grid_size = 500  # meters

rows = int(np.ceil((ymax - ymin) / grid_size))
cols = int(np.ceil((xmax - xmin) / grid_size))

polygons = []

for i in range(cols):
    for j in range(rows):
        x1 = xmin + i * grid_size
        y1 = ymin + j * grid_size
        x2 = x1 + grid_size
        y2 = y1 + grid_size
        polygons.append(box(x1, y1, x2, y2))

grid = gpd.GeoDataFrame({"geometry": polygons}, crs="EPSG:32644")

# -------------------------------
# 4️⃣ Clip grid to boundary
# -------------------------------

grid_clipped = gpd.overlay(grid, boundary, how="intersection")

print("Number of grid cells:", len(grid_clipped))

# -------------------------------
# 5️⃣ Save grid
# -------------------------------

output_path = "datasets/chennai_grid_500m.shp"
grid_clipped.to_file(output_path)

print("Grid created and saved successfully!")