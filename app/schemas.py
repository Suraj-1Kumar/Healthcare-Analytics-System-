from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime
from typing import Optional, List
from .models import UserRole



# --- SCHEMAS FOR AUTHENTICATION ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class User(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None




# Patient Schemas

class PatientBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_of_birth: date
    gender: str
    contact_number: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



# Doctor Schemas

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    contact_number: str

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



# Appointment Schemas

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    reason: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None    