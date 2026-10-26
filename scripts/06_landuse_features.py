import geopandas as gpd
import pandas as pd

# -------------------------------
# 1️⃣ Load grid
# -------------------------------
grid_path = "datasets/chennai_grid_with_elevation_drainage.shp"
grid = gpd.read_file(grid_path)

print("Grid loaded:", len(grid))

# Add unique ID
grid["grid_id"] = grid.index

# Project to metric CRS
grid = grid.to_crs(epsg=32644)

# -------------------------------
# 2️⃣ Load OSM layers
# -------------------------------
base_path = "datasets/osm_raw/southern-zone-260102-free.shp/"

landuse = gpd.read_file(base_path + "gis_osm_landuse_a_free_1.shp")
buildings = gpd.read_file(base_path + "gis_osm_buildings_a_free_1.shp")
roads = gpd.read_file(base_path + "gis_osm_roads_free_1.shp")
water = gpd.read_file(base_path + "gis_osm_water_a_free_1.shp")

# Reproject all
landuse = landuse.to_crs(grid.crs)
buildings = buildings.to_crs(grid.crs)
roads = roads.to_crs(grid.crs)
water = water.to_crs(grid.crs)

# -------------------------------
# 3️⃣ Grid area
# -------------------------------
grid["grid_area"] = grid.geometry.area

# -------------------------------
# 4️⃣ Built-up %
# -------------------------------
built_join = gpd.sjoin(buildings, grid, how="inner", predicate="intersects")

built_join["area"] = built_join.geometry.area

built_area = built_join.groupby("grid_id")["area"].sum()

grid["built_area"] = grid["grid_id"].map(built_area).fillna(0)
grid["built_percent"] = (grid["built_area"] / grid["grid_area"]) * 100

# -------------------------------
# 5️⃣ Water %
# -------------------------------
water_join = gpd.sjoin(water, grid, how="inner", predicate="intersects")

water_join["area"] = water_join.geometry.area

water_area = water_join.groupby("grid_id")["area"].sum()

grid["water_area"] = grid["grid_id"].map(water_area).fillna(0)
grid["water_percent"] = (grid["water_area"] / grid["grid_area"]) * 100

# -------------------------------
# 6️⃣ Road density
# -------------------------------
road_join = gpd.sjoin(roads, grid, how="inner", predicate="intersects")

road_join["length"] = road_join.geometry.length

road_length = road_join.groupby("grid_id")["length"].sum()

grid["road_length"] = grid["grid_id"].map(road_length).fillna(0)
grid["road_density"] = grid["road_length"] / grid["grid_area"]

# -------------------------------
# 7️⃣ Save
# -------------------------------
output_path = "datasets/chennai_grid_with_features.gpkg"
grid.to_file(output_path, driver="GPKG")

print("Land use features added successfully!")