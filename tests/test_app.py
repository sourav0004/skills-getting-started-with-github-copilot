import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    activity = "Basketball Team"
    email = "pytestuser@mergington.edu"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

def test_signup_duplicate():
    activity = "Soccer Club"
    email = "pytestdupe@mergington.edu"
    # Clean up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # First signup
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
