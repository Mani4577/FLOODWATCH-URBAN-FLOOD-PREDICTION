import geopandas as gpd
import pandas as pd
import numpy as np

grid = gpd.read_file("datasets/binary_dataset.gpkg")
rain = pd.read_csv("datasets/rainfall_features.csv").dropna()

samples = []

for i in range(1000):

    r = rain.sample(1).iloc[0]

    rain_today = r["Rainfall"]
    rain_3day = r["rain_3day"]
    rain_7day = r["rain_7day"]

    temp = grid.copy()

    temp["rain_today"] = rain_today
    temp["rain_3day"] = rain_3day
    temp["rain_7day"] = rain_7day

    # terrain vulnerability
    vulnerability = (
        (temp["flood_label"] > 0).astype(int)
    )

    # rainfall intensity factor
    rain_factor = np.clip(rain_3day / 200, 0, 1)

    # flood probability
    prob = vulnerability * rain_factor

    temp["flooded"] = np.random.binomial(1, prob)

    samples.append(temp)

dataset = pd.concat(samples)

dataset.to_file("datasets/rainfall_training_dataset.gpkg", driver="GPKG")

print("Dataset created:", len(dataset))