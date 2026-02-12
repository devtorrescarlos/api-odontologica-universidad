from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

class PatientBase(BaseModel):
    email: EmailStr
    name: Annotated[str, Field(min_length=1, strict=True)]
    age: Annotated[int, Field(gt=0)]

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True
