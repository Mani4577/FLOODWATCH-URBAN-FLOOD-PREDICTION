import geopandas as gpd
import os
import pandas as pd

# -------------------------------
# 1️⃣ Load grid with elevation
# -------------------------------

grid_path = "datasets/chennai_grid_with_elevation.shp"
grid = gpd.read_file(grid_path)

print("Grid loaded:", len(grid))

# -------------------------------
# 2️⃣ Load waterways & water bodies
# -------------------------------

waterways_path = "datasets/osm_raw/southern-zone-260102-free.shp/gis_osm_waterways_free_1.shp"
water_path = "datasets/osm_raw/southern-zone-260102-free.shp/gis_osm_water_a_free_1.shp"

waterways = gpd.read_file(waterways_path)
water = gpd.read_file(water_path)

print("Waterways:", len(waterways))
print("Water bodies:", len(water))

# -------------------------------
# 3️⃣ Reproject to grid CRS
# -------------------------------

waterways = waterways.to_crs(grid.crs)
water = water.to_crs(grid.crs)

# Combine both
drainage = gpd.GeoDataFrame(
    pd.concat([waterways, water], ignore_index=True),
    crs=grid.crs
)

# -------------------------------
# 4️⃣ Compute distance to nearest drainage
# -------------------------------

grid["dist_to_drainage"] = grid.geometry.apply(
    lambda x: drainage.distance(x).min()
)

print("Drainage distance feature added.")

# -------------------------------
# 5️⃣ Save updated grid
# -------------------------------

output_path = "datasets/chennai_grid_with_elevation_drainage.shp"
grid.to_file(output_path)

print("Drainage feature extraction completed!")