from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.waiting_room import schema, service
from app.middlewares.validation import get_current_active_user
from app.db.models.models import User

router = APIRouter()

@router.post("/arrive/{patient_id}", response_model=schema.PatientArrivalResponse)
def register_patient_arrival(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.register_arrival(db=db, patient_id=patient_id)

@router.get("/next", response_model=schema.NextPatientResponse)
def call_next_patient(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.call_next(db=db)

@router.get("/status", response_model=schema.WaitingRoomStatus)
def view_waiting_room(current_user: User = Depends(get_current_active_user)):
    return service.get_status()