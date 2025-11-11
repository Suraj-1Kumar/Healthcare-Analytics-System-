from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from .routers import (
    patients as api_patients,
    doctors as api_doctors,
    appointments as api_appointments,
    auth
)
from datetime import date, datetime

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. Mount the 'static' directory to serve CSS, JS, etc.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 2. Setup Jinja2 templates to render HTML
templates = Jinja2Templates(directory="templates")

# 3. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Web Page Routes (Serving HTML) ===

@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    """
    Display the main dashboard page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/patients", response_class=HTMLResponse)
def get_patients_page(request: Request, db: Session = Depends(get_db)):
    """
    Display the patients page with a list of all patients.
    """
    patients_list = db.query(models.Patient).all()
    return templates.TemplateResponse("patients.html", {"request": request, "patients": patients_list})

@app.post("/patients", response_class=RedirectResponse)
def create_patient_form(
    db: Session = Depends(get_db),
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: date = Form(...),
    gender: str = Form(...),
    contact_number: str = Form(...)
):
    """
    Handle form submission to create a new patient.
    """
    patient_data = schemas.PatientCreate(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        contact_number=contact_number
    )
    # We re-use the function from our API router
    api_patients.create_patient(patient=patient_data, db=db)
    # Redirect back to the patients page
    return RedirectResponse(url="/patients", status_code=303)


@app.get("/doctors", response_class=HTMLResponse)
def get_doctors_page(request: Request, db: Session = Depends(get_db)):
    """
    Display the doctors page with a list of all doctors.
    """
    doctors_list = db.query(models.Doctor).all()
    return templates.TemplateResponse("doctors.html", {"request": request, "doctors": doctors_list})

@app.post("/doctors", response_class=RedirectResponse)
def create_doctor_form(
    db: Session = Depends(get_db),
    first_name: str = Form(...),
    last_name: str = Form(...),
    specialization: str = Form(...),
    contact_number: str = Form(...)
):
    """
    Handle form submission to create a new doctor.
    """
    doctor_data = schemas.DoctorCreate(
        first_name=first_name,
        last_name=last_name,
        specialization=specialization,
        contact_number=contact_number
    )
    api_doctors.create_doctor(doctor=doctor_data, db=db)
    return RedirectResponse(url="/doctors", status_code=303)


@app.get("/appointments", response_class=HTMLResponse)
def get_appointments_page(request: Request, db: Session = Depends(get_db)):
    """
    Display the appointments page with lists of patients, doctors, and appointments.
    """
    appointments_list = db.query(models.Appointment).all()
    patients_list = db.query(models.Patient).all()
    doctors_list = db.query(models.Doctor).all()
    return templates.TemplateResponse(
        "appointments.html", 
        {
            "request": request, 
            "appointments": appointments_list,
            "patients": patients_list,
            "doctors": doctors_list
        }
    )

@app.post("/appointments", response_class=RedirectResponse)
def create_appointment_form(
    db: Session = Depends(get_db),
    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    appointment_date: datetime = Form(...),
    reason: str = Form(...)
):
    """
    Handle form submission to create a new appointment.
    """
    appointment_data = schemas.AppointmentCreate(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        reason=reason,
        status="Scheduled" # Default status
    )
    # We re-use the function from our API router
    api_appointments.create_appointment(appointment=appointment_data, db=db)
    # Redirect back to the appointments page
    return RedirectResponse(url="/appointments", status_code=303)


# === API Routes (Serving JSON) ===
# We keep these API routers, prefixed with /api, in case a mobile app needs them later.
app.include_router(auth.router, prefix="/api", tags=["API - Authentication"])
app.include_router(api_patients.router, prefix="/api", tags=["API - Patients"])
app.include_router(api_doctors.router, prefix="/api", tags=["API - Doctors"])
app.include_router(api_appointments.router, prefix="/api", tags=["API - Appointments"])