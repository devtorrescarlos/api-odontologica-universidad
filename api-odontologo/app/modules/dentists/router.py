from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.dentists import schema, service
from app.middlewares.validation import get_current_active_user
from app.db.models.models import User
from typing import List

router = APIRouter()

@router.post("/", response_model= schema.Dentist)
def create_dentist(dentist: schema.DentistCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.create_dentist(db=db, dentist=dentist)

@router.get("/", response_model=List[schema.Dentist])
def get_dentists(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.get_dentists(db=db)

@router.get("/{dentist_id}", response_model=schema.Dentist)
def get_dentist_by_id(dentist_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if dentist_id <= 0:
        raise HTTPException(status_code=400, detail="El ID del dentista debe ser un número positivo")
    
    db_dentist = service.get_dentist_by_id(db=db, dentist_id=dentist_id)
    if db_dentist is None:
        raise HTTPException(status_code=404, detail="Dentista no encontrado")
    return db_dentist

@router.put("/{dentist_id}", response_model= schema.Dentist)
def update_dentist(dentist_id: int, dentist: schema.DentistUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.update_dentist_by_id(db=db, dentist=dentist, dentist_id=dentist_id)

