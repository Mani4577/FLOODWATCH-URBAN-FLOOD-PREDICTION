import geopandas as gpd
import rasterio
import numpy as np

# Load grid dataset
grid = gpd.read_file("datasets/final_spatial_dataset.gpkg")
print("Grid loaded:", len(grid))

# Open raster
with rasterio.open("datasets/dem/chennai_flow_acc.tif") as src:
    raster = src.read(1)
    transform = src.transform
    print("Raster loaded")

# Function to sample raster at grid centroid
values = []

for geom in grid.geometry:
    x, y = geom.centroid.x, geom.centroid.y
    row, col = rasterio.transform.rowcol(transform, x, y)

    try:
        values.append(raster[row, col])
    except:
        values.append(np.nan)

# Add feature
grid["flow_acc_mean"] = values

print("Flow accumulation values extracted")

# Save dataset
grid.to_file("datasets/final_spatial_dataset.gpkg", driver="GPKG")

print("Dataset updated successfully")