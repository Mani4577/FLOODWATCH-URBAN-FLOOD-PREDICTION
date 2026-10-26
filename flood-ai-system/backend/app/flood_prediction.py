from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user
from .geo_service import geocode_location, select_grid_cells
from .rainfall_service import (
    fetch_rainfall_forecast,
    compute_rain_features,
    fetch_historical_rainfall,
    compute_historical_features
)
from .prediction_service import predict_grid_cells
from .schemas import PredictRequest
import numpy as np
from .road_impact import compute_road_impacts

router = APIRouter(prefix='/flood', tags=['flood'])


@router.post('/predict')
def flood_predict(
    request: PredictRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------
    # STEP 1: Geocoding
    # -----------------------------
    try:
        loc = geocode_location(request.location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Geocoding failed: {e}')

    # -----------------------------
    # STEP 2: Rainfall (REAL-TIME or HISTORICAL)
    # -----------------------------
    try:
        if request.date:
            # 🔁 HISTORICAL MODE
            historical = fetch_historical_rainfall(
                loc['latitude'],
                loc['longitude'],
                request.date
            )
            rain_features = compute_historical_features(historical)

        else:
            # 🌧 REAL-TIME MODE (UNCHANGED)
            forecast = fetch_rainfall_forecast(
                loc['latitude'],
                loc['longitude']
            )
            rain_features = compute_rain_features(forecast)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'Rainfall fetch failed: {e}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Rainfall fetch failed: {e}')

    # -----------------------------
    # STEP 3: Get Grid Cells
    # -----------------------------
    grid_cells = select_grid_cells(loc['latitude'], loc['longitude'])

    if grid_cells.empty:
        return {
            'location': loc,
            'flood_map': {'type': 'FeatureCollection', 'features': []},
            'alerts': ['No grid cells found in 5 km radius'],
            'explanations': []
        }

    # -----------------------------
    # STEP 4: Prediction
    # -----------------------------
    pred_grid, explanations = predict_grid_cells(grid_cells, rain_features)
    try:
        road_impacts = compute_road_impacts(
            pred_grid,
            loc['latitude'],
            loc['longitude']
        )
    except Exception :
        road_impacts = []
    # -----------------------------
    # STEP 5: Convert to GeoJSON
    # -----------------------------
    features = []
    for _, row in pred_grid.iterrows():
        props = {
            k: (float(v) if isinstance(v, (np.float32, np.float64))
                else int(v) if isinstance(v, (np.int32, np.int64))
                else v)
            for k, v in row.drop(labels=['geometry']).to_dict().items()
        }
        features.append({
            'type': 'Feature',
            'geometry': row.geometry.__geo_interface__,
            'properties': props
        })

    # -----------------------------
    # STEP 6: Response
    # -----------------------------
    return {
        'location': loc,
        'mode': "historical" if request.date else "realtime",   # ⭐ NEW (for UI clarity)
        'selected_date': request.date if request.date else None,  # ⭐ NEW
        'flood_map': {
            'type': 'FeatureCollection',
            'features': features
        },
        'alerts': [
            "⚠️ Flood Risk HIGH in this area"
            if any(e['risk_level'] == 'RED' for e in explanations)
            else ""
        ],
        'explanations': explanations,
        'rainfall': rain_features, # ⭐ NEW (helps in demo)
        'road_impacts': road_impacts,  
    }