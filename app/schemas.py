from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    email: str

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes= True

class PropertyBase(BaseModel):
    address: str
    location: str
    price: float
    description: str

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    address: Optional[str] = None
    location: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Property(PropertyBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

class PropertyVisitBase(BaseModel):
    employee_id: int
    property_id: int
    visit_date: datetime
    visitor_name: str
    visitor_email: str

class PropertyVisitCreate(PropertyVisitBase):
    feedback: Optional[str] = None

class PropertyVisitUpdate(PropertyVisitBase):
    property_id: Optional[int] = None
    employee_id: Optional[int] = None
    feedback: Optional[str] = None

class PropertyVisit(PropertyVisitBase):
    id: int
    employee_id: Optional[int] = None
    feedback: Optional[str] = None

    class Config:
        from_attributes = True

class EmployeeVisitsReport(BaseModel):
    employee_id: int
    total_visits: int
    total_distance: float

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None