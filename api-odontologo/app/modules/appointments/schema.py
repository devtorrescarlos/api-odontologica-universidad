from pydantic import BaseModel, Field
from typing_extensions import Annotated
from datetime import date, time

class AppointmentBase(BaseModel):
    date: date
    time: time
    reason: Annotated[str, Field(min_length=1, strict=True, max_length=255)]
    patient_id: int
    dentist_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
