from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models.models import Appointment
from app.modules.appointments.schema import AppointmentCreate, AppointmentUpdate

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(
        date=appointment.date,
        time=appointment.time,
        reason=appointment.reason,
        patient_id=appointment.patient_id,
        dentist_id=appointment.dentist_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()

def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def update_appointment_by_id(db: Session, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    for key, value in appointment.model_dump(exclude_unset=True).items():
        setattr(db_appointment, key, value)
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment_by_id(db: Session, appointment_id: int):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    db.delete(db_appointment)
    db.commit()
    return {"message": "Cita eliminada correctamente"}
