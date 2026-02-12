from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.modules.appointments import schema, service
from app.middlewares.validation import get_current_active_user
from app.db.models.models import User

router = APIRouter()

@router.post("/", response_model=schema.Appointment, status_code=201)
def create_appointment(appointment: schema.AppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.create_appointment(db=db, appointment=appointment)

@router.get("/", response_model=List[schema.Appointment])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.get_appointments(db=db, skip=skip, limit=limit)

@router.get("/{appointment_id}", response_model=schema.Appointment)
def get_appointment_by_id(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if appointment_id <= 0:
        raise HTTPException(status_code=400, detail="El ID de la cita debe ser un número positivo")
    
    db_appointment = service.get_appointment_by_id(db=db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return db_appointment

@router.put("/{appointment_id}", response_model=schema.Appointment)
def update_appointment(appointment_id: int, appointment: schema.AppointmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service.update_appointment_by_id(db=db, appointment_id=appointment_id, appointment=appointment)

@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if appointment_id <= 0:
        raise HTTPException(status_code=400, detail="El ID de la cita debe ser un número positivo")
    
    service.delete_appointment_by_id(db=db, appointment_id=appointment_id)
    return {"message": "Cita eliminada correctamente"}
