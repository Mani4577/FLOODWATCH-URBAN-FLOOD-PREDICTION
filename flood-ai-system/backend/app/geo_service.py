import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from .config import SPATIAL_GRID_PATH, RADIUS_M


geolocator = Nominatim(user_agent="flood-ai-system")


def geocode_location(location: str):
    result = geolocator.geocode(location)
    if result is None:
        raise ValueError(f"Location not found: {location}")
    return {
        "address": result.address,
        "latitude": result.latitude,
        "longitude": result.longitude,
    }


def load_grid():
    grid = gpd.read_file(SPATIAL_GRID_PATH)
    if grid.crs is None:
        grid = grid.set_crs("EPSG:4326")
    return grid.to_crs("EPSG:4326")


def select_grid_cells(lat: float, lon: float, grid_gdf=None):
    if grid_gdf is None:
        grid_gdf = load_grid()

    point = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")
    point = point.to_crs("EPSG:3857")
    buffered = point.buffer(RADIUS_M)

    grid_proj = grid_gdf.to_crs("EPSG:3857")
    within_cells = grid_proj[grid_proj.intersects(buffered.iloc[0])]

    if within_cells.empty:
        return gpd.GeoDataFrame(columns=grid_gdf.columns, crs=grid_gdf.crs)

    return within_cells.to_crs("EPSG:4326")
