from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- This is the function main.py will import and use ---
def create_appointment(appointment: schemas.AppointmentCreate, db: Session):
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# --- These are your original API endpoints ---
@router.post("/appointments", response_model=schemas.Appointment)
def api_create_appointment_endpoint(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new appointment.
    """
    return create_appointment(appointment=appointment, db=db)

@router.get("/appointments", response_model=list[schemas.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    API endpoint to read all appointments.
    """
    appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    return appointments