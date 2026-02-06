import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_success():
    # Usar una actividad existente y un email nuevo
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities))
    email = "testuser@example.com"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "message" in response.json()

def test_signup_duplicate():
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities))
    email = "testuser@example.com"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    # Primer registro
    client.post(signup_url)
    # Segundo registro (debería fallar)
    response = client.post(signup_url)
    assert response.status_code == 400
    assert "detail" in response.json()
