import pytest
from datetime import datetime
from app.database import get_testing_db
from app import crud
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def clean_testing_db():
    # Borra todos los datos de la base de datos de prueba antes de cada prueba
    with get_testing_db() as db:
        db.query(crud.PropertyVisit).delete()
        db.commit()

def test_get_visits_by_employee_single_visit(client, clean_testing_db):
    # Creamos una visita para el empleado en la base de datos de prueba
    with get_testing_db() as db:
        visit_data = {
            "property_id": 1,
            "visit_date": datetime.now(),
            "visitor_name": "Employee Visit",
            "visitor_email": "employee.visit@example.com",
            "feedback": "Good visit!"
        }
        crud.create_property_visit(db=db, **visit_data)

    # Enviamos una solicitud al endpoint para obtener el informe de visitas del empleado
    response = client.get("/visits/employee/1")
    assert response.status_code == 200

    # Verificamos que el formato de la respuesta sea el correcto
    assert "employee_id" in response.json()
    assert "total_visits" in response.json()
    assert "total_distance" in response.json()

    # Verificamos que el ID del empleado en la respuesta sea correcto
    assert response.json()["employee_id"] == 1

    # Verificamos que el número total de visitas sea correcto
    assert response.json()["total_visits"] == 1

    # Dado que solo hay una visita, la distancia total debe ser cero
    assert response.json()["total_distance"] == 0
