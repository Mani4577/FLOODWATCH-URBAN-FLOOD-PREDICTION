import geopandas as gpd
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# 1️⃣ Load trained model
# -----------------------------
model = joblib.load("models/rainfall_flood_model.pkl")

# -----------------------------
# 2️⃣ Load grid dataset
# -----------------------------
gdf = gpd.read_file("datasets/binary_dataset.gpkg")

print("Grid loaded:", len(gdf))

# -----------------------------
# 3️⃣ Example rainfall scenario
# -----------------------------
# You can change these values later
rain_today = 120
rain_3day = 220
rain_7day = 350

gdf["rain_today"] = rain_today
gdf["rain_3day"] = rain_3day
gdf["rain_7day"] = rain_7day

# -----------------------------
# 4️⃣ Select model features
# -----------------------------
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

# -----------------------------
# 5️⃣ Predict flood probability
# -----------------------------
gdf["flood_prob"] = model.predict_proba(X)[:,1]

# -----------------------------
# 6️⃣ Convert to risk levels
# -----------------------------
def risk_level(p):
    if p > 0.7:
        return "High"
    elif p > 0.4:
        return "Moderate"
    else:
        return "Low"

gdf["risk"] = gdf["flood_prob"].apply(risk_level)

print(gdf["risk"].value_counts())

# -----------------------------
# 7️⃣ Plot flood prediction map
# -----------------------------
fig, ax = plt.subplots(figsize=(10,10))

gdf.plot(
    column="risk",
    cmap="RdYlGn_r",   # green → yellow → red
    linewidth=0.1,
    edgecolor="black",
    legend=True,
    ax=ax
)

plt.title("Chennai Flood Prediction Map", fontsize=16)
plt.axis("off")

plt.show()