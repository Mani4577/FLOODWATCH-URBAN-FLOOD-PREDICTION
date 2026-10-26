import osmnx as ox
import geopandas as gpd
import os

# Download Chennai boundary
place_name = "Chennai, Tamil Nadu, India"

gdf = ox.geocode_to_gdf(place_name)

print("CRS:", gdf.crs)

# Save boundary
output_path = "datasets/boundary/chennai_boundary.shp"
gdf.to_file(output_path)

print("Boundary saved successfully!")