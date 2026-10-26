import rasterio
import numpy as np

# Load DEM
with rasterio.open("datasets/dem/chennai_dem.tif") as src:
    dem = src.read(1)
    transform = src.transform
    profile = src.profile

print("DEM loaded")

# Compute gradients
x, y = np.gradient(dem)

# Compute slope
slope = np.sqrt(x**2 + y**2)

print("Slope calculated")

# Save slope raster
profile.update(dtype=rasterio.float32)

with rasterio.open("datasets/dem/chennai_slope.tif", "w", **profile) as dst:
    dst.write(slope.astype(rasterio.float32), 1)

print("Slope saved: datasets/dem/chennai_slope.tif")