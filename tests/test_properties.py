import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Property
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

def test_create_property(client, db):
    property_data = {
        "address": "Pío Nono 450, Recoleta, Región Metropolitana, Chile",
        "location": "City",
        "price": 100000,
        "description": "Beautiful property"
    }

    response = client.post("/properties/", json=property_data)
    assert response.status_code == 200

    created_property = db.query(Property).filter(Property.address == "123 Main St").first()
    assert created_property is not None

def test_update_property(client, db):
    property = Property(address="456 Elm St", location="Town", price=150000, description="Nice property")
    db.add(property)
    db.commit()

    updated_data = {
        "address": "Plaza de Armas, Santiago, Región Metropolitana, Chile"
    }

    response = client.put("/properties/1", json=updated_data)
    assert response.status_code == 200

    db.refresh(property)
    assert property.address == "Plaza de Armas, Santiago, Región Metropolitana, Chile"

def test_read_property(client, db):
    property = Property(address="Plaza de Armas, Santiago, Región Metropolitana, Chile", location="Village", price=200000, description="Cozy property")
    db.add(property)
    db.commit()

    response = client.get("/properties/1")
    assert response.status_code == 200
    assert response.json()["address"] == "Plaza de Armas, Santiago, Región Metropolitana, Chile"

def test_delete_property(client, db):
    property = Property(address="202 Cedar St", location="Countryside", price=250000, description="Rustic property")
    db.add(property)
    db.commit()

    response = client.delete("/properties/1")
    assert response.status_code == 200

    deleted_property = db.query(Property).filter(Property.id == 1).first()
    assert deleted_property is None
