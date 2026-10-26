import geopandas as gpd

# Load datasets
grid_slope = gpd.read_file("datasets/chennai_grid_with_slope.gpkg")
grid_labels = gpd.read_file("datasets/final_dataset.gpkg")

print("Slope file columns:", grid_slope.columns)
print("Label file columns:", grid_labels.columns)

# Merge using grid_id
merged = grid_slope.merge(
    grid_labels[["grid_id", "flood_label"]],
    on="grid_id",
    how="left"
)

print("After merge:", merged.columns)

# Save final dataset
merged.to_file("datasets/final_dataset_with_slope.gpkg", driver="GPKG")

print("Merged dataset saved successfully!")