from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    employee = auth.authenticate_employee(db, email=form_data.username, password=form_data.password)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(data={"sub": employee.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register-employee", response_model=schemas.Employee)
def register_user(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    repository = crud.get_employee_repository(db)
    db_employee = repository.get_employee_by_email(email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(employee.password)
    return repository.create_employee(name=employee.name, email=employee.email, password=hashed_password)
