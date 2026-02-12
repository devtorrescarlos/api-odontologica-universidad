from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

class DentistBase(BaseModel):
    email: EmailStr
    name: Annotated[str, Field(min_length=1, strict=True)]
    age: Annotated[int, Field(gt=20)] # Dentist should be an adult, that's why his age should be >= 21
    speciality: Annotated[str, Field(min_length=1, strict=True)]

class DentistCreate(DentistBase):
    
    pass

class DentistUpdate(DentistBase):
    
    pass

class Dentist(DentistBase):
    id: int
    
    class Config:
        orm_mode = True