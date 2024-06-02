import pytest
from app.database import SessionLocal
from app.models import Employee
from app.main import app
from starlette.testclient import TestClient
import requests

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def test_db():
    db = SessionLocal()
    yield db
    db.close()

def create_test_employee(db, email="unique@example.com"):
    try:
        employee = Employee(name="Test Employee", email=email, hashed_password="password")
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except Exception as e:
        db.rollback()
        raise e

def get_valid_token():
    auth_url = "http://localhost:8000/token"
    login_data = {
        "username": "unique@example.com",
        "password": "password"
    }

    response = requests.post(auth_url, data=login_data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Failed to retrieve access token:", response.json())
        raise Exception("Failed to retrieve access token")

def test_get_employee(test_client, test_db):
    employee = create_test_employee(test_db)
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f"/employees/{employee.id}", headers=headers)
    assert response.status_code == 200

def test_update_employee(test_client, test_db):
    employee = create_test_employee(test_db)
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"name": "Updated Name"}
    response = test_client.put(f"/employees/{employee.id}", json=update_data, headers=headers)
    assert response.status_code == 200

def test_delete_employee(test_client, test_db):
    employee = create_test_employee(test_db)
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.delete(f"/employees/{employee.id}", headers=headers)
    assert response.status_code == 204

def test_login_employee(test_client, test_db):
    email = "unique@example.com"
    create_test_employee(test_db, email=email)
    login_data = {"email": email, "password": "password"}
    response = test_client.post("/login", json=login_data)
    assert response.status_code == 200
