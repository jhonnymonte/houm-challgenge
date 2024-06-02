import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Employee
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def client():
    return TestClient(app)

def test_read_employee(client, db):
    employee = Employee(name="John Doe", email="john@example.com", hashed_password="hash123")
    db.add(employee)
    db.commit()

    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"

def test_update_employee(client, db):
    employee = Employee(name="Jane Smith", email="jane@example.com", hashed_password="hash456")
    db.add(employee)
    db.commit()

    updated_data = {"name": "Jane Doe"}
    response = client.put("/employees/1", json=updated_data)
    assert response.status_code == 200

    db.refresh(employee)
    assert employee.name == "Jane Doe"

def test_delete_employee(client, db):
    employee = Employee(name="Sam Brown", email="sam@example.com", hashed_password="hash789")
    db.add(employee)
    db.commit()

    response = client.delete("/employees/1")
    assert response.status_code == 200

    deleted_employee = db.query(Employee).filter(Employee.id == 1).first()
    assert deleted_employee is None
