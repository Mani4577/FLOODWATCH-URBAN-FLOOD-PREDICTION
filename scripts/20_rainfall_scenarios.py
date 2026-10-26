import geopandas as gpd
import joblib
import matplotlib.pyplot as plt

model = joblib.load("models/rainfall_flood_model.pkl")

gdf = gpd.read_file("datasets/binary_dataset.gpkg")

scenarios = [
    (50, 80, 120),
    (120, 220, 350),
    (200, 350, 500)
]

fig, axes = plt.subplots(1,3, figsize=(18,6))

for i, (r_today, r3, r7) in enumerate(scenarios):

    temp = gdf.copy()

    temp["rain_today"] = r_today
    temp["rain_3day"] = r3
    temp["rain_7day"] = r7

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

    X = temp[features]

    temp["prob"] = model.predict_proba(X)[:,1]

    temp.plot(
        column="prob",
        cmap="Reds",
        linewidth=0,
        legend=False,
        ax=axes[i]
    )

    axes[i].set_title(f"Rain Today = {r_today}mm")
    axes[i].axis("off")

plt.suptitle("Flood Risk Under Different Rainfall Scenarios", fontsize=16)

plt.show()