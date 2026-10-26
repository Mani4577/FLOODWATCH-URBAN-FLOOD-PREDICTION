import os
from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from .auth import get_current_user
from datetime import datetime

router = APIRouter(prefix='/reports', tags=['reports'])
UPLOAD_DIR = 'uploads/flood_reports'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=schemas.FloodReportResponse)
def create_report(
    location: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    description: str = Form(None),
    water_level: float = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[1]
        filename = f"{int(datetime.utcnow().timestamp())}_{user.id}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(image.file.read())
        image_url = f"/uploads/flood_reports/{filename}"
    report = models.FloodReport(
        user_id=user.id,
        location=location,
        latitude=latitude,
        longitude=longitude,
        description=description,
        image_url=image_url,
        water_level=water_level,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get('/', response_model=List[schemas.FloodReportResponse])
def get_reports(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.FloodReport).order_by(models.FloodReport.timestamp.desc()).all()
