import geopandas as gpd
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# Load model
# -----------------------------
model = joblib.load("models/rainfall_flood_model.pkl")

# -----------------------------
# Load grid
# -----------------------------
gdf = gpd.read_file("datasets/binary_dataset.gpkg")

print("Grid loaded:", len(gdf))

# -----------------------------
# Rainfall scenario
# -----------------------------
rain_today = 120
rain_3day = 220
rain_7day = 350

gdf["rain_today"] = rain_today
gdf["rain_3day"] = rain_3day
gdf["rain_7day"] = rain_7day

# -----------------------------
# Features
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
# Predict probability
# -----------------------------
gdf["flood_prob"] = model.predict_proba(X)[:,1]

print(gdf["flood_prob"].describe())

# -----------------------------
# Plot probability heatmap
# -----------------------------
fig, ax = plt.subplots(figsize=(10,10))

gdf.plot(
    column="flood_prob",
    cmap="Reds",
    linewidth=0.05,
    edgecolor="black",
    legend=True,
    ax=ax
)

plt.title("Chennai Flood Probability Map", fontsize=16)
plt.axis("off")

plt.show()