from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import DATABASE_URL
from .database import Base, engine
from .schemas import PredictRequest
from .geo_service import geocode_location, select_grid_cells
from .rainfall_service import (
    fetch_rainfall_forecast,
    compute_rain_features,
    fetch_historical_rainfall,
    compute_historical_features
)
from .prediction_service import predict_grid_cells
from .auth import router as auth_router
from .reports import router as reports_router
from .historical import router as historical_router
from .road_impact import router as road_impact_router
from .flood_prediction import router as flood_router

app = FastAPI(title="Flood Monitoring Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(reports_router)
app.include_router(historical_router)
app.include_router(road_impact_router)
app.include_router(flood_router)


@app.on_event("startup")
def on_startup():
    print(f"Connecting to database: {DATABASE_URL}")
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Flood Monitoring backend is running"}


@app.post("/predict")
def predict(request: PredictRequest):
    # -----------------------------
    # STEP 1: Geocode Location
    # -----------------------------
    try:
        loc = geocode_location(request.location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Geocoding failed: {e}")

    # -----------------------------
    # STEP 2: Rainfall (REAL-TIME / HISTORICAL)
    # -----------------------------
    try:
        if request.date:
            # 🔁 HISTORICAL MODE
            historical = fetch_historical_rainfall(
                loc["latitude"],
                loc["longitude"],
                request.date
            )
            rain_features = compute_historical_features(historical)

        else:
            # 🌧 REAL-TIME MODE (UNCHANGED)
            forecast = fetch_rainfall_forecast(
                loc["latitude"],
                loc["longitude"]
            )
            rain_features = compute_rain_features(forecast)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Rainfall fetch failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rainfall fetch failed: {e}")

    # -----------------------------
    # STEP 3: Get Grid Cells
    # -----------------------------
    grid_cells = select_grid_cells(loc["latitude"], loc["longitude"])

    if grid_cells.empty:
        return {
            "location": loc,
            "mode": "historical" if request.date else "realtime",
            "selected_date": request.date if request.date else None,
            "flood_map": {"type": "FeatureCollection", "features": []},
            "alerts": ["No grid cells found in 5 km radius"],
            "explanations": [],
        }

    # -----------------------------
    # STEP 4: Prediction
    # -----------------------------
    grid_with_preds, explanations = predict_grid_cells(grid_cells, rain_features)

    # -----------------------------
    # STEP 5: Convert to GeoJSON
    # -----------------------------
    features = []
    for _, row in grid_with_preds.iterrows():
        props = row.drop(labels=["geometry"]).to_dict()
        features.append({
            "type": "Feature",
            "geometry": row.geometry.__geo_interface__,
            "properties": props,
        })

    flood_map = {"type": "FeatureCollection", "features": features}

    # -----------------------------
    # STEP 6: Alerts
    # -----------------------------
    alerts = []
    if any(ex["risk_level"] == "RED" for ex in explanations):
        alerts.append("⚠️ Flood Risk HIGH in this area")
    elif any(ex["risk_level"] == "YELLOW" for ex in explanations):
        alerts.append("⚠️ Flood Risk MEDIUM in this area")

    # -----------------------------
    # STEP 7: Final Response
    # -----------------------------
    return {
        "location": loc,
        "mode": "historical" if request.date else "realtime",   # ⭐ NEW
        "selected_date": request.date if request.date else None, # ⭐ NEW
        "flood_map": flood_map,
        "alerts": alerts,
        "explanations": explanations,
        "zones": [
            {
                "id": ex["id"],
                "probability": ex["probability"],
                "risk_level": ex["risk_level"],
                "duration": ex["duration"],
            }
            for ex in explanations
        ],
        "rainfall": rain_features,
        "summary": {
            "total_cells": len(explanations),
            "high_risk_cells": sum(1 for ex in explanations if ex["risk_level"] == "RED"),
            "medium_risk_cells": sum(1 for ex in explanations if ex["risk_level"] == "YELLOW"),
            "low_risk_cells": sum(1 for ex in explanations if ex["risk_level"] == "GREEN"),
        },
    }
