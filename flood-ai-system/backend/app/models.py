from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(256), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FloodReport(Base):
    __tablename__ = 'flood_reports'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    location = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text)
    image_url = Column(String(512))
    water_level = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship('User')

class HistoricalFlood(Base):
    __tablename__ = 'historical_floods'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    event_name = Column(String(256), nullable=False)
    description = Column(Text)
    affected_areas = Column(Text)
    rainfall = Column(Float)
    image_url = Column(String(512))
