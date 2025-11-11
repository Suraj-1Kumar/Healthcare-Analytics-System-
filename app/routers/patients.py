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
def create_patient(patient: schemas.PatientCreate, db: Session):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# --- These are your original API endpoints ---
@router.post("/patients", response_model=schemas.Patient)
def api_create_patient_endpoint(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new patient.
    """
    return create_patient(patient=patient, db=db)

@router.get("/patients", response_model=list[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    API endpoint to read all patients.
    """
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a single patient by ID.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient