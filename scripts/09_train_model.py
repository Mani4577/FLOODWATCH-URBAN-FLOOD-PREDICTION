import geopandas as gpd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier

# -------------------------------
# 1️⃣ Load dataset
# -------------------------------

data_path = "datasets/final_dataset_with_slope.gpkg"
gdf = gpd.read_file(data_path)

print("Dataset loaded:", len(gdf))

# -------------------------------
# 2️⃣ Select features
# -------------------------------

features = [
    "elev_mean",
    "elev_min",
    "elev_max",
    "elev_range",
    "dist_to_dr", 
    "slope_mean",       # NEW FEATURE       # ← use this
    "built_percent",
    "water_percent",
    "road_density"
]


X = gdf[features]
y = gdf["flood_label"]  # shapefile truncated name

# -------------------------------
# 3️⃣ Train-test split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 4️⃣ Train Random Forest
# -------------------------------
# Initialize XGBoost model
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    objective="multi:softmax",
    num_class=3,
    random_state=42,
    use_label_encoder=False,
    eval_metric="mlogloss"
)

# Train model
model.fit(X_train, y_train)

# -------------------------------
# 5️⃣ Evaluate
# -------------------------------

y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -------------------------------
# 6️⃣ Feature Importance
# -------------------------------

importances = pd.Series(model.feature_importances_, index=features)
print("\nFeature Importance:")
print(importances.sort_values(ascending=False))