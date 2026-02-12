from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models.models import Dentist
from app.modules.dentists.schema import DentistCreate, DentistUpdate

def create_dentist(db: Session, dentist: DentistCreate):
    db_dentist = Dentist(email=dentist.email, name=dentist.name, age=dentist.age, speciality=dentist.speciality)
    
    dentist_exist = db.query(Dentist).filter(Dentist.email == dentist.email).first()
    if dentist_exist:
        raise HTTPException(status_code=409, detail="El dentista ya existe")
    
    db.add(db_dentist)
    db.commit()
    db.refresh(db_dentist)
    return db_dentist

def update_dentist_by_id(db: Session, dentist: DentistUpdate, dentist_id: int):
    db_dentist = db.query(Dentist).filter(Dentist.id == dentist_id).first()
    if not db_dentist:
        raise HTTPException(status_code=404, detail="El dentista no existe")
    
    for key, value in dentist.model_dump(exclude_unset=True).items():
        setattr(db_dentist, key, value)
    
    db.add(db_dentist)
    db.commit()
    db.refresh(db_dentist)
    return db_dentist  

def get_dentists(db: Session):
    return db.query(Dentist).all()

def get_dentist_by_id(db: Session, dentist_id: int):
    return db.query(Dentist).filter(Dentist.id == dentist_id).first()

def delete_dentist_by_id(db: Session, dentist_id: int):
    db_dentist = db.query(Dentist).filter(Dentist.id == dentist_id).first()
    if not db_dentist:
        raise HTTPException(status_code=404, detail="El dentista no existe")
    
    db.delete(db_dentist)
    db.commit()
    return {"message": "Dentista eliminado correctamente"}

