from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.auth import schema, service

router = APIRouter()

@router.post("/register", response_model=schema.UserResponse, status_code=201)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db=db, user=user)

@router.post("/login", response_model=schema.Token)
def login(
    login_data: schema.LoginRequest,
    db: Session = Depends(get_db),
):
    user = service.authenticate_user(db, login_data.username, login_data.password)
    access_token = service.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=15),
    )
    return {"access_token": access_token, "token_type": "bearer"}