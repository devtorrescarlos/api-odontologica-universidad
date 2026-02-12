from pydantic import BaseModel
from typing import List

class PatientArrivalResponse(BaseModel):
    message: str
    position: int

class NextPatientResponse(BaseModel):
    attending_to: str
    id: int
    remaining_patients: int

class WaitingRoomStatus(BaseModel):
    queue_ids: List[int]
    total: int
