from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas,auth
from app.database import get_db
from app.auth import get_current_employee
router = APIRouter()

@router.post("/", response_model=schemas.Property)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    current_employee = get_current_employee(db, token)
    repository = crud.get_property_repository(db)
    return repository.create_property(
        address=property.address,
        location=property.location,
        price=property.price,
        description=property.description
    )

@router.put("/{property_id}", response_model=schemas.Property)
def update_property(property_id: int, property: schemas.PropertyUpdate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    current_employee = get_current_employee(db, token)
    repository = crud.get_property_repository(db)
    updated_property = repository.update_property(property_id=property_id, property_update=property)
    if not updated_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated_property

@router.get("/{property_id}", response_model=schemas.Property)
def read_property(property_id: int, db: Session = Depends(get_db), current_user: schemas.Employee = Depends(get_current_employee)):
    db_property = crud.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property



@router.delete("/{property_id}", response_model=schemas.Property)
def delete_property(property_id: int, db: Session = Depends(get_db), current_user: schemas.Employee = Depends(get_current_employee)):
    db_property = crud.delete_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property
