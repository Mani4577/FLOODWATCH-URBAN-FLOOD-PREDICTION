import os

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY",
    "3e53dca3ec22776c74c279341b50e126"
)

# model path
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "models", "rainfall_flood_model.pkl")
    ),
)

# spatial grid path (FIXED)
SPATIAL_GRID_PATH = os.getenv(
    "SPATIAL_GRID_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "spatial_grid.geojson"))
)

RADIUS_M = 2000

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://devakireddy:dev123@localhost:5432/flooddb"
)

FEATURE_COLUMNS = [
    "elev_mean",
    "elev_range",
    "slope_mean",
    "flow_acc_mean",
    "dist_to_dr",
    "dist_to_water",
    "drain_density",
    "built_percent",
    "water_percent",
    "road_density",
    "rain_today",
    "rain_3day",
    "rain_7day",
    "rain_intensity",
    "rain_14day"
]