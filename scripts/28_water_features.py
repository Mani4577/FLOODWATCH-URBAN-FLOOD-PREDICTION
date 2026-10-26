import geopandas as gpd
import pandas as pd

# -------------------------
# Load grid
# -------------------------
grid = gpd.read_file("datasets/chennai_grid_with_features.gpkg")

print("Grid cells:", len(grid))

# -------------------------
# Load waterways
# -------------------------
water = gpd.read_file("datasets/osm_raw/southern-zone-260102-free.shp/gis_osm_waterways_free_1.shp")
print("Waterway features:", len(water))

# -------------------------
# Match CRS
# -------------------------
water = water.to_crs(grid.crs)

# -------------------------
# Distance to water
# -------------------------
print("Computing distance to water...")

grid["dist_to_water"] = grid.geometry.apply(
    lambda geom: water.distance(geom).min()
)

# -------------------------
# Drainage density
# -------------------------
print("Computing drainage density...")

intersection = gpd.overlay(grid, water, how="intersection")

intersection["length"] = intersection.geometry.length

drain_length = (
    intersection.groupby("grid_id")["length"]
    .sum()
    .reset_index()
)

grid = grid.merge(drain_length, on="grid_id", how="left")

grid["length"] = grid["length"].fillna(0)

grid["drain_density"] = grid["length"] / grid.geometry.area

# -------------------------
# Save result
# -------------------------
grid.to_file("datasets/grid_with_water_features.gpkg", driver="GPKG")

print("Water features created successfully!")