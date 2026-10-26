from fastapi import APIRouter
from pydantic import BaseModel
import osmnx as ox
import geopandas as gpd

from .geo_service import geocode_location, select_grid_cells
from .prediction_service import predict_grid_cells
from .rainfall_service import fetch_rainfall_forecast, compute_rain_features

router = APIRouter(prefix='/road-impact', tags=['road-impact'])


class RoadRequest(BaseModel):
    location: str


# -----------------------------
# FETCH ROADS FROM OSM
# -----------------------------
def fetch_roads(lat, lon, dist=1500):
    G = ox.graph_from_point((lat, lon), dist=dist, network_type='drive')
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

    roads = edges[['name', 'geometry']].copy()
    roads['name'] = roads['name'].fillna("Unnamed Road")

    return roads


# -----------------------------
# COMPUTE ROAD IMPACT
# -----------------------------
def compute_road_impacts(grid, lat, lon):
    import osmnx as ox
    import geopandas as gpd

    # -----------------------------
    # STEP 1: Get road network
    # -----------------------------
    G = ox.graph_from_point((lat, lon), dist=2000, network_type='drive')
    edges = ox.graph_to_gdfs(G, nodes=False)

    # -----------------------------
    # STEP 2: Clean road names
    # -----------------------------
    edges["name"] = edges["name"].fillna("")

    # Convert list names → string
    edges["name"] = edges["name"].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x
    )

    # Remove empty / unnamed roads
    edges = edges[
        (edges["name"] != "") &
        (~edges["name"].str.lower().str.contains("unnamed"))
    ]

    # -----------------------------
    # STEP 3: Spatial join
    # -----------------------------
    edges = edges.to_crs(grid.crs)

    joined = gpd.sjoin(
        edges,
        grid[["geometry", "risk_level"]],
        how="left",
        predicate="intersects"
    )

    # -----------------------------
    # STEP 4: Aggregate risk per road
    # -----------------------------
    road_risk = {}

    for _, row in joined.iterrows():
        name = row["name"]
        risk = row["risk_level"]

        if not name:
            continue

        if name not in road_risk:
            road_risk[name] = []

        if isinstance(risk, str):
            road_risk[name].append(risk)

    # -----------------------------
    # STEP 5: Final risk logic
    # -----------------------------
    final_results = []

    for road, risks in road_risk.items():

        if not risks:
            continue

        if "RED" in risks:
            final = "RED"
        elif "YELLOW" in risks:
            final = "YELLOW"
        else:
            final = "GREEN"

        final_results.append({
            "road_name": road,
            "risk_level": final
        })

    # -----------------------------
    # STEP 6: REMOVE DUPLICATES + LIMIT
    # -----------------------------
    # Sort by severity
    priority = {"RED": 0, "YELLOW": 1, "GREEN": 2}

    final_results = sorted(
        final_results,
        key=lambda x: priority[x["risk_level"]]
    )

    # LIMIT to top 10 roads (clean UI)
    final_results = final_results[:10]

    return final_results

# -----------------------------
# API ENDPOINT
# -----------------------------
@router.post('/')
def get_road_impact(request: RoadRequest):

    # STEP 1: LOCATION
    loc = geocode_location(request.location)

    # STEP 2: RAIN
    forecast = fetch_rainfall_forecast(loc["latitude"], loc["longitude"])
    rain_features = compute_rain_features(forecast)

    # STEP 3: GRID
    grid_cells = select_grid_cells(loc["latitude"], loc["longitude"])

    if grid_cells.empty:
        return []

    # STEP 4: PREDICTION
    grid_with_preds, _ = predict_grid_cells(grid_cells, rain_features)

    # STEP 5: ROAD IMPACT
    road_impacts = compute_road_impacts(
        grid_with_preds,
        loc["latitude"],
        loc["longitude"]
    )

    return road_impacts