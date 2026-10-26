from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db
from .auth import get_current_user

router = APIRouter(prefix='/alerts', tags=['alerts'])

@router.post('/', response_model=schemas.AlertResponse)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get('/', response_model=List[schemas.AlertResponse])
def list_alerts(severity: str = None, location: str = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    query = db.query(models.Alert)
    if severity:
        query = query.filter(models.Alert.severity == severity)
    if location:
        query = query.filter(models.Alert.location.ilike(f"%{location}%"))
    return query.order_by(models.Alert.timestamp.desc()).all()
