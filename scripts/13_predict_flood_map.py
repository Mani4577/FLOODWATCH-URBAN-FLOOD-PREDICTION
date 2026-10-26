import geopandas as gpd
import joblib

# --------------------------
# Load trained model
# --------------------------

model = joblib.load("models/flood_model.pkl")

print("Model loaded successfully")

# --------------------------
# Load grid dataset
# --------------------------

gdf = gpd.read_file("datasets/binary_dataset.gpkg")

print("Grid loaded:", len(gdf))

# --------------------------
# Select features
# --------------------------

features = [
    "elev_mean",
    "elev_min",
    "elev_max",
    "elev_range",
    "dist_to_dr",
    "built_percent",
    "water_percent",
    "road_density"
]

X = gdf[features]

# --------------------------
# Predict flooding
# --------------------------

gdf["predicted_flood"] = model.predict(X)

print("\nPrediction distribution:")
print(gdf["predicted_flood"].value_counts())

# --------------------------
# Save prediction map
# --------------------------

output_path = "datasets/predicted_flood_map.gpkg"

gdf.to_file(output_path, driver="GPKG")

print("\nFlood prediction map saved:", output_path)