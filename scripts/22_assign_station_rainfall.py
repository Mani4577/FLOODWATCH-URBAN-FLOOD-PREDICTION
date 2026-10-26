import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load grid
grid = gpd.read_file("datasets/binary_dataset.gpkg")

# Load station data
stations = pd.read_csv("datasets/rainfall_stations.csv")

# Convert to GeoDataFrame
stations["geometry"] = stations.apply(
    lambda x: Point(x["lon"], x["lat"]), axis=1
)

stations = gpd.GeoDataFrame(stations, geometry="geometry", crs="EPSG:4326")

# Convert grid CRS
grid = grid.to_crs(epsg=32644)
stations = stations.to_crs(epsg=32644)
# Compute nearest station
nearest = gpd.sjoin_nearest(grid, stations, how="left")

# Assign station name to grid
grid["station"] = nearest["station"]

print(grid["station"].value_counts())

# Save updated dataset
grid.to_file("datasets/grid_with_station.gpkg", driver="GPKG")

print("Station assignment completed!")