import geopandas as gpd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier
import xgboost as xgb
import joblib

# -----------------------------
# Load rainfall training dataset
# -----------------------------
gdf = gpd.read_file("datasets/rainfall_training_dataset.gpkg")
print("Dataset loaded:", len(gdf))

# -----------------------------
# Feature list (expand if available)
# -----------------------------
features = [
    "elev_mean",
    "elev_range",
    "slope_mean",
    "flow_acc_mean",
    "dist_to_dr",
    "dist_to_water",
    "drain_density",
    "built_percent",
    "water_percent",
    "road_density",
    "rain_today",
    "rain_3day",
    "rain_7day",
    "rain_intensity"
]

# Ensure features exist in data
missing = [f for f in features if f not in gdf.columns]
if missing:
    raise ValueError(f"Missing features in dataset: {missing}")

# Optional derived features
if "rain_14day" not in gdf.columns and "rain_7day" in gdf.columns:
    if "date" in gdf.columns:
        try:
            gdf = gdf.sort_values("date")
        except Exception:
            gdf = gdf.sort_values("date", na_position="last")
    gdf["rain_14day"] = gdf.groupby("grid_id")["rain_today"].transform(lambda x: x.rolling(14, min_periods=1).sum())
    features.append("rain_14day")

# -----------------------------
# Grid-based split (retain spatial generalization)
# -----------------------------
unique_grids = gdf["grid_id"].unique()
train_grids, test_grids = train_test_split(unique_grids, test_size=0.2, random_state=42)
train_data_full = gdf[gdf["grid_id"].isin(train_grids)]
test_data = gdf[gdf["grid_id"].isin(test_grids)]

train_base_grids, val_grids = train_test_split(train_grids, test_size=0.15, random_state=42)
train_data = gdf[gdf["grid_id"].isin(train_base_grids)]
val_data = gdf[gdf["grid_id"].isin(val_grids)]

X_train = train_data[features]
y_train = train_data["flooded"]
X_val = val_data[features]
y_val = val_data["flooded"]
X_test = test_data[features]
y_test = test_data["flooded"]

print("Training rows:", len(X_train))
print("Validation rows:", len(X_val))
print("Testing rows:", len(X_test))
print("Train grids:", len(train_base_grids))
print("Validation grids:", len(val_grids))
print("Test grids:", len(test_grids))

# -----------------------------
# Handle class imbalance
# -----------------------------
pos_ratio = (y_train == 1).mean()
scale_pos_weight = (1 - pos_ratio) / max(pos_ratio, 1e-6)
print(f"scale_pos_weight: {scale_pos_weight:.2f}")

# -----------------------------
# Hyperparameter search
# -----------------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
param_dist = {
    "n_estimators": [100, 200, 300, 400],
    "max_depth": [3, 4, 5, 6],
    "learning_rate": [0.01, 0.02, 0.03, 0.05],
    "subsample": [0.6, 0.7, 0.8, 0.9],
    "colsample_bytree": [0.6, 0.7, 0.8, 0.9],
    "min_child_weight": [1, 2, 3, 4],
    "gamma": [0, 1, 2],
    "reg_alpha": [0, 0.1, 0.5],
    "reg_lambda": [1, 2, 4]
}

xgb_model = XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1,
    verbosity=0,
)

search = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param_dist,
    n_iter=40,
    scoring="accuracy",
    cv=cv,
    verbose=1,
    random_state=42,
    n_jobs=-1,
)

search.fit(X_train, y_train)
best_model = search.best_estimator_

print("\nBest params:", search.best_params_)
print(f"Best CV accuracy: {search.best_score_:.4f}")

# -----------------------------
# Early stopping via xgboost.cv using best params
# -----------------------------
cv_dtrain = xgb.DMatrix(X_train, label=y_train)
params_for_cv = {
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "eta": best_model.learning_rate,
    "max_depth": best_model.max_depth,
    "subsample": best_model.subsample,
    "colsample_bytree": best_model.colsample_bytree,
    "min_child_weight": best_model.min_child_weight,
    "gamma": best_model.gamma,
    "reg_alpha": best_model.reg_alpha,
    "reg_lambda": best_model.reg_lambda,
    "scale_pos_weight": scale_pos_weight,
    "verbosity": 0,
}

cv_results = xgb.cv(
    params=params_for_cv,
    dtrain=cv_dtrain,
    num_boost_round=best_model.n_estimators,
    nfold=5,
    stratified=True,
    early_stopping_rounds=25,
    metrics="auc",
    seed=42,
    as_pandas=True,
    verbose_eval=False,
)

best_n_estimators = len(cv_results)
print(f"Best n_estimators from cv: {best_n_estimators}")

best_model.set_params(n_estimators=best_n_estimators)
best_model.fit(X_train, y_train, verbose=False)

# -----------------------------
# Final evaluation
# -----------------------------
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

# -----------------------------
# Save best model
# -----------------------------
joblib.dump(best_model, "models/rainfall_flood_model.pkl")
print("\nModel saved: models/rainfall_flood_model.pkl")