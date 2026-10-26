import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.enums import Resampling as ResampleEnum
from rasterio import features
import numpy as np
from rasterstats import zonal_stats
import os

# -------------------------------
# 1️⃣ Paths
# -------------------------------

grid_path = "datasets/chennai_grid_with_features.gpkg"
dem_path = "datasets/dem/chennai_dem.tif"
projected_dem_path = "datasets/dem/dem_projected.tif"

# -------------------------------
# 2️⃣ Load grid
# -------------------------------

grid = gpd.read_file(grid_path)
print("Grid CRS:", grid.crs)

# -------------------------------
# 3️⃣ Reproject DEM to match grid CRS
# -------------------------------

with rasterio.open(dem_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs, grid.crs, src.width, src.height, *src.bounds
    )

    kwargs = src.meta.copy()
    kwargs.update({
        'crs': grid.crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open(projected_dem_path, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=grid.crs,
                resampling=Resampling.bilinear
            )

print("DEM reprojected.")

# -------------------------------
# 4️⃣ Compute slope
# -------------------------------

with rasterio.open(projected_dem_path) as src:
    dem = src.read(1)
    x, y = np.gradient(dem, src.res[0], src.res[1])
    slope = np.sqrt(x**2 + y**2)

    slope_meta = src.meta.copy()
    slope_meta.update(dtype=rasterio.float32)

    slope_path = "datasets/dem/slope.tif"
    with rasterio.open(slope_path, 'w', **slope_meta) as dst:
        dst.write(slope.astype(rasterio.float32), 1)

print("Slope raster created.")

# -------------------------------
# 5️⃣ Extract mean slope per grid
# -------------------------------

stats = zonal_stats(
    grid,
    slope_path,
    stats=["mean"],
    nodata=None
)

grid["slope_mean"] = [s["mean"] for s in stats]

# -------------------------------
# 6️⃣ Save updated dataset
# -------------------------------

grid.to_file("datasets/chennai_grid_with_slope.gpkg", driver="GPKG")

print("Slope feature added successfully!")