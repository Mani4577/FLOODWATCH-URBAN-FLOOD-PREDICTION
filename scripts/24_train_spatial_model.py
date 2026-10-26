import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib

# -----------------------------
# Load dataset
# -----------------------------
gdf = gpd.read_file("datasets/final_spatial_dataset.gpkg")
print("Original dataset rows:", len(gdf))

# -----------------------------
# Keep only ONE record per grid
# -----------------------------
gdf = gdf.drop_duplicates(subset="grid_id")

print("Unique grids:", len(gdf))

# -----------------------------
# Feature Engineering
# -----------------------------

# Terrain runoff interaction
gdf["elev_slope"] = gdf["elev_mean"] * gdf["slope_mean"]

# Urban runoff interaction
gdf["built_slope"] = gdf["built_percent"] * gdf["slope_mean"]

# Water accumulation indicator
gdf["water_drain"] = gdf["water_percent"] * gdf["drain_density"]

# Urban flood susceptibility
gdf["built_water"] = gdf["built_percent"] * gdf["water_percent"]

# -----------------------------
# Feature List
# -----------------------------
features = [
    "elev_mean",
    "elev_range",
    "slope_mean",
    "flow_acc_mean",     # <-- ADD THIS

    "dist_to_dr",
    "dist_to_water",
    "drain_density",

    "built_percent",
    "water_percent",
    "road_density",

    # engineered features
    "elev_slope",
    "built_slope",
    "water_drain",
    "built_water"
]

X = gdf[features]
y = gdf["flooded"]

# -----------------------------
# Train/Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# -----------------------------
# Train Model
# -----------------------------
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
model = XGBClassifier(
    n_estimators=800,
    max_depth=8,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    gamma=0.2,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "models/flood_susceptibility_model.pkl")

print("\nModel saved: models/flood_susceptibility_model.pkl")