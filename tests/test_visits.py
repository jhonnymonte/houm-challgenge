from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app.models import Base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app import crud

# Creamos una sesión de prueba para la base de datos
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creamos las tablas de la base de datos
Base.metadata.create_all(bind=engine)

# Creamos una instancia de TestClient
client = TestClient(app)

# Pruebas unitarias para el enrutador router
def test_create_property_visit():
    response = client.post(
        "/property-visit/",
        json={
            "property_id": 1,
            "visit_date": datetime.now().isoformat(),
            "visitor_name": "John Doe",
            "visitor_email": "john.doe@example.com",
            "feedback": "Great visit!"
        }
    )
    assert response.status_code == 200
    assert response.json()["visitor_name"] == "John Doe"

def test_read_property_visit():
    # Primero creamos una visita de propiedad para leer
    db = TestingSessionLocal()
    new_visit = crud.create_property_visit(
        db=db,
        property_id=1,
        visit_date=datetime.now(),
        visitor_name="Jane Smith",
        visitor_email="jane.smith@example.com",
        feedback="Excellent visit!"
    )
    db.close()

    # Luego intentamos leer la visita de propiedad recién creada
    response = client.get(f"/property-visit/{new_visit.id}")
    assert response.status_code == 200
    assert response.json()["visitor_name"] == "Jane Smith"

def test_update_property_visit():
    # Primero creamos una visita de propiedad para actualizar
    db = TestingSessionLocal()
    new_visit = crud.create_property_visit(
        db=db,
        property_id=1,
        visit_date=datetime.now(),
        visitor_name="Alice Johnson",
        visitor_email="alice.johnson@example.com",
        feedback="Good visit!"
    )
    db.close()

    # Luego actualizamos la visita de propiedad recién creada
    response = client.put(
        f"/property-visit/{new_visit.id}",
        json={"visitor_name": "Alice Johnson Updated"}
    )
    assert response.status_code == 200
    assert response.json()["visitor_name"] == "Alice Johnson Updated"

def test_delete_property_visit():
    # Primero creamos una visita de propiedad para eliminar
    db = TestingSessionLocal()
    new_visit = crud.create_property_visit(
        db=db,
        property_id=1,
        visit_date=datetime.now(),
        visitor_name="Bob Williams",
        visitor_email="bob.williams@example.com",
        feedback="Nice visit!"
    )
    db.close()

    # Luego eliminamos la visita de propiedad recién creada
    response = client.delete(f"/property-visit/{new_visit.id}")
    assert response.status_code == 200
    assert response.json()["visitor_name"] == "Bob Williams"

def test_get_visits_by_employee():
    # Primero creamos algunas visitas de propiedad para el empleado
    db = TestingSessionLocal()
    crud.create_property_visit(
        db=db,
        property_id=1,
        visit_date=datetime.now(),
        visitor_name="Employee Visit 1",
        visitor_email="employee.visit1@example.com",
        feedback="Good visit!"
    )
    crud.create_property_visit(
        db=db,
        property_id=2,
        visit_date=datetime.now(),
        visitor_name="Employee Visit 2",
        visitor_email="employee.visit2@example.com",
        feedback="Excellent visit!"
    )
    db.close()

    # Luego intentamos obtener las visitas del empleado
    response = client.get("/property-visit/employee/1")
    assert response.status_code == 200
    assert len(response.json()) == 2
