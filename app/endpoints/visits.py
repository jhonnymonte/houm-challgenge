from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas,auth
from app.models import PropertyVisit
from datetime import datetime
from app.database import get_db
from typing import List
router = APIRouter()

@router.post("/", response_model=schemas.PropertyVisit)
async def create_property_visit(visit: schemas.PropertyVisitCreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    current_employee = await auth.get_current_employee(db, token)
    repository = crud.get_property_visit_repository(db)
    return repository.create_property_visit(
        property_id=visit.property_id,
        visit_date=visit.visit_date,
        visitor_name=visit.visitor_name,
        visitor_email=visit.visitor_email,
        employee_id=current_employee.id,  # Asignar el ID del empleado actual
        feedback=visit.feedback  # Asegurarse de pasar el feedback
    )

@router.get("/{visit_id}", response_model=schemas.PropertyVisit)
def read_property_visit(visit_id: int, db: Session = Depends(get_db)):
    db_visit = crud.get_property_visit(db, visit_id=visit_id)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit

@router.put("/{visit_id}", response_model=schemas.PropertyVisit)
def update_property_visit(visit_id: int, visit: schemas.PropertyVisitUpdate, db: Session = Depends(get_db)):
    db_visit = crud.update_property_visit(db=db, visit_id=visit_id, property_visit=visit)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit

@router.delete("/{visit_id}", response_model=schemas.PropertyVisit)
def delete_property_visit(visit_id: int, db: Session = Depends(get_db)):
    db_visit = crud.delete_property_visit(db=db, visit_id=visit_id)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit

@router.get("/employee/{employee_id}", response_model=List[schemas.PropertyVisit])
async def get_visits_by_employee(employee_id: int, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    current_employee = await auth.get_current_employee(db, token)
    if current_employee.id != employee_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    visits = crud.get_visits_by_employee(db, employee_id)
    if not visits:
        raise HTTPException(status_code=404, detail="No visits found for this employee")
    return visits