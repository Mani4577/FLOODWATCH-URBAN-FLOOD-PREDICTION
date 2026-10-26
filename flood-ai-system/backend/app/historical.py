from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db
from .auth import get_current_user

router = APIRouter(prefix='/historical', tags=['historical'])

@router.get('/', response_model=List[schemas.HistoricalFloodResponse])
def get_historical(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.HistoricalFlood).order_by(models.HistoricalFlood.year.desc()).all()
