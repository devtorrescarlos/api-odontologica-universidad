from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.patients import schema, service
from app.middlewares.validation import get_current_active_user
from app.db.models.models import User
from typing import List

router = APIRouter()

@router.post("/", response_model=schema.Patient)
def create_patient(patient: schema.PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.create_patient(db=db, patient=patient)

@router.get("/", response_model=List[schema.Patient])
def get_all_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.get_all_patients(db=db)

@router.get("/{patient_id}", response_model=schema.Patient)
def get_patient_by_id(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.get_patient_by_id(db=db, patient_id=patient_id) 

@router.put("/{patient_id}", response_model=schema.Patient)
def update_patient(patient_id: int, patient: schema.PatientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.update_patient_by_id(db=db, patient_id=patient_id, patient=patient)

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.delete_patient_by_id(db=db, patient_id=patient_id)

