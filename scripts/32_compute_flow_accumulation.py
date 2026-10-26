import rasterio
import numpy as np
from scipy.ndimage import gaussian_filter

# Load DEM
with rasterio.open("datasets/dem/chennai_dem.tif") as src:
    dem = src.read(1)
    profile = src.profile

print("DEM loaded")

# Smooth DEM
dem = gaussian_filter(dem, sigma=1)

# Simple flow proxy (inverse elevation gradient)
flow = np.maximum(0, dem.max() - dem)

print("Flow accumulation proxy calculated")

profile.update(dtype=rasterio.float32)

with rasterio.open("datasets/dem/chennai_flow_acc.tif", "w", **profile) as dst:
    dst.write(flow.astype(rasterio.float32), 1)

print("Flow accumulation saved")