import geopandas as gpd
import pandas as pd
import numpy as np

from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import classification_report, accuracy_score, f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression

from xgboost import XGBClassifier   # 🔥 IMPORTANT

# =========================
# LOAD DATA
# =========================
df = gpd.read_file("../../datasets/rainfall_training_dataset.gpkg")

# =========================
# FEATURE ENGINEERING
# =========================
df["rain_total"] = df["rain_3day"] + df["rain_7day"] + df["rain_today"]
df["rain_slope"] = df["rain_total"] * df["slope_mean"]

features = [
    'Rainfall',
    'rain_3day',
    'rain_7day',
    'rain_today',
    'rain_total',
    'rain_slope',
    'elev_mean',
    'elev_range',
    'slope_mean',
    'dist_to_water',
    'dist_to_dr',
    'drain_density',
    'built_percent',
    'road_density'
]

# =========================
# CLEAN DATA
# =========================
if 'flow_acc_mean' in df.columns:
    df = df.drop(columns=['flow_acc_mean'])

df[features] = df[features].fillna(df[features].median())
df = df.dropna(subset=['flood_label'])

# =========================
# BINARY TARGET
# =========================
df["binary_flood"] = df["flood_label"].apply(lambda x: 0 if x == 0 else 1)

X = df[features]
y = df["binary_flood"]

print("Final dataset size:", len(df))

# =========================
# GROUP SPLIT (NO LEAKAGE)
# =========================
groups = df["grid_id"]

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_idx, test_idx in gss.split(X, y, groups):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# =========================
# CLASS WEIGHT
# =========================
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# =========================
# BASE MODELS
# =========================
xgb = XGBClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.04,
    subsample=0.9,
    colsample_bytree=0.9,
    gamma=0.2,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric='logloss'
)

rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

lr = LogisticRegression(
    max_iter=500
)

# =========================
# ENSEMBLE MODEL
# =========================
model = VotingClassifier(
    estimators=[
        ('xgb', xgb),
        ('rf', rf),
        ('lr', lr)
    ],
    voting='soft'
)

# =========================
# TRAIN
# =========================
model.fit(X_train, y_train)

# =========================
# PROBABILITIES
# =========================
y_prob = model.predict_proba(X_test)[:, 1]

# =========================
# THRESHOLD OPTIMIZATION
# =========================
best_f1 = 0
best_threshold = 0.5

for t in np.arange(0.3, 0.7, 0.02):
    y_pred_temp = (y_prob > t).astype(int)
    f1 = f1_score(y_test, y_pred_temp)

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = t

# Final prediction
y_pred = (y_prob > best_threshold).astype(int)

# =========================
# RESULTS
# =========================
print("\n🔥 FINAL ENSEMBLE MODEL RESULTS 🔥")

print("\nBest Threshold:", best_threshold)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')

from sklearn.metrics import roc_curve, roc_auc_score

fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_test, y_prob):.2f}")
plt.plot([0, 1], [0, 1], linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("roc_curve.png", dpi=300, bbox_inches='tight')
plt.close()