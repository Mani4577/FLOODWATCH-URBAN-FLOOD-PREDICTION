import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib

# --------------------------
# Load rainfall dataset
# --------------------------

gdf = gpd.read_file("datasets/rainfall_training_dataset.gpkg")

print("Dataset loaded:", len(gdf))

# --------------------------
# Feature list
# --------------------------

features = [
    "elev_mean",
    "elev_min",
    "elev_max",
    "elev_range",
    "dist_to_dr",
    "built_percent",
    "water_percent",
    "road_density",
    "rain_today",
    "rain_3day",
    "rain_7day"
]

X = gdf[features]
y = gdf["flooded"]

# --------------------------
# Train-test split
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------
# Train model
# --------------------------

model = XGBClassifier(
    n_estimators=400,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=10,   # IMPORTANT
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------
# Evaluate
# --------------------------

y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --------------------------
# Save model
# --------------------------

joblib.dump(model, "models/rainfall_flood_model.pkl")

print("\nModel saved: models/rainfall_flood_model.pkl")