import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import jwt
from . import models, schemas
from .database import SessionLocal

JWT_SECRET = os.getenv('JWT_SECRET', 'supersecret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

router = APIRouter(prefix='/auth', tags=['auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@router.post('/register', response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail='User already exists')
    user_obj = models.User(username=user.username, email=user.email, password_hash=create_password_hash(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@router.post('/login', response_model=schemas.TokenResponse)
def login(form: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    token = create_access_token({'sub': user.username})
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/me', response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
