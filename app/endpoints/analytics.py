from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.utils import calculate_distance
from typing import List

router = APIRouter()

@router.get("/visits/employee/{employee_id}", response_model=schemas.EmployeeVisitsReport)
def get_visits_by_employee(employee_id: int, db: Session = Depends(get_db)):
    visits = crud.get_visits_by_employee(db, employee_id)
    
    total_visits = len(visits)
    total_distance = 0

    if total_visits < 2:
        return schemas.EmployeeVisitsReport(employee_id=employee_id, total_visits=total_visits, total_distance=0)

    for i in range(len(visits) - 1):
        property_location = (visits[i].property.latitude, visits[i].property.longitude)
        next_property_location = (visits[i + 1].property.latitude, visits[i + 1].property.longitude)
        
        distance = calculate_distance(property_location, next_property_location)
        if distance is not None:
            total_distance += distance

    return schemas.EmployeeVisitsReport(employee_id=employee_id, total_visits=total_visits, total_distance=total_distance)



