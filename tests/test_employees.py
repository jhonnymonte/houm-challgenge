import pytest
from fastapi.testclient import TestClient
from app.main import app  # suponiendo que tu aplicación FastAPI se llama 'app'
from app.models import Employee
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

# Configuración para las pruebas
@pytest.fixture
def db():
    # Crea una base de datos temporal para las pruebas
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def client():
    # Crea un cliente de prueba para interactuar con la aplicación FastAPI
    return TestClient(app)

# Casos de prueba para cada endpoint
def test_read_employee(client, db):
    # Agrega algunos datos de prueba a la base de datos
    employee = Employee(name="John Doe", email="john@example.com", hashed_password="hash123")
    db.add(employee)
    db.commit()

    # Realiza una solicitud al endpoint y verifica la respuesta
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"

def test_update_employee(client, db):
    # Agrega algunos datos de prueba a la base de datos
    employee = Employee(name="Jane Smith", email="jane@example.com", hashed_password="hash456")
    db.add(employee)
    db.commit()

    # Realiza una solicitud PUT al endpoint para actualizar el empleado
    updated_data = {"name": "Jane Doe"}
    response = client.put("/employees/1", json=updated_data)
    assert response.status_code == 200

    # Verifica que el empleado se haya actualizado correctamente en la base de datos
    db.refresh(employee)
    assert employee.name == "Jane Doe"

def test_delete_employee(client, db):
    # Agrega algunos datos de prueba a la base de datos
    employee = Employee(name="Sam Brown", email="sam@example.com", hashed_password="hash789")
    db.add(employee)
    db.commit()

    # Realiza una solicitud DELETE al endpoint para eliminar el empleado
    response = client.delete("/employees/1")
    assert response.status_code == 200

    # Verifica que el empleado se haya eliminado correctamente de la base de datos
    deleted_employee = db.query(Employee).filter(Employee.id == 1).first()
    assert deleted_employee is None
