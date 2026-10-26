import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("datasets/predicted_flood_map.gpkg")

fig, ax = plt.subplots(figsize=(8,8))

gdf.plot(
    column="predicted_flood",
    cmap="RdYlBu_r",
    legend=True,
    ax=ax
)

plt.title("Predicted Flood Risk Map (Chennai)")
plt.show()