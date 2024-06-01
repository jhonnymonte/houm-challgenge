from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel
from typing import Optional



class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    visits = relationship("PropertyVisit", back_populates="employee")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    location = Column(String)
    price = Column(Float)
    description = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    visits = relationship("PropertyVisit", back_populates="property")


class PropertyVisit(Base):
    __tablename__ = "property_visits"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    visit_date = Column(DateTime, nullable=False)
    visitor_name = Column(String, nullable=False)
    visitor_email = Column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    feedback = Column(String, nullable=True)

    property = relationship("Property", back_populates="visits")
    employee = relationship("Employee")
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None