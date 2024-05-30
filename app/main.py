# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.endpoints import employees, properties, visits, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(properties.router, prefix="/properties", tags=["properties"])
app.include_router(visits.router, prefix="/visits", tags=["visits"])

