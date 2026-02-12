from fastapi import FastAPI
from app.modules.patients.router import router as patients_router
from app.modules.dentists.router import router as dentists_router
from app.modules.auth.router import router as auth_router
from app.modules.appointments.router import router as appointments_router
from app.modules.waiting_room.router import router as waiting_room_router

app = FastAPI();

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(patients_router, prefix="/patients", tags=["patients"])
app.include_router(dentists_router, prefix="/dentists", tags=["dentists"])
app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
app.include_router(waiting_room_router, prefix="/attention", tags=["attention"])

@app.get("/")
def root():
        return {"message": "Server started!"}