from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.models.models import Patient
from app.modules.patients.schema import PatientCreate, PatientUpdate


def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(email=patient.email, name=patient.name, age=patient.age)
    
    # Validation
    patient_exist = db.query(Patient).filter(Patient.email == patient.email).first()
    if patient_exist:
        raise HTTPException(status_code=409, detail="El paciente ya existe")
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient 

def get_all_patients(db: Session):
    return db.query(Patient).all()

def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="El paciente no existe")
    return patient

def update_patient_by_id(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="El paciente no existe")
    
    for key, value in patient.model_dump(exclude_unset=True).items():
        setattr(db_patient, key, value)
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient  

def delete_patient_by_id(db: Session, patient_id: int):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="El paciente no existe")
    db.delete(db_patient)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Paciente eliminado correctamente"
        }
    )   