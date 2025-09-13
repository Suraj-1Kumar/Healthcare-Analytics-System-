from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum
from .database import Base
import enum

# Define an Enum for user roles
class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    PATIENT = "Patient"

# User model for authentication
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole))

# Patient model
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(50))
    contact_number = Column(String(20), unique=True)

# Doctor model
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    specialization = Column(String(255), index=True)
    contact_number = Column(String(20), unique=True)

# Appointment model
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    appointment_date = Column(DateTime)
    reason = Column(String(255))
    status = Column(String(50), default="Scheduled")
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))