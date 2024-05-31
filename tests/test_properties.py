import pytest
from fastapi.testclient import TestClient
from app.main import app  # suponiendo que tu aplicación FastAPI se llama 'app'
from app.models import Property
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
def test_create_property(client, db):
    # Define los datos de prueba para crear una propiedad
    property_data = {
        "address": "123 Main St",
        "location": "City",
        "price": 100000,
        "description": "Beautiful property"
    }

    # Realiza una solicitud POST al endpoint para crear una propiedad
    response = client.post("/properties/", json=property_data)
    assert response.status_code == 200

    # Verifica que la propiedad se haya creado correctamente en la base de datos
    created_property = db.query(Property).filter(Property.address == "123 Main St").first()
    assert created_property is not None

def test_update_property(client, db):
    # Agrega algunos datos de prueba a la base de datos
    property = Property(address="456 Elm St", location="Town", price=150000, description="Nice property")
    db.add(property)
    db.commit()

    # Define los datos de prueba para actualizar la propiedad
    updated_data = {
        "address": "789 Oak St"
    }

    # Realiza una solicitud PUT al endpoint para actualizar la propiedad
    response = client.put("/properties/1", json=updated_data)
    assert response.status_code == 200

    # Verifica que la propiedad se haya actualizado correctamente en la base de datos
    db.refresh(property)
    assert property.address == "789 Oak St"

def test_read_property(client, db):
    # Agrega algunos datos de prueba a la base de datos
    property = Property(address="101 Pine St", location="Village", price=200000, description="Cozy property")
    db.add(property)
    db.commit()

    # Realiza una solicitud GET al endpoint para leer la propiedad
    response = client.get("/properties/1")
    assert response.status_code == 200
    assert response.json()["address"] == "101 Pine St"

def test_delete_property(client, db):
    # Agrega algunos datos de prueba a la base de datos
    property = Property(address="202 Cedar St", location="Countryside", price=250000, description="Rustic property")
    db.add(property)
    db.commit()

    # Realiza una solicitud DELETE al endpoint para eliminar la propiedad
    response = client.delete("/properties/1")
    assert response.status_code == 200

    # Verifica que la propiedad se haya eliminado correctamente de la base de datos
    deleted_property = db.query(Property).filter(Property.id == 1).first()
    assert deleted_property is None
