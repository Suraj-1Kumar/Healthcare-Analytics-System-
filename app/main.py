from fastapi import FastAPI
from . import models
from .database import engine
from .routers import patients, doctors, appointments, auth

# Create ann instance of the FastAPI class
app = FastAPI()

# Tags for better organization in the API docs
app.include_router(auth.router, tags=["Authentication"])
app.include_router(patients.router, tags=["Patients"])
app.include_router(doctors.router, tags=["Doctors"])
app.include_router(appointments.router, tags=["Appointments"])

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)



# Define a route for the root url ("/")
@app.get("/")
def read_root():
    return {"message": "Welcome to the Healthcare Patient Analytics System API!"}