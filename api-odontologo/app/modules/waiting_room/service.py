from sqlalchemy.orm import Session
from fastapi import HTTPException
from collections import deque
from datetime import date

from app.db.models.models import Patient, Appointment

waiting_room = deque()

def register_arrival(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
    today = date.today()
    appointment = db.query(Appointment).filter(
        Appointment.patient_id == patient_id,
        Appointment.date == today
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=400, detail=f"El paciente {patient.name} no tiene una cita programada para hoy.")

    if patient_id in waiting_room:
        raise HTTPException(status_code=400, detail="El paciente ya está en la sala de espera")

    waiting_room.append(patient_id)
    
    return {
        "message": f"Paciente {patient.name} registrado en la sala de espera",
        "position": len(waiting_room)
    }

def call_next(db: Session):
    if not waiting_room:
        raise HTTPException(status_code=404, detail="No hay pacientes en la sala de espera")

    # 5. FIFO Logic: Remove the first one (Dequeue)
    next_id = waiting_room.popleft()
    
    patient = db.query(Patient).filter(Patient.id == next_id).first()
    
    if not patient:
         raise HTTPException(status_code=404, detail=f"Internal Error: Patient with ID {next_id} not found.")

    return {
        "attending_to": patient.name,
        "id": patient.id,
        "remaining_patients": len(waiting_room)
    }

def get_status():
    return {"queue_ids": list(waiting_room), "total": len(waiting_room)}
