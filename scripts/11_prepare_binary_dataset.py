import geopandas as gpd

# Load dataset
gdf = gpd.read_file("datasets/final_dataset.gpkg")

print("Dataset loaded:", len(gdf))
print("Columns:", gdf.columns)

# Convert flood_label → binary flooded
# 0 = no flood
# 1 or 2 = flooded

gdf["flooded"] = gdf["flood_label"].apply(lambda x: 1 if x > 0 else 0)

print("\nBinary flood distribution:")
print(gdf["flooded"].value_counts())

# Save new dataset
gdf.to_file("datasets/binary_dataset.gpkg", driver="GPKG")

print("\nBinary dataset saved successfully!")