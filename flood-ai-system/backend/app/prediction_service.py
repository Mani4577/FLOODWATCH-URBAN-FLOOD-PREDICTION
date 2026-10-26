import pandas as pd
import shap
import numpy as np
from .model_loader import get_model
from .config import FEATURE_COLUMNS
from .shap_service import format_shap_explanation


def risk_level_from_probability(p):
    if p < 0.3:
        return "GREEN"
    if p < 0.6:
        return "YELLOW"
    return "RED"


def duration_from_rain(total_mm):
    if total_mm < 50:
        return "few hours"
    if total_mm <= 100:
        return "1-2 days"
    return "3-5 days"


def predict_grid_cells(grid_gdf, rain_features):
    model = get_model()
    grid = grid_gdf.copy()

    # ---------------------------------------------
    # ADD RAIN FEATURES
    # ---------------------------------------------
    for f, v in rain_features.items():
        grid[f] = v

    # Ensure all features exist
    for col in FEATURE_COLUMNS:
        if col not in grid.columns:
            grid[col] = 0.0

    # Prepare input
    X = grid[FEATURE_COLUMNS].copy()
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    # ---------------------------------------------
    # MODEL PREDICTION
    # ---------------------------------------------
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[:, 1]
    else:
        prob = model.predict(X)

    grid["flood_probability"] = prob

    # ---------------------------------------------
    # ✅ RAIN LOGIC (ONLY ONCE — CLEAN)
    # ---------------------------------------------
    rain = grid["rain_3day"].fillna(0)

    rain_norm = rain / 100.0

    # Scale probability using rainfall
    grid["flood_probability"] *= (0.4 + rain_norm)

    # HARD RULE: no rain → almost no flood
    grid.loc[rain < 10, "flood_probability"] = 0.05

    # Clamp values
    grid["flood_probability"] = grid["flood_probability"].clip(0, 1)

    # ---------------------------------------------
    # FINAL LABELS
    # ---------------------------------------------
    grid["risk_level"] = grid["flood_probability"].apply(risk_level_from_probability)
    grid["duration"] = grid["rain_3day"].apply(duration_from_rain)

    # ---------------------------------------------
    # ✅ SHAP EXPLANATION (FIXED)
    # ---------------------------------------------
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        if isinstance(shap_values, list):
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

    except Exception as e:
        print("SHAP ERROR:", e)
        shap_values = np.zeros((len(X), len(FEATURE_COLUMNS)))

    explanation_records = []

    for idx in range(len(grid)):
        shap_row = shap_values[idx]

        explanation = format_shap_explanation(shap_row)

        explanation_records.append({
            "id": int(grid.index[idx]),
            "probability": float(grid.iloc[idx]["flood_probability"]),
            "risk_level": str(grid.iloc[idx]["risk_level"]),
            "duration": str(grid.iloc[idx]["duration"]),
            "main_causes": explanation
        })

    return grid, explanation_records