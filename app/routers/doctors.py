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
def create_doctor(doctor: schemas.DoctorCreate, db: Session):
    db_doctor = models.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# --- These are your original API endpoints ---
@router.post("/doctors", response_model=schemas.Doctor)
def api_create_doctor_endpoint(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new doctor.
    """
    return create_doctor(doctor=doctor, db=db)

@router.get("/doctors", response_model=list[schemas.Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    API endpoint to read all doctors.
    """
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    return doctors

@router.get("/doctors/{doctor_id}", response_model=schemas.Doctor)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a single doctor by ID.
    """
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor