from pydantic import BaseModel
from typing import Dict, List, Any,Optional
from datetime import datetime


class PredictRequest(BaseModel):
    location: str
    date: Optional[str] = None   # NEW FIELD

class LocationResponse(BaseModel):
    address: str
    latitude: float
    longitude: float

class GridPrediction(BaseModel):
    id: Any
    probability: float
    risk_level: str
    duration: str
    shap: Dict[str, float]

class PredictResponse(BaseModel):
    location: LocationResponse
    flood_map: Dict[str, Any]
    alerts: List[str]
    explanations: List[Dict[str, Any]]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class AlertCreate(BaseModel):
    location: str
    message: str
    severity: str

class AlertResponse(AlertCreate):
    id: int
    timestamp: str
    class Config:
        orm_mode = True

class FloodReportCreate(BaseModel):
    location: str
    latitude: float
    longitude: float
    description: str
    water_level: float

class FloodReportResponse(FloodReportCreate):
    id: int
    user_id: int
    image_url: str | None
    timestamp: str
    class Config:
        orm_mode = True

class HistoricalFloodResponse(BaseModel):
    id: int
    year: int
    event_name: str
    description: str
    affected_areas: str
    rainfall: float
    image_url: str | None
    class Config:
        orm_mode = True
