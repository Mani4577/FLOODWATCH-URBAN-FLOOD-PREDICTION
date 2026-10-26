import geopandas as gpd
import pandas as pd

# -------------------------------
# 1️⃣ Load grid with features
# -------------------------------

grid_path = "datasets/chennai_grid_with_features.gpkg"
grid = gpd.read_file(grid_path)

grid = grid.to_crs(epsg=32644)
grid["grid_id"] = grid.index

print("Grid loaded:", len(grid))

# -------------------------------
# 2️⃣ Load flood hazard polygons
# -------------------------------

flood_path = "datasets/flood_labels/1bfef958-d4cc-4e50-a926-445e65bac7a8 (1).kml"
flood = gpd.read_file(flood_path)

flood = flood.to_crs(grid.crs)

print("Flood polygons:", len(flood))

# -------------------------------
# 3️⃣ Spatial join
# -------------------------------

joined = gpd.sjoin(grid, flood, how="left", predicate="intersects")

# -------------------------------
# 4️⃣ Create severity label
# -------------------------------

def map_severity(x):
    if x == "HIGH":
        return 2
    elif x == "MODERATE":
        return 1
    else:
        return 0

joined["flood_label"] = joined["CATEGORY"].apply(map_severity)

# Some grid cells may have duplicates → take max severity
final_labels = joined.groupby("grid_id")["flood_label"].max()

grid["flood_label"] = grid["grid_id"].map(final_labels).fillna(0)

# -------------------------------
# 5️⃣ Save final dataset
# -------------------------------

output_path = "datasets/final_dataset.gpkg"
grid.to_file(output_path, driver="GPKG")

print("Flood labels added successfully!")
print(grid["flood_label"].value_counts())