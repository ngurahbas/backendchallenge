from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_echo_valid_json():
    payload = {"hello": "world", "num": 42}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_nested():
    payload = {"data": {"nested": [1, 2, 3], "deep": {"key": "value"}}}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_array():
    payload = [1, 2, 3, "four"]
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_auth_token_valid():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_token_invalid_password():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]


def test_auth_token_unknown_user():
    response = client.post(
        "/auth/token",
        json={"username": "nobody", "password": "x"},
    )
    assert response.status_code == 401
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]
